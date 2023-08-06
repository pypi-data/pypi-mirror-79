import numpy as np
import matplotlib
import sys
from os import path
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn import preprocessing
from joblib import dump, load
from astropy.io import fits

'''
The routine classify allows to classify the elements of a given
dataset using any classifier prealably trained with the train
functions. 

The dataset must be given to the function as a pandas DataFrame.

If the classifier object is already loaded, the function takes the
classifier variable name as argument, otherwise the user must specify
a path to a joblib file in order to load the classifier.

@author: Sylvain Breton
'''

def classify (dataset,
              clf=None,
              clf_name=None, 
              summary=True, 
              frame_name='classification_summary.csv',
              verbose=0) : 

  '''
  Generic template for classifying datasets.
  
  :param dataset: must be given as a pandas DataFrame.
  The id of the elements must be given as the index 
  of the DataFrame.
  :type dataset: pandas.DataFrame

  :param clf: name of the classifier to use for the classification.
  Default None.
  :type clf_name: object

  :param clf_name: if clf not given, name of the file where the 
  classifier to use has been saved. Default None.
  :type clf_name: str

  :param summary: save a frame summarizing the probability of classification 
  of the dataset, default True
  :type summary: bool

  :param frame_name: name of the csv file where to store the results
  of the classification, default 'classification_summary.csv'
  :type frame_name: str

  :param verbose: set to 0 to print additional intels about the training.
  :type verbose: int

  :return: summary DataFrame of the classification.
  :rtype: pandas DataFrame

  :Example:
  
  >>> import pandas as pd
  >>> from pushkin.train import train_rf
  >>> data, target = datasets.load_iris (return_X_y=True)
  >>> training_set = pd.DataFrame (data=data)
  >>> training_set['label'] = target
  >>> dataset = pd.DataFrame (data=data)
  >>> clf = train_rf (training_set, plot=True, summary=False, save=False)
  >>> df = classify (dataset, clf)
  '''
 
  df = dataset
  input_param = df.columns.values
  input_param = input_param.astype ('U20')
  df.columns = input_param

  df = df.dropna (axis=0)
  if verbose==0 :
    print ('Number of element that will be classified: ', df.index.size)
 
  df = df.sort_index (axis=1)

  #------------------------------------------------------------------------------------------------------------------------
  #------------------------------------------------------------------------------------------------------------------------
  #------------------------------------------------------------------------------------------------------------------------
  
  if clf==None :
    #LOADING CLASSIFIER IF NO EXISTING CLASSIFIER HAS BEEN SPECIFIED
    clf = load (clf_name)
  
  #------------------------------------------------------------------------------------------------------------------------
  #------------------------------------------------------------------------------------------------------------------------
  #------------------------------------------------------------------------------------------------------------------------
  
  label_pred = clf.predict (df.to_numpy ())
  proba = clf.predict_proba (df.to_numpy ())
    
  frame_summary = pd.DataFrame (index=df.index, data=proba)
  frame_summary['label_pred'] = label_pred.astype ('U20')

  if summary==True :
    frame_summary.to_csv (frame_name)
    print ('Summary frame saved in', frame_name)
  
  return frame_summary 

