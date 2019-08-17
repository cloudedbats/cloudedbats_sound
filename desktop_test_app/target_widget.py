#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://cloudedbats.org
# Copyright (c) 2019 Arnold Andreasson 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

from PyQt5 import QtCore
from PyQt5 import QtWidgets

class TargetWidget(QtWidgets.QWidget):
    """ """
    def __init__(self, parent=None):
        """ """
        super().__init__(parent)
        self.clear()
        
        self.selected_wavefile_path = None
        
        # Widgets.
        self.targetdir_edit = QtWidgets.QLineEdit('wavefiles_target')
        self.targetdir_browse_button = QtWidgets.QPushButton('Browse...')
        self.targetdir_browse_button.clicked.connect(self.targetdir_browse)
        
        self.subdir_1_edit = QtWidgets.QLineEdit('unidentified')
        self.copy_subdir_1_button = QtWidgets.QPushButton('Alt+1')
        self.copy_subdir_1_button.clicked.connect(self.copy_subdir_1)
        
        self.subdir_2_edit = QtWidgets.QLineEdit('barbastella')
        self.copy_subdir_2_button = QtWidgets.QPushButton('Alt+2')
        self.copy_subdir_2_button.clicked.connect(self.copy_subdir_2)
        
        self.subdir_3_edit = QtWidgets.QLineEdit('eptesicus')
        self.copy_subdir_3_button = QtWidgets.QPushButton('Alt+3')
        self.copy_subdir_3_button.clicked.connect(self.copy_subdir_3)
        
        self.subdir_4_edit = QtWidgets.QLineEdit('myotis')
        self.copy_subdir_4_button = QtWidgets.QPushButton('Alt+4')
        self.copy_subdir_4_button.clicked.connect(self.copy_subdir_4)
        
        self.subdir_5_edit = QtWidgets.QLineEdit('nyctalus')
        self.copy_subdir_5_button = QtWidgets.QPushButton('Alt+5')
        self.copy_subdir_5_button.clicked.connect(self.copy_subdir_5)
        
        self.subdir_6_edit = QtWidgets.QLineEdit('pipistrellus')
        self.copy_subdir_6_button = QtWidgets.QPushButton('Alt+6')
        self.copy_subdir_6_button.clicked.connect(self.copy_subdir_6)
        
        self.subdir_7_edit = QtWidgets.QLineEdit('plecotus')
        self.copy_subdir_7_button = QtWidgets.QPushButton('Alt+7')
        self.copy_subdir_7_button.clicked.connect(self.copy_subdir_7)
        
        self.subdir_8_edit = QtWidgets.QLineEdit('vespertilio')
        self.copy_subdir_8_button = QtWidgets.QPushButton('Alt+8')
        self.copy_subdir_8_button.clicked.connect(self.copy_subdir_8)
        
        self.subdir_9_edit = QtWidgets.QLineEdit('misc')
        self.copy_subdir_9_button = QtWidgets.QPushButton('Alt+9')
        self.copy_subdir_9_button.clicked.connect(self.copy_subdir_9)
        
        self.subdir_0_edit = QtWidgets.QLineEdit('trash')
        self.copy_subdir_0_button = QtWidgets.QPushButton('Alt+0')
        self.copy_subdir_0_button.clicked.connect(self.copy_subdir_0)
        
        self.deletefromsource_checkbox = QtWidgets.QCheckBox('Delete from source')
        self.deletefromsource_checkbox.setChecked(False)
        
        self.targetlists_combo = QtWidgets.QComboBox()
        self.targetlists_combo.setEditable(False)
