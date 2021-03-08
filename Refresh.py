# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Refresh.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import os

from PyQt5 import QtCore, QtGui, QtWidgets

import traceback

dev_auth = [0, ""]  # Developer ID and Auth Key

title = ""
name = ""


class Ui_Refresh(object):
    def __init__(self, x, y, z, w):
        global name, dev_auth, title
        name = x
        dev_auth[0] = y
        dev_auth[1] = z
        title = w
    def setupUi(self, Refresh):
        Refresh.setObjectName("Refresh")
        Refresh.setFixedSize(800, 600)
        Refresh.setStyleSheet("background-color: black")
        self.centralwidget = QtWidgets.QWidget(Refresh)
        self.centralwidget.setObjectName("centralwidget")
        self.refreshBtn = QtWidgets.QPushButton(self.centralwidget)
        self.refreshBtn.setGeometry(QtCore.QRect(320, 230, 170, 70))
        self.refreshBtn.setStyleSheet("color: black; background-color: grey;")
        font = QtGui.QFont()
        font.setFamily("Tw Cen MT Condensed Extra Bold")
        font.setPointSize(16)
        self.refreshBtn.setFont(font)
        self.refreshBtn.setObjectName("refreshBtn")
        Refresh.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Refresh)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        Refresh.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Refresh)
        self.statusbar.setObjectName("statusbar")
        Refresh.setStatusBar(self.statusbar)

        self.refreshBtn.clicked.connect(self.backWindow)
        self.refreshBtn.clicked.connect(Refresh.close)
        self.refreshBtn.setAutoDefault(True)

        self.retranslateUi(Refresh)
        QtCore.QMetaObject.connectSlotsByName(Refresh)

    def backWindow(self):
        global name, dev_auth, logfile, title
        from LiveMatch import Ui_LiveMatchWindow
        try:
            # create window
            self.window = QtWidgets.QMainWindow()
            # grabs ui of second window
            self.ui = Ui_LiveMatchWindow(name, dev_auth[0], dev_auth[1], title)
            # sets up the second ui in the new window
            self.ui.setupUi(self.window)
            # set title
            self.window.setWindowTitle(title)
            # display new window
            self.window.show()
        except Exception:
            username = os.getlogin()
            with open(f"C:\\Users\\{username}\\Desktop\\PaladinsLiveBeta-Error.log", "a") as logfile:
                traceback.print_exc(file=logfile)
            raise

    def retranslateUi(self, Refresh):
        _translate = QtCore.QCoreApplication.translate
        Refresh.setWindowTitle(_translate("Refresh", "MainWindow"))
        self.refreshBtn.setText(_translate("Refresh", "Hit 'R'"))
        self.refreshBtn.setShortcut(_translate("Refresh", "R"))
