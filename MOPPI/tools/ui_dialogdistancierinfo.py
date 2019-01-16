# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui

class Ui_DialogDistancierInfo(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(780, 290)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        Dialog.setFont(font)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(450, 240, 291, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.comboBox = QtGui.QComboBox(Dialog)
        self.comboBox.setGeometry(QtCore.QRect(140, 40, 221, 22))
        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(30, 42, 91, 20))
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.comboBoxb = QtGui.QComboBox(Dialog)
        self.comboBoxb.setGeometry(QtCore.QRect(140, 80, 221, 22))
        self.comboBoxb.setFont(font)
        self.comboBoxb.setObjectName("comboBoxb")
        self.labelb = QtGui.QLabel(Dialog)
        self.labelb.setGeometry(QtCore.QRect(30, 82, 91, 20))
        self.labelb.setFont(font)
        self.labelb.setObjectName("labelb")
        self.comboBoxc = QtGui.QComboBox(Dialog)
        self.comboBoxc.setGeometry(QtCore.QRect(140, 120, 221, 22))
        self.comboBoxc.setFont(font)
        self.comboBoxc.setObjectName("comboBoxc")
        self.labelc = QtGui.QLabel(Dialog)
        self.labelc.setGeometry(QtCore.QRect(30, 122, 91, 20))
        self.labelc.setFont(font)
        self.labelc.setObjectName("labelc")
        self.comboBoxe = QtGui.QComboBox(Dialog)
        self.comboBoxe.setGeometry(QtCore.QRect(140, 160, 221, 22))
        self.comboBoxe.setFont(font)
        self.comboBoxe.setObjectName("comboBoxe")
        self.labele = QtGui.QLabel(Dialog)
        self.labele.setGeometry(QtCore.QRect(30, 162, 91, 20))
        self.labele.setFont(font)
        self.labele.setObjectName("labele")

        self.lineedit = QtGui.QLineEdit(Dialog)
        self.lineedit.setGeometry(QtCore.QRect(140, 200, 321, 22))
        self.lineedit.setFont(font)
        self.lineedit.setObjectName("lineedit")
        self.labeld = QtGui.QLabel(Dialog)
        self.labeld.setGeometry(QtCore.QRect(30, 202, 91, 20))
        self.labeld.setFont(font)
        self.labeld.setObjectName("labeld")

        self.comboBox2 = QtGui.QComboBox(Dialog)
        self.comboBox2.setGeometry(QtCore.QRect(520, 40, 221, 22))
        self.comboBox2.setFont(font)
        self.comboBox2.setObjectName("comboBox2")
        self.label2 = QtGui.QLabel(Dialog)
        self.label2.setGeometry(QtCore.QRect(400, 42, 91, 20))
        self.label2.setFont(font)
        self.label2.setObjectName("label2")
        self.comboBox2b = QtGui.QComboBox(Dialog)
        self.comboBox2b.setGeometry(QtCore.QRect(520, 80, 221, 22))
        self.comboBox2b.setFont(font)
        self.comboBox2b.setObjectName("comboBox2b")
        self.label2b = QtGui.QLabel(Dialog)
        self.label2b.setGeometry(QtCore.QRect(400, 82, 91, 20))
        self.label2b.setFont(font)
        self.label2b.setObjectName("label2b")
        self.comboBox2c = QtGui.QComboBox(Dialog)
        self.comboBox2c.setGeometry(QtCore.QRect(520, 120, 221, 22))
        self.comboBox2c.setFont(font)
        self.comboBox2c.setObjectName("comboBox2c")
        self.label2c = QtGui.QLabel(Dialog)
        self.label2c.setGeometry(QtCore.QRect(400, 122, 91, 20))
        self.label2c.setFont(font)
        self.label2c.setObjectName("label2c")
        self.comboBox2e = QtGui.QComboBox(Dialog)
        self.comboBox2e.setGeometry(QtCore.QRect(520, 160, 221, 22))
        self.comboBox2e.setFont(font)
        self.comboBox2e.setObjectName("comboBox2e")
        self.label2e = QtGui.QLabel(Dialog)
        self.label2e.setGeometry(QtCore.QRect(400, 162, 101, 20))
        self.label2e.setFont(font)
        self.label2e.setObjectName("label2e")

        self.retranslateUi(Dialog)
        self.buttonBox.rejected.connect(Dialog.reject)
        self.buttonBox.accepted.connect(Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Personnel ID", None))
        self.labelb.setText(QtGui.QApplication.translate("Dialog", "Personnel Long", None))
        self.labelc.setText(QtGui.QApplication.translate("Dialog", "Personnel Lat", None))
        self.labeld.setText(QtGui.QApplication.translate("Dialog", "Clef API", None))
        t = u"Personnel Métier"
        self.labele.setText(t.encode('latin-1'))

        self.label2.setText(QtGui.QApplication.translate("Dialog", "Etablissement ID", None))
        self.label2b.setText(QtGui.QApplication.translate("Dialog", "Etablissement Long", None))
        self.label2c.setText(QtGui.QApplication.translate("Dialog", "Etablissement Lat", None))
        t2 = u"Etablissement Métier"
        self.label2e.setText(t2.encode('latin-1'))
