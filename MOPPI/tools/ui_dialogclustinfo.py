# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui

class Ui_DialogClustInfo(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(450, 250)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        Dialog.setFont(font)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(130, 210, 291, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.comboBox = QtGui.QComboBox(Dialog)
        self.comboBox.setGeometry(QtCore.QRect(200, 40, 221, 22))
        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(30, 42, 151, 20))
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.comboBox2 = QtGui.QComboBox(Dialog)
        self.comboBox2.setGeometry(QtCore.QRect(200, 100, 221, 22))
        self.comboBox2.setFont(font)
        self.comboBox2.setObjectName("comboBox2")
        self.label2 = QtGui.QLabel(Dialog)
        self.label2.setGeometry(QtCore.QRect(30, 102, 151, 20))
        self.label2.setFont(font)
        self.label2.setObjectName("label2")
        self.lineedit3 = QtGui.QLineEdit(Dialog)
        self.lineedit3.setGeometry(QtCore.QRect(200, 160, 221, 22))
        self.lineedit3.setFont(font)
        self.lineedit3.setObjectName("lineedit3")
        self.label3 = QtGui.QLabel(Dialog)
        self.label3.setGeometry(QtCore.QRect(30, 162, 151, 20))
        self.label3.setFont(font)
        self.label3.setObjectName("label3")

        self.retranslateUi(Dialog)
        self.buttonBox.rejected.connect(Dialog.reject)
        self.buttonBox.accepted.connect(Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Identifiant Point", None))
        self.label2.setText(QtGui.QApplication.translate("Dialog", "Valeur Point", None))
        self.label3.setText(QtGui.QApplication.translate("Dialog", "Nombre de groupes", None))
