#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://cloudedbats.org
# Copyright (c) 2019 Arnold Andreasson 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import sys
import numpy
import pathlib
from PyQt5 import QtCore
from PyQt5 import QtWidgets

import desktop_test_app

class WavefilesWidget(QtWidgets.QWidget):
    """ """
    def __init__(self, parent=None):
        """ """
        super().__init__(parent)
        #
        self.clear()
        # Widgets.
        
        self.workspacedir_edit = QtWidgets.QLineEdit('')
#         self.workspacedir_edit.textChanged.connect(self.workspace_changed)
        self.workspacedir_button = QtWidgets.QPushButton('Browse...')
        self.workspacedir_button.clicked.connect(self.workspace_dir_browse)
        
        self.surveys_tableview = desktop_test_app.ToolboxQTableView()
        self.surveys_tableview.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        
        self.scanallfiles_button = QtWidgets.QPushButton('Scan all files...')
        
###         self.surveys_tableview.clicked.connect(self.selected_survey_changed)
#         self.surveys_tableview.getSelectionModel().selectionChanged.connect(self.selected_survey_changed)

#         self.button = QtWidgets.QPushButton('Update')
#         self.button.clicked.connect(self.update)
#         # Plot.
#         self.plot_setup()
#         
#         self.slider_center = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
#         self.slider_center.setFocusPolicy (QtCore.Qt.NoFocus)
#         self.slider_center.valueChanged[int].connect(self.plot_redraw)
#         self.slider_center.sliderReleased.connect(self.plot_redraw)
#         
#         self.slider_zoom = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
#         self.slider_zoom.setFocusPolicy (QtCore.Qt.NoFocus)
#         self.slider_zoom.valueChanged.connect(self.plot_redraw)
#         self.slider_zoom.sliderReleased.connect(self.plot_redraw)
#         #
#         self.slider_center.setValue(50.0)
#         self.slider_zoom.setValue(0.0)
        # Layout.
        
        form1 = QtWidgets.QGridLayout()
        gridrow = 0
        label = QtWidgets.QLabel('Source directory:')
        form1.addWidget(label, gridrow, 0, 1, 1)
        gridrow += 1
        form1.addWidget(self.workspacedir_edit, gridrow, 0, 1, 10)
        form1.addWidget(self.workspacedir_button, gridrow, 11, 1, 1)
        gridrow += 1
        form1.addWidget(self.surveys_tableview, gridrow, 0, 1, 12)
        gridrow += 1
        form1.addWidget(self.scanallfiles_button, gridrow, 0, 1, 1)


        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(form1)
#         layout.addWidget(self.canvas)
#         layout.addWidget(self.slider_center)
#         layout.addWidget(self.slider_zoom)
#         layout.addWidget(self.button)
        
        self.setLayout(layout)
        
        self.refresh_survey_list()
        
    def clear(self):
        """ """
    
    def workspace_dir_browse(self):
        """ """
        dirdialog = QtWidgets.QFileDialog(self)
        dirdialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        dirdialog.setFileMode(QtWidgets.QFileDialog.Directory)
        dirdialog.setOptions(QtWidgets.QFileDialog.ShowDirsOnly |
                             QtWidgets.QFileDialog.DontResolveSymlinks)
        dirdialog.setDirectory(str(self.workspacedir_edit.text()))
        dirpath = dirdialog.getExistingDirectory()
        if dirpath:
            self.workspacedir_edit.setText(dirpath)
    
    def refresh_survey_list(self):
        """ """
        try:
            self.surveys_tableview.blockSignals(True)
            self.surveys_tableview.getSelectionModel().blockSignals(True)
            self.workspacedir_edit.blockSignals(True)
            #
            self.workspacedir_edit.setText('data')
            #
            dataset_table = desktop_test_app.DatasetTable()
            header = ['wavefile', 'target subdir']
            header_cap = []
            for item in header:
                header_cap.append(item.capitalize().replace('_', ' '))
            dataset_table.set_header(header_cap)
            #
#             selected_survey_index = None
#             for index, key in enumerate(sorted(h5_survey_dict)):
#                 h5_dict = h5_survey_dict[key]
#                 row = []
#                 for head in header:
#                     row.append(h5_dict.get(head, ''))
#                 dataset_table.append_row(row)
#                 h5_file = h5_dict.get('h5_file', None)
#                 if h5_file and (h5_file == h5_selected_survey):
#                     selected_survey_index = index
            #
            self.surveys_tableview.setTableModel(dataset_table)
            self.surveys_tableview.resizeColumnsToContents()
            #
#             if selected_survey_index is not None:
#                 qt_index =self.surveys_tableview.model().index(selected_survey_index, 0)
#                 self.surveys_tableview.setCurrentIndex(qt_index)
        finally:
            self.surveys_tableview.blockSignals(False)
            self.surveys_tableview.getSelectionModel().blockSignals(False)
            self.workspacedir_edit.blockSignals(False)
 
