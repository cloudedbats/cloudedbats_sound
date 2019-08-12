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

from matplotlib.backends import backend_qt5agg
from matplotlib import pyplot

class PlottingWidget(QtWidgets.QWidget):
    """ """
    def __init__(self, parent=None):
        """ """
        super().__init__(parent)
#         self.setMinimumSize(1500, 700)
        #
        self.clear()
        # Widgets.
        # Plot.
        self.plot_setup()
        
        self.slider_center = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.slider_center.setFocusPolicy (QtCore.Qt.NoFocus)
        self.slider_center.valueChanged[int].connect(self.plot_redraw)
        self.slider_center.sliderReleased.connect(self.plot_redraw)
        
        self.slider_zoom = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.slider_zoom.setFocusPolicy (QtCore.Qt.NoFocus)
        self.slider_zoom.valueChanged.connect(self.plot_redraw)
        self.slider_zoom.sliderReleased.connect(self.plot_redraw)
        #
        self.slider_center.setValue(50.0)
        self.slider_zoom.setValue(0.0)
        
        
        self.hidesilent_checkbox = QtWidgets.QCheckBox('Hide silent parts')
        self.hidesilent_checkbox.setChecked(True)
        
        self.maxfreq_combo = QtWidgets.QComboBox()
        self.maxfreq_combo.setEditable(False)
#         self.maxfreq_combo.setMinimumWidth(400)
        self.maxfreq_combo.addItem('Nyquist/2')
        self.maxfreq_combo.addItem('50')
        self.maxfreq_combo.addItem('80')
        self.maxfreq_combo.addItem('100')
        self.maxfreq_combo.addItem('150')
        self.maxfreq_combo.addItem('200')
        self.maxfreq_combo.addItem('250')
        
        self.reset_button = QtWidgets.QPushButton('Reset')
#         self.reset_button.clicked.connect(self.sourcedir_browse)

        
        self.autoreset_checkbox = QtWidgets.QCheckBox('Auto reset')
        self.autoreset_checkbox.setChecked(True)

        
        
        
        # Layout.
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.toolbar, 1)
        layout.addWidget(self.canvas, 100)
        
        form1 = QtWidgets.QGridLayout()
        gridrow = 0
        label = QtWidgets.QLabel('Scroll:')
        form1.addWidget(label, gridrow, 0, 1, 1)
        form1.addWidget(self.slider_center, gridrow, 1, 1, 18)
        form1.addWidget(self.reset_button, gridrow, 19, 1, 1)
        gridrow += 1
        label = QtWidgets.QLabel('Zoom:')
        form1.addWidget(label, gridrow, 0, 1, 1)
        form1.addWidget(self.slider_zoom, gridrow, 1, 1, 18)
        form1.addWidget(self.autoreset_checkbox, gridrow, 19, 1, 1)
        gridrow += 1
        hlayout = QtWidgets.QHBoxLayout()
        hlayout.addWidget(self.hidesilent_checkbox)
        hlayout.addWidget(QtWidgets.QLabel('Max frequency:'))
        hlayout.addWidget(self.maxfreq_combo)
        hlayout.addStretch()
#         hlayout.addWidget(self.autoreset_checkbox)
#         hlayout.addWidget(self.scanfiles_button)
#         hlayout.addWidget(self.scanfiles_button)
#         hlayout.addWidget(self.scanfiles_button)
#         hlayout.addWidget(self.scanfiles_button)
#         hlayout.addStretch()
        form1.addLayout(hlayout, gridrow, 0, 1, 20)
        
        layout.addLayout(form1, 1)
        
        self.setLayout(layout)
