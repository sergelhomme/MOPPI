from PyQt4 import QtCore, QtGui
from ui_dialoggeocodage import Ui_DialogGeocodage
class DialogGeocodage(QtGui.QDialog):
  def __init__(self, parent):
    QtGui.QDialog.__init__(self, parent)
    self.ui = Ui_DialogGeocodage()
    self.ui.setupUi(self)




