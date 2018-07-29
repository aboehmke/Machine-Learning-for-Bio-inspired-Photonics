#!python
# copy for machine learning project

import loadSPEfilesML
# from csv import writer
import csv

def writeSPEtoCSV(spefilename):
    '''converts wavelengths and counts from spe file to new csv file.'''
    data = loadSPEfilesML.load(spefilename)   # returns (f._wavelengths, img)
    W = data[0]
    I = data[1]
    lenW = len(W)
    spefilename0 = spefilename.split('/')[1] # get rid of directory name
    csvfilename = spefilename0.split('.')[0]+'.csv'
    # with open(‘name.txt’, ‘sth’ ) as f: followed by indented code closes file automatically at end of indented block
    with open(csvfilename,'w') as f:
        writer = csv.writer(f)
        writer.writerows([W,I]) # list of lists
    print("Writing complete")
    return csvfilename,lenW

def appendSPEtoCSV(spefilename,csvfilename,lenW):
    '''appends counts from spe file to given csv file.'''
    # print(spefilename)
    data = loadSPEfilesML.load(spefilename)
    I = data[1]
    sz = len(I)
    if sz == lenW:
        with open(csvfilename,'a') as f:
            writer = csv.writer(f)
            writer.writerow(I) # list of lists
            wrongsizefile='-'
    else:
        wrongsizefile = spefilename# wrong size
    return csvfilename,wrongsizefile

def allSPEtoCSV(spefilenames):
    '''takes list of spefilenames, returns csv file.'''
    wr = writeSPEtoCSV('WS2reflection_spectra/'+spefilenames[0])
    csvfile = wr[0]
    lenW = wr[1]
    # print(len(spefilenames)) = 112
    # range(1,len(spefilenames) = [1,2,...,111]
    # for i in range(1,len(spefilenames)):
    #     spefile = 'WS2reflection_spectra/'+spefilenames[i]
    wrongsizefiles = []
    for spefile in spefilenames[1:-1]:
        ap = appendSPEtoCSV('WS2reflection_spectra/'+spefile,csvfile,lenW)
        csvfile = ap[0]
        if ap[1] != '-':
            wrongsizefiles.append(ap[1])
    print('length spefiles= ',len(spefilenames))
    # print('length wrongsizefiles= ',len(wrongsizefiles))
    return csvfile,wrongsizefiles
