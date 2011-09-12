#!/usr/bin/python
import sys, glob, os, getopt
import matplotlib.pyplot as plt

class simple_plot:
    singlePlot = []
    count = 0
    figures = []
    figure = plt.figure(1)
    X = []
    Y = []
    xLabels = []
    yLabels = []
    legends = []
    names = []
    
    def new_plot(self, singlePlot, filename):
        self.count += 1
        self.X.append([])
        self.Y.append([])
        self.xLabels.append([])
        self.yLabels.append([])
        self.legends.append([])
        self.singlePlot.append(singlePlot)
        self.names.append(filename)
        self.figures.append(plt.figure(self.count))
        return self.count-1
        
    def add_curve_data(self, x, y, legend, xLabel, yLabel):
        self.X[self.count-1].append(x)
        self.Y[self.count-1].append(y)
        self.xLabels[self.count-1].append(xLabel)
        self.yLabels[self.count-1].append(yLabel)
        self.legends[self.count-1].append(legend)
        
    def add_curve_data_to_index(self, index, x, y, legend, xLabel, yLabel):
        self.X[index].append(x)
        self.Y[index].append(y)
        self.xLabels[index].append(xLabel)
        self.yLabels[index].append(yLabel)
        self.legends[index].append(legend)

    def generate_plots(self):
        '''Plots X against Y onto subplot and draw the legend if legend is not None'''
        for index in range(self.count):
            if self.singlePlot[index]:
                subPlot = self.figures[index].add_subplot(1, 1, 1)
                for i in range(len(self.X[index])):
                    if self.legends[index][i] == None:
                        subPlot.plot(self.X[index][i], self.Y[index][i])
                    else:
                        subPlot.plot(self.X[index][i], self.Y[index][i], label=self.legends[index][i])
                        subPlot.legend()
                    subPlot.set_xlabel(self.xLabels[index][i])
                    subPlot.set_ylabel(self.yLabels[index][i])
            else:
                for i in range(len(self.X[index])):
                    subPlot = self.figures[index].add_subplot(len(self.X[index]), 1, i+1)
                    if self.legends[index][i] == None:
                        subPlot.plot(self.X[index][i], self.Y[index][i])
                    else:
                        subPlot.plot(self.X[index][i], self.Y[index][i], label=self.legends[index][i])
                        subPlot.legend()
                    subPlot.set_xlabel(self.xLabels[index][i])
                    subPlot.set_ylabel(self.yLabels[index][i])

    
    def save_plots(self, outputDirectory):
        # check if output directory already exists
        if outputDirectory == None:
            print "No output directory specified"
            sys.exit(2)
        if len(outputDirectory) != 0:
            if outputDirectory[-1] != '/':
                outputDirectory += '/'
        if not os.path.exists(outputDirectory):
            os.makedirs(outputDirectory)
        
        for index in range(self.count):
            plt.figure(index+1)
            plt.savefig(outputDirectory + self.names[index] + '.png', format='png')
        
