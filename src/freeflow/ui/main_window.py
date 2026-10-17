import sys
import subprocess
from pathlib import Path
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import QUrl, Qt, QVariantAnimation, QEasingCurve
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QSpacerItem, QSizePolicy, QProgressBar
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from .elements import SeekBar

root_path = Path(__file__).parent
video_path = root_path / "sample-10s-2160p.mp4"

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
        self.player.setSource(QtCore.QUrl.fromLocalFile(video_path))
        self.videoWidget = QVideoWidget()
        self.videoWidget.setAspectRatioMode(Qt.AspectRatioMode.KeepAspectRatio)
        self.player.setVideoOutput(self.videoWidget)
        self.player.play()

        self.seekBar = SeekBar(Qt.Orientation.Horizontal)

        self.is_dragging = False
        self.seekBar.sliderPressed.connect(self._on_slider_pressed)
        self.seekBar.sliderReleased.connect(self._on_slider_released)

        self.player.positionChanged.connect(self._updateProgress)
        self.player.durationChanged.connect(self._updateDuration)

        self.seekBar.sliderMoved.connect(self._seekVideo)
        if hasattr(self.seekBar, 'user_seeked'):
            self.seekBar.user_seeked.connect(self._seekVideo)

        layout = QtWidgets.QVBoxLayout()
        container.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.videoWidget, stretch=1)
        layout.addWidget(self.seekBar)
        bottomGap = QSpacerItem(20, 60, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        layout.addSpacerItem(bottomGap)

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

    def _updateDuration(self, duration):
        if duration > 0:
            self.seekBar.setMaximum(duration)

    def _seekVideo(self, value):
        if self.player.duration() > 0:
            if self.player.playbackState() == QMediaPlayer.PlaybackState.StoppedState:
                self.player.pause()
            self.player.setPosition(value)
