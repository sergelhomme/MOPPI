from PyQt4 import QtCore, QtGui
from ui_dialogdistancierinfo import Ui_DialogDistancierInfo
class DialogDistancierInfo(QtGui.QDialog):
  def __init__(self, parent):
    QtGui.QDialog.__init__(self, parent)
    self.ui = Ui_DialogDistancierInfo()
    self.ui.setupUi(self)




