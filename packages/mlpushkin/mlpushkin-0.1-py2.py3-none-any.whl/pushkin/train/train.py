import numpy as np
import matplotlib
import sys
from os import path
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import NeighborhoodComponentsAnalysis
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from joblib import dump, load
from astropy.io import fits

'''
The function used to train machine learning classifier are given here.
For now, random forest, multi-layer perceptron neural network and K-nearest
neighbors methods are implemented :
- train_rf (training_set)
- train_nn (training_set)
- train_knn (training_set)

sklearn tools are wrapped into ergonomic ready-to-use functions, but all the
hyperparameters of the classifiers are still tunable through the optional 
argument of the functions.

For each function, the only mandatory parameter is the input training set,
which must be given as a pandas DataFrame. 

@author: Sylvain Breton
'''

def train_rf (training_set,
              save=False,
              clf_name='rf_classifier.joblib', 
              summary=False, 
              frame_name='test_rf_summary.csv', 
              plot=True,
              test_size=0.15, 
              verbose=0,
              cmap='winter', 
              fontsize=30, 
              lettercolor='white',
              #hyper-parameter of the classifier
              n_estimators=100, criterion='gini', max_depth=None, 
              min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=0.0, 
              max_features='auto', max_leaf_nodes=None, min_impurity_decrease=0.0, 
              min_impurity_split=None, bootstrap=True, oob_score=False, 
              n_jobs=None, random_state=256, warm_start=False, 
              class_weight=None, ccp_alpha=0.0, max_samples=None) :

  '''
  Generic template for training random forest classifiers.
  
  :param training_set: pandas DataFrame. It is mandatory
  that one of the columns is named 'label'.
  The id of the stars (KIC, TIC, etc.) must be given as the index 
  of the DataFrame.
  :type training_set: pandas.DataFrame

  :param save: if set on true the function will save a version of the trained classifier
  in joblib files. Default False. 
  :type save: bool

  :param clf_name: name of the file where to save the classifier, default 'rf_classifier'
  :type clf_name: str

  :param summary: save a frame summarizing the probability of classification 
  of the training set, default False.
  :type summary: bool

  :param frame_name: name of the csv file where to store the results
  of the test step, default 'test_summary.csv'
  :type frame_name: str

  :param plot: set to True to show the correlation matrix between parameters, the confusion matrix and
  the relative important between parameter, default True
  :type plot: bool`

  :param test_size: fraction of data that will be used as test set, default 0.15.
  :type test_size: float

  :param verbose: set to 0 to print additional intels about the training, default 0.
  :type verbose: int

  :param cmap: color map (see matplotlib doc) to use when plotting the confusion matrix,
  default 'winter'.
  :type cmap: str 

  :param fontsize: size of the font to use in the confusion matrix, default 20, 
  :type fontsize: str

  :param lettercolor: color (see matplotlib doc) used for the characters in the confusion matrix,
  default 'white'.
  :type lettercolor: str

  For the hyper-parameter of the classifier, refer to scikit-learn documentation.

  :return: the trained classifier.
  :rtype: object

  :Example:
  
  >>> import pandas as pd
  >>> data, target = datasets.load_iris (return_X_y=True)
  >>> training_set = pd.DataFrame (data=data)
  >>> training_set['label'] = target
  >>> train_rf (training_set, plot=True, summary=False, save=False)

  '''
 
  df = training_set
  df['label'] = df['label'].map (str)

  # convert columns name from int/float to string
  # (if it has not been done yet) to ensure stability
  # of the code
  input_param = df.columns.values
  input_param = input_param.astype ('U20')
  df.columns = input_param

  input_param = np.setdiff1d (input_param, np.array(['label']))

  df = df.dropna (axis=0)
  if verbose==0 :
    print ('Number of elements in the training set', df.index.size)
  
  #------------------------------------------------------------------------------------------------------------------------
  #------------------------------------------------------------------------------------------------------------------------
  #------------------------------------------------------------------------------------------------------------------------
  
  #CREATING TRAINING AND TESTING SET
  
  try :
    frame_label = df[['label']]
  except KeyError :
    print ('KeyError : the input training set needs to have a columns \'label\', training interrupted.')
    sys.exit ()
  df = df [input_param]
  df = df.sort_index (axis=1)

  if test_size > 0 :
    df_train, df_test, frame_label_train, frame_label_test = train_test_split (df, frame_label, test_size=test_size,
                                                                               random_state=random_state)

    data_test = df_test.to_numpy (dtype=np.float64) 
    label_test = frame_label_test.to_numpy (dtype='U20') 
    label_test = np.ravel (label_test)
    id_test = df_test.index 
  else :
    df_train = df
    frame_label_train = frame_label

  data_train = df_train.to_numpy (dtype=np.float64) 
  label_train = frame_label_train.to_numpy (dtype='U20') 
  label_train = np.ravel (label_train)
  id_train = df_train.index 
  training_class = np.unique (label_train)
    
    
  
  correl_parameters = np.corrcoef (data_train, rowvar=False)
  
  #------------------------------------------------------------------------------------------------------------------------
  #------------------------------------------------------------------------------------------------------------------------
  #------------------------------------------------------------------------------------------------------------------------
  
  #TRAINING CLASSIFIER
  
  clf = RandomForestClassifier (n_estimators=n_estimators, criterion=criterion, max_depth=max_depth, 
                                min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf, 
                                min_weight_fraction_leaf=min_weight_fraction_leaf, 
                                max_features=max_features, max_leaf_nodes=max_leaf_nodes, 
                                min_impurity_decrease=min_impurity_decrease, 
                                min_impurity_split=min_impurity_split, bootstrap=bootstrap, oob_score=oob_score, 
                                n_jobs=n_jobs, random_state=random_state, verbose=verbose, warm_start=warm_start, 
                                class_weight=class_weight, ccp_alpha=ccp_alpha, max_samples=max_samples)
  
  clf.fit (data_train, label_train)
  
  if save==True :
    dump (clf, clf_name)
  
  #------------------------------------------------------------------------------------------------------------------------
  #------------------------------------------------------------------------------------------------------------------------
  #------------------------------------------------------------------------------------------------------------------------
  
  #TESTING CLASSIFIER AND PLOTTING RESULTS
  if test_size > 0 :

    feature_importance = clf.feature_importances_
    label_pred = clf.predict (data_test)
    proba = clf.predict_proba (data_test)

      
    if verbose==0 :
      print (clf.get_params ())
      print ('Feature importance')
      print (df.columns.values)
      print (clf.feature_importances_)

    print ('Validation score : ', clf.score (data_test, label_test))

    if plot==True :
    
      
      fig = plt.figure (figsize=(16,16))
      fig_2 = plt.figure (figsize=(32,32))
      fig_3 = plt.figure (figsize=(32,32))
      ax1 = fig.add_subplot (111)
      ax2 = fig_2.add_subplot (111)
      ax3 = fig_3.add_subplot (111)
      
      c3 = ax3.pcolor (correl_parameters, cmap='RdYlGn_r', vmin=-1., vmax=1.)
      fig.colorbar (c3, ax=ax3)
      
      conf_matrix = confusion_matrix (label_test, label_pred, training_class)

      ax1.set_xticks ([i+0.5 for i in range (training_class.size)])
      ax1.set_yticks ([i+0.5 for i in range (training_class.size)])
      ax1.set_xticklabels (training_class)
      ax1.set_yticklabels (['pred_'+ elt for elt in training_class])

      for x in range (training_class.size) :
        for y in range (training_class.size) :
          ax1.text (x+0.5, y+0.5, '%-s' % conf_matrix [x, y], 
                    horizontalalignment='center', verticalalignment='center', 
                    fontsize=fontsize, color=lettercolor) 
      
      c1 = ax1.pcolor (conf_matrix, cmap=cmap)
      fig.colorbar (c1, ax=ax1)
      
      ax2.barh ([i for i in range (1, input_param.size+1)], feature_importance, color='black')
      
      ax2.set_yticks ([i for i in range (1, input_param.size+1)])
      ax2.set_yticklabels (input_param)
      ax3.set_xticks (np.array([i for i in range (1, input_param.size+1)]) - 0.5)
      ax3.set_yticks (np.array([i for i in range (1, input_param.size+1)]) - 0.5)
      ax3.set_xticklabels (input_param)
      ax3.set_yticklabels (input_param)
      
      ax2.tick_params (axis='x', labelrotation = 90.)
      ax3.tick_params (axis='x', labelrotation = 90.)
      
      ax2.set_ylabel (r'Importance of each parameter for the classification')
      ax2.tick_params (axis='y', labelleft=False, labelright=True, left=False)
      
      ax3.set_xlabel (r'Correlation between the parameters from the training data set')
      
      plt.show ()
    
    if summary==True :
      frame_summary = pd.DataFrame (index=frame_label_test.index, data=proba, columns=training_class)
      frame_summary = frame_summary.join (frame_label_test)
      frame_summary['label_pred'] = label_pred.astype ('U20')
      frame_summary.to_csv (frame_name)
      print ('Summary frame saved in', frame_name)

  if save==True :
    print ('Classifier saved in', clf_name)
  
  return clf 

