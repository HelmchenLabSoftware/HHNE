import os       # allows file operations and direct command line execution
from PyQt5 import QtGui, QtCore, QtWidgets

from src import pynwb_helper, param_helper


class NWBGUI_MenuActions:
    def __init__(self, dialog, gui, interface):
        self.dialog = dialog
        self.gui = gui
        self.gui_interface = interface

        # React to menu operations
        self.gui.actionNew.triggered.connect(self.newfile)
        self.gui.actionOpen.triggered.connect(self.openfile)
        self.gui.actionSave.triggered.connect(self.savefile)
        self.gui.actionSave_as.triggered.connect(self.savefileas)
        self.gui.actionSave_as.triggered.connect(self.savefileas)
        self.gui.actionExit.triggered.connect(self.dialog.close)
        self.gui.actionLoadParamFile.triggered.connect(self.loadparams)
        self.gui.actionInfo.triggered.connect(self.fileinfo)

        # Global variables
        self.currentFile = ""               # Path to current file
        self.previousFile = ""              # Path to current file

        # Load default parameter file
        self.currentParamFile = "paramfiles/param-default.json"
        self.def_params = param_helper.loadparams(self.currentParamFile)


    # Re-used implementation of save-file dialog with a given caption. Saves the filepath to current_file
    def savefileImpl(self, caption):
        self.currentFile = QtWidgets.QFileDialog.getSaveFileName(caption=caption, directory="~/", filter="Neuroscience Without Borders files (*.nwb)")
        self.currentFile = os.path.splitext(self.currentFile[0])[0] + ".nwb"
        self.gui.overviewFileLineEdit.setText(self.currentFile)


    # Creates a new .NWB file. Allows data interface in response
    def newfile(self):
        self.savefileImpl("New project file")
        print("Made new file", os.path.basename(self.currentFile))
        self.current_params = self.def_params
        self.gui_interface.initData(self.current_params)



    # Opens an existing .NWB file. Allows data interface in response
    def openfile(self):
        # Get filename and read file
        self.currentFile = QtWidgets.QFileDialog.getOpenFileName(caption="Open project file", directory="~/", filter="Neuroscience Without Borders files (*.nwb)")
        self.currentFile = os.path.splitext(self.currentFile[0])[0] + ".nwb"
        self.gui.overviewFileLineEdit.setText(self.currentFile)
        self.nwbfile = pynwb_helper.readfile(self.currentFile)

        # Update interface w.r.t read parameters
        self.current_params = self.def_params
        self.current_params["file"] = pynwb_helper.getprojectparams(self.nwbfile)
        self.gui_interface.initData(self.current_params)
        print("Opened file", os.path.basename(self.currentFile))



    # Save changes to the file
    # After imported data is saved, clear data window
    # Don't save and complain if metadata for imported data was not filled in
    def savefile(self):
        param_file = self.gui_interface.getProjectParams()
        self.nwbfile = pynwb_helper.newfile(param_file)
        pynwb_helper.writefile(self.nwbfile, self.currentFile)

        print("Saved file", os.path.basename(self.currentFile))
        self.gui_interface.dataTreeClear()


    # Save header of this file under new name. Note that data is not auto-copied in this case.
    # If one wants to copy-paste the entire file, that can be done in standard file browser
    def savefileas(self):
        self.previousFile = self.currentFile
        self.savefileImpl("Save project file header as")
        print("Saved header of original file", os.path.basename(self.previousFile), "to new file", os.path.basename(self.currentFile))
        self.gui_interface.dataTreeClear()


    # Loads default parameters from the parameter file
    def loadparams(self):
        self.currentParamFile = QtWidgets.QFileDialog.getOpenFileName(caption="Open param file", directory="paramfiles/", filter="parameter files (*.txt)")[0]
        self.def_params = param_helper.loadparams(self.currentParamFile)


    # Extract info about this file
    def fileinfo(self):
        d = QtWidgets.QDialog()
        d.setFixedWidth(400)
        d.setFixedHeight(230)

        textedit1 = QtWidgets.QTextEdit("This fancy box will desplay complete file info one day", d)
        textedit1.setFixedWidth(400)
        textedit1.setFixedHeight(150)
        textedit1.set(False)

        b1 = QtWidgets.QPushButton("ok", d)
        b1.move(150, 170)
        b1.clicked.connect(d.close)

        d.setWindowTitle("Dialog")
        d.setWindowModality(QtCore.Qt.ApplicationModal)
        d.exec_()

