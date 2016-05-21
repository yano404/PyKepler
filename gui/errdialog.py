# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/takayuki/Desktop/program/python/Spyder_workspcae/PyQt_test/ui/PyQt_test/errdialog.ui'
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

class Ui_ErrDialog(object):
    def setupUi(self, ErrDialog):
        ErrDialog.setObjectName(_fromUtf8("ErrDialog"))
        ErrDialog.resize(200, 100)
        self.verticalLayout = QtGui.QVBoxLayout(ErrDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_ErrMSG = QtGui.QLabel(ErrDialog)
        self.label_ErrMSG.setText(_fromUtf8(""))
        self.label_ErrMSG.setObjectName(_fromUtf8("label_ErrMSG"))
        self.verticalLayout.addWidget(self.label_ErrMSG)
        self.pushButton_ErrOK = QtGui.QPushButton(ErrDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_ErrOK.sizePolicy().hasHeightForWidth())
        self.pushButton_ErrOK.setSizePolicy(sizePolicy)
        self.pushButton_ErrOK.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pushButton_ErrOK.setObjectName(_fromUtf8("pushButton_ErrOK"))
        self.verticalLayout.addWidget(self.pushButton_ErrOK, QtCore.Qt.AlignHCenter)

        self.retranslateUi(ErrDialog)
        QtCore.QMetaObject.connectSlotsByName(ErrDialog)

    def retranslateUi(self, ErrDialog):
        ErrDialog.setWindowTitle(_translate("ErrDialog", "Dialog", None))
        self.pushButton_ErrOK.setText(_translate("ErrDialog", "OK", None))

