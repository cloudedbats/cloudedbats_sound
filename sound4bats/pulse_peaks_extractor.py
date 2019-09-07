#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://cloudedbats.org
# Copyright (c) 2019 Arnold Andreasson 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import numpy
import pathlib
import wave

import dsp4bats

class PulsePeaksExtractor():
    """ """
    def __init__(self, debug=False):
        """ """
        self.debug = debug
        self.clear()
    
    def clear(self):
        """ """
        # Parameters.
        self.sampling_freq_hz = None
        self.filter_low_hz = None
        self.filter_high_hz = None
        # Calculated paramteres.
        self.filtered_noise_level_db = -100.0 # Low value if not used.
        # Utils.
        self.signal_util = None
        self.spectrum_wide = None
        self.spectrum_narrow = None
        #
        self.result_table = []
    
    def extract_peaks_from_file(self, wavefile_path, 
                                filter_low_hz=17000, filter_high_hz=None,
                                factor_steps_per_s=10000, 
                                min_amp_level_dbfs = -50, 
                                min_amp_level_relative = False):
        """ """
        self.clear()
        wavefile_path = pathlib.Path(wavefile_path)
        self.factor_steps_per_s = factor_steps_per_s
        self.min_amp_level_dbfs = min_amp_level_dbfs
        self.min_amp_level_relative = min_amp_level_relative
        
        with wave.open(str(wavefile_path), 'r') as wave_file:
#             nchannels = wave_file.getnchannels() # 1=mono, 2=stereo.
#             sampwidth = wave_file.getsampwidth() # sample width in bytes.
            sampling_freq = wave_file.getframerate() # Sampling frequency.
            nframes = wave_file.getnframes() # Number of audio frames.
            # Is it TE or not?
            if int(sampling_freq > 90000):
                sampling_freq_hz = sampling_freq
                lenght_s = int(nframes) / int(sampling_freq)
            else:
                # Probably time expansion by a factor of 10.
                sampling_freq_hz = sampling_freq * 10
                lenght_s = int(nframes) / int(sampling_freq) / 10
            # Read sound.
            buffer_raw = wave_file.readframes(int(nframes))
    #         buffer_raw = wave_file.readframes(sampling_freq_hz) # Max 1 sec.
            signal = numpy.fromstring(buffer_raw, dtype=numpy.int16) / 32767
        
        self.new_result_table()
        # Metadata.
        metadata = {}
        metadata['rec_sampling_freq_hz'] = str(sampling_freq_hz)
        metadata['rec_number_of_frames'] = str(nframes)
        metadata['rec_lenght_s'] = str(lenght_s)
        metadata['peaks_filter_low_hz'] = str(filter_low_hz)
        metadata['peaks_filter_high_hz'] = str(filter_high_hz)
        self.add_metadata(metadata)
        # Extract the peak values.
        self.setup(sampling_freq_hz)
        signal_filtered = self.filter(signal, filter_low_hz=filter_low_hz, filter_high_hz=filter_high_hz)
        self.extract_peaks(signal_filtered)
    
    def setup(self, sampling_freq_hz=384000):
        """ Setup utils. """
        self.sampling_freq = sampling_freq_hz
        # Time domain.
        self.signal_util = dsp4bats.SignalUtil(sampling_freq_hz)
        # Freq. domain for fast scanning.
        self.spectrum_wide = dsp4bats.DbfsSpectrumUtil(window_size=2048,
                                                  window_function='hanning',
                                                  sampling_freq=sampling_freq_hz)
        # Freq. domain for detailed scanning.
        self.spectrum_narrow = dsp4bats.DbfsSpectrumUtil(window_size=512,
                                                window_function='kaiser',
                                                kaiser_beta=20,
                                                  sampling_freq=sampling_freq_hz)
    
    def filter(self, signal, filter_low_hz=None, filter_high_hz=None):
        """ Time domain filtering and noise level. """
        self.filter_low_hz = filter_low_hz
        self.filter_high_hz = filter_high_hz
        #
        signal_filtered = self.signal_util.butterworth_filter(signal, 
                                                     low_freq_hz=self.filter_low_hz,
                                                     high_freq_hz=self.filter_high_hz)
        self.filtered_noise_level_db = self.signal_util.noise_level_in_db(signal_filtered)
        
        if self.debug:
            # Get all noise levels.
            noise_level = self.signal_util.noise_level(signal)
            noise_level_db = self.signal_util.noise_level_in_db(signal)
            filtered_noise_level = self.signal_util.noise_level(signal_filtered)
            print('Noise level:', 
                  numpy.round(noise_level, 5), 
                  ' after filtering: ', 
                  numpy.round(filtered_noise_level, 5), 
                  '\nNoise level (db):', 
                  numpy.round(noise_level_db, 5), 
                  ' after filtering: ', 
                  numpy.round(self.filtered_noise_level_db, 5), 
                  )
        
        return signal_filtered
    
    def extract_peaks(self, signal):
        """ """
        self.amp_limit_dbfs = self.min_amp_level_dbfs
        if self.min_amp_level_relative:
            self.amp_limit_dbfs = self.filtered_noise_level_db + self.min_amp_level_dbfs
        #
        time_s = 0.0
        pulse_ix = 0
        time_start = 0.0
        index_space_counter = 0 # Used to separate pulses.
        index_space_counter_start = int(self.factor_steps_per_s / 100) # Used to separate pulses.
        #
        try:
            size = int(len(signal) / self.sampling_freq * self.factor_steps_per_s)
            jump = int(self.sampling_freq/self.factor_steps_per_s)
            # Create the spectrogram matrix.
            matrix = self.spectrum_narrow.calc_dbfs_matrix(signal, matrix_size=size, jump=jump)
            #
            for index, spectrum_dbfs in enumerate(matrix):
                # Interpolate to get maximum freq and amp.
                freq_hz, amp = self.spectrum_narrow.interpolate_spectral_peak(spectrum_dbfs)
                # Extract.
                if amp >= self.amp_limit_dbfs:
                    index_space_counter = index_space_counter_start
                    time_s = time_start + index / self.factor_steps_per_s
                    row_type = 1
                    self.add_result_row(row_type, time_s, freq_hz, amp, pulse_ix)
                else:
                    # For the pulse index counter. Accept 10 ms before increment.
                    index_space_counter -= 1
                    if index_space_counter > 0:
                        time_s = time_start + index / self.factor_steps_per_s
                    elif index_space_counter == 0:
                        pulse_ix += 1
            #
            metadata = {}
            metadata['peaks_noise_level_dbfs'] = str(self.filtered_noise_level_db)
            metadata['peaks_amp_limit_dbfs'] = str(self.amp_limit_dbfs)
            metadata['peaks_number_of_pulses'] = str(pulse_ix)
            self.add_metadata(metadata)
            
