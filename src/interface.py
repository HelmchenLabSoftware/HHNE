import os       # allows file operations and direct command line execution
import datetime # get current time

from PyQt5 import QtGui, QtCore, QtWidgets

from src import stdoutForward, qtree_helper

class NWBGUI_Interface:
    def __init__(self, parent, gui):
        self.gui = gui
        self.parent = parent

        # Redirect python output to a window in QT
        self.stdoutHandler = stdoutForward.stdout2textbox(self.gui.pyOutTextEdit)

        # React to active elements
        self.gui.overviewSessionTimeNowButton.clicked.connect(self.setCurrentTime)
        self.gui.dataImportButton.clicked.connect(self.dataImportReact)
        self.gui.dataClearButton.clicked.connect(self.dataTreeClear)
        self.gui.dataStageComboBox.currentIndexChanged.connect(lambda : self.updateTypeComboBox(parent.gui_menuactions.current_params))
        self.gui.dataTypeComboBox.currentIndexChanged.connect(lambda: self.updateDataMetaQTree(parent.gui_menuactions.current_params))


    ########################
    # Overview Tab
    ########################


    # Put current timestamp in metadata
    def setCurrentTime(self):
        self.gui.overviewSessionTimeLineEdit.setText(datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p"))


    def setProjectParams(self, params):
        self.gui.overviewTitleLineEdit.setText(params['name'])
        self.gui.overviewSessionDescriptionLineEdit.setText(params['session_description'])
        self.gui.overviewIdentifierLineEdit.setText(params['identifier'])
        self.gui.overviewExperimenterLineEdit.setText(params['experimenter'])
        self.gui.overviewLabLineEdit.setText(params['lab'])
        self.gui.overviewInstitutionLineEdit.setText(params['institution'])
        self.gui.overviewExperimentDescriptionLineEdit.setText(params['experiment_description'])
        self.gui.overviewSessionIDLineEdit.setText(params['session_id'])
        self.gui.overviewSessionTimeLineEdit.setText(params['session_start_time'].strftime("%A, %d. %B %Y %I:%M%p"))


    def getProjectParams(self):
        params = {}
        params['name'] = self.gui.overviewTitleLineEdit.text()
        params['session_description'] = self.gui.overviewSessionDescriptionLineEdit.text()
        params['identifier'] = self.gui.overviewIdentifierLineEdit.text()
        params['experimenter'] = self.gui.overviewExperimenterLineEdit.text()
        params['lab'] = self.gui.overviewLabLineEdit.text()
        params['institution'] = self.gui.overviewInstitutionLineEdit.text()
        params['experiment_description'] = self.gui.overviewExperimentDescriptionLineEdit.text()
        params['session_id'] = self.gui.overviewSessionIDLineEdit.text()
        params['session_start_time'] = datetime.datetime.strptime(self.gui.overviewSessionTimeLineEdit.text(), "%A, %d. %B %Y %I:%M%p")
        return params


    ########################
    # Data Tab
    ########################

    def initData(self, params):
        self.dataTabEnable()
        self.setProjectParams(params['file'])
        self.updateStageComboBox(params)


    # Respond to data import button
    # Choose from available data import methods. Ask user to select file(s) to import
    # In case of Raw data, only import the selected file names
    # In case of importable files, parse them into hdf5, after user entered metadata and saved file
    # Add metadata options into qtreewidget based on selected stage and type. Force user to fill in before saving
    def dataImportReact(self):
        fileList = QtWidgets.QFileDialog.getOpenFileNames(caption="Import data files", directory="~/")[0]
        fileStr = ", ".join([os.path.basename(item) for item in fileList])
        print("Selected", len(fileList), "datafile links")
        qtree_helper.qtreeAddItem(self.gui.dataMetaTreeWidget, ['datafiles', fileStr])
        self.dataTreeEnable(True)


    # Enable data tab (in response to having a valid file to operate on)
    def dataTabEnable(self):
        self.gui.dataTab.setEnabled(True)


    # Enable QTree and buttons associated with QTree actions
    def dataTreeEnable(self, enable):
        self.gui.dataMetaTreeWidget.setEnabled(enable)
        self.gui.dataClearButton.setEnabled(enable)
        self.gui.dataGuessParamButton.setEnabled(enable)
        self.gui.dataExtraFieldButton.setEnabled(enable)


    # Clear and disable QTree
    def dataTreeClear(self):
        self.gui.dataMetaTreeWidget.clear()
        self.gui.dataMetaTreeWidget.setEnabled(False)
        self.dataTreeEnable(False)


    def updateStageComboBox(self, paramStageDict):
        self.gui.dataStageComboBox.blockSignals(True)
        self.gui.dataStageComboBox.clear()
        self.gui.dataStageComboBox.insertItem(0, "<Select Stage>")
        for it in paramStageDict.keys():
            if it != "file":
                self.gui.dataStageComboBox.insertItem(1, it)

        self.gui.dataStageComboBox.blockSignals(False)


    def updateTypeComboBox(self, paramStageDict):
        self.gui.dataTypeComboBox.blockSignals(True)
        self.gui.dataTypeComboBox.clear()
        stageName = self.gui.dataStageComboBox.itemText(self.gui.dataStageComboBox.currentIndex())
        paramTypeDict = paramStageDict[stageName]
        self.gui.dataTypeComboBox.insertItem(0, "<Select Type>")
        for it in paramTypeDict.keys():
            self.gui.dataTypeComboBox.insertItem(1, it)

        self.gui.dataTypeComboBox.blockSignals(False)


    def updateDataMetaQTree(self, paramStageDict):
        self.gui.dataMetaTreeWidget.blockSignals(True)
        stageName = self.gui.dataStageComboBox.itemText(self.gui.dataStageComboBox.currentIndex())
        typeName = self.gui.dataTypeComboBox.itemText(self.gui.dataTypeComboBox.currentIndex())
        paramValueDict = paramStageDict[stageName][typeName]

        self.gui.dataMetaTreeWidget.clear()
        for key, val in paramValueDict.items():
            self.qtreeAddItem(self.gui.dataMetaTreeWidget, )

        self.gui.dataMetaTreeWidget.blockSignals(False)




