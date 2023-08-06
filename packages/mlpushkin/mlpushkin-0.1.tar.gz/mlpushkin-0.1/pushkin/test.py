import pandas as pd
from train import train_nn, train_rf, train_knn
from classify import classify
from sklearn import datasets

#Test with a Kepler stars sample for rotation
# ----------------------------------------------------------------------------
#training_set = pd.read_csv ('../data_test/training_set_rot.csv', index_col=0)
#training_set = training_set.sample (n=1000)

#Test with the iris sample provided by sklearn
# ----------------------------------------------------------------------------
data, target = datasets.load_iris (return_X_y=True)
training_set = pd.DataFrame (data=data)
training_set['label'] = target
dataset = pd.DataFrame (data=data)

#Test with the digits sample
# ----------------------------------------------------------------------------
#data, target = datasets.load_digits (return_X_y=True)
#training_set = pd.DataFrame (data=data)
#training_set['label'] = target

train_rf (training_set, plot=False, summary=False, save=False)
#train_nn (training_set, plot=True, summary=False, save=False)
#train_knn (training_set, plot=False, n_neighbors=3, weights='distance')
#classify (dataset, clf_name='rf_classifier.joblib') 
#classify (dataset, clf_name='nn_classifier.joblib') 
