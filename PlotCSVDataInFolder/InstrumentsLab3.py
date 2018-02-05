#! usr/bin/env python3
import numpy as np 
import matplotlib.pyplot as plt
import os
import csv
import re

part1_regex = re.compile(r"""(                    
    (\w*\d_)       # Lab Number
    (\s)?               # Space
    (\d*)               # Number of Samples
    (\s)                # Space
    (\d*)             # Sampling Freq
    (hz)
    (\.[a-zA-Z]{2,4})   # Suffix
                        )""", re.VERBOSE)

part2_regex = re.compile(r"""(                    
    (\w{3}\d{1}_)       # Lab Number
    (FFT\s|p2_)           # Part number or test
    (raw\sdata|resample)?
    (\s)?
    (\d*)               # Number of Samples
    (_)?
    (\s)?           # Space
    (\d*|\w{2,4})             # Sampling Freq
    
    (\.[a-zA-Z]{2,4})   # Suffix
                        )""", re.VERBOSE)

def get_graph_title(data_filename):

    str_1_matches = part1_regex.findall(data_filename)
    for match in str_1_matches:
        if match[-4] == ' ':
            n_samples = str_1_matches[0][-5]
            s_freq = str_1_matches[0][-3]
            graph_title = '200 Hz Signal with {} samples drawn at {} Hz.'.format(n_samples, s_freq)
            # print(graph_title)
            return graph_title

    str_2_matches = part2_regex.findall(data_filename)
    for match in str_2_matches:
        if match[3].startswith('r'):
            d_source = match[3].title()
            n_samples = match[-5]
            s_freq = match[-2]
            graph_title = '200 Hz Signal LabView FFT {} Transform with\n {} samples drawn at {} Hz.'.format(d_source, n_samples, s_freq)
            # print(graph_title)
            return graph_title
        else:
            s_freq = match[-5]
            if match[-2].lower() == 'fftr':
                graph_title = 'Aluminum Bar Vibration Labview Raw Data FFT with\n {} Hz. Sampling Frequency'.format(s_freq)
                # print(graph_title)
                return graph_title
            elif match[-2].lower() == 'fft':
                graph_title = 'Aluminum Bar Vibration Labview Resampled FFT with\n {} Hz. Sampling Frequency'.format(s_freq)
                return graph_title
                # print(graph_title)
            else:
                graph_title = 'Aluminum Bar Vibration Accelerometer Data with\n {} Hz. Sampling Frequency'.format(s_freq)
                return graph_title
                # print(graph_title)

def readFile(fileName):
    x_values = []
    y_values = []
    with open(fileName) as file:
        reader = csv.reader(file, delimiter='\t')
        next(reader, None)
        data = list(reader)
    for line in data:
        x_values.append(line[0])
        y_values.append(line[1])
    return x_values, y_values

    



def log_filetype_within(directory, extension):
    # Creates a log file containing all of the files of a given type
    # within the folder tree.

    results = []

    # results = str()

    # os.walk moves through the whole folder tree and looks at each
    # item within. Returns these three arguments.
    for dirpath, dirnames, files in os.walk(directory):
        # Files is an iterable containing a list of the directories
        # inside of the current 'step' folder.
        # if dirpath.startswith('./Lab3'):
        #     print(files)
        #     os.chdir(dirpath)
        for name in files:
            if name.lower().endswith(extension) and name.lower().startswith('lab3'):
                # print(name)
                os.chdir(dirpath)
                x_values, y_values = readFile(name)
                max_y = max(y_values)
                max_y_loc = y_values.index(max_y)
                max_x = x_values[max_y_loc]
                print(name)
                print(get_graph_title(name))
                plt.plot(x_values, y_values)
                plt.title(get_graph_title(name))
                if 'fft' in name.lower():
                    plt.xlabel('Frequency (Hz)')
                else:
                    plt.xlabel('Time (s)')
                plt.ylabel('Amplitude')
                plt.savefig('{}.pdf'.format(name[:-4]), bbox_inches='tight')
                plt.show()
                plt.close()
                    
            # os.chdir('..')

    

log_filetype_within(os.getcwd(), '.txt',)
