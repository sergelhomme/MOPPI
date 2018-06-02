from PyQt4 import QtCore, QtGui
from ui_dialogoptim import Ui_DialogOptim
class DialogOptim(QtGui.QDialog):
  def __init__(self, parent):
    QtGui.QDialog.__init__(self, parent)
    self.ui = Ui_DialogOptim()
    self.ui.setupUi(self)




