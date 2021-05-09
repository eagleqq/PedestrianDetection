import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QCursor, QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from cv2 import cv2

from src.detect.peopledetect import PeopleDetect
from src.gui import ui_mainwindow
from src.threads.videoreadthread import VideoReadThread
from PIL import Image, ImageDraw, ImageFont
import numpy as np

class PDMainWindow(QMainWindow, ui_mainwindow.Ui_MainWindow):
    def __init__(self):
        super(PDMainWindow, self).__init__()
        self.setupUi(self)
        self.initWidget()
        self.initConnect()

        self.people_detect = PeopleDetect()
        self.videoReadThread = VideoReadThread()
        self.videoReadThread.signalFrame.connect(self.slotVideoDetect)

    def initWidget(self):
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowTitle("行人安全检测系统")
        # self.setFixedSize(self.width(), self.height())
        # self.menubar.setNativeMenuBar(False)  # 不同平台
        # self.setStyleSheet("#MainWindow{border-image:url(./icons/bg.jpg)}")
        self.setWindowIcon(QIcon("./icons/icon.jpg"))
        self.setWindowFlags(Qt.FramelessWindowHint)  # 去掉标题栏
        self.setWindowOpacity(0.9)  # 设置透明

    def initConnect(self):
        self.pushButton_close.clicked.connect(self.slotCloseWin)
        self.radioButton_img.toggled.connect(self.slotSelectImg)
        self.radioButton_video.toggled.connect(self.slotSelectVideo)
        self.radioButton_cam.toggled.connect(self.slotSelectCam)
        self.pushButto_select.clicked.connect(self.slotSelectPath)
        self.pushButton_run.clicked.connect(self.slotCamRun)
        self.slotSelectImg()

    def slotCloseWin(self):
        self.videoReadThread.threadStop()
        self.close()

    def slotSelectImg(self):
        self.pushButto_select.setVisible(True)
        self.pushButton_run.setVisible(False)
        self.lineEdit_path.setText("")

    def slotSelectVideo(self):
        self.pushButto_select.setVisible(True)
        self.pushButton_run.setVisible(False)
        self.lineEdit_path.setText("")

    def slotSelectCam(self):
        self.pushButto_select.setVisible(False)
        self.pushButton_run.setVisible(True)
        self.lineEdit_path.setText("系统摄像头")

    def slotSelectPath(self):
        if self.radioButton_img.isChecked():
            fileName, fileType = QFileDialog.getOpenFileName(
                self, "选取文件", os.getcwd(), "图片(*.jpg)")
            self.lineEdit_path.setText(fileName)
            if fileName:
                frame = cv2.imread(fileName)
                self.showImgToLabel(frame, 1)
                orig, image, count = self.people_detect.detectImg(fileName)
                self.lcdNumber.display(count)
                if count > 0:
                    text = "行人碰撞预警({}人)".format(count)
                    image = self.drawText(text, image)
                self.showImgToLabel(image, 2)
        elif self.radioButton_video.isChecked():
            fileName, fileType = QFileDialog.getOpenFileName(
                self, "选取文件", os.getcwd(), "视频(*.mp4)")
            self.lineEdit_path.setText(fileName)
            if fileName:
                self.videoReadThread.threadStart(fileName)

    def showImgToLabel(self, frame, id=1):
        result_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        qtImg = QImage(result_frame.data,
                       result_frame.shape[1],
                       result_frame.shape[0],
                       QImage.Format_RGB888)
        if id == 1:
            self.label_img1.setScaledContents(True)
            self.label_img1.setPixmap(QPixmap.fromImage(qtImg))
        elif id == 2:
            self.label_img2.setScaledContents(True)
            self.label_img2.setPixmap(QPixmap.fromImage(qtImg))

    def slotCamRun(self):
        print("启动摄像头")
        if "打开" in self.pushButton_run.text():
            self.videoReadThread.threadStart(0)
            self.pushButton_run.setText("关闭摄像头")
        else:
            self.videoReadThread.threadStop()
            self.pushButton_run.setText("打开摄像头")

    def slotVideoDetect(self, frame, retFrame, count):
        self.showImgToLabel(frame, 1)
        self.showImgToLabel(retFrame, 2)
        self.lcdNumber.display(count)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    def drawText(self, text, img):
        cv2img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pilimg = Image.fromarray(cv2img)
        draw = ImageDraw.Draw(pilimg)
        font = ImageFont.truetype("SimHei.ttf", 20, encoding="utf-8")
        draw.text((100, 50), text, (255, 0, 0), font=font)
        cv2charimg = cv2.cvtColor(np.array(pilimg), cv2.COLOR_RGB2BGR)
        return cv2charimg