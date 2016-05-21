# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/takayuki/Desktop/program/python/Spyder_workspcae/PyQt_test/ui/PyQt_test/caldialog.ui'
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

class Ui_CalDialog(object):
    def setupUi(self, CalDialog):
        CalDialog.setObjectName(_fromUtf8("CalDialog"))
        CalDialog.resize(400, 100)
        CalDialog.setMouseTracking(True)
        self.verticalLayout = QtGui.QVBoxLayout(CalDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.progressBar_Cal = QtGui.QProgressBar(CalDialog)
        self.progressBar_Cal.setProperty("value", 24)
        self.progressBar_Cal.setObjectName(_fromUtf8("progressBar_Cal"))
        self.verticalLayout.addWidget(self.progressBar_Cal)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_CalStop = QtGui.QPushButton(CalDialog)
        self.pushButton_CalStop.setObjectName(_fromUtf8("pushButton_CalStop"))
        self.horizontalLayout.addWidget(self.pushButton_CalStop)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(CalDialog)
        QtCore.QMetaObject.connectSlotsByName(CalDialog)

    def retranslateUi(self, CalDialog):
        CalDialog.setWindowTitle(_translate("CalDialog", "Dialog", None))
        self.pushButton_CalStop.setText(_translate("CalDialog", "Stop", None))

