import sys
from pathlib import Path
from PySide6.QtGui import QIcon
from .ui.main_window import MainWindow
from PySide6.QtWidgets import QApplication

root_path = Path(__file__).parent
icon_path = root_path / "static" / "freeflow-icon.png"

def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(str(icon_path)))

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
