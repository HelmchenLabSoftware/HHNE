import sys
from PyQt5 import QtGui, QtCore, QtWidgets



# Stream class for standart output forwarding
class myStream(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))

    def flush(self):
        pass


# Forwards the standard output to a textbox in QT
class stdout2textbox():
    def __init__(self, qTextEdit):
        # Replace standard output stream with magic stream
        sys.stdout = myStream(textWritten=self.normalOutputWritten)
        self.qTextEdit = qTextEdit

    def __del__(self):
        # Restore sys.stdout
        sys.stdout = sys.__stdout__


    def normalOutputWritten(self, text):
        """Append text to the QTextEdit."""
        # Maybe QTextEdit.append() works as well
        cursor = self.qTextEdit.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.qTextEdit.setTextCursor(cursor)
        self.qTextEdit.ensureCursorVisible()