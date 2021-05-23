import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QCursor, QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from cv2 import cv2

import time
from src.detect.peopledetect import PeopleDetect
from src.gui import ui_mainwindow
from src.gui.constant import SYS_NAME, SYS_VERSION
from src.gui.selectpath import SelectPathDialog
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
        # 视频读取线程
        self.videoReadThread = VideoReadThread()
        self.videoReadThread.signalFrame.connect(self.slotUpdateResult)
        # 摄像头读取线程
        self.cameraReadThread = VideoReadThread()
        self.cameraReadThread.signalFrame.connect(self.slotUpdateResult)

        self.beginRecoding = False   # 是否开始录制
        self.beginRecodingTime = ""  # 开始录制时间
        self.video_out = None
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')

    def initWidget(self):
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowTitle(SYS_NAME)
        # self.setFixedSize(self.width(), self.height())
        # self.menubar.setNativeMenuBar(False)  # 不同平台
        # self.setStyleSheet("#MainWindow{border-image:url(./icons/bg.jpg)}")
        self.setWindowIcon(QIcon("./icons/icon.jpg"))
        # self.setWindowFlags(Qt.FramelessWindowHint)  # 去掉标题栏
        # self.setWindowOpacity(0.9)  # 设置透明
        self.statusbar.setStyleSheet("color:green")

    def initConnect(self):
        # 菜单栏 - 图片
        self.actionopenImage.triggered.connect(self.slotOpenImage)
        # 菜单栏 - 视频
        self.actionopenVideo.triggered.connect(self.slotOpenVideo)
        self.actioncloseVideo.triggered.connect(self.slotCloseVideo)
        # 菜单栏 - 摄像头
        self.actionopenCam.triggered.connect(self.slotOpenCamera)
        self.actioncloseCam.triggered.connect(self.slotCloseCamera)
        # 菜单栏 - 录制
        self.actionbeginRecoding.triggered.connect(self.slotBeginRecoding)
        self.actionendRecoding.triggered.connect(self.slotEndRecoding)
        # 菜单栏 - 帮助
        self.actionabout.triggered.connect(self.slotShowAbout)
        self.actioninstructions.triggered.connect(self.slotOpenInstructions)

    def slotOpenImage(self):
        """
        离线识别：打开本地图片识别
        :return:
        """
        spdia = SelectPathDialog()
        spdia.setType("image")
        spdia.exec()
        if spdia.getIsSure():
            filePath = spdia.getPath()
            print(filePath)
            frame = cv2.imread(filePath)
            self.showImgToLabel(frame, 1)
            orig, image, count = self.people_detect.detectImg(filePath)
            self.lcdNumber.display(count)
            if count > 0:
                text = "行人碰撞预警({}人)".format(count)
                image = self.drawText(text, image)
            self.showImgToLabel(image, 2)

    def slotOpenVideo(self):
        """
        离线识别：打开本地视频识别
        :return:
        """
        if self.cameraReadThread.isRunning():
            QMessageBox.information(self, '提示', '摄像头已经打开，请先关闭摄像头读取！', QMessageBox.Yes)
            return
        if self.videoReadThread.isRunning():
            QMessageBox.information(self, '提示', '视频已经打开，请先关闭视频读取！', QMessageBox.Yes)
            return
        spdia = SelectPathDialog()
        spdia.setType("video")
        spdia.exec()
        if spdia.getIsSure():
            filePath = spdia.getPath()
            print(filePath)
            self.videoReadThread.threadStart(filePath)

    def slotCloseVideo(self):
        """
        关闭视频，停止线程后即可关闭
        :return:
        """
        print("关闭视频")
        self.videoReadThread.threadStop()
        QMessageBox.information(self, '提示', '已关闭！', QMessageBox.Yes)

    def slotOpenCamera(self):
        """
        在线识别： 打开摄像头识别
        :return:
        """
        print("启动摄像头")
        if self.videoReadThread.isRunning():
            QMessageBox.information(self, '提示', '请先关闭视频读取', QMessageBox.Yes)
            return
        if self.cameraReadThread.isRunning():
            QMessageBox.information(self, '提示', '摄像头已经打开，请先关闭摄像头读取！', QMessageBox.Yes)
            return
        self.cameraReadThread.threadStart(0)

    def slotCloseCamera(self):
        """
        关闭摄像头，停止线程后即可关闭
        :return:
        """
        print("关闭摄像头")
        self.cameraReadThread.threadStop()
        QMessageBox.information(self, '提示', '已关闭！', QMessageBox.Yes)

    def slotBeginRecoding(self):
        """
        开始录制
        :return:
        """
        if self.videoReadThread.isRunning() or self.cameraReadThread.isRunning():
            self.beginRecoding = True
            self.beginRecodingTime = time.strftime('%Y-%m-%d_%H:%M:%S')
            print("开始录制时间：{}".format(self.beginRecodingTime))
            video_filename = '{}.avi'.format(self.beginRecodingTime)
            print(video_filename)
            self.video_out = cv2.VideoWriter('output.avi', self.fourcc, 30.0, (640, 480))
            info = '视频录制将保存于本地文件{}.avi'.format(self.beginRecodingTime)
            self.statusbar.showMessage(info)
            QMessageBox.information(self,'提示',info, QMessageBox.Yes)
        else:
            QMessageBox.information(self, '提示', '视频或者摄像头未打开无法开启录制！', QMessageBox.Yes)

    def slotEndRecoding(self):
        """
        结束录制
        :return:
        """
        if self.beginRecoding:  # 已经开始录制中
            self.video_out.release()
            self.beginRecoding = False
            print("结束录制时间：{}".format(time.strftime('%Y-%m-%d %H:%M:%S')))
            QMessageBox.information(self, '提示', ' 已结束录制！', QMessageBox.Yes)
        else:
            QMessageBox.information(self, '提示', '无法结束录制，请先开启录制！', QMessageBox.Yes)

    def showImgToLabel(self, frame, id=1):
        """
        显示图片到qt label上
        :param frame:  图片
        :param id: 哪个label上
        :return:
        """
        size = self.geometry()
        self.label_img1.setMaximumWidth(size.width() / 2 - 50)
        self.label_img2.setMaximumWidth(size.width() / 2 - 50)
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

    def slotUpdateResult(self, frame, retFrame, count):
        """
        刷新结果
        :param frame:  原图
        :param retFrame: 结果图
        :param count: 数量
        :return:
        """
        # 显示原图
        self.showImgToLabel(frame, 1)
        # 显示结果图
        self.showImgToLabel(retFrame, 2)
        # 显示人数
        self.lcdNumber.display(count)
        # 保存视频
        if self.beginRecoding:
            if self.video_out:
                try:
                    self.video_out.write(retFrame)
                except Exception as e:
                    print("保存视频异常")
                    print(str(e))

    def mousePressEvent(self, event):
        """
        鼠标按压
        :param event:
        :return:
        """
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        """
        鼠标移动
        :param QMouseEvent:
        :return:
        """
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        """
        鼠标释放
        :param QMouseEvent:
        :return:
        """
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    def drawText(self, text, img):
        """
        绘制文字
        :param text:  文字内容
        :param img:  图片
        :return:
        """
        cv2img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pilimg = Image.fromarray(cv2img)
        draw = ImageDraw.Draw(pilimg)
        font = ImageFont.truetype("SimHei.ttf", 20, encoding="utf-8")
        draw.text((100, 50), text, (255, 0, 0), font=font)
        cv2charimg = cv2.cvtColor(np.array(pilimg), cv2.COLOR_RGB2BGR)
        return cv2charimg

    def closeEvent(self, event):
        """
        重写closeEvent方法，实现dialog窗体关闭时执行一些代码
        :param event: close()触发的事件
        :return: None
        """
        reply = QMessageBox.question(self,
                                     '本程序',
                                     "是否要退出程序？",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.slotKillAllThread()
            event.accept()
        else:
            event.ignore()

    def slotKillAllThread(self):
        """
        窗口关闭，退出所有线程
        :return:
        """
        if self.videoReadThread.isRunning():
            self.videoReadThread.threadStop()
        if self.cameraReadThread.isRunning():
            self.cameraReadThread.threadStop()

    def slotShowAbout(self):
        info = "系统名称：{} \n 版本：{} ".format(SYS_NAME, SYS_VERSION)
        QMessageBox.information(self, '关于', info, QMessageBox.Yes)

    def slotOpenInstructions(self):
        QMessageBox.information(self, '使用说明', "请查看程序安装目录中”使用说明书.pdf“", QMessageBox.Yes)

if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    win = PDMainWindow()
    win.show()
    sys.exit(app.exec_())
