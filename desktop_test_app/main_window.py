#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://cloudedbats.org
# Copyright (c) 2019 Arnold Andreasson 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import time
import codecs
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui

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
        self._createCentralWidget()
        self._createActions()
        self._createMenu()
        self._createStatusBar()
        self._activity = None
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
        self._filemenu = self.menuBar().addMenu(self.tr('File'))
        self._filemenu.addSeparator()
        self._filemenu.addAction(self._quitaction)
        
        self._action = self.menuBar().addMenu(self.tr('Actions'))
        self._action.addSeparator()
        self._action.addAction(self._zoom_in)
        self._action.addAction(self._zoom_out)
        self._action.addAction(self._scrollright)
        self._action.addAction(self._scrollleft)
        self._action.addSeparator()
        self._action.addAction(self._previous)
        self._action.addAction(self._next)
        self._action.addSeparator()
        self._action.addAction(self._copy_0)
        self._action.addAction(self._copy_1)
        self._action.addAction(self._copy_2)
        self._action.addAction(self._copy_3)
        self._action.addAction(self._copy_4)
        self._action.addAction(self._copy_5)
        self._action.addAction(self._copy_6)
        self._action.addAction(self._copy_7)
        self._action.addAction(self._copy_8)
        self._action.addAction(self._copy_9)
        
        self._helpmenu = self.menuBar().addMenu(self.tr('Help'))
        self._helpmenu.addSeparator()
        self._helpmenu.addAction(self._aboutaction)
    
    def _createStatusBar(self):
        """ """
        self.statusBar().showMessage(self.tr('CloudedBats.'))
    
    def _createCentralWidget(self):
        """ """
        self.wavefile_widget = desktop_test_app.WavefilesWidget()
        self.central_widget = desktop_test_app.PlottingWidget()
        self.target_widget = desktop_test_app.TargetWidget()
        
        splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        splitter.addWidget(self.wavefile_widget)
        splitter.addWidget(self.central_widget)
        splitter.addWidget(self.target_widget)
        splitter.setStretchFactor(0, 10)
        splitter.setStretchFactor(1, 80)
        splitter.setStretchFactor(2, 10)
        #
