from PyQt4 import QtCore, QtGui
from ui_dialogdistancierinfotm import Ui_DialogDistancierInfoTM
class DialogDistancierInfoTM(QtGui.QDialog):
  def __init__(self, parent):
    QtGui.QDialog.__init__(self, parent)
    self.ui = Ui_DialogDistancierInfoTM()
    self.ui.setupUi(self)




