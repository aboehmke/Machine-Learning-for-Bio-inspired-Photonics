from keras.models import Sequential
from keras.layers.core import Dense, Activation
# from keras.optimizers import SGD, RMSprop
from keras.utils import np_utils
# Keras is a high-level neural networks API, written in Python and
#capable of running on top of TensorFlow, CNTK, or Theano.
# TensorFlow: a machine learning framework

# import matplotlib.pyplot as plt
import numpy as np
# from scipy import misc

import pandas # Python data analysis library

class neuralnet(object): 
    '''defines a new object called "neuralnet", which is the output of the loadData() function.
    3 optional paramters: batch_size, nb_classes, nb_epoch
    '''

    def __init__(self,batch_size=100,nb_classes=3,nb_epoch=100):
       # Some generic parameters for the learning process
        self.batch_size = batch_size
        self.nb_classes = nb_classes
        self.nb_epoch   = nb_epoch
        self.loadData()

    def loadData(self,path):
        '''
        Takes path to directory containing spe files.
   	  Loads data from file into object.
   	  trainfile='train.txt',testfile='test.txt',labels_train='labels_train.txt',labels)test='labels_test.txt'
   	  '''       
        #,trainfile='train.txt',testfile='test.txt',labels_train='labels_train.txt',labels_test='labels_test.txt'):
    
        import SPEtoCSVml
        import os
        spefilenames = []
        for root,dirs,files in os.walk(path):
            for file in files:
                if file.endswith('.spe'):
                    spefilenames.append(file)
        x = SPEtoCSVml.allSPEtoCSV(spefilenames)
        trainfile = x[0]
#        wrongsizefiles = x[1]
         
        self.train = pandas.read_csv(trainfile,header=None)
        self.test = pandas.read_csv(testfile,header=None)
        # creates attributes train and test (type DataFrame) from trainfile.csv and testfile.csv
        
        # pandas.read_csv returns DataFrame([data, index, columns, dtype, copy])
        #Two-dimensional size-mutable, potentially heterogeneous tabular data structure
        #with labeled axes (rows and columns).
        
        # header : int or list of ints. If file contains no header row, 
        #then you should explicitly pass header=None. 

        self.train = self.train.as_matrix()
        self.test = self.test.as_matrix()
        # .as_matrix method converts the dataframe to its Numpy-array representation.
        # i.e. >>> type(self.train) --> numpy.ndarray
        print(self.train.shape)

        self.train = self.train.transpose()
        self.test = self.test.transpose()
        # why transpose? 

        self.labels_train = pandas.read_csv(labels_train,header=None)
        self.labels_test = pandas.read_csv(labels_test,header=None)
        # what're labels for? 

        self.labels_train = self.labels_train.as_matrix()
        self.labels_test = self.labels_test.as_matrix()

        self.labels_train = np.resize(self.labels_train, self.labels_train.shape[1])
        self.labels_test = np.resize(self.labels_test, self.labels_test.shape[1])
        # 

        self.labels_train = np_utils.to_categorical(self.labels_train,self.nb_classes)
        self.labels_test  = np_utils.to_categorical(self.labels_test,self.nb_classes)
        # np_utils ?

    def buildModel(self):
        self.model = Sequential()
        # The Sequential model is a linear stack of layers.
        # You can create a Sequential model by passing a list of layer instances to the constructor
        self.model.add(Dense(80,input_shape=(80,)))
        # the first layer in a Sequential model (and only the first, because following layers can do automatic shape inference) 
        #needs to receive information what input shape to expect. 
        self.model.add(Activation('relu'))
        self.model.add(Dense(40))
        self.model.add(Activation('relu'))
        self.model.add(Dense(3))
        self.model.add(Activation('softmax'))
        sgd = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)
        self.model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=["accuracy"])

    def fit(self):
        self.model.fit(self.train,self.labels_train,
        batch_size=self.batch_size,
        nb_epoch=self.nb_epoch,
        verbose=0,
        validation_data = (self.test,self.labels_test))

    def showResults(self):
        score = self.model.evaluate(self.test,self.labels_test)
        print('Test score:', score[0])
        print('Test accuracy:', score[1])
        return score[1]
