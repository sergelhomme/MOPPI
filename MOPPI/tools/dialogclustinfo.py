from PyQt4 import QtCore, QtGui
from ui_dialogclustinfo import Ui_DialogClustInfo
class DialogClustInfo(QtGui.QDialog):
  def __init__(self, parent):
    QtGui.QDialog.__init__(self, parent)
    self.ui = Ui_DialogClustInfo()
    self.ui.setupUi(self)




