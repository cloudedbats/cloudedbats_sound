#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://cloudedbats.org
# Copyright (c) 2019 Arnold Andreasson 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import sys
import pathlib
from PyQt5 import QtCore
from PyQt5 import QtWidgets

import desktop_test_app

class WavefilesWidget(QtWidgets.QWidget):
    """ """
    def __init__(self, parent=None):
        """ """
        super().__init__(parent)
        self.clear()
        
        # Widgets.
        self.sourcedir_edit = QtWidgets.QLineEdit('wavefiles')
        self.sourcedir_edit.textChanged.connect(self.refresh_survey_list)
        self.sourcedir_button = QtWidgets.QPushButton('Browse...')
        self.sourcedir_button.clicked.connect(self.sourcedir_browse)
        
        self.wavefiles_tableview = desktop_test_app.ToolboxQTableView()
        self.wavefiles_tableview.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        
        self.scanfiles_button = QtWidgets.QPushButton('Scan files...')
        self.scanfiles_button.clicked.connect(self.scan_files)
        self.externalapp_button = QtWidgets.QPushButton('External app')
        self.externalapp_button.setStatusTip(self.tr('The selected file will be opened in an external application.'))
        self.externalapp_button.clicked.connect(self.external_app)
        
        self.previous_button = QtWidgets.QPushButton('Previous')
        self.previous_button.clicked.connect(self.previous_wavefile)
        self.next_button = QtWidgets.QPushButton('Next')
        self.next_button.clicked.connect(self.next_wavefile)
        
        # Action when selected wavefile has changed.
        self.wavefiles_tableview.getSelectionModel().selectionChanged.connect(self.selected_wavefile_changed)
        
        # Layout.        
        form1 = QtWidgets.QGridLayout()
        gridrow = 0
        label = QtWidgets.QLabel('Source directory:')
        form1.addWidget(label, gridrow, 0, 1, 1)
        gridrow += 1
        form1.addWidget(self.sourcedir_edit, gridrow, 0, 1, 10)
        form1.addWidget(self.sourcedir_button, gridrow, 11, 1, 1)
        gridrow += 1
        form1.addWidget(self.wavefiles_tableview, gridrow, 0, 1, 12)
        gridrow += 1
        hlayout = QtWidgets.QHBoxLayout()
        hlayout.addWidget(self.previous_button)
        hlayout.addWidget(self.next_button)
        hlayout.addStretch()
        form1.addLayout(hlayout, gridrow, 0, 1, 12)
        gridrow += 1
        hlayout = QtWidgets.QHBoxLayout()
        hlayout.addWidget(self.scanfiles_button)
        hlayout.addWidget(self.externalapp_button)
        hlayout.addStretch()
        form1.addLayout(hlayout, gridrow, 0, 1, 12)
        #
        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(form1)
        #
        self.setLayout(layout)
        
        # List available wavefiles.
        self.refresh_survey_list()
        
    def clear(self):
        """ """
    
    def sourcedir_browse(self):
        """ """
        dirdialog = QtWidgets.QFileDialog(self)
        dirdialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        dirdialog.setFileMode(QtWidgets.QFileDialog.Directory)
        dirdialog.setOptions(QtWidgets.QFileDialog.ShowDirsOnly |
                             QtWidgets.QFileDialog.DontResolveSymlinks)
        dirdialog.setDirectory(str(self.sourcedir_edit.text()))
        dirpath = dirdialog.getExistingDirectory()
        if dirpath:
            self.sourcedir_edit.setText(dirpath)
        #
        self.refresh_survey_list()
    
    def refresh_survey_list(self):
        """ """
        try:
            self.wavefiles_tableview.blockSignals(True)
            self.wavefiles_tableview.getSelectionModel().blockSignals(True)
            self.sourcedir_edit.blockSignals(True)
            #
            dir_path = str(self.sourcedir_edit.text())
            path_list = []
            file_ext_list = ['*.wav', '*.WAV']
            for file_ext in file_ext_list:
                for file_name in pathlib.Path(dir_path).glob(file_ext):
                    file_name_str = file_name.name
                    file_name_str = file_name_str.replace('._', '') # TODO: Strange chars when reading from ext. SSD?
                    if file_name_str not in path_list:
                        path_list.append(file_name_str)
            #
            dataset_table = desktop_test_app.DatasetTable()
            header = ['wavefile', 'target_subdir']
            header_cap = []
            for item in header:
                header_cap.append(item.capitalize().replace('_', ' '))
            dataset_table.set_header(header_cap)
            #
            for wave_file_path in sorted(path_list):
                dataset_table.append_row([wave_file_path, ''])
            #
            self.wavefiles_tableview.setTableModel(dataset_table)
            self.wavefiles_tableview.resizeColumnsToContents()
            #
#             if selected_survey_index is not None:
#                 qt_index =self.wavefiles_tableview.model().index(selected_survey_index, 0)
#                 self.wavefiles_tableview.setCurrentIndex(qt_index)
            
            qt_index = self.wavefiles_tableview.model().index(0, 0)
            self.wavefiles_tableview.setCurrentIndex(qt_index)
            
            self.selected_wavefile_changed()

        finally:
            self.wavefiles_tableview.blockSignals(False)
            self.wavefiles_tableview.getSelectionModel().blockSignals(False)
            self.sourcedir_edit.blockSignals(False)
            
    def selected_wavefile_changed(self):
        """ """
        try:
            modelIndex = self.wavefiles_tableview.currentIndex()
            if modelIndex.isValid():
                wavefile_name = str(self.wavefiles_tableview.model().index(modelIndex.row(), 0).data())
#                 # Sync.
#                 app_core.DesktopAppSync().set_selected_item_id(item_id)
                print('Wavefile selected:', wavefile_name)
            else:
                print('Wavefile selected: - ')
#                 app_core.DesktopAppSync().clear_selected_item_id()
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            desktop_test_app.Logging().error('Exception: (' + debug_info + '): ' + str(e))
    
    def previous_wavefile(self):
        """ """
        modelIndex = self.wavefiles_tableview.currentIndex()
        if modelIndex.isValid() and (modelIndex.row() > 0):
#             h5_survey = self.wavefiles_tableview.model().index(modelIndex.row(), 0).data()
            qt_index = self.wavefiles_tableview.model().index(modelIndex.row() - 1, 0)
            self.wavefiles_tableview.setCurrentIndex(qt_index)
    
    def next_wavefile(self):
        """ """
        modelIndex = self.wavefiles_tableview.currentIndex()
        size = self.wavefiles_tableview.model().rowCount()

        if modelIndex.isValid() and (modelIndex.row() < (size - 1)):
#             h5_survey = self.wavefiles_tableview.model().index(modelIndex.row(), 0).data()
            qt_index = self.wavefiles_tableview.model().index(modelIndex.row() + 1, 0)
            self.wavefiles_tableview.setCurrentIndex(qt_index)
    
    def scan_files(self):
        """ """
     
    def external_app(self):
        """ """
        path_to_app = '/usr/bin/sonic-visualiser'
        
        modelIndex = self.wavefiles_tableview.currentIndex()
        if modelIndex.isValid():
            wavefile_name = str(self.wavefiles_tableview.model().index(modelIndex.row(), 0).data())
            wavefile_path = str(pathlib.Path(str(self.sourcedir_edit.text()), wavefile_name))            
            print('Wavefile selected:', wavefile_path, ' Path to external app: ', path_to_app)
            if (wavefile_path):
                process = QtCore.QProcess(self)
    #             process.start(path_to_app, [wavefile_path, wavefile_path])
                process.start(path_to_app, [wavefile_path])


