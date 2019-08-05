#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://cloudedbats.org
# Copyright (c) 2019 Arnold Andreasson 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import time
import codecs
from PyQt5 import QtWidgets
from PyQt5 import QtCore

import desktop_test_app

class MainWindow(QtWidgets.QMainWindow):
    """ """
    def __init__(self):
        """ """
        # Initialize parent.
        super(MainWindow, self).__init__()
        self.setWindowTitle(self.tr('CloudedBats.org - Desktop Test Application'))
        # Version.
        self._version = ''
        # Note: Tools menu is public.
        self.toolsmenu = None
        # Load app settings.
        self._ui_settings = QtCore.QSettings()
        # Logging. Log to file.
        self._logfile = codecs.open('desktop_test_app_log.txt', mode = 'w', encoding = 'cp1252')
        self._logfile.write('CloudedBats.org ' +
                             time.strftime('%Y-%m-%d %H:%M:%S') )
        self._logfile.write('')
        desktop_test_app.Logging().set_log_target(self)
        # Setup main window.
        self._createActions()
        self._createMenu()
        self._createStatusBar()
        self._activity = None
        self._createCentralWidget()
        # Load last used window positions.
        size = self._ui_settings.value('XMainWindow/Size', QtCore.QSize(900, 600))
        position = self._ui_settings.value('XMainWindow/Position', QtCore.QPoint(100, 80))
        # Check if outside window.
        screengeometry = QtWidgets.QDesktopWidget().screenGeometry()
        if ((size.width() + position.x()) > screengeometry.width()) or \
            ((size.height() + position.y()) > screengeometry.height()):
            size.setWidth(900)
            size.setHeight(600)
            position.setX(100)
            position.setY(80)
        elif (position.x() < -10) or \
             (position.y() < -10):
            size.setWidth(900)
            size.setHeight(600)
            position.setX(100)
            position.setY(80)
        else:
            try:   
                self.setGeometry(self._ui_settings.value('MainWindow/Geometry'))
                self.restoreState(self._ui_settings.value('MainWindow/State'))
                size = self._ui_settings.value('MainWindow/Size', QtCore.QVariant(QtCore.QSize(900, 600))) #.toSize()
                position = self._ui_settings.value('MainWindow/Position', QtCore.QVariant(QtCore.QPoint(100, 50))) #.toPoint()
            except:
                pass # May contain None at first start on new computer.
        #
        self.resize(size)
        self.move(position)
    
    def closeEvent(self, event):
        """ Called on application shutdown. """
        # Stores current window positions.
        self._ui_settings.setValue('MainWindow/Size', QtCore.QVariant(self.size()))
        self._ui_settings.setValue('MainWindow/Position', QtCore.QVariant(self.pos()))
        self._ui_settings.setValue('MainWindow/State', self.saveState())
        self._ui_settings.setValue('MainWindow/Geometry', self.geometry())
        # And finally close the log file.
        self._logfile.close
    
    def _createMenu(self):
        """ """
        self._filemenu = self.menuBar().addMenu(self.tr('&File'))
        self._filemenu.addSeparator()
        self._filemenu.addAction(self._quitaction)
        self._helpmenu = self.menuBar().addMenu(self.tr('&Help'))
        self._helpmenu.addSeparator()
        self._helpmenu.addAction(self._aboutaction)
    
    def _createStatusBar(self):
        """ """
        self.statusBar().showMessage(self.tr('CloudedBats.'))
    
    def _createCentralWidget(self):
        """ """
        wavefile_widget = desktop_test_app.WavefilesWidget()
        central_widget = desktop_test_app.PlottingWidget()
        target_widget = desktop_test_app.TargetWidget()
        
        
        splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        splitter.addWidget(wavefile_widget)
        splitter.addWidget(central_widget)
        splitter.addWidget(target_widget)
        splitter.setStretchFactor(0, 5)
        splitter.setStretchFactor(1, 90)
        splitter.setStretchFactor(2, 5)
        #
#         layout = QtWidgets.QHBoxLayout()
#         layout.addWidget(splitter)
        
        self.setCentralWidget(splitter)
        
        central_widget.update()
        
#         self._activitystack = QtWidgets.QStackedLayout()
#         # Layout widgets.
#         widget = QtWidgets.QWidget(self) 
#         layout = QtWidgets.QVBoxLayout()
#         widget.setLayout(layout)
#         self.setCentralWidget(widget)
# ###        layout.addWidget(self._activityheader)
#         layout.addLayout(self._activitystack)
#         # Dummy stack content.
#         dummy = QtWidgets.QWidget(self)
#         self._activitystack.addWidget(dummy)
       
    def _createActions(self):
        """ Common application related actions. """
        self._quitaction = QtWidgets.QAction(self.tr('&Quit'), self)
        self._quitaction.setShortcut(self.tr('Ctrl+Q'))
        self._quitaction.setStatusTip(self.tr('Quit the application'))
        self._quitaction.triggered.connect(self.close)
        #
        self._aboutaction = QtWidgets.QAction(self.tr('&About'), self)
        self._aboutaction.setStatusTip(self.tr('Show the application\'s About box'))
        self._aboutaction.triggered.connect(self._about)

    def write_to_log(self, message):
        """ Log to file and to the log tool when available. """
#        self.console.addItem(message)
        try:
            self._logfile.write(message + '\r\n')
            self._logfile.flush()
        #
        except Exception as e:
            print('Exception (write_to_log):', e)
    
    def _about(self):
        """ """
        about_text = desktop_test_app.HelpTexts().get_text('about')
        about_text = about_text.replace('###version###', 
                            ' Version: ' + self._version)
        
        QtWidgets.QMessageBox.about(self, self.tr('About'), self.tr(about_text))
    
    