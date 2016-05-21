# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/takayuki/Desktop/program/python/Spyder_workspcae/PyQt_test/ui/PyQt_test/tableviewer.ui'
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

class Ui_TableViewer(object):
    def setupUi(self, TableViewer):
        TableViewer.setObjectName(_fromUtf8("TableViewer"))
        TableViewer.resize(500, 400)
        self.centralwidget = QtGui.QWidget(TableViewer)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lineEdit_Leap = QtGui.QLineEdit(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_Leap.sizePolicy().hasHeightForWidth())
        self.lineEdit_Leap.setSizePolicy(sizePolicy)
        self.lineEdit_Leap.setObjectName(_fromUtf8("lineEdit_Leap"))
        self.gridLayout.addWidget(self.lineEdit_Leap, 0, 2, 1, 1)
        self.comboBox_ChoosePlanet = QtGui.QComboBox(self.centralwidget)
        self.comboBox_ChoosePlanet.setObjectName(_fromUtf8("comboBox_ChoosePlanet"))
        self.gridLayout.addWidget(self.comboBox_ChoosePlanet, 0, 0, 1, 1)
        self.label_Leap = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_Leap.sizePolicy().hasHeightForWidth())
        self.label_Leap.setSizePolicy(sizePolicy)
        self.label_Leap.setObjectName(_fromUtf8("label_Leap"))
        self.gridLayout.addWidget(self.label_Leap, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.tableView_PlanetData = QtGui.QTableView(self.centralwidget)
        self.tableView_PlanetData.setObjectName(_fromUtf8("tableView_PlanetData"))
        self.verticalLayout.addWidget(self.tableView_PlanetData)
        TableViewer.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(TableViewer)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 500, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuTable_Viewer = QtGui.QMenu(self.menubar)
        self.menuTable_Viewer.setObjectName(_fromUtf8("menuTable_Viewer"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuExport = QtGui.QMenu(self.menuFile)
        self.menuExport.setObjectName(_fromUtf8("menuExport"))
        TableViewer.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(TableViewer)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        TableViewer.setStatusBar(self.statusbar)
        self.actionSave = QtGui.QAction(TableViewer)
        self.actionSave.setObjectName(_fromUtf8("actionSave"))
        self.actionSave_as = QtGui.QAction(TableViewer)
        self.actionSave_as.setObjectName(_fromUtf8("actionSave_as"))
        self.actionLoad = QtGui.QAction(TableViewer)
        self.actionLoad.setObjectName(_fromUtf8("actionLoad"))
        self.actionViewer = QtGui.QAction(TableViewer)
        self.actionViewer.setObjectName(_fromUtf8("actionViewer"))
        self.actionAbout_Table_Viewer = QtGui.QAction(TableViewer)
        self.actionAbout_Table_Viewer.setObjectName(_fromUtf8("actionAbout_Table_Viewer"))
        self.actionExport_JSON = QtGui.QAction(TableViewer)
        self.actionExport_JSON.setObjectName(_fromUtf8("actionExport_JSON"))
        self.actionCSV = QtGui.QAction(TableViewer)
        self.actionCSV.setObjectName(_fromUtf8("actionCSV"))
        self.actionJSON = QtGui.QAction(TableViewer)
        self.actionJSON.setObjectName(_fromUtf8("actionJSON"))
        self.menuTable_Viewer.addAction(self.actionAbout_Table_Viewer)
        self.menuExport.addAction(self.actionCSV)
        self.menuExport.addAction(self.actionJSON)
        self.menuFile.addAction(self.actionLoad)
        self.menuFile.addAction(self.menuExport.menuAction())
        self.menubar.addAction(self.menuTable_Viewer.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(TableViewer)
        QtCore.QMetaObject.connectSlotsByName(TableViewer)

    def retranslateUi(self, TableViewer):
        TableViewer.setWindowTitle(_translate("TableViewer", "MainWindow", None))
        self.label_Leap.setText(_translate("TableViewer", "Leap:", None))
        self.menuTable_Viewer.setTitle(_translate("TableViewer", "Table Viewer", None))
        self.menuFile.setTitle(_translate("TableViewer", "File", None))
        self.menuExport.setTitle(_translate("TableViewer", "Export", None))
        self.actionSave.setText(_translate("TableViewer", "Export CSV", None))
        self.actionSave_as.setText(_translate("TableViewer", "Save as...", None))
        self.actionLoad.setText(_translate("TableViewer", "Load", None))
        self.actionViewer.setText(_translate("TableViewer", "Viewer", None))
        self.actionAbout_Table_Viewer.setText(_translate("TableViewer", "About Table Viewer", None))
        self.actionExport_JSON.setText(_translate("TableViewer", "Export JSON", None))
        self.actionCSV.setText(_translate("TableViewer", "CSV", None))
        self.actionJSON.setText(_translate("TableViewer", "JSON", None))

