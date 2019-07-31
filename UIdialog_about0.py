# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog_about(object):
    def setupUi(self, Dialog_about):
        Dialog_about.setObjectName("Dialog_about")
        Dialog_about.resize(448, 398)
        self.gridLayout = QtWidgets.QGridLayout(Dialog_about)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.tb_about = QtWidgets.QTextBrowser(Dialog_about)
        self.tb_about.setObjectName("tb_about")
        self.gridLayout.addWidget(self.tb_about, 0, 0, 1, 1)
        self.pb_close_about = QtWidgets.QPushButton(Dialog_about)
        self.pb_close_about.setObjectName("pb_close_about")
        self.gridLayout.addWidget(self.pb_close_about, 1, 0, 1, 1)

        self.retranslateUi(Dialog_about)
        QtCore.QMetaObject.connectSlotsByName(Dialog_about)

    def retranslateUi(self, Dialog_about):
        _translate = QtCore.QCoreApplication.translate
        Dialog_about.setWindowTitle(_translate("Dialog_about", "Dialog_about"))
        self.tb_about.setHtml(_translate("Dialog_about", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">DataViewer program reads HDF5 database format, general CSV format data, and exports to CSV format data or can Copy/Paste into excel spreadsheet directly.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Python Code Information:</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">    python                    3.6.1</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">    pyqt                        5.6.0 </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">    pandas                    0.18.1</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Author: YoonJun Kim </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Version: 0.2.0</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Date Released: 09/14/2017</p></body></html>"))
        self.pb_close_about.setText(_translate("Dialog_about", "Close"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog_about = QtWidgets.QDialog()
    ui = Ui_Dialog_about()
    ui.setupUi(Dialog_about)
    Dialog_about.show()
    sys.exit(app.exec_())

