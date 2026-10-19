import sys
import subprocess
from pathlib import Path
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import QUrl, Qt, QVariantAnimation, QEasingCurve, QSize, QStandardPaths, QTimer, QEvent
from PySide6.QtGui import QGuiApplication, QIcon, QAction, QKeySequence, QShortcut, QActionGroup
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QSpacerItem, QSizePolicy, QProgressBar, QLabel, QPushButton, QFileDialog, QSlider, QMenu
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput, QMediaFormat, QAudio
from PySide6.QtMultimediaWidgets import QVideoWidget
from .elements import SeekBar

from ..core import config

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Freeflow Media Player")
        self.resize(680, 440)

        container = QWidget()
        self.setCentralWidget(container)

        self.fullscreen = False
        self.accentColor = config.accentColor

        self.player = QMediaPlayer()
        self.audioOutput = QAudioOutput()
        self.player.setAudioOutput(self.audioOutput)
        self.audioOutput.setVolume(1.0)
        self.player.durationChanged.connect(self._updateDurationPre)
        
        self.videoWidget = QVideoWidget()
        self.videoWidget.setAspectRatioMode(Qt.AspectRatioMode.KeepAspectRatio)
        self.videoWidget.installEventFilter(self)
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
        self.playpauseButton.setFixedSize(35, 35)
        self.playpauseButton.clicked.connect(self._play_pause)
        self.playpauseButton.setStyleSheet("margin-bottom: 2px;")

        self.skipforwardButton = QPushButton()
        self.skipforwardButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.skipforwardButton.setText(">>")
        self.skipforwardButton.setFixedSize(35, 35)
        self.skipforwardButton.clicked.connect(self._skip_forward)
        self.skipforwardButton.setStyleSheet("margin-bottom: 2px;")

        self.skipbackButton = QPushButton()
        self.skipbackButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.skipbackButton.setText("<<")
        self.skipbackButton.setFixedSize(35, 37)
        self.skipbackButton.clicked.connect(self._skip_backwards)
        self.skipbackButton.setStyleSheet("margin-bottom: 2px; margin-left: 2px;")

        self.fullscreenButton = QPushButton()
        self.fullscreenButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.fullscreenButton.setText("⎡ ⎦")
        self.fullscreenButton.setFixedSize(35, 35)
        self.fullscreenButton.clicked.connect(self._fullscreen_mode)
        self.fullscreenButton.setStyleSheet("margin-bottom: 2px;")
    
        self.ccButton = QPushButton()
        self.ccButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.ccButton.setText("CC")
        self.ccButton.setFixedSize(35, 35)
        self.ccButton.clicked.connect(self._toggle_subtitles)
        self.ccButton.setStyleSheet("margin-bottom: 2px;")

        self.settingsButton = QPushButton()
        self.settingsButton.setStyleSheet("margin-bottom: 2px; margin-left: 2px;")
        self.settingsButton.setFixedSize(24, 35)
        self.settingsMenu = QMenu()
        self.playbackSpeedSub = self.settingsMenu.addMenu("Playback Speed")
        
        self.psGroup = QActionGroup(self.playbackSpeedSub)
        self.psGroup.setExclusive(True)

        speeds = [
            ("x0.25", 'es'),
            ("x0.5", 's'),
            ("x0.75", 'sm'),
            ("x1.0", 'm'),
            ("x1.5", 'slf'),
            ("x2.0", 'f'),
            ("x3.0", 'ef')
        ]
        
        for text, key in speeds:
            action = QAction(text, self.playbackSpeedSub)
            action.setCheckable(True)

            if key == 'm':
                action.setChecked(True)
                
            self.psGroup.addAction(action)
            self.playbackSpeedSub.addAction(action)

            action.triggered.connect(lambda checked, k=key: self._playback_rate(k))

        self.settingsButton.setMenu(self.settingsMenu)

        self.volLabel = QLabel()
        self.volLabel.setText("100%")

        self.volSlider = QSlider(Qt.Orientation.Horizontal)
        self.volSlider.setFixedWidth(200)
        self.volSlider.setRange(0, 100)
        self.volSlider.setValue(100)
        self.volSlider.valueChanged.connect(self._update_volume)
        self.volSlider.setStyleSheet(f"""
            QSlider:horizontal {{
                min-height: 20px;
            }}

            QSlider::groove:horizontal {{
                height: 15px; 
                border: 1px solid #CCCCCC;
                border-radius: 4px;
            }}

            QSlider::sub-page:horizontal {{
                background-color: {self.accentColor}; 
                border: 1px solid {self.accentColor};
                border-radius: 3px;
            }}

            QSlider::add-page:horizontal {{
                border-radius: 3px;
            }}
        """)

        self.is_dragging = False
        self.seekBar.sliderPressed.connect(self._on_slider_pressed)
        self.seekBar.sliderReleased.connect(self._on_slider_released)

        self.player.positionChanged.connect(self._updateProgress)
        self.player.durationChanged.connect(self._updateDuration)

        QShortcut(QKeySequence(Qt.Key.Key_Space), self, self._play_pause)
        QShortcut(QKeySequence(Qt.Key.Key_P), self, self._play_pause)
        QShortcut(QKeySequence(Qt.Key.Key_Left), self, self._skip_backwards)
        QShortcut(QKeySequence(Qt.Key.Key_Right), self, self._skip_forward)
        QShortcut(QKeySequence(Qt.Key.Key_F11), self, self._fullscreen_mode)
        QShortcut(QKeySequence(Qt.Key.Key_Escape), self, self._fullscreen_mode_exit)

        self.seekBar.sliderMoved.connect(self._seekVideo)
        if hasattr(self.seekBar, 'user_seeked'):
            self.seekBar.user_seeked.connect(self._seekVideo)

        self._createMenuBar()
        self.controlWidget = QWidget()
        controlLayout = QtWidgets.QVBoxLayout(self.controlWidget)
        controlLayout.setContentsMargins(0, 0, 0, 0)

        controlsLayout = QtWidgets.QHBoxLayout()
        controlsLayout.setContentsMargins(10, 0, 10, 0)
        controlsLayout.addWidget(self.leftLabel)
        controlsLayout.addWidget(self.seekBar, stretch=1)
        controlsLayout.addWidget(self.rightLabel)
        controlLayout.addLayout(controlsLayout)

        subControlsLayout = QtWidgets.QHBoxLayout()
        subControlsLayout.setContentsMargins(0, 0, 0, 0)
        subControlsLayout.addWidget(self.skipbackButton)
        subControlsLayout.addWidget(self.playpauseButton)
        subControlsLayout.addWidget(self.skipforwardButton)
        subControlsLayout.addStretch()
        subControlsLayout.addWidget(self.ccButton)
        subControlsLayout.addWidget(self.volSlider)
        subControlsLayout.addWidget(self.volLabel)
        subControlsLayout.addWidget(self.fullscreenButton)
        subControlsLayout.addWidget(self.settingsButton)
        controlLayout.addLayout(subControlsLayout)

        layout = QtWidgets.QVBoxLayout()
        container.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.videoWidget, stretch=1)
        layout.addWidget(self.controlWidget)

        self.hideTimer = QTimer(self)
        self.hideTimer.setInterval(2500)
        self.hideTimer.timeout.connect(self._hide_controls)

    def eventFilter(self, obj, event):
        if self.fullscreen and obj == self.videoWidget:
            if event.type() == QEvent.Type.MouseMove:
                self.controlWidget.show()
                self.hideTimer.start()
        return super().eventFilter(obj, event)

    def mouseMoveEvent(self, event):
        if self.fullscreen:
            self.controlWidget.show()
            self.hideTimer.start()
        super().mouseMoveEvent(event)

    def _hide_controls(self):
        if self.fullscreen and not self.is_dragging:
            if not self.controlWidget.underMouse():
                self.controlWidget.hide()
            else:
                self.hideTimer.start()

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

    def _createMenuBar(self):
        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(True)
        menu_bar.setStyleSheet("QMenuBar { padding: 0px; } QMenuBar::item { padding-top: 1px; padding-bottom: 1px; padding-left: 5px; padding-right: 5px; margin-right: 3px; }")
        
        file_menu = menu_bar.addMenu("&File")
        view_menu = menu_bar.addMenu("& View")
        help_menu = menu_bar.addMenu("&Help")

        open_action = QAction("&Open File", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.setStatusTip("Open a video/media file")
        open_action.triggered.connect(self._on_open_cmd)
        file_menu.addAction(open_action)

        toggle_fullscreen = QAction("&Toggle Fullscreen", self)
        toggle_fullscreen.setShortcut(QKeySequence(Qt.Key.Key_F11))
        toggle_fullscreen.setStatusTip("Toggle Fullscreen Mode")
        toggle_fullscreen.triggered.connect(self._fullscreen_mode)
        view_menu.addAction(toggle_fullscreen)
    
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
            winTitle = f"{Path(video_path).stem} - {video_path} - Freeflow Media Player"
            self.setWindowTitle(winTitle)

    def _skip_forward(self):
        if self.player.duration() > 0:
            new_position = min(self.player.position() + 5000, self.player.duration())
            self.player.setPosition(new_position)
            self.player.play()

    def _skip_backwards(self):
        if self.player.duration() > 0:
            new_position = min(self.player.position() - 5000, self.player.duration())
            self.player.setPosition(new_position)
            self.player.play()

    def _fullscreen_mode(self):
        if not self.fullscreen:
            if self.player.duration() > 0:
                self.menuBar().hide()
                self.showFullScreen()
                self.fullscreen = True
                self.setMouseTracking(True)
                self.videoWidget.setMouseTracking(True)
                self.hideTimer.start()
        else:
            self.hideTimer.stop()
            self.menuBar().show()
            self.showNormal()
            self.fullscreen = False
            self.controlWidget.show()
            self.setMouseTracking(False)
            self.videoWidget.setMouseTracking(False)

    def _fullscreen_mode_exit(self):
        if self.fullscreen:
            self.hideTimer.stop()
            self.menuBar().show()
            self.showNormal()
            self.fullscreen = False
            self.controlWidget.show()
            self.setMouseTracking(False)
            self.videoWidget.setMouseTracking(False)

    def _update_volume(self, value):
        self.volLabel.setText(f"{value}%")
        normalisedVol = value / 100.0
        logVol = QAudio.convertVolume(
            normalisedVol,
            QAudio.VolumeScale.LinearVolumeScale,
            QAudio.VolumeScale.LogarithmicVolumeScale
        )
        self.audioOutput.setVolume(logVol)

    def _toggle_subtitles(self):
        if self.player.duration() <= 0:
            return
        tracks = self.player.subtitleTracks()
        if not tracks:
            return
        current_track = self.player.activeSubtitleTrack()
        if current_track == -1:
            next_track = 0  
        elif current_track < len(tracks) - 1:
            next_track = current_track + 1
        else:
            next_track = -1  
        try:
            self.player.setActiveSubtitleTrack(next_track)
        except Exception:
            return
        if next_track == -1:
            self.ccButton.setStyleSheet("margin-bottom: 10px;")
        else:
            self.ccButton.setStyleSheet(f"margin-bottom: 10px; background-color: {self.accentColor}; color: white;")

    def _playback_rate(self, pr):
        if pr == 'es':
            self.player.setPlaybackRate(0.25)
        elif pr == 's':
            self.player.setPlaybackRate(0.5)
        elif pr == 'sm':
            self.player.setPlaybackRate(0.75)
        elif pr == 'slf':
            self.player.setPlaybackRate(1.5)
        elif pr == 'f':
            self.player.setPlaybackRate(2.0)
        elif pr == 'ef':
            self.player.setPlaybackRate(3.0)
        else:
            self.player.setPlaybackRate(1.0)