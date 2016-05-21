# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/takayuki/Desktop/program/python/Spyder_workspcae/PyQt_test/ui/PyQt_test/ViewerManager.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_ViewerManager(object):
    def setupUi(self, ViewerManager):
        ViewerManager.setObjectName(_fromUtf8("ViewerManager"))
        ViewerManager.resize(640, 480)
        self.centralwidget = QtGui.QWidget(ViewerManager)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.treeView_PlanetAttribute = QtGui.QTreeView(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeView_PlanetAttribute.sizePolicy().hasHeightForWidth())
        self.treeView_PlanetAttribute.setSizePolicy(sizePolicy)
        self.treeView_PlanetAttribute.setMinimumSize(QtCore.QSize(100, 200))
        self.treeView_PlanetAttribute.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.treeView_PlanetAttribute.setObjectName(_fromUtf8("treeView_PlanetAttribute"))
        self.verticalLayout.addWidget(self.treeView_PlanetAttribute)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pushButton_showtime = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_showtime.sizePolicy().hasHeightForWidth())
        self.pushButton_showtime.setSizePolicy(sizePolicy)
        self.pushButton_showtime.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pushButton_showtime.setObjectName(_fromUtf8("pushButton_showtime"))
        self.gridLayout.addWidget(self.pushButton_showtime, 0, 3, 1, 1)
        self.label_Time = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_Time.sizePolicy().hasHeightForWidth())
        self.label_Time.setSizePolicy(sizePolicy)
        self.label_Time.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_Time.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_Time.setObjectName(_fromUtf8("label_Time"))
        self.gridLayout.addWidget(self.label_Time, 0, 1, 1, 1)
        self.lineEdit_Time = QtGui.QLineEdit(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_Time.sizePolicy().hasHeightForWidth())
        self.lineEdit_Time.setSizePolicy(sizePolicy)
        self.lineEdit_Time.setMaximumSize(QtCore.QSize(150, 16777215))
        self.lineEdit_Time.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lineEdit_Time.setObjectName(_fromUtf8("lineEdit_Time"))
        self.gridLayout.addWidget(self.lineEdit_Time, 0, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        ViewerManager.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(ViewerManager)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuKepler_VIewer = QtGui.QMenu(self.menubar)
        self.menuKepler_VIewer.setObjectName(_fromUtf8("menuKepler_VIewer"))
        self.menuFIle = QtGui.QMenu(self.menubar)
        self.menuFIle.setObjectName(_fromUtf8("menuFIle"))
        ViewerManager.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(ViewerManager)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        ViewerManager.setStatusBar(self.statusbar)
        self.actionSave = QtGui.QAction(ViewerManager)
        self.actionSave.setObjectName(_fromUtf8("actionSave"))
        self.actionSave_Image = QtGui.QAction(ViewerManager)
        self.actionSave_Image.setObjectName(_fromUtf8("actionSave_Image"))
        self.actionLoad = QtGui.QAction(ViewerManager)
        self.actionLoad.setObjectName(_fromUtf8("actionLoad"))
        self.actionAbout_Kepler_Viewer = QtGui.QAction(ViewerManager)
        self.actionAbout_Kepler_Viewer.setObjectName(_fromUtf8("actionAbout_Kepler_Viewer"))
        self.menuKepler_VIewer.addAction(self.actionAbout_Kepler_Viewer)
        self.menuFIle.addAction(self.actionSave)
        self.menuFIle.addAction(self.actionSave_Image)
        self.menuFIle.addAction(self.actionLoad)
        self.menubar.addAction(self.menuKepler_VIewer.menuAction())
        self.menubar.addAction(self.menuFIle.menuAction())

        self.retranslateUi(ViewerManager)
        QtCore.QMetaObject.connectSlotsByName(ViewerManager)

    def retranslateUi(self, ViewerManager):
        ViewerManager.setWindowTitle(_translate("ViewerManager", "MainWindow", None))
        self.pushButton_showtime.setText(_translate("ViewerManager", "plot", None))
        self.label_Time.setText(_translate("ViewerManager", "Time:", None))
        self.menuKepler_VIewer.setTitle(_translate("ViewerManager", "Kepler VIewer", None))
        self.menuFIle.setTitle(_translate("ViewerManager", "FIle", None))
        self.actionSave.setText(_translate("ViewerManager", "Save", None))
        self.actionSave_Image.setText(_translate("ViewerManager", "Save Image", None))
        self.actionLoad.setText(_translate("ViewerManager", "Load", None))
        self.actionAbout_Kepler_Viewer.setText(_translate("ViewerManager", "About Kepler Viewer", None))

