from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QSlider, QStyleOptionSlider, QStyle

class SeekBar(QSlider):
    userSeeked = Signal(int)
    def __init__(self, orientation=Qt.Orientation.Horizontal, parent=None):
        super().__init__(orientation, parent)
        self.slider_pressed = False
        self.sliderPressed.connect(self._on_pressed)
        self.sliderPressed.connect(self._on_released)

        self.setStyleSheet(
            """
            QSlider:horizontal {
                margin-left: 10px;
                margin-right: 10px;
                margin-bottom: 10px;
                min-height: 20px;
            }

            QSlider::groove:horizontal {
                height: 15px; 
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                background-color: #E0E0E0;
            }

            QSlider::sub-page:horizontal {
                background-color: #0078D4; 
                border: 1px solid #0078D4;
                border-radius: 3px;
            }

            QSlider::add-page:horizontal {
                background-color: #E0E0E0;
                border-radius: 3px;
            }
        """
        )

    def _on_pressed(self):
        self.slider_pressed = True
        
    def _on_released(self):
        self.slider_pressed = False
        self.userSeeked.emit(self.value())

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            opt = QStyleOptionSlider()
            self.initStyleOption(opt)
            sr = self.style().subControlRect(QStyle.ComplexControl.CC_Slider, opt, QStyle.SubControl.SC_SliderGroove, self)

            slider_width = sr.width()
            click_x = event.position().x() - sr.left()

            if slider_width > 0:
                new_value = QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), click_x, slider_width)
                self.setValue(new_value)
                self.userSeeked.emit(new_value)
            
            event.accept()
        super().mousePressEvent(event)
