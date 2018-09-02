#!python
# create labels for neuralnet.loadData
import graphing

def LabelsCSV(spefilenames,wrongsizefiles):
    import csv
    labels = LabelData(spefilenames,wrongsizefiles)
    csvfilename = 'labels.csv'
    with open(csvfilename,'w') as f:
        writer = csv.writer(f)
        # writer.writerows([W,I]) # list of lists
        writer.writerow(labels)
    print("Writing complete")
    return csvfilename

def LabelData(spefilenames,wrongsizefiles):
    '''Prompts user to label input data, returns list of labels.
    If >3 layers, labeled '10'. If unknown number of layers, labeled 0.'''
    # print(len(spefilenames))
    # print(type(spefilenames))
    import numpy as np
    labels = []
    for i in range(len(spefilenames)):
        graphing.display_spectra()
        if spefilenames[i] not in wrongsizefiles:
            plotData(spefilenames[i])
            label = input("number of layers = ")
            # IF label == '?': ...
                # remove?
            labels.append(label)
    print(labels)
    # return np.asarray(labels)
    return labels


def plotData(spefilename):
    '''Display each spectrum for user to label.'''
    name = spefilename.split('.')[0]
    import loadSPEfilesML
    data = loadSPEfilesML.load('WS2reflection_spectra/'+spefilename)
    W = data[0]
    I = data[1]
    I1L = loadSPEfilesML.load('WS2reflection_spectra/20180527-WS2_3_1.spe')[1]
    I2L = loadSPEfilesML.load('WS2reflection_spectra/20180527-WS2_3_3.spe')[1]
    I3L = loadSPEfilesML.load('WS2reflection_spectra/20180527-WS2_2_2.spe')[1]
    from matplotlib import pyplot as plt
    fig,ax = plt.subplots(nrows=1)
    ax.plot(W,I1L,'b:')
    ax.plot(W,I2L,'c:')
    ax.plot(W,I3L,'g:')
    ax.plot(W,I,'m:')
    ax.set(xlim=[W[590],W[3539]])
    # ax.set(xlim=[W[0],W[-1]])
    # ,ylim=[0,1])
    ax.set_xlabel('wavelength [nm]')
    ax.set_ylabel('intensity [a.u.]')
    plt.show()
    # consider labeling global max, distances between peaks, normalizing better...