#         #        
#         self.button.keyPressEvent = self.test_keyPressEvent
        
    def clear(self):
        self.time = []
        self.freq = []
        self.amp = []
        self.header = None
    
    def plot_setup(self):
        """ """
        self.figure = pyplot.figure()
        self.canvas = backend_qt5agg.FigureCanvasQTAgg(self.figure)
        self.toolbar = backend_qt5agg.NavigationToolbar2QT(self.canvas, self)
        self.figure.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.1)
        self.axes = self.figure.add_subplot(111)
    
    def update(self):
        """ """
        self.settings()
        self.data()
        self.plot()
    
    def settings(self):
        """ """
        self.sampling_freq_hz = 384000
        self.freq_min = None
        self.freq_max = 100
    
    def data(self):
        """ """
        self.time = []
        self.freq = []
        self.amp = []
        self.header = None
        #
        pulse_peaks_path = pathlib.Path('wavefiles/pulse_peaks.txt')
        
        with pulse_peaks_path.open('r') as peaks_file:
            for row in peaks_file:
                print(row.strip())
                row_parts = row.split('\t')
                #
                if self.header == None:
                    self.header = row_parts
                    continue
                #
                if row_parts[0] == '1':
                    if float(row_parts[3]) > -100: # -100 means silent.
                            self.time.append(float(row_parts[1]))
                            self.freq.append(float(row_parts[2]))
                            self.amp.append(float(row_parts[3]))
        #
    def plot_redraw(self):
        """ """
        if len(self.time) < 1:
            return
        
        self.time_min = 0.0
        self.time_max = 4.0
        self.freq_min = 0.0
        self.freq_max = 100.0
        
        slider_center_value = self.slider_center.value() / 100.0 - 0.5
        slider_zoom_value = (self.slider_zoom.value() / 100.0)
        
        time_interval = (self.time_max - self.time_min)
        
        time_min =  self.time_min + (time_interval * slider_center_value)
        time_max = self.time_max + (time_interval * slider_center_value)
        
        time_min_new = time_min
        time_max_new = time_max
        if (slider_zoom_value > 0.0) and (slider_zoom_value < 1.0):
            time_c = time_min + ((time_max - time_min) / 2.0)
            time_min_new = time_c - ((1.0 - slider_zoom_value) * time_interval / 2)
            time_max_new = time_c + ((1.0 - slider_zoom_value) * time_interval / 2)
        
        self.axes.set_xlim(time_min_new, time_max_new)
        
        self.canvas.draw_idle()
    
    
    def plot(self):
        """ """
        self.slider_center.setValue(50.0)
        self.slider_zoom.setValue(0.0)
        
        if len(self.time) < 1:
            return
        
        self.time_min = 0.0
        self.time_max = 4.0
        self.freq_min = 0.0
        self.freq_max = 100.0
        
        slider_center_value = self.slider_center.value() / 100.0 - 0.5 # Value -1 to 1.
        slider_zoom_value = (self.slider_zoom.value() / 100.0)
        
        print('slider_center_value: ', slider_center_value)
        print('slider_zoom_value: ', slider_zoom_value)
        
        time_interval = self.time_max - self.time_min
        
        time_min =  self.time_min + (time_interval * slider_center_value)
        time_max = self.time_max + (time_interval * slider_center_value)
        
        freq_min = 0
        freq_max = 100
        
        if self.freq_max:
            freq_max = self.freq_max
        else:
            freq_max = int(self.sampling_freq_hz) / 2 / 1000
        
        amp_min = abs(min(self.amp))
#         sizes = [((x+amp_min)**1.5) * 0.01 for x in amp]
        sizes = [numpy.sqrt(x+amp_min) * 0.2 for x in self.amp]
        
        self.figure.clear()
        self.axes = self.figure.add_subplot(111)
        scatter = self.axes.scatter(self.time, self.freq, c=self.amp, s=sizes, cmap='Reds')
        
#         self.figure.colorbar(scatter, ax=self.axes, label='dBFS')
#         self.figure.colorbar(scatter, ax=self.axes, label='dBFS', 
#                              fraction=0.046, pad=0.1)
        from mpl_toolkits import axes_grid1
        divider = axes_grid1.make_axes_locatable(self.axes)
        cax = divider.append_axes("right", size="1.5%", pad=0.1)
        self.figure.colorbar(scatter, cax=cax, label='dBFS')
        #
        self.axes.set(ylim=(freq_min, freq_max),
                      xlim=(time_min, time_max),
                      ylabel='Frequency (kHz)',
                      xlabel='Time (s)')
        #
        self.axes.minorticks_on()
        major_yticks = numpy.arange(0, freq_max, 10)
        minor_yticks = numpy.arange(0, freq_max, 5)
        self.axes.set_yticks(major_yticks)
        self.axes.set_yticks(minor_yticks, minor=True)
        
        self.axes.grid(which='major', linestyle='-', linewidth='0.5', alpha=0.5)
        self.axes.grid(which='minor', linestyle='-', linewidth='0.5', alpha=0.2)
        #
        self.canvas.draw()
    
    def zoom_in(self):
        """ """
        self.slider_zoom.setValue(self.slider_zoom.value() + 1)
    
    def zoom_out(self):
        """ """
        self.slider_zoom.setValue(self.slider_zoom.value() - 1)
    
    def scroll_left(self):
        """ """
        self.slider_center.setValue(self.slider_center.value() - 1)
    
    def scroll_right(self):
        """ """
        self.slider_center.setValue(self.slider_center.value() + 1)
    
#     def test_keyPressEvent(self, event):
#             if event.key() == QtCore.Qt.Key_Right:
#                 self.slider_center.setValue(self.slider_center.value() + 1)
#             elif event.key() == QtCore.Qt.Key_Left:
#                 self.slider_center.setValue(self.slider_center.value() - 1)
#             elif event.key() == QtCore.Qt.Key_Up:
#                 self.slider_zoom.setValue(self.slider_zoom.value() + 1)
#             elif event.key() == QtCore.Qt.Key_Down:
#                 self.slider_zoom.setValue(self.slider_zoom.value() - 1)
#             else:
# #                 super().keyPressEvent(event)
#                 self.keyPressEvent(event)

