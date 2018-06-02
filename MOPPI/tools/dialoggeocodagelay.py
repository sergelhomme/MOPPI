from PyQt4 import QtCore, QtGui
from ui_dialoggeocodagelay import Ui_DialogGeocodageLay
class DialogGeocodageLay(QtGui.QDialog):
  def __init__(self, parent):
    QtGui.QDialog.__init__(self, parent)
    self.ui = Ui_DialogGeocodageLay()
    self.ui.setupUi(self)




