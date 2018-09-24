#!python
# copy for machine learning project

import loadSPEfilesML
# from csv import writer
import csv
import smoothen
import pandas as pd
import os.path as path


def SPEtoCSV2(path, spefilenames):
    # make sure
    for filename in spefilenames:
        data = loadSPEfilesML.load(path + filename)
        raw = {'Wavelengths': data[0], 'Intensities': data[1]}
        df = pd.DataFrame(raw, columns=['Wavelengths', 'Intensities'])
        df.to_csv(path + 'WS2 reflection spectra - CSV\\' + filename[:-4] + '.csv')
    print('Successfully converted .spe files to .csv files!')


def writeSPEtoCSV(filename, bckgrnd):
    '''converts counts from spe file to new csv file'''
    # labellst = input('Is this a label list? (Y/N)')
    csvfilename = 'data.csv'
    data = loadSPEfilesML.load(filename)   # returns (f._wavelengths, img)
    bgdata = loadSPEfilesML.load(bckgrnd)
    # W = data[0]
    I = Bckgrnd(data[1],bgdata[1])
    lenI = len(I)
    with open(csvfilename,'w') as f:
        writer = csv.writer(f)
        # writer.writerows([W,I]) # list of lists
        writer.writerow(I)
    print("Writing complete")
    return csvfilename,lenI

def appendSPEtoCSV(filename,bckgrnd,csvfilename,lenI):
    '''appends counts from spe file to given csv file.'''
    data = loadSPEfilesML.load(filename)
    bgdata = loadSPEfilesML.load(bckgrnd)
    I = Bckgrnd(data[1],bgdata[1])
    sz = len(I)
    if sz == lenI:
        with open(csvfilename,'a') as f:
            writer = csv.writer(f)
            writer.writerow(I) # list of lists
            wrongsizefile='-'
    else:
        wrongsizefile = filename.split('/')[1] # wrong size
    return csvfilename,wrongsizefile

def allSPEtoCSV(spefilenames,path):
    '''takes list of spefilenames, returns csv file.
    filename format: date-material_num-misc.spe
    '''
    import fixfilenames as ffn
    (newfilenames, bckgrnds) = ffn.FixFilenames(path)
    # ~ create csv file ~
    wr = writeSPEtoCSV('WS2 reflection spectra/'+newfilenames[0],'WS2 reflection spectra/'+bckgrnds[0])
    csvfile = wr[0]
    lenI = wr[1]
    # for i in range(1,len(spefilenames)):
    #     spefile = 'WS2reflection_spectra/'+spefilenames[i]
    wrongsizefiles = []
    # ~ add rows to csv file ~
    # for spefile in newfilenames[1:-1]:
    remaining = newfilenames[1:-1]
    for i in range(len(remaining)):
        spefile = remaining[i]
        bckgrnd = bckgrnds[i]
        ap = appendSPEtoCSV('WS2 reflection spectra/'+spefile,'WS2 reflection spectra/'+bckgrnd,csvfile,lenI)
        csvfile = ap[0]
        if ap[1] != '-':
            wrongsizefiles.append(ap[1])
    # print('length wrongsizefiles= ',len(wrongsizefiles))
    return csvfile,newfilenames,wrongsizefiles

# ~ Preprocessing ~

# def Cut():
#     '''make files same size'''
# replace wrongsizefiles thing with making files the same size, if they're close in size

# def Normalize(I):
#     I = savitzky_golay(I, 31, 4)
#     mx = max(I)
#     N = [n/mx for n in I]
#     return N

# to remove background, associate each spefile with its bckgrnd file
def Bckgrnd(I_raw,b_raw):
    I = smoothen.savitzky_golay(I_raw, 31, 4)
    b = smoothen.savitzky_golay(b_raw, 31, 4)
    s = [((I[i]/b[i])-1) for i in range(len(I))]
    return s
