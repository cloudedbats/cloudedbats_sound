#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://cloudedbats.org
# Copyright (c) 2019 Arnold Andreasson 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import numpy
import pathlib
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from matplotlib.backends import backend_qt5agg
from matplotlib import pyplot

import datetime
import sound4bats

class PlottingWidget(QtWidgets.QWidget):
    """ """
    def __init__(self, parent=None):
        """ """
        super().__init__(parent)
        
        self.selected_wavefile_path = None
        
        self.clear()
        # Widgets.
        # Plot.
        self.plot_setup()
        
        self.wavefile_label = QtWidgets.QLabel('Selected wavefile: ')
        self.wavefile_name_label = QtWidgets.QLabel('')
        font = QtGui.QFont('Helvetica', pointSize=-1, weight=QtGui.QFont.Bold)
        self.wavefile_name_label.setFont(font)
        
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
        
        self.usetoolbar_checkbox = QtWidgets.QCheckBox('Navigation toolbar')
        self.usetoolbar_checkbox.setChecked(False)
        self.usetoolbar_checkbox.stateChanged.connect(self.usetoolbar_changed)
        
        self.compactview_checkbox = QtWidgets.QCheckBox('Compact view')
        self.compactview_checkbox.setChecked(True)
        self.compactview_checkbox.stateChanged.connect(self.compactview_changed)
        
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
        self.reset_button.clicked.connect(self.reset)
        
        self.autoreset_checkbox = QtWidgets.QCheckBox('Auto reset')
        self.autoreset_checkbox.setChecked(True)
        
        # Layout.
        layout = QtWidgets.QVBoxLayout()

        hlayout = QtWidgets.QHBoxLayout()
        hlayout.addWidget(self.wavefile_label)
        hlayout.addWidget(self.wavefile_name_label, 100)
        layout.addLayout(hlayout)
        
        layout.addWidget(self.canvas, 100)
        
        form1 = QtWidgets.QGridLayout()
        gridrow = 0
        form1.addWidget(self.toolbar, gridrow, 0, 1, 20)
        
        self.hscroll_label = QtWidgets.QLabel('Horizontal scroll:')
        form1.addWidget(self.hscroll_label, gridrow, 0, 1, 1)
        form1.addWidget(self.slider_center, gridrow, 1, 1, 18)
        form1.addWidget(self.reset_button, gridrow, 19, 1, 1)
        gridrow += 1
        self.hzoom_label = QtWidgets.QLabel('Horizontal zoom:')
        form1.addWidget(self.hzoom_label, gridrow, 0, 1, 1)
        form1.addWidget(self.slider_zoom, gridrow, 1, 1, 18)
        form1.addWidget(self.autoreset_checkbox, gridrow, 19, 1, 1)
        gridrow += 1
        hlayout = QtWidgets.QHBoxLayout()
        hlayout.addWidget(self.usetoolbar_checkbox)
        hlayout.addWidget(self.compactview_checkbox)
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
        
        # Updeate visibility.
        self.usetoolbar_changed()
        
        self.setLayout(layout)
#         #        
#         self.button.keyPressEvent = self.test_keyPressEvent
        
    def clear(self):
        self.time = []
        self.freq = []
        self.amp = []
        self.header = None
        
    def set_selected_wavefile(self, wavefile_path):
        """ """
        try:
            if wavefile_path:
                self.selected_wavefile_path = pathlib.Path(wavefile_path)
                self.wavefile_name_label.setText(str(self.selected_wavefile_path.name))
                self.update()
        except:
            pass
    
    def reset(self):
        """ """
        self.slider_center.setValue(50.0)
        self.slider_zoom.setValue(0.0)
        
#         toolbar = self.canvas.toolbar # Get the toolbar handler
        self.toolbar.update()
        
        self.update()
#         self.plot_redraw()
    
    def plot_setup(self):
        """ """
        self.figure = pyplot.figure()
        self.canvas = backend_qt5agg.FigureCanvasQTAgg(self.figure)
        self.toolbar = backend_qt5agg.NavigationToolbar2QT(self.canvas, self)
        self.figure.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.1)
        self.axes = self.figure.add_subplot(111)
    
    def update(self):
        """ """
        if self.selected_wavefile_path:
            peaks_file_path = pathlib.Path(str(self.selected_wavefile_path).replace('.wav', '_PEAKS.txt').replace('.WAV', '_PEAKS.txt'))
            if not peaks_file_path.exists():
                self.create_peaks_file(self.selected_wavefile_path, peaks_file_path)
            #
            self.read_peaks_file(peaks_file_path)
            self.plot()
        else:
            self.figure.clear()
    
    def read_peaks_file(self, peaks_file_path):
        """ """
        self.sampling_freq_hz = 384000
        self.time_min = 0.0
        self.time_max = 5.0
        self.freq_min = 0.0
        self.freq_max = 100.0
        
        self.time = []
        self.freq = []
        self.amp = []
        self.header = None
        #
        pulse_peaks_path = pathlib.Path(peaks_file_path)
        
        with pulse_peaks_path.open('r') as peaks_file:
            for row in peaks_file:
