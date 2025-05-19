import np as np
import pip
import math

import scipy.stats
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from ipywidgets import interact, widgets
from IPython.core.pylabtools import figsize

import sklearn
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import sklearn.neighbors as skl_nb
import sklearn.discriminant_analysis as skl_da
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.preprocessing import StandardScaler

#Egen import
from sklearn.metrics import roc_curve

import pandas as pd
from pandas import *




#### reading CSV file
data_train = read_csv('training_data_fall2024.csv', dtype={"increase_stock": str, "hour_of_day": int, "day_of_week": int, "month": int,\
                                                     "holiday": int, "weekday": int, "summertime": int, "temp": float, "dew": float,\
                                                     "humidity": float, "precip": float, "snow": float, "snowdepth": float, "windspeed": float,\
                                                     "cloudcover": float, "visibility": float})


data_test = read_csv('test_data_fall2024.csv', dtype={"increase_stock": str, "hour_of_day": int, "day_of_week": int, "month": int,\
                                                     "holiday": int, "weekday": int, "summertime": int, "temp": float, "dew": float,\
                                                     "humidity": float, "precip": float, "snow": float, "snowdepth": float, "windspeed": float,\
                                                     "cloudcover": float, "visibility": float})



# ----------------------------------------------------------------------------------------------------------------#

#%%

###### Plots to check for significans #######

categories = {}
categories_std = {}

df = pd.DataFrame(data_train)
data_processed = df.drop(columns='increase_stock')

for i in data_processed[:0]:

    categories[i] = max(data_processed[i])  #max values
    categories_std[i] = np.std(data_processed[i])   #standard deviation


# - sign for descended values, omit if low-high sorting required
res = {val[0]: val[1] for val in sorted(categories.items(), key=lambda x: (-x[1], x[0]))}
res_std = {val[0]: val[1] for val in sorted(categories_std.items(), key=lambda x: (-x[1], x[0]))}


Variables = list(res.keys())
Max_values = list(res.values())

Variables_std = list(res_std.keys())
Values_std = list(res_std.values())


fig = plt.figure(figsize = (20, 10))
plt.bar(Variables, Max_values, color='magenta')
plt.xlabel("Maximum variable value")
plt.ylabel("Variables")


fig_std = plt.figure(figsize = (20, 10))
plt.bar(Variables_std, Values_std, color='green')
plt.xlabel("Standard Deviation")
plt.ylabel("Variables")


#plt.show()


# ----------------------------------------------------------------------------------------------------------------#

#%%


################ Classification labels y_train ##################


pd.plotting.scatter_matrix(data_train.iloc[:, 1:15], figsize=(15, 15))

df = pd.DataFrame(data_train)

data_opt = df.drop(columns = 'holiday')
data_opt_final = data_opt.drop(columns = 'snow')

pd.plotting.scatter_matrix(data_opt_final.iloc[:,1:13], figsize=(13,13))

#plt.show()



######## Sampling indices for trainig #########


'''Randomly samples rows from data_train to create your training dataset. This ensures you have a smaller, well-defined training set for your model.'''


np.random.seed(1)
trainI = np.random.choice(data_train.shape[0], size=1000, replace=False)
trainIndex = data_train.index.isin(trainI)
train = data_train.iloc[trainIndex]


testI = np.random.choice(data_test.shape[0], size=400, replace=False)
testIndex = data_test.index.isin(testI)
#test = data_test.iloc[testIndex]



'''The ~ operator ensures that rows in data_test with the same index as data_train are excluded.
 This ensures no row from data_train is accidentally "memorized" by the model during training.'''
test = data_test[~data_test.index.isin(trainIndex)]



# Define the training and testing datasets
X_train = train[['hour_of_day','day_of_week','month','weekday','summertime','temp','dew','humidity','precip','snowdepth','windspeed','cloudcover','visibility']]
Y_train = train['increase_stock']


# New test data_train
X_test = test[['hour_of_day','day_of_week','month','weekday','summertime','temp','dew','humidity','precip','snowdepth','windspeed','cloudcover','visibility']]

common_rows = pd.merge(X_train, X_test, how='inner')
print(f"Number of overlapping rows: {len(common_rows)}")


# ----------------------------------------------------------------------------------------------------------------#

#%%

#################### LDA ######################


# Initialize and train the LDA model

'''Regularization helps prevent overfitting by constraining the model's complexity. For LDA, you can add shrinkage'''
LDA = skl_da.LinearDiscriminantAnalysis(solver='lsqr', shrinkage='auto')
LDA.fit(X_train, Y_train)
print("Model summary:")
print(LDA)


Y_test = LDA.predict(X_test)
Y_test_bin = [] #binary representation

for i in Y_test:
    if i == 'low_bike_demand':
        Y_test_bin.append(0)
    if i == 'high_bike_demand':
        Y_test_bin.append(1)


###### Probabilities and Confusion matrix: LDA #######


# Predict probabilities for the test set
predict_prob = LDA.predict_proba(X_test)
print("Model summary:")
print(LDA)

'''
The predict_proba() function is designed to give the probability estimates for each class label in a classification task.

The predict_proba() function in SVC utilizes a method called Platt scaling to convert the decision values from the SVM into
probabilities. Platt scaling is a post-processing step that applies a logistic regression model to the decision values, which
are the distances of the samples from the hyperplane.

Once trained, the logistic regression model is used to convert the decision function scores into probabilities.
This is done for each class, resulting in a probability distribution over all classes.
'''

