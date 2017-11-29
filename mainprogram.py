import locale   # language settings for date/time
import os       # allows file operations and direct command line execution
import sys      # command line arguments

from PyQt5 import QtGui, QtCore, QtWidgets

from nwbgui.mainwindow import Ui_MainWindow

from src import interface, menuactions

#######################################
# Compile QT File
#######################################
qtCompilePrefStr = 'pyuic5 '\
                   + os.path.join(os.path.dirname(os.path.abspath(__file__)), 'nwbgui/mainwindow.ui')\
                   + ' -o ' + os.path.join(os.path.dirname(os.path.abspath(__file__)), 'nwbgui/mainwindow.py')
print(qtCompilePrefStr)
os.system(qtCompilePrefStr)




#######################################################
# Main Window
#######################################################
class NWB_GUI () :
    def __init__(self, dialog):
        self.dialog = dialog
        self.gui = Ui_MainWindow()
        self.gui.setupUi(dialog)

        # Define helper classes
        self.gui_interface = interface.NWBGUI_Interface(self, self.gui)
        self.gui_menuactions = menuactions.NWBGUI_MenuActions(self.dialog, self.gui, self.gui_interface)




#######################################################
## Start the QT window
#######################################################
if __name__ == '__main__' :
    app = QtWidgets.QApplication(sys.argv)
    mainwindow = QtWidgets.QMainWindow()
    locale.setlocale(locale.LC_TIME, "en_GB.utf8")
    pth1 = NWB_GUI(mainwindow)
    mainwindow.show()
    sys.exit(app.exec_())