#                 print(row.strip())
                row_parts = [x.strip() for x in row.split('\t')]
                row_type= row_parts[0]
                #
                if self.header is None:
                    self.header = row_parts
                else:
                    if row_type == '0':
                        key = row_parts[5]
                        value = row_parts[6]
                        if key == 'rec_framerate_hz':
                            try: 
                                self.sampling_freq_hz = float(value)
                            except: pass
                        if key == 'rec_lenght_s':
                            try: 
                                self.time_max = float(value)
                            except: pass
                    
                    if row_type == '1':
                        try:
                            row_time = float(row_parts[1])
                            row_freq = float(row_parts[2])
                            row_amp = float(row_parts[3])
                            if row_amp > -100.0: # -100 means silent.
                                    self.time.append(row_time)
                                    self.freq.append(row_freq)
                                    self.amp.append(row_amp)
                        except: pass
    
    def plot_redraw(self):
        """ """
        if len(self.time) < 1:
            return
        
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
        
#         self.time_min = 0.0
#         self.time_max = 4.0
#         self.freq_min = 0.0
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
        
        
#         QtWidgets.QApplication.processEvents()
        
    
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
    
    def usetoolbar_changed(self):
        """ """
        self.reset()
        if self.usetoolbar_checkbox.isChecked():
            self.hscroll_label.hide()
            self.hzoom_label.hide()
            self.slider_center.hide()
            self.reset_button.hide()
            self.slider_zoom.hide()
            self.autoreset_checkbox.hide()
            self.toolbar.show()
        else:
            self.toolbar.hide()
            self.hscroll_label.show()
            self.hzoom_label.show()
            self.slider_center.show()
            self.reset_button.show()
            self.slider_zoom.show()
            self.autoreset_checkbox.show()
        #
        self.plot_redraw()
    
    def compactview_changed(self):
        """ """
    
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

    def create_peaks_file(self, wavefile_path, peaks_file_path):
        """ """
        extractor = sound4bats.PulsePeaksExtractor()
        extractor.extract_peaks_from_file(wavefile_path)
        extractor.save_result_table(file_path=str(peaks_file_path))
        
        return
        
#         print('PulseShapeExtractor test_dynamic_canvas_OLD started. ',  datetime.datetime.now())
#         
#     #     file_path = pathlib.Path('../data', 'test_chirp_generator.wav')
#         file_path = pathlib.Path(wavefile_path)
#         
#         with wave.open(str(file_path), 'r') as wave_file:
#             nchannels = wave_file.getnchannels() # 1=mono, 2=stereo.
#             sampwidth = wave_file.getsampwidth() # sample width in bytes.
#             framerate = wave_file.getframerate() # Sampling frequency.
#             nframes = wave_file.getnframes() # Number of audio frames.
#             
#             if int(framerate > 90000):
#                 framerate_hz = framerate
#                 lenght_s = int(nframes) / int(framerate)
#             else:
#                 # Probably time division by a factor of 10.
#                 framerate_hz = framerate * 10
#                 lenght_s = int(nframes) / int(framerate) / 10
#                 
#             buffer_raw = wave_file.readframes(int(nframes))
#     #         buffer_raw = wave_file.readframes(framerate_hz) # Max 1 sec.
#             signal = numpy.fromstring(buffer_raw, dtype=numpy.int16) / 32767
#         
#         print('framerate_hz: ', framerate_hz, ' lenght_s: ', lenght_s)
#         
#         extractor = sound4bats.PulsePeaksExtractor(debug=True)
#         extractor.setup(framerate_hz)
#         signal_filtered = extractor.filter(signal, filter_low_hz=20000, filter_high_hz=100000)
#         extractor.new_result_table()
#         extractor.extract_peaks(signal_filtered)
#         
#         peaks_file_path = pathlib.Path(str(self.selected_wavefile_path).replace('.wav', '_PEAKS.txt').replace('.WAV', '_PEAKS.txt'))
#         
#         extractor.save_result_table(file_path=str(peaks_file_path))
#         
#         print('Length: ', len(extractor.get_result_table()))
        
#         # Plot.
#         time = []
#         freq = []
#         amp = []
#         for row in extractor.get_result_table():
#             if row[0] == 1:
#     #             if row[3] > -100: # -100 means silent.
#                     time.append(float(row[1]))
#                     freq.append(float(row[2]))
#                     amp.append(float(row[3]))
#         #
#         amp_min = abs(min(amp))
#         sizes = [((x+amp_min)**1.2) * 0.1 for x in amp]
#         
#     #     matplotlib.pyplot.scatter(time, freq, c=sizes, s=sizes, cmap='Blues')
#         matplotlib.pyplot.scatter(time, freq, c=amp, s=sizes, cmap='Reds')
#         matplotlib.pyplot.show()
        
        print('\n')
        print('PulseShapeExtractor test_dynamic_canvas_OLD ended. ',  datetime.datetime.now(), '\n')
    
       
        
        
        