# Maybe later:
#             # Calculate start time for next buffer.
#             time_start += len(signal) / self.sampling_freq
#             # Timebeat to enable scrolling when silent.
#             self.push_item((time_start,5, ix, 1)) 
#             self.add_row([time_start, 5, ix, 1]) 
        #
        except Exception as e:
            print('Exception: ', e)
    
    def new_result_table(self):
        """ """
        self.result_table = []
        
    def get_result_table(self):
        """ """
        return self.result_table
    
    def add_metadata(self, metadata={}):
        """ """
        for key, value in metadata.items():
            self.result_table.append(['0', '', '', '', '', key, value])
    
    def add_result_row(self, row_type, time_s, freq_hz, amp_dbfs, pulse_ix, info_key='', info_value=''):
        """ """
        freq_khz = numpy.round(freq_hz/1000.0, 1)
        amp_dbfs = numpy.round(amp_dbfs)
        
        self.result_table.append([row_type, time_s, freq_khz, amp_dbfs, pulse_ix, info_key, info_value])
        
    def save_result_table(self, file_path):
        """ """
        file_path = pathlib.Path(file_path)
        
        with file_path.open('w') as table_file:
            # Write header.
            table_file.write('\t'.join(['type', 'time_s', 'freq_khz', 'amp_dbfs', 'pulse_ix', 'info_key', 'info_value']) + '\n')
            for row in self.result_table:
                table_file.write('\t'.join([str(x) for x in row]) + '\n')
        
        return self.result_table
    


### TEST ###
if __name__ == "__main__":
    
    import datetime
    import matplotlib.pyplot
    
    """ """
    print('PulseShapeExtractor test started. ',  datetime.datetime.now())
    
#     wavefile_path = pathlib.Path('../wavefiles', 'M004092.WAV')
#     peaks_file_path = pathlib.Path('../wavefiles', 'M004092_PEAKS.txt')
    wavefile_path = pathlib.Path('../wavefiles', 'test_chirp_generator.wav')
    peaks_file_path = pathlib.Path('../wavefiles', 'test_chirp_generator_PEAKS.txt')
    
    extractor = PulsePeaksExtractor()
    extractor.extract_peaks_from_file(wavefile_path)
    extractor.save_result_table(file_path=str(peaks_file_path))
    
    print('Length: ', len(extractor.get_result_table()))
    
    # Plot.
    time = []
    freq = []
    amp = []
    for row in extractor.get_result_table():
        if row[0] == 1:
            if row[3] > -100: # -100 means silent.
                time.append(float(row[1]))
                freq.append(float(row[2]))
                amp.append(float(row[3]))
    #
    amp_min = abs(min(amp))
    sizes = [numpy.sqrt(x+amp_min) * 0.2 for x in amp]
    matplotlib.pyplot.scatter(time, freq, c=amp, s=sizes, cmap='Reds')
    matplotlib.pyplot.show()
    
    print('\n')
    print('PulseShapeExtractor test ended. ',  datetime.datetime.now(), '\n')
    
