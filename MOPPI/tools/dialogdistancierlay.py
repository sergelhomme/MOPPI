from PyQt4 import QtCore, QtGui
from ui_dialogdistancierlay import Ui_DialogDistancierLay
class DialogDistancierLay(QtGui.QDialog):
  def __init__(self, parent):
    QtGui.QDialog.__init__(self, parent)
    self.ui = Ui_DialogDistancierLay()
    self.ui.setupUi(self)




