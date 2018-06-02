from PyQt4 import QtCore, QtGui
from ui_dialogdistancierinfoshp2 import Ui_DialogDistancierInfoShp2
class DialogDistancierInfoShp2(QtGui.QDialog):
  def __init__(self, parent):
    QtGui.QDialog.__init__(self, parent)
    self.ui = Ui_DialogDistancierInfoShp2()
    self.ui.setupUi(self)




