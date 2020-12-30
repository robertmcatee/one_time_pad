#! /usr/bin/env python3
"""
Generate One Time Pad files, or serve the pads up using a CherryPy server.
"""
from jinja2 import DictLoader, Environment
import secrets

import otp_main

"""Simple PyQt5."""
import sys, os

# 1. Import `QApplication` and all the required widgets

from PyQt5 import QtCore, QtWidgets, QtPrintSupport


class Window(QtWidgets.QMainWindow):
    """Main Window."""
    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        self.setWindowTitle('One Time Pad')
        self.text = QtWidgets.QTextEdit(self)
        self.setCentralWidget(self.text)
        #self._createMenu()
        self._createToolBar()
        self._createStatusBar()

    def _createMenu(self):
        self.menu = self.menuBar().addMenu("&Menu")
        self.menu.addAction('&Generate', self.generatePad)
        self.menu.addAction('&Print Preview', self.handlePreview)
        self.menu.addAction('&Print', self.handlePrint)
        self.menu.addAction('&Exit', self.close)


    def _createToolBar(self):
        tools = QtWidgets.QToolBar()
        self.addToolBar(tools)
        tools.addAction('&Generate', self.generatePad)
        tools.addAction('&Print Preview', self.handlePreview)
        tools.addAction('&Print', self.handlePrint)
        tools.addAction('&Exit', self.close)

    def _createStatusBar(self):
        status = QtWidgets.QStatusBar()
        status.showMessage("One Time Pad - Version 0.1")
        self.setStatusBar(status)

    def handlePrint(self):
        dialog = QtPrintSupport.QPrintDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            #self.centralWidget.document().print_(dialog.printer())
            self.text.document().print_(dialog.printer())

    def handlePreview(self):
        dialog = QtPrintSupport.QPrintPreviewDialog()
        dialog.paintRequested.connect(lambda p: self.text.print_(p))
        dialog.exec_()

    def generatePad(self):
        messages = (otp_main.generate_message() for _ in range(otp_main.MESSAGE_COUNT))
        #messages = (otp_main.generate_message() for _ in range(1))

        messages_list = list(messages)

        template = otp_main.env.get_template('one_time_pad')

        output = template.render(messages=messages_list)

        self.text = QtWidgets.QTextEdit(output)
        self.setCentralWidget(win.text)

if __name__ == '__main__':
    # https://realpython.com/python-pyqt-gui-calculator/
    app = QtWidgets.QApplication(sys.argv)
    win = Window()

    win.generatePad()

    win.show()
    sys.exit(app.exec_())