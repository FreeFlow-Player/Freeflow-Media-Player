import sys
import subprocess
from pathlib import Path
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import QUrl, Qt, QVariantAnimation, QEasingCurve, QSize, QStandardPaths
from PySide6.QtGui import QGuiApplication, QIcon, QAction, QKeySequence
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QSpacerItem, QSizePolicy, QProgressBar, QLabel, QPushButton, QFileDialog
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput, QMediaFormat
from PySide6.QtMultimediaWidgets import QVideoWidget
from .elements import SeekBar

root_path = Path(__file__).parent.parent

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Freeflow Media Player")
        self.resize(680, 440)

        container = QWidget()
        self.setCentralWidget(container)
        
        self.player = QMediaPlayer()
        self.audioOutput = QAudioOutput()
        self.player.setAudioOutput(self.audioOutput)
        self.audioOutput.setVolume(1.0)
        self.player.durationChanged.connect(self._updateDurationPre)
        self.videoWidget = QVideoWidget()
        self.videoWidget.setAspectRatioMode(Qt.AspectRatioMode.KeepAspectRatio)
        self.player.setVideoOutput(self.videoWidget)

        self.seekBar = SeekBar(Qt.Orientation.Horizontal)
        self.leftLabel = QLabel()
        self.leftLabel.setText("--:--")
        self.leftLabel.setStyleSheet("margin-bottom: 10px;")
        self.rightLabel = QLabel()
        self.rightLabel.setText("--:--")
        self.rightLabel.setStyleSheet("margin-bottom: 10px;")

        self.playpauseButton = QPushButton()
        self.playpauseButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.playpauseButton.setText("▐▐")
        self.playpauseButton.setFixedSize(48, 48)
        self.playpauseButton.clicked.connect(self._play_pause)

        self.is_dragging = False
        self.seekBar.sliderPressed.connect(self._on_slider_pressed)
        self.seekBar.sliderReleased.connect(self._on_slider_released)

        self.player.positionChanged.connect(self._updateProgress)
        self.player.durationChanged.connect(self._updateDuration)

        self.seekBar.sliderMoved.connect(self._seekVideo)
        if hasattr(self.seekBar, 'user_seeked'):
            self.seekBar.user_seeked.connect(self._seekVideo)

        self._createMenuBar()

        layout = QtWidgets.QVBoxLayout()
        container.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.videoWidget, stretch=1)
        controlsLayout = QtWidgets.QHBoxLayout()
        controlsLayout.setContentsMargins(10, 0, 10, 0)
        controlsLayout.addWidget(self.leftLabel)
        controlsLayout.addWidget(self.seekBar, stretch=1)
        controlsLayout.addWidget(self.rightLabel)
        layout.addLayout(controlsLayout)
        subControlsLayout = QtWidgets.QHBoxLayout()
        subControlsLayout.addStretch()
        subControlsLayout.addWidget(self.playpauseButton)
        subControlsLayout.addStretch()
        layout.addLayout(subControlsLayout)

    def _on_slider_pressed(self):
        self.is_dragging = True

    def _on_slider_released(self):
        self.is_dragging = False
        if self.player.playbackState() == QMediaPlayer.PlaybackState.StoppedState:
            self.player.pause()
        self.player.setPosition(self.seekBar.value())
        self.player.play()

    def _updateProgress(self, position):
        if not self.is_dragging:
            self.seekBar.blockSignals(True)
            self.seekBar.setValue(position)
            self.seekBar.blockSignals(False)
        totalSec = position // 1000
        minutes, seconds = divmod(totalSec, 60)
        fTime = f"{minutes:02d}:{seconds:02d}"
        self.leftLabel.setText(fTime)

    def _updateDurationPre(self, durationMs):      
        self.leftLabel.setText("00:00")
        totalSec = durationMs // 1000
        minutes, seconds = divmod(totalSec, 60)
        fTime = f"{minutes:02d}:{seconds:02d}"
        self.rightLabel.setText(fTime)
        self.seekBar.setRange(0, durationMs)

    def _updateDuration(self, duration):
        if duration > 0:
            self.seekBar.setMaximum(duration)

    def _seekVideo(self, value):
        if self.player.duration() > 0:
            if self.player.playbackState() == QMediaPlayer.PlaybackState.StoppedState:
                self.player.pause()
            self.player.setPosition(value)

    def _play_pause(self):
        if self.player.isPlaying():
            self.player.pause()
            self.playpauseButton.setText("▶")
        else:
            self.player.play()
            self.playpauseButton.setText("▐▐")

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if event.key() in (Qt.Key.Key_Space, Qt.Key.Key_P):
            self._play_pause()
            event.accept()
        else:
            super().keyPressEvent(event)

    def _createMenuBar(self):
        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(True)
        menu_bar.setStyleSheet("QMenuBar { padding: 0px; } QMenuBar::item { padding-top: 1px; padding-bottom: 1px; padding-left: 5px; padding-right: 5px; margin-right: 3px; }")
        
        file_menu = menu_bar.addMenu("&File")
        help_menu = menu_bar.addMenu("&Help")

        open_action = QAction("&Open File", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.setStatusTip("Open a video/media file")
        open_action.triggered.connect(self._on_open_cmd)
        file_menu.addAction(open_action)
    
    def _on_open_cmd(self):
        supFormats = QMediaFormat().supportedFileFormats(QMediaFormat.Decode)
        unique_extensions = set()
        for fmtId in supFormats:
            MIME_type = QMediaFormat(fmtId).mimeType()
            if MIME_type.name().startswith("video/"):
                for ext in MIME_type.suffixes():
                    unique_extensions.add(f"*.{ext}")

        ext_string = " ".join(sorted(unique_extensions))
        file_filter = f"Video Files ({ext_string});;All Files (*)"
        downloads_dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DownloadLocation)

        video_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Open File", 
            downloads_dir,
            file_filter
        )

        if video_path:
            selFiles = [video_path]
            video_path = selFiles[0]
            self.player.setSource(QtCore.QUrl.fromLocalFile(video_path))
            self.player.play()
            self.playpauseButton.setText("▐▐")