def train_nn (training_set,
              save=False,
              clf_name='nn_classifier.joblib', 
              summary=False, 
              frame_name='test_nn_summary.csv', 
              plot=True,
              test_size=0.15, 
              verbose=True,
              cmap='winter', 
              fontsize=20, 
              lettercolor='white',
              #hyper-parameter of the classifier
              hidden_layer_sizes=(100, ), 
              activation='relu', 
              solver='adam', 
              alpha=0.0001, batch_size='auto', 
              learning_rate='constant', 
              learning_rate_init=0.001, 
              power_t=0.5, 
              max_iter=200, 
              shuffle=True, 
              random_state=None, 
              tol=0.0001, 
              warm_start=False, 
              momentum=0.9, 
              nesterovs_momentum=True, 
              early_stopping=False, 
              validation_fraction=0.1, 
              beta_1=0.9, 
              beta_2=0.999, 
              epsilon=1e-08, 
              n_iter_no_change=10, 
              max_fun=15000) :

  '''
  Generic template for training neural networks classifiers.
  
  :param training_set: pandas DataFrame. It is mandatory
  that one of the columns is named 'label'.
  The id of the stars (KIC, TIC, etc.) must be given as the index 
  of the DataFrame.
  :type training_set: pandas.DataFrame

  :param save: if set on true the function will save a version of the trained classifier
  in joblib files. Default False. 
  :type save: bool

  :param clf_name: name of the file where to save the classifier, default 'rf_classifier'
  :type clf_name: str

  :param summary: save a frame summarizing the probability of classification 
  of the training set, default False.
  :type summary: bool

  :param frame_name: name of the csv file where to store the results
  of the test step, default 'test_summary.csv'
  :type frame_name: str

  :param plot: set to True to show the correlation matrix between parameters, the confusion matrix and
  the relative important between parameter, default True
  :type plot: bool`

  :param test_size: fraction of data that will be used as test set, default 0.15.
  :type test_size: float

  :param verbose: set to True to print additional intels about the training, default True.
  :type verbose: bool

  :param cmap: color map (see matplotlib doc) to use when plotting the confusion matrix,
  default 'winter'.
  :type cmap: str 

  :param fontsize: size of the font to use in the confusion matrix, default 20, 
  :type fontsize: str

  :param lettercolor: color (see matplotlib doc) used for the characters in the confusion matrix,
  default 'white'.
  :type lettercolor: str

  For the hyper-parameter of the classifier, refer to scikit-learn documentation.

  :return: the trained classifier.
  :rtype: object

  :Example:
 
  >>> import pandas as pd
  >>> data, target = datasets.load_iris (return_X_y=True)
  >>> training_set = pd.DataFrame (data=data)
  >>> training_set['label'] = target
  >>> train_nn (training_set, plot=True, summary=False, save=False)

  '''
 
  df = training_set
  df['label'] = df['label'].map (str)

  # convert columns name from int/float to string
  # (if it has not been done yet) to ensure stability
  # of the code
  input_param = df.columns.values
  input_param = input_param.astype ('U20')
  df.columns = input_param

  input_param = np.setdiff1d (input_param, np.array(['label']))

  df = df.dropna (axis=0)
  if verbose==0 :
    print ('Number of elements in the training set', df.index.size)
  
  #------------------------------------------------------------------------------------------------------------------------
  #------------------------------------------------------------------------------------------------------------------------
  #------------------------------------------------------------------------------------------------------------------------
  
  #CREATING TRAINING AND TESTING SET
  
  try :
    frame_label = df[['label']]
  except KeyError :
    print ('KeyError : the input training set needs to have a columns \'label\', training interrupted.')
    sys.exit ()
  df = df [input_param]
  df = df.sort_index (axis=1)
  

  if test_size > 0 :
    df_train, df_test, frame_label_train, frame_label_test = train_test_split (df, frame_label, test_size=test_size)

    data_test = df_test.to_numpy (dtype=np.float64) 
    label_test = frame_label_test.to_numpy (dtype='U20') 
    label_test = np.ravel (label_test)
    id_test = df_test.index 

  else :
    df_train = df
    frame_label_train = frame_label
  
  data_train = df_train.to_numpy (dtype=np.float64) 
  label_train = frame_label_train.to_numpy (dtype='U20') 
  label_train = np.ravel (label_train)
  id_train = df_train.index 
  training_class = np.unique (label_train)
  
  
  correl_parameters = np.corrcoef (data_train, rowvar=False)
  
  #------------------------------------------------------------------------------------------------------------------------
  #------------------------------------------------------------------------------------------------------------------------
  #------------------------------------------------------------------------------------------------------------------------
  
  #TRAINING CLASSIFIER
  scaler = preprocessing.StandardScaler()

  mlp = MLPClassifier(hidden_layer_sizes=hidden_layer_sizes, activation=activation, solver=solver, 
                      alpha=alpha, batch_size=batch_size, learning_rate=learning_rate, 
                      learning_rate_init=learning_rate_init, power_t=power_t, max_iter=max_iter, 
                      shuffle=shuffle, random_state=random_state, tol=tol, verbose=verbose, 
                      warm_start=warm_start, momentum=momentum, nesterovs_momentum=nesterovs_momentum,
                      early_stopping=early_stopping, validation_fraction=validation_fraction, 
                      beta_1=beta_1, beta_2=beta_2, epsilon=epsilon, n_iter_no_change=n_iter_no_change, 
                      max_fun=max_fun) 
  
  clf = Pipeline([('scaler', scaler), ('mlp', mlp)])
  clf.fit (data_train, label_train)

  if save==True :
    dump (clf, clf_name)
  
  #------------------------------------------------------------------------------------------------------------------------
  #------------------------------------------------------------------------------------------------------------------------
  #------------------------------------------------------------------------------------------------------------------------
  
  #TESTING CLASSIFIER AND PLOTTING RESULTS
  if test_size > 0 :

    label_pred = clf.predict (data_test)
    proba = clf.predict_proba (data_test)
      
    if verbose==True :
      print (clf.get_params ())

    print ('Validation score : ', clf.score (data_test, label_test))

    if plot==True :
    
      
      fig = plt.figure (figsize=(6,6))
      fig_2 = plt.figure (figsize=(6,6))
      ax1 = fig.add_subplot (111)
      ax2 = fig_2.add_subplot (111)
      
      c2 = ax2.pcolor (correl_parameters, cmap='RdYlGn_r', vmin=-1., vmax=1.)
      fig.colorbar (c2, ax=ax2)
      
      conf_matrix = confusion_matrix (label_test, label_pred, training_class)

      ax1.set_xticks ([i+0.5 for i in range (training_class.size)])
      ax1.set_yticks ([i+0.5 for i in range (training_class.size)])
      ax1.set_xticklabels (training_class)
      ax1.set_yticklabels (['pred_'+ elt for elt in training_class])

      for x in range (training_class.size) :
        for y in range (training_class.size) :
          ax1.text (x+0.5, y+0.5, '%-s' % conf_matrix [x, y], 
                    horizontalalignment='center', verticalalignment='center', 
                    fontsize=fontsize, color=lettercolor) 
      
      c1 = ax1.pcolor (conf_matrix, cmap=cmap)
      fig.colorbar (c1, ax=ax1)
      
      ax2.set_xticks (np.array([i for i in range (1, input_param.size+1)]) - 0.5)
      ax2.set_yticks (np.array([i for i in range (1, input_param.size+1)]) - 0.5)
      ax2.set_xticklabels (input_param)
      ax2.set_yticklabels (input_param)
      
      ax2.tick_params (axis='x', labelrotation = 90.)
      
      ax2.set_xlabel (r'Correlation between the parameters from the training data set')
      
      plt.show ()
    
    if summary==True :
      frame_summary = pd.DataFrame (index=frame_label_test.index, data=proba, columns=training_class)
      frame_summary = frame_summary.join (frame_label_test)
      frame_summary['label_pred'] = label_pred.astype ('U20')
      frame_summary.to_csv (frame_name)
      print ('Summary frame saved in', frame_name)

  if save==True :
    print ('Classifier saved in', clf_name)
  
  return clf 


