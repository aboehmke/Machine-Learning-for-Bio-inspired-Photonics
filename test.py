#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import SPEtoCSVml
import os
import Label

spefilenames = []
# path to spe files:
# path = '/Users/AB/Downloads/WS2reflection_spectra/'
spe_path = 'D:\Python Projects\MachineLearningNN\WS2 reflection spectra\\'      # directory
csv_path = 'D:\Python Projects\MachineLearningNN\WS2 reflection spectra - CSV\\'
for root, dirs, files in os.walk(spe_path):
    for file in files:
        if file.endswith('.spe'):
            spefilenames.append(file)
spefilenames.sort(key=str.lower) # https://www.asciitable.com/
# print('make data file')
SPEtoCSVml.SPEtoCSV2(spe_path, csv_path, spefilenames)




#x = SPEtoCSVml.allSPEtoCSV(spefilenames, csv_path)
#trainfile = x[0]
#newfilenames = x[1]
#wrongsizefiles = x[2]


#train = pd.read_csv(trainfile, header=None)
#train = train.as_matrix()
#print(train.shape)


#print('make label file')
#labels_train = Label.LabelsCSV(newfilenames, wrongsizefiles)
#labels_train = pd.read_csv(labels_train, header=None)
#labels_train = labels_train.as_matrix()
#print(labels_train.shape)
#labels_train = np.resize(labels_train, labels_train.shape[1])
