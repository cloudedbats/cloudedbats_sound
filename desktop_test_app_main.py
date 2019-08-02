#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://cloudedbats.org
# Copyright (c) 2019 Arnold Andreasson 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

"""
Main module for the desktop application.
Organization name, domain and application name are used by QSettings. Settings
are stored in the register on Windows (path: "HKEY_CURRENT_USER/Software/...), 
in $HOME/.config on Linux and in $HOME/Library/Preferences on MacOS.
"""

# Matplotlib for PyQt5. 
# Backend must be defined before other matplotlib imports.
import matplotlib
matplotlib.use('Qt5agg')

import sys
from PyQt5 import QtWidgets
import desktop_test_app

def desktop_app():
    """ """
    app = QtWidgets.QApplication(sys.argv)
    app.setOrganizationName('CloudedBats.org')
    app.setOrganizationDomain('cloudedbats.org')
    app.setApplicationName('DesktopTestApp')
    
    # Create application and start the main event loop. 
    window = desktop_test_app.MainWindow()
    window.show()
    sys.exit(app.exec_())
    
# ===== Main. =====
if __name__ == "__main__":
    
    desktop_app()
    