def train_knn (training_set,
              save=False,
              clf_name='knn_classifier.joblib', 
              summary=False, 
              frame_name='test_knn_summary.csv', 
              plot=True,
              test_size=0.15, 
              verbose=0,
              cmap='winter', 
              fontsize=20, 
              lettercolor='white',
              #hyper-parameter of the nca
              n_components=None, 
              init='auto', 
              warm_start=False, 
              max_iter=50, 
              tol=1e-05, 
              callback=None, 
              random_state=None,
              #hyper-parameter of the knn
              n_neighbors=5, 
              weights='uniform', 
              algorithm='auto', 
              leaf_size=30, 
              p=2, 
              metric='minkowski', 
              metric_params=None, 
              n_jobs=None) :

  '''
  Generic template for training K nearest neighbours classifiers.
  
  :param training_set: pandas DataFrame. It is mandatory
  that one of the columns is named 'label'.
  The id of the stars (KIC, TIC, etc.) must be given as the index 
  of the DataFrame.
  :type training_set: pandas.DataFrame

  :param save: if set on true the function will save a version of the trained classifier
  in joblib files. Default False. 
  :type save: bool

  :param clf_name: name of the file where to save the classifier, default 'rf_classifier'
  :type clf_name: str

  :param summary: save a frame summarizing the probability of classification 
  of the training set, default False.
  :type summary: bool

  :param frame_name: name of the csv file where to store the results
  of the test step, default 'test_summary.csv'
  :type frame_name: str

  :param plot: set to True to show the correlation matrix between parameters, the confusion matrix and
  the relative important between parameter, default True
  :type plot: bool`

  :param test_size: fraction of data that will be used as test set, default 0.15.
  :type test_size: float

  :param verbose: set to True to print additional intels about the training, default True.
  :type verbose: bool

  :param cmap: color map (see matplotlib doc) to use when plotting the confusion matrix,
  default 'winter'.
  :type cmap: str 

  :param fontsize: size of the font to use in the confusion matrix, default 20, 
  :type fontsize: str

  :param lettercolor: color (see matplotlib doc) used for the characters in the confusion matrix,
  default 'white'.
  :type lettercolor: str

  For the hyper-parameter of the classifier, refer to scikit-learn documentation.

  :Example:

  >>> import pandas as pd
  >>> data, target = datasets.load_iris (return_X_y=True)
  >>> training_set = pd.DataFrame (data=data)
  >>> training_set['label'] = target
  >>> train_knn (training_set, plot=True, summary=False, save=False)

  '''
 
  df = training_set
  df['label'] = df['label'].map (str)

  # convert columns name from int/float to string
  # (if it has not been done yet) to ensure stability
  # of the code
  input_param = df.columns.values
  input_param = input_param.astype ('U20')
  df.columns = input_param

  input_param = np.setdiff1d (input_param, np.array(['label']))

  df = df.dropna (axis=0)
  if verbose==0 :
    print ('Number of elements in the training set', df.index.size)
  
  #------------------------------------------------------------------------------------------------------------------------
  #------------------------------------------------------------------------------------------------------------------------
  #------------------------------------------------------------------------------------------------------------------------
  
  #CREATING TRAINING AND TESTING SET
  
  try :
    frame_label = df[['label']]
  except KeyError :
    print ('KeyError : the input training set needs to have a columns \'label\', training interrupted.')
    sys.exit ()

  df = df [input_param]
  df = df.sort_index (axis=1)
  
  if test_size > 0 :
    df_train, df_test, frame_label_train, frame_label_test = train_test_split (df, frame_label, test_size=test_size)

    data_test = df_test.to_numpy (dtype=np.float64) 
    label_test = frame_label_test.to_numpy (dtype='U20') 
    label_test = np.ravel (label_test)
    id_test = df_test.index 
  else :
    df_train = df
    frame_label_train = frame_label
  
  data_train = df_train.to_numpy (dtype=np.float64) 
  label_train = frame_label_train.to_numpy (dtype='U20') 
  label_train = np.ravel (label_train)
  id_train = df_train.index 
  training_class = np.unique (label_train)
  
  
  correl_parameters = np.corrcoef (data_train, rowvar=False)
  
  #------------------------------------------------------------------------------------------------------------------------
  #------------------------------------------------------------------------------------------------------------------------
  #------------------------------------------------------------------------------------------------------------------------
  
  #TRAINING CLASSIFIER
  nca = NeighborhoodComponentsAnalysis(n_components=n_components, init=init, warm_start=warm_start, 
                                       max_iter=max_iter, tol=tol, callback=callback, 
                                       verbose=verbose, random_state=random_state)
  knn = KNeighborsClassifier (n_neighbors=n_neighbors, weights=weights, algorithm=algorithm, 
                             leaf_size=leaf_size, p=p, metric=metric, 
                             metric_params=metric_params, n_jobs=n_jobs)
  clf = Pipeline([('nca', nca), ('knn', knn)])
  
  clf.fit (data_train, label_train)

  if save==True :
    dump (clf, clf_name)
  
  #------------------------------------------------------------------------------------------------------------------------
  #------------------------------------------------------------------------------------------------------------------------
  #------------------------------------------------------------------------------------------------------------------------
  
  #TESTING CLASSIFIER AND PLOTTING RESULTS
  if test_size > 0 :

    label_pred = clf.predict (data_test)
    proba = clf.predict_proba (data_test)
      
    if verbose==True :
      print (clf.get_params ())

    print ('Validation score : ', clf.score (data_test, label_test))

    if plot==True :
    
      fig = plt.figure (figsize=(6,6))
      fig_2 = plt.figure (figsize=(6,6))
      ax1 = fig.add_subplot (111)
      ax2 = fig_2.add_subplot (111)
      
      c2 = ax2.pcolor (correl_parameters, cmap='RdYlGn_r', vmin=-1., vmax=1.)
      fig.colorbar (c2, ax=ax2)
      
      conf_matrix = confusion_matrix (label_test, label_pred, training_class)

      ax1.set_xticks ([i+0.5 for i in range (training_class.size)])
      ax1.set_yticks ([i+0.5 for i in range (training_class.size)])
      ax1.set_xticklabels (training_class)
      ax1.set_yticklabels (['pred_'+ elt for elt in training_class])

      for x in range (training_class.size) :
        for y in range (training_class.size) :
          ax1.text (x+0.5, y+0.5, '%-s' % conf_matrix [x, y], 
                    horizontalalignment='center', verticalalignment='center', 
                    fontsize=fontsize, color=lettercolor) 
      
      c1 = ax1.pcolor (conf_matrix, cmap=cmap)
      fig.colorbar (c1, ax=ax1)
      
      ax2.set_xticks (np.array([i for i in range (1, input_param.size+1)]) - 0.5)
      ax2.set_yticks (np.array([i for i in range (1, input_param.size+1)]) - 0.5)
      ax2.set_xticklabels (input_param)
      ax2.set_yticklabels (input_param)
      
      ax2.tick_params (axis='x', labelrotation = 90.)
      
      ax2.set_xlabel (r'Correlation between the parameters from the training data set')
      
      plt.show ()
    
    if summary==True :
      frame_summary = pd.DataFrame (index=frame_label_test.index, data=proba, columns=training_class)
      frame_summary = frame_summary.join (frame_label_test)
      frame_summary['label_pred'] = label_pred.astype ('U20')
      frame_summary.to_csv (frame_name)
      print ('Summary frame saved in', frame_name)

  if save==True :
    print ('Classifier saved in', clf_name)
  
  return clf 
