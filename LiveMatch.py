# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LiveMatch.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import asyncio
import arez
from urllib.request import Request, urlopen
import os
import traceback
import pickle
import math

from PyQt5 import QtCore, QtGui, QtWidgets

dev_auth = [0, ""]  # Developer ID and Auth Key

with open('model', 'rb') as f:
    model = pickle.load(f)

match_name = ""

title = ""
name = ""
status = ""
map_name = ""
queue_name = ""

championsurl1 = []
ranks1 = []
kdas1 = []
df1 = []
winrates1 = []
winrates1text = []
awinrates1 = []
champlvl1 = []
playerlvl1 = []
names1 = []

championsurl2 = []
ranks2 = []
kdas2 = []
df2 = []
winrates2 = []
winrates2text = []
awinrates2 = []
champlvl2 = []
playerlvl2 = []
names2 = []


async def live_match(n):
    global status, map_name, queue_name, match_name
    # create an API instance
    api = arez.PaladinsAPI(dev_auth[0], dev_auth[1])
    # fetch Player stats
    player = await api.get_player(n)
    # gets player status, and reformat to only display status and not the IGN
    status = (await player.get_status()).status.name
    # if the player is not in a match
    if status != "In Match":
        # then close api
        await api.close()
        # return that it isn't in match
        return False
    # if in match then get status
    status1 = await player.get_status()
    # and get live match info
    match = await status1.get_live_match()
    await match.expand_players()
    # get match name
    try:
        map_name = match.map_name
    except AttributeError:
        status = "(ERROR) could not acquire match data from Paladins API"
        await api.close()
        return False
    # and type of match
    try:
        queue_name = match.queue.name
    except AttributeError:
        status = "(ERROR) could not acquire match data from Paladins API"
        await api.close()
        return False
    # string together the match name and type
    match_name = map_name + ": " + queue_name
    # get live of live players of team1
    team1 = match.team1
    # same for team 2
    team2 = match.team2
    # for each team member
    for i in range(0, len(team1), 1):
        # get the champion icon
        championsurl1.append(team1[i].champion.icon_url)
        # get the champion mastery
        champlvl1.append(team1[i].mastery_level)
        # get their account level
        playerlvl1.append(team1[i].account_level)
        # check if their name exists in the system
        id = team1[i].player.name
        # if it does exit
        if id != "":
            # add their name to the team name list
            names1.append(id)
            # get the acc # of the player
            id = team1[i].player.id
            # use the # to access the full player stats
            p = await api.get_player(id)
            # get their keyboard rank
            ranks1.append(p.ranked_keyboard.rank.name)
            # get every champion stats on the account
            champion_stats = await p.get_champion_stats()
            # find the specific champion they are playing this match
            champions_stat = await get_champion(champion_stats, team1[i].champion.name)
            # find the champions kda and add it to the team kda list
            try:
                kdas1.append(int(champions_stat.kda2 * 100) / 100)
            # if it cannot be added
            except AttributeError:
                # add error message to the kda list
                kdas1.append("N/A")
            # find the champions df and add it to the team df list
            try:
                df1.append(champions_stat.df)
            # if it cannot be added
            except AttributeError:
                # add error message to the df list
                df1.append("N/A")
            # find the champions winrate and add it to the team winrate list
            try:
                winrates1text.append(champions_stat.winrate_text)
                winrates1.append(champions_stat.winrate)
            # if it cannot be added
            except AttributeError:
                # add error message to the df list
                winrates1.append("N/A")
                winrates1text.append("N/A")
            try:
                if queue_name == "Casual Siege":
                    awinrates1.append(p.casual.winrate)
                elif queue_name == "Competitive Keyboard":
                    awinrates1.append(p.ranked_keyboard.winrate)
            except AttributeError:
                # add error message to the df list
                awinrates1.append("N/A")
        else:
            # if name doesn't exit add name as an error
            names1.append("N/A")
            # append their "rank"
            ranks1.append(team1[i].rank.name)
            # append error as kda
            kdas1.append("N/A")
            # same with df
            df1.append("N/A")
            # same with winrate
            winrates1.append(team1[i].winrate)
            winrates1text.append(team1[i].winrate_text)
            try:
                if queue_name == "Casual Siege":
                    awinrates1.append(p.casual.winrate)
                elif queue_name == "Competitive Keyboard":
                    awinrates1.append(p.ranked_keyboard.winrate)
            except AttributeError:
                # add error message to the df list
                awinrates1.append("N/A")
    # same thing for team 2 members
    for i in range(0, len(team2), 1):
        championsurl2.append(team2[i].champion.icon_url)
        champlvl2.append(team2[i].mastery_level)
        playerlvl2.append(team2[i].account_level)
        id = team2[i].player.name
        if id != "":
            names2.append(id)
            id = team2[i].player.id
            p = await api.get_player(id)
            ranks2.append(p.ranked_keyboard.rank.name)
            champion_stats = await p.get_champion_stats()
            champions_stat = await get_champion(champion_stats, team2[i].champion.name)
            try:
                kdas2.append(int(champions_stat.kda2 * 100) / 100)
            except AttributeError:
                kdas2.append("N/A")
            try:
                df2.append(champions_stat.df)
            except AttributeError:
                df2.append("N/A")
            try:
                winrates2.append(champions_stat.winrate)
                winrates2text.append(champions_stat.winrate_text)
            except AttributeError:
                winrates2.append("N/A")
                winrates2text.append("N/A")
            try:
                if queue_name == "Casual Siege":
                    awinrates2.append(p.casual.winrate)
                elif queue_name == "Competitive Keyboard":
                    awinrates2.append(p.ranked_keyboard.winrate)
            except AttributeError:
                # add error message to the df list
                awinrates2.append("N/A")
        else:
            names2.append("N/A")
            ranks2.append(team2[i].rank.name)
            kdas2.append("N/A")
            df2.append("N/A")
            winrates2.append(team2[i].winrate)
            winrates2text.append(team2[i].winrate_text)
            try:
                if queue_name == "Casual Siege":
                    awinrates2.append(p.casual.winrate)
                elif queue_name == "Competitive Keyboard":
                    awinrates2.append(p.ranked_keyboard.winrate)
            except AttributeError:
                # add error message to the df list
                awinrates2.append("N/A")
    # if team members are less than 55
    if len(team1) < 5:
        # then for each missing member (bot)
        for i in range(0, 5 - len(team1), 1):
            # append their icon url as bot
            championsurl1.append("BOT")
    if len(team2) < 5:
        for i in range(0, 5 - len(team2), 1):
            # append their icon url as bot
            championsurl2.append("BOT")
    # close the api
    await api.close()
    return True


