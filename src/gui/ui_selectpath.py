# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_selectpath.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(613, 109)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setMinimumSize(QtCore.QSize(0, 30))
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.lineEdit_path = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_path.setMinimumSize(QtCore.QSize(0, 38))
        self.lineEdit_path.setStyleSheet("color: rgb(255, 0, 0);")
        self.lineEdit_path.setObjectName("lineEdit_path")
        self.horizontalLayout_2.addWidget(self.lineEdit_path)
        self.pushButto_select = QtWidgets.QPushButton(Dialog)
        self.pushButto_select.setMinimumSize(QtCore.QSize(0, 38))
        self.pushButto_select.setStyleSheet("background-color: rgb(85, 170, 255);")
        self.pushButto_select.setObjectName("pushButto_select")
        self.horizontalLayout_2.addWidget(self.pushButto_select)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButto_cancel = QtWidgets.QPushButton(Dialog)
        self.pushButto_cancel.setMinimumSize(QtCore.QSize(0, 38))
        self.pushButto_cancel.setStyleSheet("background-color: rgb(85, 170, 255);")
        self.pushButto_cancel.setObjectName("pushButto_cancel")
        self.horizontalLayout.addWidget(self.pushButto_cancel)
        self.pushButto_sure = QtWidgets.QPushButton(Dialog)
        self.pushButto_sure.setMinimumSize(QtCore.QSize(0, 38))
        self.pushButto_sure.setStyleSheet("background-color: rgb(85, 170, 255);")
        self.pushButto_sure.setObjectName("pushButto_sure")
        self.horizontalLayout.addWidget(self.pushButto_sure)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "离线识别"))
        self.label.setText(_translate("Dialog", "文件路径"))
        self.pushButto_select.setText(_translate("Dialog", "选择文件"))
        self.pushButto_cancel.setText(_translate("Dialog", "取消"))
        self.pushButto_sure.setText(_translate("Dialog", "确定"))

