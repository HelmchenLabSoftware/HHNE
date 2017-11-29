from PyQt5 import QtGui, QtCore, QtWidgets


# Add new item to QTree from list of strings
def qtreeAddItem(self, qtree, vallist):
    item = QtWidgets.QTreeWidgetItem(qtree)
    qtree.addTopLevelItem(item)

    for idx, val in enumerate(vallist):
        item.setText(idx, val)