#         self.targetlists_combo.setMinimumWidth(400)
        self.targetlists_combo.addItem('default')

        self.managetargetlists_button = QtWidgets.QPushButton('Manage lists...')
        
        # Layout.
        form1 = QtWidgets.QGridLayout()
        gridrow = 0
        label = QtWidgets.QLabel('Main target directory:')
        form1.addWidget(label, gridrow, 0, 1, 3)
        gridrow += 1
        form1.addWidget(self.targetdir_edit, gridrow, 0, 1, 2)
        form1.addWidget(self.targetdir_browse_button, gridrow, 2, 1, 1)
        gridrow += 1
        form1.addWidget(QtWidgets.QLabel(''), gridrow, 0, 1, 3)
        gridrow += 1
        form1.addWidget(QtWidgets.QLabel('Copy to subdirectories:'), gridrow, 0, 1, 3)
        gridrow += 1
        form1.addWidget(self.subdir_1_edit, gridrow, 0, 1, 2)
        form1.addWidget(self.copy_subdir_1_button, gridrow, 2, 1, 1)
        gridrow += 1
        form1.addWidget(self.subdir_2_edit, gridrow, 0, 1, 2)
        form1.addWidget(self.copy_subdir_2_button, gridrow, 2, 1, 1)
        gridrow += 1
        form1.addWidget(self.subdir_3_edit, gridrow, 0, 1, 2)
        form1.addWidget(self.copy_subdir_3_button, gridrow, 2, 1, 1)
        gridrow += 1
        form1.addWidget(self.subdir_4_edit, gridrow, 0, 1, 2)
        form1.addWidget(self.copy_subdir_4_button, gridrow, 2, 1, 1)
        gridrow += 1
        form1.addWidget(self.subdir_5_edit, gridrow, 0, 1, 2)
        form1.addWidget(self.copy_subdir_5_button, gridrow, 2, 1, 1)
        gridrow += 1
        form1.addWidget(self.subdir_6_edit, gridrow, 0, 1, 2)
        form1.addWidget(self.copy_subdir_6_button, gridrow, 2, 1, 1)
        gridrow += 1
        form1.addWidget(self.subdir_7_edit, gridrow, 0, 1, 2)
        form1.addWidget(self.copy_subdir_7_button, gridrow, 2, 1, 1)
        gridrow += 1
        form1.addWidget(self.subdir_8_edit, gridrow, 0, 1, 2)
        form1.addWidget(self.copy_subdir_8_button, gridrow, 2, 1, 1)
        gridrow += 1
        form1.addWidget(self.subdir_9_edit, gridrow, 0, 1, 2)
        form1.addWidget(self.copy_subdir_9_button, gridrow, 2, 1, 1)
        gridrow += 1
        form1.addWidget(self.subdir_0_edit, gridrow, 0, 1, 2)
        form1.addWidget(self.copy_subdir_0_button, gridrow, 2, 1, 1)
        gridrow += 1
        form1.addWidget(self.deletefromsource_checkbox, gridrow, 0, 1, 3)
        gridrow += 1
        form1.addWidget(QtWidgets.QLabel(''), gridrow, 0, 1, 3)
        gridrow += 1
        form1.addWidget(QtWidgets.QLabel('Target lists:'), gridrow, 0, 1, 3)
        gridrow += 1
        form1.addWidget(self.targetlists_combo, gridrow, 0, 1, 3)
        gridrow += 1
        form1.addWidget(self.managetargetlists_button, gridrow, 0, 1, 1)
        
        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(form1)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def clear(self):
        """ """
    
    def set_selected_wavefile(self, wavefile_path):
        """ """
        self.selected_wavefile_path = wavefile_path
    
    def targetdir_browse(self):
        """ """
        dirdialog = QtWidgets.QFileDialog(self)
        dirdialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        dirdialog.setFileMode(QtWidgets.QFileDialog.Directory)
        dirdialog.setOptions(QtWidgets.QFileDialog.ShowDirsOnly |
                             QtWidgets.QFileDialog.DontResolveSymlinks)
        dirdialog.setDirectory(str(self.targetdir_edit.text()))
        dirpath = dirdialog.getExistingDirectory()
        if dirpath:
            self.targetdir_edit.setText(dirpath)
    
    def copy_subdir_0(self):
        """ """
        print('DEBUG: copy_subdir_0')
    
    def copy_subdir_1(self):
        """ """
        print('DEBUG: copy_subdir_1')
    
    def copy_subdir_2(self):
        """ """
        print('DEBUG: copy_subdir_2')
    
    def copy_subdir_3(self):
        """ """
        print('DEBUG: copy_subdir_3')
    
    def copy_subdir_4(self):
        """ """
        print('DEBUG: copy_subdir_4')
    
    def copy_subdir_5(self):
        """ """
        print('DEBUG: copy_subdir_5')
    
    def copy_subdir_6(self):
        """ """
        print('DEBUG: copy_subdir_6')
    
    def copy_subdir_7(self):
        """ """
        print('DEBUG: copy_subdir_7')
    
    def copy_subdir_8(self):
        """ """
        print('DEBUG: copy_subdir_8')
    
    def copy_subdir_9(self):
        """ """
        print('DEBUG: copy_subdir_9')
    

