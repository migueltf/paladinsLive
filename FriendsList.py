# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FriendsList.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
from time import sleep

from PyQt5 import QtCore, QtGui, QtWidgets

import concurrent.futures
import asyncio
import arez
import urllib.request
import os
import traceback
from datetime import datetime, date

dev_auth = [0, ""]  # Developer ID and Auth Key

title = ""
name = ""

friend_list = []
avatar_url1 = []
avatar_url2 = []
names1 = []
names2 = []
statuses1 = []
statuses2 = []
rank1 = []
rank2 = []
login1 = []
login2 = []
creation1 = []
creation2 = []


async def friends_list(n):
    global friend_list, avatar_url1, names1, statuses1, rank1, login1, creation1, avatar_url2, names2
    global statuses2, rank2, login2, creation2
    api = arez.PaladinsAPI(dev_auth[0], dev_auth[1])
    p = await api.get_player(n)
    # get players friend list
    friend_list = await p.get_friends()
    tests = []
    for i in range(0, len(friend_list), 1):
        tests.append(check_player(i, api))
    await asyncio.gather(*tests)
    if len(names1) == 0 and len(names2) == 0:
        await api.close()
        return False
    await api.close()
    return True


async def check_player(i, api):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        try:
            # if player exist
            status = (await friend_list[i].get_status()).status.name
            # if the player is online
            if status != "Offline" and friend_list[i].private is False:
                p = await api.get_player(friend_list[i].id)
                try:
                    statuses1.append((await p.get_status()).status.name)
                except arez.exceptions.HTTPException:
                    statuses1.append("Error")
                executor.submit(online_data, friend=p)
            # if not
            elif status == "Offline" and friend_list[i].private is False:
                p = await api.get_player(friend_list[i].id)
                try:
                    statuses2.append((await p.get_status()).status.name)
                except arez.exceptions.HTTPException:
                    statuses2.append("Error")
                executor.submit(offline_data, friend=p)
        except arez.exceptions.NotFound:
            # if there's a problem, then skip
            pass


def online_data(friend):
    avatar_url1.append(friend.avatar_url)
    names1.append(friend.name)
    rank1.append(friend.ranked_keyboard.rank.name)
    login1.append("Now")
    day = str(friend.created_at.day)
    creation1.append(day + " " + month_string(friend.created_at.month) + " " +
                     str(friend.created_at.year))


def offline_data(friend):
    avatar_url2.append(friend.avatar_url)
    names2.append(friend.name)
    rank2.append(friend.ranked_keyboard.rank.name)
    now = datetime.now()
    time = now.time()
    date1 = datetime.date(now)
    login2.append(grab_time(date1, time, friend))
    day = str(friend.created_at.day)
    creation2.append(day + " " + month_string(friend.created_at.month) + " " +
                     str(friend.created_at.year))


def grab_time(d, t, p):
    if (d - p.last_login.date()).days > 0:
        if (d - p.last_login.date()).days >= 365:
            year = (d - p.last_login.date()).days // 365
            if year == 1:
                date1 = str(year) + " year ago"
            else:
                date1 = str(year) + " years ago"
        elif (d - p.last_login.date()).days == 1:
            date1 = str((d - p.last_login.date()).days) + " day ago"
        else:
            date1 = str((d - p.last_login.date()).days) + " days ago"
        return date1
    else:
        date1 = datetime.combine(date.today(), t) - datetime.combine(date.today(), p.last_login.time())
        if date1.seconds > 0:
            if date1.seconds >= 3600:
                time = date1.seconds // 3600
                if time == 1:
                    time = str(time) + " hour ago"
                else:
                    time = str(time) + " hours ago"
            elif date1.seconds >= 60:
                time = date1.seconds // 60
                if time == 1:
                    time = str(time) + " minute ago"
                else:
                    time = str(time) + " minutes ago"
            else:
                time = date1.seconds
                if time == 1:
                    time = str(time) + " second ago"
                else:
                    time = str(time) + " seconds ago"
        else:
            time = "Now"
        return time


def string_day(d):
    if len(d) != 2:
        d = "0" + d
    return d


def month_string(x):
    switcher = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August",
                9: "September", 10: "October", 11: "November", 12: "December"}
    return switcher.get(x, lambda: "Error")