#         layout = QtWidgets.QHBoxLayout()
#         layout.addWidget(splitter)
        
        self.setCentralWidget(splitter)
        
        self.central_widget.update()
        
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
        self._quitaction = QtWidgets.QAction(self.tr('Quit'), self)
        self._quitaction.setShortcut(self.tr('Ctrl+Q'))
        self._quitaction.setStatusTip(self.tr('Quit the application'))
        self._quitaction.triggered.connect(self.close)
        
        # Central widget.
        self._zoom_in = QtWidgets.QAction(self.tr('Zoom in'), self)
        self._zoom_in.setShortcut(self.tr('Alt+Shift+Up'))
        self._zoom_in.setStatusTip(self.tr('Zoom in'))
        self._zoom_in.triggered.connect(self.central_widget.zoom_in)
        
        self._zoom_out = QtWidgets.QAction(self.tr('Zoom out'), self)
        self._zoom_out.setShortcut(self.tr('Alt+Shift+Down'))
        self._zoom_out.setStatusTip(self.tr('Zoom out'))
        self._zoom_out.triggered.connect(self.central_widget.zoom_out)
        
        self._scrollright = QtWidgets.QAction(self.tr('Scroll right'), self)
        self._scrollright.setShortcut(self.tr('Alt+Shift+Right'))
        self._scrollright.setStatusTip(self.tr('Scroll right'))
        self._scrollright.triggered.connect(self.central_widget.scroll_right)
        
        self._scrollleft = QtWidgets.QAction(self.tr('Scroll left'), self)
        self._scrollleft.setShortcut(self.tr('Alt+Shift+Left'))
        self._scrollleft.setStatusTip(self.tr('Scroll left'))
        self._scrollleft.triggered.connect(self.central_widget.scroll_left)
        
        # Wavefile widget.
        self._previous = QtWidgets.QAction(self.tr('Previous wavefile'), self)
        self._previous.setShortcut(self.tr('Alt+Left'))
        self._previous.setStatusTip(self.tr('Previous wavefile'))
        self._previous.triggered.connect(self.wavefile_widget.previous_wavefile)
        
        self._next = QtWidgets.QAction(self.tr('Next wavefile'), self)
        self._next.setShortcut(self.tr('Alt+Right'))
        self._next.setStatusTip(self.tr('Next wavefile'))
        self._next.triggered.connect(self.wavefile_widget.next_wavefile)
        
        # Target widget.
        self._copy_0 = QtWidgets.QAction(self.tr('Copy file 0'), self)
        self._copy_0.setShortcut(self.tr('Alt+0'))
        self._copy_0.setStatusTip(self.tr('Copy file to target subdirectory, number 0.'))
        self._copy_0.triggered.connect(self.target_widget.copy_subdir_0)
        
        self._copy_1 = QtWidgets.QAction(self.tr('Copy file 1'), self)
        self._copy_1.setShortcut(self.tr('Alt+1'))
        self._copy_1.setStatusTip(self.tr('Copy file to target subdirectory, number 1.'))
        self._copy_1.triggered.connect(self.target_widget.copy_subdir_1)
        
        self._copy_2 = QtWidgets.QAction(self.tr('Copy file 2'), self)
        self._copy_2.setShortcut(self.tr('Alt+2'))
        self._copy_2.setStatusTip(self.tr('Copy file to target subdirectory, number 2.'))
        self._copy_2.triggered.connect(self.target_widget.copy_subdir_2)
        
        self._copy_3 = QtWidgets.QAction(self.tr('Copy file 3'), self)
        self._copy_3.setShortcut(self.tr('Alt+3'))
        self._copy_3.setStatusTip(self.tr('Copy file to target subdirectory, number 3.'))
        self._copy_3.triggered.connect(self.target_widget.copy_subdir_3)
        
        self._copy_4 = QtWidgets.QAction(self.tr('Copy file 4'), self)
        self._copy_4.setShortcut(self.tr('Alt+4'))
        self._copy_4.setStatusTip(self.tr('Copy file to target subdirectory, number 4.'))
        self._copy_4.triggered.connect(self.target_widget.copy_subdir_4)
        
        self._copy_5 = QtWidgets.QAction(self.tr('Copy file 5'), self)
        self._copy_5.setShortcut(self.tr('Alt+5'))
        self._copy_5.setStatusTip(self.tr('Copy file to target subdirectory, number 5.'))
        self._copy_5.triggered.connect(self.target_widget.copy_subdir_5)
        
        self._copy_6 = QtWidgets.QAction(self.tr('Copy file 6'), self)
        self._copy_6.setShortcut(self.tr('Alt+6'))
        self._copy_6.setStatusTip(self.tr('Copy file to target subdirectory, number 6.'))
        self._copy_6.triggered.connect(self.target_widget.copy_subdir_6)
        
        self._copy_7 = QtWidgets.QAction(self.tr('Copy file 7'), self)
        self._copy_7.setShortcut(self.tr('Alt+7'))
        self._copy_7.setStatusTip(self.tr('Copy file to target subdirectory, number 7.'))
        self._copy_7.triggered.connect(self.target_widget.copy_subdir_7)
        
        self._copy_8 = QtWidgets.QAction(self.tr('Copy file 8'), self)
        self._copy_8.setShortcut(self.tr('Alt+8'))
        self._copy_8.setStatusTip(self.tr('Copy file to target subdirectory, number 8.'))
        self._copy_8.triggered.connect(self.target_widget.copy_subdir_8)
        
        self._copy_9 = QtWidgets.QAction(self.tr('Copy file 9'), self)
        self._copy_9.setShortcut(self.tr('Alt+9'))
        self._copy_9.setStatusTip(self.tr('Copy file to target subdirectory, number 9.'))
        self._copy_9.triggered.connect(self.target_widget.copy_subdir_9)
        
        # Help.
        self._aboutaction = QtWidgets.QAction(self.tr('About'), self)
        self._aboutaction.setStatusTip(self.tr('Show the application\'s About box'))
        self._aboutaction.triggered.connect(self._about)
        
    def action_test(self, action):
        """ """
        print("DEBUG: Action: ", action)
        
        

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
    
    