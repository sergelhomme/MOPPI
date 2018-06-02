from PyQt4 import QtCore, QtGui
from ui_dialogdistancierinfoshp import Ui_DialogDistancierInfoShp
class DialogDistancierInfoShp(QtGui.QDialog):
  def __init__(self, parent):
    QtGui.QDialog.__init__(self, parent)
    self.ui = Ui_DialogDistancierInfoShp()
    self.ui.setupUi(self)




