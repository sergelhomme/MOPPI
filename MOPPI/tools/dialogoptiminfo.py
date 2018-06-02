from PyQt4 import QtCore, QtGui
from ui_dialogoptiminfo import Ui_DialogOptimInfo
class DialogOptimInfo(QtGui.QDialog):
  def __init__(self, parent):
    QtGui.QDialog.__init__(self, parent)
    self.ui = Ui_DialogOptimInfo()
    self.ui.setupUi(self)




