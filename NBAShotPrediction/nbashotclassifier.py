# Author: Devante Wilson
# Date: February 18, 2018
#
# This program is an NBA shot classifier for the regular 2015-2016 season.

# import required libraries
from __future__ import print_function, division
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, RobustScaler, MinMaxScaler
from sklearn.metrics import classification_report, accuracy_score

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
palette = sns.color_palette('deep', 5)
palette[1], palette[2] = palette[2], palette[1]

# define file name
file_name = 'train.csv'
# load the NBA shot data set using Pandas
nba = pd.read_csv(file_name)

# show heatmap of missing values
# plt.figure(figsize=(12, 12))
# sns.heatmap(nba.isnull(), yticklabels=False, cbar=False, cmap='jet')
# plt.show()

# # check missing data (final check)
# print(nba[nba.isnull().any(axis=1)])

# convert categorical classes into binary values to feed to the model
action_type = pd.get_dummies(nba['ACTION_TYPE'])
shot_type = pd.get_dummies(nba['SHOT_TYPE'])
shot_zone_area = pd.get_dummies(nba['SHOT_ZONE_AREA'])
shot_zone_basic = pd.get_dummies(nba['SHOT_ZONE_BASIC'])
shot_zone_range = pd.get_dummies(nba['SHOT_ZONE_RANGE'])

# drop old and unnecessary headers from data frame
nba = nba.drop(['ACTION_TYPE', 'EVENTTIME', 'GAME_DATE', 'GAME_ID', 'HTM',
                'MINUTES_REMAINING', 'PERIOD', 'PLAYER_ID', 'PLAYER_NAME', 'QUARTER', 'SECONDS_REMAINING',
                'SHOT_ATTEMPTED_FLAG', 'SHOT_TIME', 'SHOT_TYPE', 'SHOT_ZONE_AREA', 'SHOT_ZONE_BASIC',
                'SHOT_ZONE_RANGE', 'TEAM_ID', 'TEAM_NAME', 'VTM', 'LOC_X', 'LOC_Y'], axis=1)

# add all of the new features
nba = pd.concat([nba, action_type, shot_type, shot_zone_area, shot_zone_basic, shot_zone_range], axis=1)

# define prediction target
y = nba['SHOT_MADE_FLAG']
# set prediction data (return view/copy with column(s) removed)
X = nba.drop(['SHOT_MADE_FLAG', 'GAME_EVENT_ID'], axis=1)

# create a standard scaler object
scaler = StandardScaler()

# standard scale the training data
X_scaled = scaler.fit_transform(X)

# create logistic regression model (transformed = 1 / (1 + e^-x))
logmodel = LogisticRegression()

# fit/train the model on the training data
logmodel.fit(X_scaled, y)

# get predictions for the trained model
predictions_train = logmodel.predict(X_scaled)

# evaluate performance of the model
print(classification_report(y, predictions_train))
print("Accuracy: {}".format(accuracy_score(y, predictions_train))) # can alternatively use model.score(X, y)

# import test data
test_nba = pd.read_csv('solution_no_answer.csv')

# convert categorical classes into binary values to feed into the model
test_action_type = pd.get_dummies(test_nba['ACTION_TYPE'])
test_shot_type = pd.get_dummies(test_nba['SHOT_TYPE'])
test_shot_zone_area = pd.get_dummies(test_nba['SHOT_ZONE_AREA'])
test_shot_zone_basic = pd.get_dummies(test_nba['SHOT_ZONE_BASIC'])
test_shot_zone_range = pd.get_dummies(test_nba['SHOT_ZONE_RANGE'])

# get new dataframe for test data
test_nba = test_nba.drop(['ACTION_TYPE', 'EVENTTIME', 'GAME_DATE', 'HTM',
            'MINUTES_REMAINING', 'PERIOD', 'PLAYER_ID', 'PLAYER_NAME', 'QUARTER', 'SECONDS_REMAINING',
            'SHOT_ATTEMPTED_FLAG', 'SHOT_TIME', 'SHOT_TYPE', 'SHOT_ZONE_AREA', 'SHOT_ZONE_BASIC',
            'SHOT_ZONE_RANGE', 'TEAM_ID', 'TEAM_NAME', 'VTM', 'LOC_X', 'LOC_Y'], axis=1)

# add the new features
test_nba = pd.concat([test_nba, test_action_type, test_shot_type, test_shot_zone_area,
                      test_shot_zone_basic, test_shot_zone_range], axis=1)

# set prediction data (return view/copy with column(s) removed)
X_test = test_nba.drop('GAME_EVENT_ID', axis=1)

# add missing headers (two categories from ACTION_TYPE)
X_test['Running Alley Oop Layup Shot'] = pd.Series(0, index=X_test.index)
X_test['Driving Jump Shot'] = pd.Series(0, index=X_test.index)

# generate predictions based on test data
predictions_test = logmodel.predict(X_test)

# create submission for Kaggle
submission = pd.DataFrame({"GAME_EVENT_ID": test_nba["GAME_EVENT_ID"], "SHOT_MADE_FLAG": predictions_test})

# write submission to csv
submission.to_csv("logreg_submission2.csv", index=False) # do not save index values