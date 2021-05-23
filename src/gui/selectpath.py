import os

from PyQt5.QtWidgets import QDialog, QMessageBox, QFileDialog

from src.gui import ui_selectpath


class SelectPathDialog(QDialog, ui_selectpath.Ui_Dialog):
    def __init__(self):
        super(SelectPathDialog, self).__init__()
        self.setupUi(self)
        self.isSure = False
        self.type = None
        self.pushButto_cancel.clicked.connect(self.slotCancel)
        self.pushButto_select.clicked.connect(self.slotSelectPath)
        self.pushButto_sure.clicked.connect(self.slotSure)

    def setType(self, type="image"):
        self.type = type

    def slotSelectPath(self):
        fileName = ""
        if self.type == "image":
            fileName, fileType = QFileDialog.getOpenFileName(
                self, "选取文件", os.getcwd(), "图片(*.jpg)")
        elif self.type == "video":
            fileName, fileType = QFileDialog.getOpenFileName(
                self, "选取文件", os.getcwd(), "视频(*.mp4)")
        self.lineEdit_path.setText(fileName)

    def slotCancel(self):
        self.isSure = False
        self.close()

    def slotSure(self):
        path = self.lineEdit_path.text()
        if path:
            self.isSure = True
            self.close()
        else:
            QMessageBox.information(self, '提示', '路径不能为空！', QMessageBox.Yes)


    def getIsSure(self):
        return self.isSure

    def getPath(self):
        return self.lineEdit_path.text()


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    win = SelectPathDialog()
    win.setType("image")
    win.exec()
    sys.exit(app.exec_())