print('--------------------------------------')


print("The class order in the model:")
print(LDA.classes_)
print("Examples of predicted probabilities for LDA:")
with np.printoptions(suppress=True, precision=3):
    print(predict_prob[0:5])  # Inspect the first 5 predictions

print('--------------------------------------')

# Classify predictions based on probability threshold
prediction = np.where(predict_prob[:, 0] <= 0.5, 'low_bike_demand', 'high_bike_demand')
print("Predictions:")
print(prediction[0:5], '\n')  # Inspect the first 5 predictions after labeling

print('--------------------------------------')

# Confusion matrix
print("Confusion matrix, LDA:")
print(pd.crosstab(prediction, Y_test), '\n')

print('--------------------------------------')

# Accuracy calculation
print(f"Accuracy: {np.mean(prediction == Y_test):.3f}")


print('--------------------------------------')



#%%
# ----------------------------------------------------------------------------------------------------------------#

########### Grid Search #############

param_grid = {'solver': ['svd', 'lsqr', 'eigen'],'shrinkage': [None, 'auto', 0.1, 0.5, 0.9]}

grid_search = GridSearchCV(
    estimator=LDA,
    param_grid=param_grid,
    cv=5,  # 5-fold cross-validation
    scoring='accuracy',  # Use accuracy as the metric
    verbose=1)

grid_search.fit(X_train, Y_train)

print('--------------------------------------')

# Best model and parameters
print("Best Parameters:", grid_search.best_params_)
print("Best Cross-Validation Score:", grid_search.best_score_)

print('--------------------------------------')

# Predict using the best model
best_model = grid_search.best_estimator_
predict_prob_grid = best_model.predict_proba(X_test)

# Classify predictions
prediction_grid = np.where(predict_prob_grid[:, 0] <= 0.5, 'low_bike_demand', 'high_bike_demand')
accuracy_grid = np.mean(prediction_grid == Y_test)

# Confusion matrix after GridSearch
conf_matrix_grid = pd.crosstab(prediction_grid, Y_test)
print("Confusion matrix after GridSearch:")
print(conf_matrix_grid)

print('--------------------------------------')

# Accuracy after GridSearch
print(f"Accuracy (with GridSearch): {accuracy_grid:.3f}")

print('--------------------------------------')

'''
# Evaluate the performance
print("\nClassification Report:")
print(classification_report(Y_test, y_pred))
'''



# ----------------------------------------------------------------------------------------------------------------#


#%%

############################# QDA ##################################

# Initialize and train the QDA model
qda = skl_da.QuadraticDiscriminantAnalysis()
qda.fit(X_train, Y_train)
print("Model summary:")
print(qda)


print('--------------------------------------')

############# Probabilities and Confusion matrix: QDA ############

# Predict probabilities for the test set
predict_prob = qda.predict_proba(X_test)
print("The class order in the model:")
print(qda.classes_)
print("Examples of predicted probabilities for QDA:")
with np.printoptions(suppress=True, precision=5):
    print(predict_prob[0:5])  # Inspect the first 5 predictions

print('--------------------------------------')

# Classify predictions based on probability threshold
prediction = np.empty(len(X_test), dtype=object)
prediction = np.where(predict_prob[:, 0] <= 0.5, 'low_bike_demand', 'high_bike_demand')
print("Predictions:")
print(prediction[0:5], '\n')  # Inspect the first 5 predictions after labeling

print('--------------------------------------')

# Confusion matrix
print("Confusion matrix, QDA:")
print(pd.crosstab(prediction, Y_test), '\n')

print('--------------------------------------')

# Accuracy calculation
print(f"Accuracy: {np.mean(prediction == Y_test):.3f}")

print('--------------------------------------')


#%%

########### Grid Search: QDA #############

# Define the parameter grid
param_grid = {'reg_param': [0.0, 0.1, 0.2, 0.5, 0.9], 'store_covariance': [True, False]}

# Perform GridSearchCV
grid_search = GridSearchCV(
    estimator=qda,
    param_grid=param_grid,
    cv=5,
    scoring='accuracy',
    verbose=1)
grid_search.fit(X_train, Y_train)

# Print the best parameters and the best score
print("Best Parameters:", grid_search.best_params_)
print("Best Cross-Validation Score:", grid_search.best_score_)

print('--------------------------------------')

# Get the best model from Grid Search
best_qda = grid_search.best_estimator_

# Predict probabilities on the test set
predict_prob = best_qda.predict_proba(X_test)

print("The class order in the model:")
print(best_qda.classes_)
print("Examples of predicted probabilities for QDA:")
with np.printoptions(suppress=True, precision=5):
    print(predict_prob[0:5])  # Inspect the first 15 predictions

print('--------------------------------------')

# Classify predictions based on a probability threshold
prediction = np.where(predict_prob[:, 0] <= 0.5, 'low_bike_demand', 'high_bike_demand')
print("Predictions:")
print(prediction[0:5], '\n')  # Inspect the first 15 predictions after labeling

print('--------------------------------------')

# Confusion matrix
conf_matrix = confusion_matrix(Y_test, prediction)
print("Confusion matrix, QDA:")
print(pd.DataFrame(conf_matrix, columns=['Predicted Low', 'Predicted High'], index=['Actual Low', 'Actual High']), '\n')

print('--------------------------------------')

# Accuracy calculation
accuracy = accuracy_score(Y_test, prediction)
print(f"Accuracy: {accuracy:.3f}")
