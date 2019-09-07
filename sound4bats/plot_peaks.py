#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://cloudedbats.org
# Copyright (c) 2019 Arnold Andreasson 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import numpy

import sound4bats

class PlotPeaks(sound4bats.PlotBase):
    """ """
    def __init__(self, figure, canvas=None):
        """ """
        super().__init__(figure, canvas)
    
    def create_axes(self):
        """ """
        self.axes = self.figure.add_subplot(111)

    def plot(self):
        """ """
        if len(self.x) < 1:
            # Nothing to plot.
            self.figure.clear()
            return 
        
        # Sliders for center and zoom.
        slider_center_value = self.slider_center_percent / 100.0 - 0.5 # Value -1 to 1.
        slider_zoom_value = (self.slider_zoom_percent / 100.0)
        x_interval = self.x_max - self.x_min
        x_min =  self.x_min + (x_interval * slider_center_value)
        x_max = self.x_max + (x_interval * slider_center_value)
        x_min_new = x_min
        x_max_new = x_max
        if (slider_zoom_value > 0.0) and (slider_zoom_value < 1.0):
            x_c = x_min + ((x_max - x_min) / 2.0)
            x_min_new = x_c - ((1.0 - slider_zoom_value) * x_interval / 2)
            x_max_new = x_c + ((1.0 - slider_zoom_value) * x_interval / 2)
        
        z_min = abs(min(self.z))
        sizes = [numpy.sqrt(x+z_min) * 0.2 for x in self.z]
        
        scatter = self.axes.scatter(self.x, self.y, c=self.z, s=sizes, cmap='Reds')
        
        from mpl_toolkits import axes_grid1
        divider = axes_grid1.make_axes_locatable(self.axes)
        cax = divider.append_axes("right", size="1.5%", pad=0.1)
        self.figure.colorbar(scatter, cax=cax, label='dBFS')
        #
        self.axes.set(ylim=(self.y_min, self.y_max),
                      xlim=(x_min_new, x_max_new),
                      xlabel=self.x_label,
                      ylabel=self.y_label)
        #
        self.axes.minorticks_on()
        major_yticks = numpy.arange(0, self.y_max, 10)
        minor_yticks = numpy.arange(0, self.y_max, 5)
        self.axes.set_yticks(major_yticks)
        self.axes.set_yticks(minor_yticks, minor=True)
        
        self.axes.grid(which='major', linestyle='-', linewidth='0.5', alpha=0.5)
        self.axes.grid(which='minor', linestyle='-', linewidth='0.5', alpha=0.2)
        #
        if self.canvas:
            self.canvas.draw()
        else:
            print('DEBUG: For test only...')
            pyplot.draw()
            pyplot.show()
            print('...test done.')


### TEST ###
if __name__ == '__main__':
    """ """
    from matplotlib import pyplot
     
    figure = pyplot.figure()
    plot_test = PlotPeaks(figure, canvas=None)
    plot_test.set_labels(x_label='Time (sec.)', y_label='Freq. (kHz)', z_label='dBMS')
    plot_test.set_values(x=[1,2,3], y=[20,50,10], z=[-20,-10,-15])
    plot_test.set_limits(x_min=0.0, x_max=4.0, y_min=0.0, y_max=100.0)
    plot_test.set_center_and_zoom(slider_center_percent=50.0, slider_zoom_percent=0.0)
    plot_test.plot()
