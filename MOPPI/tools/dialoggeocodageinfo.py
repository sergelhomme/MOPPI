from PyQt4 import QtCore, QtGui
from ui_dialoggeocodageinfo import Ui_DialogGeocodageInfo
class DialogGeocodageInfo(QtGui.QDialog):
  def __init__(self, parent):
    QtGui.QDialog.__init__(self, parent)
    self.ui = Ui_DialogGeocodageInfo()
    self.ui.setupUi(self)




