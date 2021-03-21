import sys

from PyQt5.QtWidgets import QApplication

from src.gui.mainwindow import PDMainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = PDMainWindow()
    win.show()
    sys.exit(app.exec_())
