#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://cloudedbats.org
# Copyright (c) 2019 Arnold Andreasson 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import pathlib

class PulsePeaksReader():
    """ """
    def __init__(self):
        """ """
        self.clear()
    
    def clear(self):
        """ """
        self.metadata = {}
        self.pulse_peaks_table = []
    
    def get_metadata(self):
        """ """
        return self.metadata

    def get_pulse_peaks_table(self):
        """ """
        return self.pulse_peaks_table
    
    def get_time_freq_amp_ix(self):
        """ """
        x_time = []
        y_freq = []
        z_amp = []
        ix_amp = []
        for row in self.pulse_peaks_table:
            if row[0] == '1':
                if float(row[3]) > -100: # -100 means silent.
                    x_time.append(float(row[1]))
                    y_freq.append(float(row[2]))
                    z_amp.append(float(row[3]))
                    ix_amp.append(float(row[4]))
                        
        return x_time, y_freq, z_amp, ix_amp
    
    def read_pulse_peaks_file(self, file_path):
        """ """
        self.clear()
        
        pulse_peaks_path = pathlib.Path(file_path)
        with pulse_peaks_path.open('r') as peaks_file:
            for row in peaks_file:
                row_parts = [x.strip() for x in row.split('\t')]
                if row_parts[0] == '0':
                    metadata_key = row_parts[5]
                    metadata_value = row_parts[6]
                    self.metadata[metadata_key] = metadata_value
                if row_parts[0] in ['1', '2', '3', '4', '5']:
                    self.pulse_peaks_table.append(row_parts)



### TEST ###
if __name__ == "__main__":
    
    import numpy
    import datetime
    import matplotlib.pyplot
    
    """ """
    print('PulsePeaksReader test started. ',  datetime.datetime.now())
    # Read.
    reader = PulsePeaksReader()
    peaks_file_path = pathlib.Path('../wavefiles', 'test_chirp_generator_PEAKS.txt')
    reader.read_pulse_peaks_file(file_path=str(peaks_file_path))
    print('Length: ', len(reader.get_pulse_peaks_table()))
    # Metadata.
    print('Metadata: ', reader.get_metadata())
    # Plot.
    time, freq, amp, _ix = reader.get_time_freq_amp_ix()
    amp_min = abs(min(amp))
    sizes = [numpy.sqrt(x+amp_min) * 0.2 for x in amp]
    matplotlib.pyplot.scatter(time, freq, c=amp, s=sizes, cmap='Reds')
    matplotlib.pyplot.show()
    
    print('\n')
    print('PulsePeaksReader test ended. ',  datetime.datetime.now(), '\n')
    