async def get_champion(list, name):
    # for each champion in the list
    for i in range(0, len(list), 1):
        # if the champion name is equal to the champion name currently being played
        if list[i].champion.name == name:
            # return the champion object being player
            return list[i]


class Ui_LiveMatchWindow(object):
    def __init__(self, x, y, z, w):
        global name, dev_auth, title
        # set the name
        name = x
        # current dev Id
        dev_auth[0] = y
        # current auth key
        dev_auth[1] = z
        # set current title
        title = w

    def setupUi(self, LiveMatchWindow):
        LiveMatchWindow.setObjectName("LiveMatchWindow")
        LiveMatchWindow.setFixedSize(1280, 720)
        LiveMatchWindow.setStyleSheet("background-color: black;")
        self.centralwidget = QtWidgets.QWidget(LiveMatchWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.backBtn = QtWidgets.QPushButton(self.centralwidget)
        self.backBtn.setGeometry(QtCore.QRect(0, 0, 110, 50))
        self.backBtn.setStyleSheet("color: black; background-color: grey;")
        font = QtGui.QFont()
        font.setFamily("Tw Cen MT")
        font.setPointSize(14)
        self.backBtn.setFont(font)
        self.backBtn.setObjectName("backBtn")
        self.refreshBtn = QtWidgets.QPushButton(self.centralwidget)
        self.refreshBtn.setGeometry(QtCore.QRect(1170, 0, 110, 50))
        self.refreshBtn.setStyleSheet("color: black; background-color: grey;")
        font = QtGui.QFont()
        font.setFamily("Tw Cen MT")
        font.setPointSize(14)
        self.refreshBtn.setFont(font)
        self.refreshBtn.setObjectName("refreshBtn")
        self.Champions1 = QtWidgets.QLabel(self.centralwidget)
        self.Champions1.setGeometry(QtCore.QRect(40, 70, 90, 30))
        self.Champions1.setStyleSheet("color: #cccccc;")
        font = QtGui.QFont()
        font.setFamily("Tw Cen MT")
        font.setPointSize(14)
        self.Champions1.setFont(font)
        self.Champions1.setObjectName("Champions1")
        self.Champions2 = QtWidgets.QLabel(self.centralwidget)
        self.Champions2.setGeometry(QtCore.QRect(680, 70, 90, 30))
        self.Champions2.setStyleSheet("color: #cccccc;")
        font = QtGui.QFont()
        font.setFamily("Tw Cen MT")
        font.setPointSize(14)
        self.Champions2.setFont(font)
        self.Champions2.setObjectName("Champions2")
        self.kdas1 = QtWidgets.QLabel(self.centralwidget)
        self.kdas1.setGeometry(QtCore.QRect(160, 70, 40, 30))
        self.kdas1.setStyleSheet("color: #cccccc;")
        font = QtGui.QFont()
        font.setFamily("Tw Cen MT")
        font.setPointSize(14)
        self.kdas1.setFont(font)
        self.kdas1.setObjectName("kdas1")
        self.kdas2 = QtWidgets.QLabel(self.centralwidget)
        self.kdas2.setGeometry(QtCore.QRect(800, 70, 40, 30))
        self.kdas2.setStyleSheet("color: #cccccc;")
        font = QtGui.QFont()
        font.setFamily("Tw Cen MT")
        font.setPointSize(14)
        self.kdas2.setFont(font)
        self.kdas2.setObjectName("kdas2")
        self.Winrates1 = QtWidgets.QLabel(self.centralwidget)
        self.Winrates1.setGeometry(QtCore.QRect(250, 70, 70, 30))
        self.Winrates1.setStyleSheet("color: #cccccc;")
        font = QtGui.QFont()
        font.setFamily("Tw Cen MT")
        font.setPointSize(14)
        self.Winrates1.setFont(font)
        self.Winrates1.setObjectName("Winrates1")
        self.Winrates2 = QtWidgets.QLabel(self.centralwidget)
        self.Winrates2.setGeometry(QtCore.QRect(890, 70, 70, 30))
        self.Winrates2.setStyleSheet("color: #cccccc;")
        font = QtGui.QFont()
        font.setFamily("Tw Cen MT")
        font.setPointSize(14)
        self.Winrates2.setFont(font)
        self.Winrates2.setObjectName("Winrates2")
        self.Levels1 = QtWidgets.QLabel(self.centralwidget)
        self.Levels1.setGeometry(QtCore.QRect(370, 70, 70, 30))
        self.Levels1.setStyleSheet("color: #cccccc;")
        font = QtGui.QFont()
        font.setFamily("Tw Cen MT")
        font.setPointSize(14)
        self.Levels1.setFont(font)
        self.Levels1.setObjectName("Levels1")
        self.Levels2 = QtWidgets.QLabel(self.centralwidget)
        self.Levels2.setGeometry(QtCore.QRect(1010, 70, 70, 30))
        font = QtGui.QFont()
        font.setFamily("Tw Cen MT")
        font.setPointSize(14)
        self.Levels2.setFont(font)
        self.Levels2.setObjectName("Levels2")
        self.Levels2.setStyleSheet("color: #cccccc;")
        self.Ranks1 = QtWidgets.QLabel(self.centralwidget)
        self.Ranks1.setGeometry(QtCore.QRect(500, 70, 50, 30))
        self.Ranks1.setStyleSheet("color: #cccccc;")
        font = QtGui.QFont()
        font.setFamily("Tw Cen MT")
        font.setPointSize(14)
        self.Ranks1.setFont(font)
        self.Ranks1.setObjectName("Ranks1")
        self.Ranks2 = QtWidgets.QLabel(self.centralwidget)
        self.Ranks2.setGeometry(QtCore.QRect(1140, 70, 50, 30))
        self.Ranks2.setStyleSheet("color: #cccccc;")
        font = QtGui.QFont()
        font.setFamily("Tw Cen MT")
        font.setPointSize(14)
        self.Ranks2.setFont(font)
        self.Ranks2.setObjectName("Ranks2")
        self.vs = QtWidgets.QLabel(self.centralwidget)
        self.vs.setGeometry(QtCore.QRect(600, 355, 31, 16))
        font = QtGui.QFont()
        font.setFamily("Tw Cen MT")
        font.setPointSize(14)
        self.vs.setFont(font)
        self.vs.setObjectName("vs")
        self.vs.setStyleSheet("color: #cccccc;")
        LiveMatchWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(LiveMatchWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 26))
        self.menubar.setObjectName("menubar")
        LiveMatchWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(LiveMatchWindow)
        self.statusbar.setObjectName("statusbar")
        LiveMatchWindow.setStatusBar(self.statusbar)

        self.backBtn.clicked.connect(self.backWindow)
        self.backBtn.clicked.connect(LiveMatchWindow.close)
        self.backBtn.setAutoDefault(True)

        self.refreshBtn.clicked.connect(self.openRefresh)
        self.refreshBtn.clicked.connect(LiveMatchWindow.close)
        self.refreshBtn.setAutoDefault(True)

        loop = asyncio.get_event_loop()
        # attempted to find user in a live match
        inMatch = loop.run_until_complete(live_match(name))

        # if they're not in a livematch
        if not inMatch:
            # create an label to notify user
            self.invalid = QtWidgets.QLabel(self.centralwidget)
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
            self.invalid.setText(name + ": " + status)
            # adjust size
            self.invalid.adjustSize()
            # and center the text
            self.invalid.move((LiveMatchWindow.width() - self.invalid.width()) // 2,
                              (LiveMatchWindow.height() - self.invalid.height()) // 2)
        else:
            # if it's valid set the VS text
            self.vs.setText("VS")
            # set images of champions and rank for each player
            self.set_images()
            # display data found
            self.set_data(LiveMatchWindow.width())
            self.predictmatch(LiveMatchWindow.width(), LiveMatchWindow.height())

        self.retranslateUi(LiveMatchWindow)
        QtCore.QMetaObject.connectSlotsByName(LiveMatchWindow)

    def predictmatch(self, width, height):
        if len(winrates1) == 5:
            sumwin1 = 0
            den1 = 0
            sumwin2 = 0
            den2 = 0
            sumkda1 = 0
            den3 = 0
            sumkda2 = 0
            den4 = 0
            sumdf1 = 0
            den5 = 0
            sumdf2 = 0
            den6 = 0
            sumawin1 = 0
            den7 = 0
            sumawin2 = 0
            den8 = 0
            for i in range(len(winrates1)):
                if winrates1[i] != "N/A" and not math.isnan(float(winrates1[i])):
                    sumwin1 += winrates1[i]
                    den1 += 1
                if winrates2[i] != "N/A" and not math.isnan(float(winrates2[i])):
                    sumwin2 += winrates2[i]
                    den2 += 1
                if kdas1[i] != "N/A":
                    sumkda1 += kdas1[i]
                    den3 += 1
                if kdas2[i] != "N/A":
                    sumkda2 += kdas2[i]
                    den4 += 1
                if df1[i] != "N/A":
                    sumdf1 += df1[i]
                    den5 += 1
                if df2[i] != "N/A":
                    sumdf2 += df2[i]
                    den6 += 1
                if awinrates1[i] != "N/A" and not math.isnan(float(awinrates1[i])):
                    sumawin1 += awinrates1[i]
                    den7 += 1
                if awinrates2[i] != "N/A" and not math.isnan(float(awinrates2[i])):
                    sumawin2 += awinrates2[i]
                    den8 += 1
            windif = sumwin1 / den1 - sumwin2 / den2
            kdadif = sumkda1 / den3 - sumkda2 / den4
            dfdif = sumdf1 / den5 - sumdf2 / den6
            awindif = sumawin1 / den7 - sumawin2 / den8
            # create an label to notify user
            self.predict = QtWidgets.QLabel(self.centralwidget)
            # set style
            self.predict.setStyleSheet("color: #cccccc;")
            # set font
            font = QtGui.QFont()
            font.setFamily("Tw Cen MT Condensed Extra Bold")
            font.setPointSize(24)
            self.predict.setFont(font)
            # set object name
            self.predict.setObjectName("predict")
            # display username and players status
            self.predict.setText(str(model.predict_proba([[windif, kdadif, dfdif, awindif]])))
            # adjust size
            self.predict.adjustSize()
            self.predict.move((width - self.predict.width()) // 2, height - (self.predict.height() + 20))

    def set_data(self, width):
        self.match = QtWidgets.QLabel(self.centralwidget)
        self.match.setStyleSheet("color: #cccccc;")
        self.match.setText(match_name)
        font = QtGui.QFont()
        font.setFamily("Tw Cen MT")
        font.setPointSize(26)
        self.match.setFont(font)
        self.match.setObjectName("match_name")
        self.match.adjustSize()
        self.match.setGeometry(QtCore.QRect((width - self.match.width()) // 2, 0, 0, 0))
        self.match.adjustSize()

        for i in range(0, len(championsurl1), 1):
            if championsurl1[i] != "BOT":
                self.kda = QtWidgets.QLabel(self.centralwidget)
                self.kda.setStyleSheet("color: #cccccc;")
                self.kda.setText(str(kdas1[i]))
                font = QtGui.QFont()
                font.setFamily("Tw Cen MT")
                font.setPointSize(16)
                self.kda.setFont(font)
                self.kda.setObjectName("kda1")
                self.kda.adjustSize()
                self.kda.setGeometry(QtCore.QRect(160, 110 * i + 120, 0, 0))
                self.kda.adjustSize()
                self.df = QtWidgets.QLabel(self.centralwidget)
                self.df.setStyleSheet("color: #cccccc;")
                self.df.setText("df: " + str(df1[i]))
                font = QtGui.QFont()
                font.setFamily("Tw Cen MT")
                font.setPointSize(12)
                self.df.setFont(font)
                self.df.setObjectName("df1")
                self.df.adjustSize()
                self.df.setGeometry(QtCore.QRect(160, 110 * i + 120 + self.kda.height(), 0, 0))
                self.df.adjustSize()
                self.winrate = QtWidgets.QLabel(self.centralwidget)
                self.winrate.setStyleSheet("color: #cccccc;")
                self.winrate.setText(str(winrates1text[i]))
                font = QtGui.QFont()
                font.setFamily("Tw Cen MT")
                font.setPointSize(14)
                self.winrate.setFont(font)
                self.winrate.setObjectName("winrate1")
                self.winrate.adjustSize()
                self.winrate.setGeometry(QtCore.QRect(250, 110 * i + 155 - (self.winrate.height() // 2), 0, 0))
                self.winrate.adjustSize()
                self.acclvl = QtWidgets.QLabel(self.centralwidget)
                self.acclvl.setStyleSheet("color: #cccccc;")
                self.acclvl.setText("LVL: " + str(playerlvl1[i]))
                font = QtGui.QFont()
                font.setFamily("Tw Cen MT")
                font.setPointSize(16)
                self.acclvl.setFont(font)
                self.acclvl.setObjectName("acclvl1")
                self.acclvl.adjustSize()
                self.acclvl.setGeometry(QtCore.QRect(370, 110 * i + 120, 0, 0))
                self.acclvl.adjustSize()
                self.masterlvl = QtWidgets.QLabel(self.centralwidget)
                self.masterlvl.setStyleSheet("color: #cccccc;")
                self.masterlvl.setText("masterylvl: " + str(champlvl1[i]))
                font = QtGui.QFont()
                font.setFamily("Tw Cen MT")
                font.setPointSize(11)
                self.masterlvl.setFont(font)
                self.masterlvl.setObjectName("masterlvl1")
                self.masterlvl.adjustSize()
                self.masterlvl.setGeometry(QtCore.QRect(370, 110 * i + 120 + self.acclvl.height(), 0, 0))
                self.masterlvl.adjustSize()
                self.name = QtWidgets.QLabel(self.centralwidget)
                self.name.setStyleSheet("color: #cccccc;")
                self.name.setText(names1[i])
                font = QtGui.QFont()
                font.setFamily("Tw Cen MT")
                font.setPointSize(14)
                self.name.setFont(font)
                self.name.setObjectName("name1")
                self.name.adjustSize()
                self.name.setGeometry(QtCore.QRect(40, 110 * i + 190, 0, 0))
                self.name.adjustSize()
            else:
                self.name = QtWidgets.QLabel(self.centralwidget)
                self.name.setStyleSheet("color: #cccccc;")
                self.name.setText("BOT")
                font = QtGui.QFont()
                font.setFamily("Tw Cen MT Condensed Extra Bold")
                font.setPointSize(28)
                self.name.setFont(font)
                self.name.setObjectName("name1")
                self.name.adjustSize()
                self.name.setGeometry(QtCore.QRect(40, 110 * i + 155 - self.name.width() // 2, 0, 0))
                self.name.adjustSize()
            if championsurl2[i] != "BOT":
                self.kda = QtWidgets.QLabel(self.centralwidget)
                self.kda.setStyleSheet("color: #cccccc;")
                self.kda.setText(str(kdas2[i]))
                font = QtGui.QFont()
                font.setFamily("Tw Cen MT")
                font.setPointSize(16)
                self.kda.setFont(font)
                self.kda.setObjectName("kda2")
                self.kda.adjustSize()
                self.kda.setGeometry(QtCore.QRect(800, 110 * i + 120, 0, 0))
                self.kda.adjustSize()
                self.df = QtWidgets.QLabel(self.centralwidget)
                self.df.setStyleSheet("color: #cccccc;")
                self.df.setText("df: " + str(df2[i]))
                font = QtGui.QFont()
                font.setFamily("Tw Cen MT")
                font.setPointSize(12)
                self.df.setFont(font)
                self.df.setObjectName("df6")
                self.df.adjustSize()
                self.df.setGeometry(QtCore.QRect(800, 110 * i + 120 + self.kda.height(), 0, 0))
                self.df.adjustSize()
                self.winrate = QtWidgets.QLabel(self.centralwidget)
                self.winrate.setStyleSheet("color: #cccccc;")
                self.winrate.setText(str(winrates2text[i]))
                font = QtGui.QFont()
                font.setFamily("Tw Cen MT")
                font.setPointSize(14)
                self.winrate.setFont(font)
                self.winrate.setObjectName("winrate2")
                self.winrate.adjustSize()
                self.winrate.setGeometry(QtCore.QRect(890, 110 * i + 155 - (self.winrate.height() // 2), 0, 0))
                self.winrate.adjustSize()
                self.acclvl = QtWidgets.QLabel(self.centralwidget)
                self.acclvl.setStyleSheet("color: #cccccc;")
                self.acclvl.setText("LVL: " + str(playerlvl2[i]))
                font = QtGui.QFont()
                font.setFamily("Tw Cen MT")
                font.setPointSize(16)
                self.acclvl.setFont(font)
                self.acclvl.setObjectName("acclvl2")
                self.acclvl.adjustSize()
                self.acclvl.setGeometry(QtCore.QRect(1010, 110 * i + 120, 0, 0))
                self.acclvl.adjustSize()
                self.masterlvl = QtWidgets.QLabel(self.centralwidget)
                self.masterlvl.setStyleSheet("color: #cccccc;")
                self.masterlvl.setText("masterylvl: " + str(champlvl2[i]))
                font = QtGui.QFont()
                font.setFamily("Tw Cen MT")
                font.setPointSize(11)
                self.masterlvl.setFont(font)
                self.masterlvl.setObjectName("masterlvl2")
                self.masterlvl.adjustSize()
                self.masterlvl.setGeometry(QtCore.QRect(1010, 110 * i + 120 + self.acclvl.height(), 0, 0))
                self.masterlvl.adjustSize()
                self.name = QtWidgets.QLabel(self.centralwidget)
                self.name.setStyleSheet("color: #cccccc;")
                self.name.setText(names2[i])
                font = QtGui.QFont()
                font.setFamily("Tw Cen MT")
                font.setPointSize(14)
                self.name.setFont(font)
                self.name.setObjectName("name2")
                self.name.adjustSize()
                self.name.setGeometry(QtCore.QRect(680, 110 * i + 190, 0, 0))
                self.name.adjustSize()
            else:
                self.name = QtWidgets.QLabel(self.centralwidget)
                self.name.setStyleSheet("color: #cccccc;")
                self.name.setText("BOT")
                font = QtGui.QFont()
                font.setFamily("Tw Cen MT Condensed Extra Bold")
                font.setPointSize(28)
                self.name.setFont(font)
                self.name.setObjectName("name2")
                self.name.adjustSize()
                self.name.setGeometry(QtCore.QRect(680, 110 * i + 155 - self.name.width() // 2, 0, 0))
                self.name.adjustSize()

    def set_images(self):
        for i in range(0, len(championsurl1), 1):
            if championsurl1[i] != "BOT":
                try:
                    image = QtGui.QImage()
                    request = Request(championsurl1[i], headers={"User-Agent": "Mozilla/5.0"})
                    image.loadFromData(urlopen(request).read())
                    self.champ = QtWidgets.QLabel(self.centralwidget)
                    self.champ.setGeometry(QtCore.QRect(40, 110 * i + 120, 70, 70))
                    self.champ.setPixmap(QtGui.QPixmap(image))
                    self.champ.setScaledContents(True)
                except Exception:
                    self.champ = QtWidgets.QLabel(self.centralwidget)
                    self.champ.setGeometry(QtCore.QRect(40, 110 * i + 120, 70, 70))
                    self.champ.setStyleSheet("color: #cccccc;")
                    font = QtGui.QFont()
                    font.setFamily("Tw Cen MT Condensed Extra Bold")
                    font.setPointSize(26)
                    self.champ.setFont(font)
                    self.champ.setObjectName("champ")
                    self.champ.setText("New")
                    self.champ.adjustSize()
                self.rank = QtWidgets.QLabel(self.centralwidget)
                self.rank.setGeometry(QtCore.QRect(500, 110 * i + 155 - self.champ.width() // 2, 70, 70))
                self.rank.setObjectName("rank1")
                self.rank.setPixmap(QtGui.QPixmap(str(os.getcwd()) + "/img/rank/" + ranks1[i] + ".png"))
                self.rank.setScaledContents(True)
            if championsurl2[i] != "BOT":
                try:
                    image = QtGui.QImage()
                    request = Request(championsurl2[i], headers={"User-Agent": "Mozilla/5.0"})
                    image.loadFromData(urlopen(request).read())
                    self.champ = QtWidgets.QLabel(self.centralwidget)
                    self.champ.setGeometry(QtCore.QRect(680, 110 * i + 120, 70, 70))
                    self.champ.setPixmap(QtGui.QPixmap(image))
                    self.champ.setScaledContents(True)
                except Exception:
                    self.champ = QtWidgets.QLabel(self.centralwidget)
                    self.champ.setGeometry(QtCore.QRect(680, 110 * i + 120, 70, 70))
                    self.champ.setStyleSheet("color: #cccccc;")
                    font = QtGui.QFont()
                    font.setFamily("Tw Cen MT Condensed Extra Bold")
                    font.setPointSize(26)
                    self.champ.setFont(font)
                    self.champ.setObjectName("champ")
                    self.champ.setText("New")
                    self.champ.adjustSize()
                self.rank = QtWidgets.QLabel(self.centralwidget)
                self.rank.setGeometry(QtCore.QRect(1140, 110 * i + 120, 70, 70))
                self.rank.setObjectName("rank2")
                self.rank.setPixmap(QtGui.QPixmap(str(os.getcwd()) + "/img/rank/" + ranks2[i] + ".png"))
                self.rank.setScaledContents(True)

    def openRefresh(self):
        global dev_auth, logfile, title
        # reset all match data
        self.reset_data()
        # import refresh ui
        from Refresh import Ui_Refresh
        try:
            # create window
            self.window = QtWidgets.QMainWindow()
            # grabs ui of second window
            self.ui = Ui_Refresh(name, dev_auth[0], dev_auth[1], title)
            # sets up the second ui in the new window
            self.ui.setupUi(self.window)
            # set title
            self.window.setWindowTitle(title)
            # display new window
            self.window.show()
        # if there's a crash write in error log
        except Exception:
            username = os.getlogin()
            with open(f"C:\\Users\\{username}\\Desktop\\PaladinsLiveBeta-Error.log", "a") as logfile:
                traceback.print_exc(file=logfile)
            raise

    def backWindow(self):
        global dev_auth, logfile, title
        # reset all match data
        self.reset_data()
        # import ui of previous window
        from LiveorFriends import Ui_LiveMatchorFriendsWindow
        try:
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

    def reset_data(self):
        global name, status, map_name, queue_name, championsurl1, ranks1, kdas1, df1, winrates1, champlvl1, playerlvl1
        global names1, championsurl2, ranks2, kdas2, df2, winrates2, champlvl2, playerlvl2, names2
        global awinrates1, awinrates2, winrates1text, winrates2text
        status = ""
        map_name = ""
        queue_name = ""
        championsurl1 = []
        ranks1 = []
        df1 = []
        winrates1 = []
        winrates1text = []
        awinrates1 = []
        champlvl1 = []
        playerlvl1 = []
        names1 = []
        championsurl2 = []
        ranks2 = []
        kdas2 = []
        df2 = []
        winrates2 = []
        winrates2text = []
        awinrates2 = []
        champlvl2 = []
        playerlvl2 = []
        names2 = []

    def retranslateUi(self, LiveMatchWindow):
        _translate = QtCore.QCoreApplication.translate
        LiveMatchWindow.setWindowTitle(_translate("LiveMatchWindow", "MainWindow"))
        self.backBtn.setText(_translate("LiveMatchWindow", "Esc"))
        self.backBtn.setShortcut(_translate("LiveMatchWindow", "Esc"))
        self.refreshBtn.setText(_translate("LiveMatchWindow", "Refresh"))
        self.refreshBtn.setShortcut(_translate("LiveMatchWindow", "R"))
        self.Champions1.setText(_translate("LiveMatchWindow", "Champions:"))
        self.Champions1.adjustSize()
        self.Champions2.setText(_translate("LiveMatchWindow", "Champions:"))
        self.Champions2.adjustSize()
        self.kdas1.setText(_translate("LiveMatchWindow", "KDA:"))
        self.kdas1.adjustSize()
        self.kdas2.setText(_translate("LiveMatchWindow", "KDA:"))
        self.kdas2.adjustSize()
        self.Winrates1.setText(_translate("LiveMatchWindow", "Winrate:"))
        self.Winrates1.adjustSize()
        self.Winrates2.setText(_translate("LiveMatchWindow", "Winrate:"))
        self.Winrates2.adjustSize()
        self.Levels1.setText(_translate("LiveMatchWindow", "Levels:"))
        self.Levels1.adjustSize()
        self.Levels2.setText(_translate("LiveMatchWindow", "Levels:"))
        self.Levels2.adjustSize()
        self.Ranks1.setText(_translate("LiveMatchWindow", "Rank:"))
        self.Ranks1.adjustSize()
        self.Ranks2.setText(_translate("LiveMatchWindow", "Rank:"))
        self.Ranks1.adjustSize()
