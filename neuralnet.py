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

    def loadData(self,trainfile='train.txt',testfile='test.txt',labels_train='labels_train.txt',labels_test='labels_test.txt'):
        '''
   	  Loads data from file into object.
   	  trainfile='train.txt',testfile='test.txt',labels_train='labels_train.txt',labels)test='labels_test.txt'
   	  '''       
         
         
        self.train = pandas.read_csv(trainfile,header=None)
        self.test = pandas.read_csv(testfile,header=None)
        # creates attributes train and test (type DataFrame) from trainfile.csv and testfile.csv
        
        # pandas.read_csv returns DataFrame([data, index, columns, dtype, copy])
        #Two-dimensional size-mutable, potentially heterogeneous tabular data structure
        #with labeled axes (rows and columns).
        
        # header : int or list of ints, default ‘infer’. 
        #Row number(s) to use as the column names, and the start of the data. 
        #Default behavior is to infer the column names: 
        #if no names are passed the behavior is identical to header=0 and 
        #column names are inferred from the first line of the file.
        #if column names are passed explicitly then the behavior is identical to 
        #header=None. If file contains no header row, then you should explicitly pass header=None. 
        #Explicitly pass header=0 to be able to replace existing names.
        # --> File has no header row, names must be passed explicitly. 

        self.train = self.train.as_matrix()
        self.test = self.test.as_matrix()
        # .as_matrix method ... 

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
        # 

    def buildModel(self):
        self.model = Sequential()
        self.model.add(Dense(80,input_shape=(80,)))
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