class Ui_FriendsList(object):
    def __init__(self, x, y, z, w):
        global name, dev_auth, title
        name = x
        dev_auth[0] = y
        dev_auth[1] = z
        title = w

    def setupUi(self, FriendsList):
        sizeObject = QtWidgets.QDesktopWidget().screenGeometry(-1)
        FriendsList.setObjectName("FriendsList")
        FriendsList.setFixedSize(900, sizeObject.height() - 175)
        FriendsList.setStyleSheet("background-color: black;")
        self.centralwidget = QtWidgets.QWidget(FriendsList)
        self.centralwidget.setObjectName("centralwidget")
        self.Players = QtWidgets.QLabel(self.centralwidget)
        self.Players.setGeometry(QtCore.QRect(40, 70, 71, 21))
        font = QtGui.QFont()
        font.setFamily("Tw Cen MT")
        font.setPointSize(14)
        self.Players.setFont(font)
        self.Players.setObjectName("Players")
        self.Players.setStyleSheet("color: #cccccc;")
        self.Statuses = QtWidgets.QLabel(self.centralwidget)
        self.Statuses.setGeometry(QtCore.QRect(200, 70, 61, 21))
        font = QtGui.QFont()
        font.setFamily("Tw Cen MT")
        font.setPointSize(14)
        self.Statuses.setFont(font)
        self.Statuses.setObjectName("Statuses")
        self.Statuses.setStyleSheet("color: #cccccc;")
        self.Ranks = QtWidgets.QLabel(self.centralwidget)
        self.Ranks.setGeometry(QtCore.QRect(380, 70, 61, 21))
        font = QtGui.QFont()
        font.setFamily("Tw Cen MT")
        font.setPointSize(14)
        self.Ranks.setFont(font)
        self.Ranks.setObjectName("Ranks")
        self.Ranks.setStyleSheet("color: #cccccc;")
        self.LastLogins = QtWidgets.QLabel(self.centralwidget)
        self.LastLogins.setGeometry(QtCore.QRect(480, 70, 101, 21))
        font = QtGui.QFont()
        font.setFamily("Tw Cen MT")
        font.setPointSize(14)
        self.LastLogins.setFont(font)
        self.LastLogins.setObjectName("LastLogins")
        self.LastLogins.setStyleSheet("color: #cccccc;")
        self.Creations = QtWidgets.QLabel(self.centralwidget)
        self.Creations.setGeometry(QtCore.QRect(660, 70, 91, 21))
        font = QtGui.QFont()
        font.setFamily("Tw Cen MT")
        font.setPointSize(14)
        self.Creations.setFont(font)
        self.Creations.setObjectName("Creations")
        self.Creations.setStyleSheet("color: #cccccc;")
        self.backBtn = QtWidgets.QPushButton(self.centralwidget)
        self.backBtn.setGeometry(QtCore.QRect(0, 0, 110, 50))
        font = QtGui.QFont()
        font.setFamily("Tw Cen MT")
        font.setPointSize(14)
        self.backBtn.setFont(font)
        self.backBtn.setObjectName("backBtn")
        self.backBtn.setStyleSheet("background-color: grey; color: black;")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(0, 100, 900, sizeObject.height() - 275))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 588, 2018))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.frame.setEnabled(True)
        self.frame.setMinimumSize(QtCore.QSize(0, 0))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout.addWidget(self.frame)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        FriendsList.setCentralWidget(self.centralwidget)

        self.backBtn.clicked.connect(self.goback)
        self.backBtn.clicked.connect(FriendsList.close)

        loop = asyncio.get_event_loop()
        hasFriends = loop.run_until_complete(friends_list(name))

        if hasFriends:
            self.set_images()
            self.set_data()
        else:
            # create an label to notify user
            self.invalid = QtWidgets.QLabel(self.frame)
            # set style
            self.invalid.setStyleSheet("color: #cccccc;")
            # set font
            font = QtGui.QFont()
            font.setFamily("Tw Cen MT Condensed Extra Bold")
            font.setPointSize(28)
            self.invalid.setFont(font)
            # set object name
            self.invalid.setObjectName("invalid")
            # display username and players status
            self.invalid.setText("You have no friends :(")
            # adjust size
            self.invalid.adjustSize()
            # and center the text
            self.invalid.move((FriendsList.width() - self.invalid.width()) // 2,
                              (FriendsList.height() - self.invalid.height()) // 2)

        self.retranslateUi(FriendsList)
        QtCore.QMetaObject.connectSlotsByName(FriendsList)

    def set_data(self):
        # this will be used to keep track of iterator for the next list
        temp = 0
        for i in range(0, len(names1), 1):
            self.name = QtWidgets.QLabel(self.frame)
            self.name.setStyleSheet("color: #cccccc;")
            self.name.setText(names1[i])
            font = QtGui.QFont()
            font.setFamily("Tw Cen MT")
            font.setPointSize(14)
            self.name.setFont(font)
            self.name.setObjectName("names1")
            self.name.adjustSize()
            self.name.move(self.avatar.x(), 110 * i + self.avatar.height() + 20)
            self.status = QtWidgets.QLabel(self.frame)
            self.status.setStyleSheet("color: #cccccc;")
            self.status.setText(statuses1[i])
            font = QtGui.QFont()
            font.setFamily("Tw Cen MT Condensed Extra Bold")
            font.setPointSize(20)
            self.status.setFont(font)
            self.status.setObjectName("statuses1")
            self.status.adjustSize()
            self.status.move(230 - self.status.width() // 2, 110 * i + 20 + self.avatar.height() // 4)
            self.lastlogin = QtWidgets.QLabel(self.frame)
            self.lastlogin.setStyleSheet("color: #cccccc;")
            self.lastlogin.setText(login1[i])
            font = QtGui.QFont()
            font.setFamily("Tw Cen MT Condensed Extra Bold")
            font.setPointSize(16)
            self.lastlogin.setFont(font)
            self.lastlogin.setObjectName("lastlogins1")
            self.lastlogin.adjustSize()
            self.lastlogin.move(490 - self.lastlogin.width() // 4, 110 * i + 20 + self.avatar.height() // 4)
            self.creation = QtWidgets.QLabel(self.frame)
            self.creation.setStyleSheet("color: #cccccc;")
            self.creation.setText(creation1[i])
            font = QtGui.QFont()
            font.setFamily("Tw Cen MT Condensed Extra Bold")
            font.setPointSize(16)
            self.creation.setFont(font)
            self.creation.setObjectName("creations1")
            self.creation.adjustSize()
            self.creation.move(680 - self.creation.width() // 4, 110 * i + 20 + self.avatar.height() // 4)
            if i == len(names1) - 1:
                temp = i + 1
        for i in range(0, len(names2), 1):
            self.name = QtWidgets.QLabel(self.frame)
            self.name.setStyleSheet("color: #cccccc;")
            self.name.setText(names2[i])
            font = QtGui.QFont()
            font.setFamily("Tw Cen MT")
            font.setPointSize(14)
            self.name.setFont(font)
            self.name.setObjectName("names1")
            self.name.adjustSize()
            self.name.move(self.avatar.x(), 110 * (i + temp) + self.avatar.height() + 20)
            self.status = QtWidgets.QLabel(self.frame)
            self.status.setStyleSheet("color: #cccccc;")
            self.status.setText(statuses2[i])
            font = QtGui.QFont()
            font.setFamily("Tw Cen MT Condensed Extra Bold")
            font.setPointSize(20)
            self.status.setFont(font)
            self.status.setObjectName("statuses2")
            self.status.adjustSize()
            self.status.move(230 - self.status.width() // 2, 110 * (i + temp) + 20 + self.avatar.height() // 4)
            self.lastlogin = QtWidgets.QLabel(self.frame)
            self.lastlogin.setStyleSheet("color: #cccccc;")
            self.lastlogin.setText(login2[i])
            font = QtGui.QFont()
            font.setFamily("Tw Cen MT Condensed Extra Bold")
            font.setPointSize(16)
            self.lastlogin.setFont(font)
            self.lastlogin.setObjectName("lastlogins1")
            self.lastlogin.adjustSize()
            self.lastlogin.move(490 - self.lastlogin.width() // 4, 110 * (i + temp) + 20 + self.avatar.height() // 4)
            self.creation = QtWidgets.QLabel(self.frame)
            self.creation.setStyleSheet("color: #cccccc;")
            self.creation.setText(creation2[i])
            font = QtGui.QFont()
            font.setFamily("Tw Cen MT Condensed Extra Bold")
            font.setPointSize(16)
            self.creation.setFont(font)
            self.creation.setObjectName("creations1")
            self.creation.adjustSize()
            self.creation.move(680 - self.creation.width() // 4, 110 * (i + temp) + 20 + self.avatar.height() // 4)

    def set_images(self):
        # this will be used to keep track of iterator for the next list
        temp = 0
        for i in range(0, len(names1), 1):
            try:
                self.avatar = QtWidgets.QLabel(self.frame)
                image = QtGui.QImage()
                image.loadFromData(urllib.request.urlopen(avatar_url1[i]).read())
                self.avatar.show()
                self.avatar.setGeometry(QtCore.QRect(30, 110 * i + 20, 70, 70))
                self.avatar.setPixmap(QtGui.QPixmap(image))
                self.avatar.setScaledContents(True)
            except Exception:
                self.avatar = QtWidgets.QLabel(self.frame)
                self.avatar.setStyleSheet("color: #cccccc;")
                font = QtGui.QFont()
                font.setFamily("Tw Cen MT Condensed Extra Bold")
                font.setPointSize(26)
                self.avatar.setFont(font)
                self.avatar.setObjectName("avatar")
                self.avatar.setText("New")
                self.avatar.adjustSize()
                self.avatar.setGeometry(QtCore.QRect(30, 110 * i + 20, 70, 70))
            self.rank = QtWidgets.QLabel(self.frame)
            self.rank.setGeometry(QtCore.QRect(360, 110 * i + 20, 70, 70))
            self.rank.setObjectName("rank1")
            self.rank.setPixmap(QtGui.QPixmap(str(os.getcwd()) + "/img/rank/" + rank1[i] + ".png"))
            self.rank.setScaledContents(True)
            if i == len(names1) - 1:
                temp = i + 1
        for i in range(0, len(names2), 1):
            try:
                self.avatar = QtWidgets.QLabel(self.frame)
                image = QtGui.QImage()
                image.loadFromData(urllib.request.urlopen(avatar_url2[i]).read())
                self.avatar.show()
                self.avatar.setGeometry(QtCore.QRect(30, 110 * (i + temp) + 20, 70, 70))
                self.avatar.setPixmap(QtGui.QPixmap(image))
                self.avatar.setScaledContents(True)
            except Exception:
                self.avatar = QtWidgets.QLabel(self.frame)
                self.avatar.setStyleSheet("color: #cccccc;")
                font = QtGui.QFont()
                font.setFamily("Tw Cen MT Condensed Extra Bold")
                font.setPointSize(26)
                self.avatar.setFont(font)
                self.avatar.setObjectName("avatar")
                self.avatar.setText("New")
                self.avatar.adjustSize()
                self.avatar.setGeometry(QtCore.QRect(30, 110 * (i + temp) + 20, 70, 70))
            self.rank = QtWidgets.QLabel(self.frame)
            self.rank.setGeometry(QtCore.QRect(360, 110 * (i + temp) + 20, 70, 70))
            self.rank.setObjectName("rank1")
            self.rank.setPixmap(QtGui.QPixmap(str(os.getcwd()) + "/img/rank/" + rank2[i] + ".png"))
            self.rank.setScaledContents(True)
            if i == len(names2) - 1:
                self.frame.setMinimumHeight(110 * (i + temp) + 50 + self.avatar.height())

    def reset(self):
        global friend_list, avatar_url1, avatar_url2, names1, names2, statuses1, statuses2
        global rank1, rank2, login1, login2, creation1, creation2
        friend_list = []
        avatar_url1 = []
        avatar_url2 = []
        names1 = []
        names2 = []
        statuses1 = []
        statuses2 = []
        rank1 = []
        rank2 = []
        login1 = []
        login2 = []
        creation1 = []
        creation2 = []

    def goback(self):
        global name, dev_auth, logfile, title
        # import ui of previous window
        from LiveorFriends import Ui_LiveMatchorFriendsWindow
        try:
            # reset data
            self.reset()
            # create window
            self.window = QtWidgets.QMainWindow()
            # grabs ui of second window
            self.ui = Ui_LiveMatchorFriendsWindow(name, dev_auth[0], dev_auth[1], title)
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

    def retranslateUi(self, FriendsList):
        _translate = QtCore.QCoreApplication.translate
        FriendsList.setWindowTitle(_translate("FriendsList", "FriendsList"))
        self.Players.setText(_translate("FriendsList", "Player:"))
        self.Statuses.setText(_translate("FriendsList", "Status:"))
        self.Ranks.setText(_translate("FriendsList", "Rank:"))
        self.LastLogins.setText(_translate("FriendsList", "Last Login:"))
        self.Creations.setText(_translate("FriendsList", "Creation:"))
        self.backBtn.setText(_translate("FriendsList", "Esc"))
        self.backBtn.setShortcut(_translate("FriendsList", "Esc"))
