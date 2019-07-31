# -*- coding: utf-8 -*-


from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog_Summary(object):
    def setupUi(self, Dialog_Summary):
        Dialog_Summary.setObjectName("Dialog_Summary")
        Dialog_Summary.resize(641, 419)
        self.gridLayout = QtWidgets.QGridLayout(Dialog_Summary)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.pb_close_summary = QtWidgets.QPushButton(Dialog_Summary)
        self.pb_close_summary.setObjectName("pb_close_summary")
        self.gridLayout.addWidget(self.pb_close_summary, 1, 0, 1, 1)
        self.tv_summary = QtWidgets.QTableView(Dialog_Summary)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.tv_summary.setFont(font)
        self.tv_summary.setObjectName("tv_summary")
        self.gridLayout.addWidget(self.tv_summary, 0, 0, 1, 1)

        self.retranslateUi(Dialog_Summary)
        QtCore.QMetaObject.connectSlotsByName(Dialog_Summary)

    def retranslateUi(self, Dialog_Summary):
        _translate = QtCore.QCoreApplication.translate
        Dialog_Summary.setWindowTitle(_translate("Dialog_Summary", "Dialog_Summary"))
        self.pb_close_summary.setText(_translate("Dialog_Summary", "Close"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog_Summary = QtWidgets.QDialog()
    ui = Ui_Dialog_Summary()
    ui.setupUi(Dialog_Summary)
    Dialog_Summary.show()
    sys.exit(app.exec_())

