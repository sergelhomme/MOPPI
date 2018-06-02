from PyQt4 import QtCore, QtGui
from ui_dialogclustering import Ui_DialogClustering
class DialogClustering(QtGui.QDialog):
  def __init__(self, parent):
    QtGui.QDialog.__init__(self, parent)
    self.ui = Ui_DialogClustering()
    self.ui.setupUi(self)




