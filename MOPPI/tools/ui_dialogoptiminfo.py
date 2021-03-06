# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui

class Ui_DialogOptimInfo(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(340, 490)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        Dialog.setFont(font)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(40, 440, 261, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.comboBox = QtGui.QComboBox(Dialog)
        self.comboBox.setGeometry(QtCore.QRect(160, 30, 141, 22))
        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(30, 32, 121, 20))
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.comboBox2 = QtGui.QComboBox(Dialog)
        self.comboBox2.setGeometry(QtCore.QRect(160, 90, 141, 22))
        self.comboBox2.setFont(font)
        self.comboBox2.setObjectName("comboBox2")
        self.label2 = QtGui.QLabel(Dialog)
        self.label2.setGeometry(QtCore.QRect(30, 92, 121, 20))
        self.label2.setFont(font)
        self.label2.setObjectName("label2")
        self.comboBox3 = QtGui.QComboBox(Dialog)
        self.comboBox3.setGeometry(QtCore.QRect(160, 150, 141, 22))
        self.comboBox3.setFont(font)
        self.comboBox3.setObjectName("comboBox3")
        self.label3 = QtGui.QLabel(Dialog)
        self.label3.setGeometry(QtCore.QRect(30, 152, 121, 20))
        self.label3.setFont(font)
        self.label3.setObjectName("label3")
        self.comboBox4 = QtGui.QComboBox(Dialog)
        self.comboBox4.setGeometry(QtCore.QRect(160, 210, 141, 22))
        self.comboBox4.setFont(font)
        self.comboBox4.setObjectName("comboBox4")
        self.label4 = QtGui.QLabel(Dialog)
        self.label4.setGeometry(QtCore.QRect(30, 212, 121, 20))
        self.label4.setFont(font)
        self.label4.setObjectName("label4")
        self.comboBox5 = QtGui.QComboBox(Dialog)
        self.comboBox5.setGeometry(QtCore.QRect(160, 270, 141, 22))
        self.comboBox5.setFont(font)
        self.comboBox5.setObjectName("comboBox5")
        self.label5 = QtGui.QLabel(Dialog)
        self.label5.setGeometry(QtCore.QRect(30, 272, 121, 20))
        self.label5.setFont(font)
        self.label5.setObjectName("label5")
        self.comboBox6 = QtGui.QComboBox(Dialog)
        self.comboBox6.setGeometry(QtCore.QRect(160, 330, 141, 22))
        self.comboBox6.setFont(font)
        self.comboBox6.setObjectName("comboBox6")
        self.label6 = QtGui.QLabel(Dialog)
        self.label6.setGeometry(QtCore.QRect(30, 332, 121, 20))
        self.label6.setFont(font)
        self.label6.setObjectName("label6")
        self.comboBox7 = QtGui.QComboBox(Dialog)
        self.comboBox7.setGeometry(QtCore.QRect(160, 390, 141, 22))
        self.comboBox7.setFont(font)
        self.comboBox7.setObjectName("comboBox7")
        self.label7 = QtGui.QLabel(Dialog)
        self.label7.setGeometry(QtCore.QRect(30, 392, 121, 20))
        self.label7.setFont(font)
        self.label7.setObjectName("label7")

        self.retranslateUi(Dialog)
        self.buttonBox.rejected.connect(Dialog.reject)
        self.buttonBox.accepted.connect(Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Identifiant Personnel", None))
        self.label2.setText(QtGui.QApplication.translate("Dialog", "Nombre Personnel", None))
        self.label3.setText(QtGui.QApplication.translate("Dialog", "Identifiant Etablissement", None))
        t = u"Capacité Etablissement"
        self.label4.setText(t.encode('latin-1'))
        t2 = u"Départ Distancier"
        self.label5.setText(t2.encode('latin-1'))
        t3 = u"Arrivée Distancier"
        self.label6.setText(t3.encode('latin-1'))
        self.label7.setText(QtGui.QApplication.translate("Dialog", "Temps", None))

