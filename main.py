import sys
from PyQt6.QtWidgets import QApplication
from gui.main_window import Demo


def main():
    app = QApplication(sys.argv)
    window = Demo()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
