#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://cloudedbats.org
# Copyright (c) 2019 Arnold Andreasson 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import numpy
import pathlib

import dsp4bats

class PulsePeaksReader():
    """ """
    def __init__(self, debug=False):
        """ """
        self.debug = debug
        self.clear()
    
    def clear(self):
        """ """
#         # Parameters.
#         self.sampling_freq_hz = None
#         self.filter_low_hz = None
#         self.filter_high_hz = None
#         # Calculated paramteres.
#         self.filtered_noise_level_db = -100.0 # Low value if not used.
#         # Utils.
#         self.signal_util = None
#         self.spectrum_wide = None
#         self.spectrum_narrow = None
#         #
#         self.result_table = []
#     
#     def setup(self, sampling_freq_hz=384000):
#         """ Setup utils. """
#         self.sampling_freq = sampling_freq_hz
#         # Time domain.
#         self.signal_util = dsp4bats.SignalUtil(sampling_freq_hz)
#         # Freq. domain for fast scanning.
#         self.spectrum_wide = dsp4bats.DbfsSpectrumUtil(window_size=2048,
#                                                   window_function='hanning',
#                                                   sampling_freq=sampling_freq_hz)
#         # Freq. domain for detailed scanning.
#         self.spectrum_narrow = dsp4bats.DbfsSpectrumUtil(window_size=512,
# #                                                   window_function='hanning',
#                                                 window_function='kaiser',
#                                                 kaiser_beta=20,
# #                                                 kaiser_beta=14,
#                                                   sampling_freq=sampling_freq_hz)
#     
#     def filter(self, signal, filter_low_hz=None, filter_high_hz=None):
#         """ Time domain filtering and noise level. """
#         self.filter_low_hz = filter_low_hz
#         self.filter_high_hz = filter_high_hz
#         #
#         signal_filtered = self.signal_util.butterworth_filter(signal, 
#                                                      low_freq_hz=self.filter_low_hz,
#                                                      high_freq_hz=self.filter_high_hz)
#         self.filtered_noise_level_db = self.signal_util.noise_level_in_db(signal_filtered)
#         
#         if self.debug:
#             # Get all noise levels.
#             noise_level = self.signal_util.noise_level(signal)
#             noise_level_db = self.signal_util.noise_level_in_db(signal)
#             filtered_noise_level = self.signal_util.noise_level(signal_filtered)
#             print('Noise level:', 
#                   numpy.round(noise_level, 5), 
#                   ' after filtering: ', 
#                   numpy.round(filtered_noise_level, 5), 
#                   '\nNoise level (db):', 
#                   numpy.round(noise_level_db, 5), 
#                   ' after filtering: ', 
#                   numpy.round(self.filtered_noise_level_db, 5), 
#                   )
#         
#         return signal_filtered
#     
#     def extract_peaks(self, signal, 
#                       factor_steps_per_s=10000, 
#                       min_amp_level_dbfs = -50, 
#                       min_amp_level_relative = False):
#         """ """
#         # Settings.
#         self.factor_steps_per_s = factor_steps_per_s # Factor is number of steps per sec.
#         # Select the highest value of these. 
#         self.amp_limit_dbfs = min_amp_level_dbfs
#         if min_amp_level_relative:
#             self.amp_limit_dbfs = self.filtered_noise_level_db + min_amp_level_dbfs
#         #
#         time_s = 0.0
#         pulse_ix = 0
#         time_start = 0.0
#         index_space_counter = 0 # Used to separate pulses.
#         index_space_counter_start = 20 # Used to separate pulses.
#         #
#         try:
#             size = int(len(signal) / self.sampling_freq * self.factor_steps_per_s)
#             jump = int(self.sampling_freq/self.factor_steps_per_s)
#             # Create the spectrogram matrix.
#             matrix = self.spectrum_narrow.calc_dbfs_matrix(signal, matrix_size=size, jump=jump)
#             
# ####            matrix = matrix - 10 
#             
#             #
#             for index, spectrum_dbfs in enumerate(matrix):
#                 # Interpolate to get maximum freq and amp.
#                 freq_hz, amp = self.spectrum_narrow.interpolate_spectral_peak(spectrum_dbfs)
#                 # Extract.
#                 if amp >= self.amp_limit_dbfs:
#                     
#                     
#                     
#                     
# #                     # Standard deviation.
# #                     sdev = numpy.std(spectrum_dbfs)
# #                     smean = numpy.mean(spectrum_dbfs)
# #                     smax = numpy.max(spectrum_dbfs)
# #                     print('SDEV: ', sdev, '   MEAN: ', smean, '   MAX: ', smax)
#                     
#                     
#                     
#                     
#                     index_space_counter = index_space_counter_start
#                     time_s = time_start + index / self.factor_steps_per_s
#                     #
#                     row_type = 1
#                     self.add_result_row(row_type, time_s, freq_hz, amp, pulse_ix)
#                 else:
#                     index_space_counter -= 1
#                     if index_space_counter > 0:
#                         row_type = 1
#                         time_s = time_start + index / self.factor_steps_per_s
#                         freq_hz = 0.0
#                         amp_dbfs = -100.0
#                         self.add_result_row(row_type, time_s, freq_hz, amp_dbfs, pulse_ix)
#                     elif index_space_counter == 0:
#                         pulse_ix += 1
#             
# # Maybe later:
# #             # Calculate start time for next buffer.
# #             time_start += len(signal) / self.sampling_freq
# #             # Timebeat to enable scrolling when silent.
# #             self.push_item((time_start,5, ix, 1)) 
# #             self.add_row([time_start, 5, ix, 1]) 
#         #
#         except Exception as e:
#             print('Exception: ', e)
#     
#     def new_result_table(self):
#         """ """
#         self.result_table = []
#         
#     def get_result_table(self):
#         """ """
#         return self.result_table
#     
#     def add_result_row(self, row_type, time_s, freq_hz, amp_dbfs, pulse_ix, info_key='', info_value=''):
#         """ """
#         freq_khz = numpy.round(freq_hz/1000.0, 1)
#         amp_dbfs = numpy.round(amp_dbfs)
#         
#         self.result_table.append([row_type, time_s, freq_khz, amp_dbfs, pulse_ix, info_key, info_value])
#         
#     def save_result_table(self, file_path):
#         """ """
#         file_path = pathlib.Path(file_path)
#         
#         with file_path.open('w') as table_file:
#             # Write header.
#             table_file.write('\t'.join(['type', 'time_s', 'freq_khz', 'amp_dbfs', 'pulse_ix', 'info_key', 'info_value']) + '\n')
#             for row in self.result_table:
#                 table_file.write('\t'.join([str(x) for x in row]) + '\n')
#         
#         return self.result_table
#     
# 
# 
# # === MAIN ===    
# if __name__ == "__main__":
#     
#     import datetime
#     import wave
#     import matplotlib.pyplot
#     
#     """ """
#     print('PulseShapeExtractor test_dynamic_canvas_OLD started. ',  datetime.datetime.now())
#     
# #     file_path = pathlib.Path('../data', 'test_chirp_generator.wav')
#     file_path = pathlib.Path('../data', 'M004092.WAV')
#     
#     with wave.open(str(file_path), 'r') as wave_file:
#         nchannels = wave_file.getnchannels() # 1=mono, 2=stereo.
#         sampwidth = wave_file.getsampwidth() # sample width in bytes.
#         framerate = wave_file.getframerate() # Sampling frequency.
#         nframes = wave_file.getnframes() # Number of audio frames.
#         
#         if int(framerate > 90000):
#             frame_rate_hz = framerate
#             lenght_s = int(nframes) / int(framerate)
#         else:
#             # Probably time division by a factor of 10.
#             frame_rate_hz = framerate * 10
#             lenght_s = int(nframes) / int(framerate) / 10
#             
#         buffer_raw = wave_file.readframes(int(nframes))
# #         buffer_raw = wave_file.readframes(frame_rate_hz) # Max 1 sec.
#         signal = numpy.fromstring(buffer_raw, dtype=numpy.int16) / 32767
#     
#     print('frame_rate_hz: ', frame_rate_hz, ' lenght_s: ', lenght_s)
#     
#     extractor = PulsePeaksExtractor(debug=True)
#     extractor.setup(frame_rate_hz)
#     signal_filtered = extractor.filter(signal, filter_low_hz=20000, filter_high_hz=100000)
#     extractor.new_result_table()
#     extractor.extract_peaks(signal_filtered)
#     extractor.save_result_table(file_path='../data/pulse_peaks.txt')
#     
#     print('Length: ', len(extractor.get_result_table()))
#     
#     # Plot.
#     time = []
#     freq = []
#     amp = []
#     for row in extractor.get_result_table():
#         if row[0] == 1:
# #             if row[3] > -100: # -100 means silent.
#                 time.append(float(row[1]))
#                 freq.append(float(row[2]))
#                 amp.append(float(row[3]))
#     #
#     amp_min = abs(min(amp))
#     sizes = [((x+amp_min)**1.2) * 0.1 for x in amp]
#     
# #     matplotlib.pyplot.scatter(time, freq, c=sizes, s=sizes, cmap='Blues')
#     matplotlib.pyplot.scatter(time, freq, c=amp, s=sizes, cmap='Reds')
#     matplotlib.pyplot.show()
#     
#     print('\n')
#     print('PulseShapeExtractor test_dynamic_canvas_OLD ended. ',  datetime.datetime.now(), '\n')
#     
