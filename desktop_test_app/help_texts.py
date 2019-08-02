#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://cloudedbats.org
# Copyright (c) 2019 Arnold Andreasson 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

class HelpTexts(object):  
    """ Help texts for the desktop application. 
        Mostly displayed in util_qt.RichTextQLabel labels, basic HTML tags can be used. 
    """
    
    def __init__(self, parent = None):  
        """ """
        self._texts = {}
        self._add_texts()
    
    def get_text(self, key):
        """ """
        try:
            return self._texts[key]
        except:
            pass
        return ''
    
    def _add_texts(self):
        """ """
        
        # Start activity.
        
        self._texts['dummy'] = """
        <p>&nbsp;</p>
        <h2>Welcome to CloudedBats - Desktop test application</h2>        
        """
        
        # About.
        
        self._texts['about'] = """
        <p>
        <b>CloudedBats - Desktop test application</b> <br>
        ###version###
        </p>
        <p>
        This test application is a part of the open source 
        <a href="http://cloudedbats.org">CloudedBats.org</a>
        software project.
        </p>
        <p>
        More information and source code at GitHub: 
        <a href="https://github.com/cloudedbats/cloudedbats_sound"> cloudedbats_sound</a>.
        </p>
        <p>
        Developed by: Arnold Andreasson, Sweden.<br/>        
        Contact and feedback: info@cloudedbats.org
        </p>
        """
