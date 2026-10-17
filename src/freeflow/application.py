import sys
from .ui.main_window import MainWindow
from PySide6.QtWidgets import QApplication

def main():
    app = QApplication([])

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
    