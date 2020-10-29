# -*- coding: utf-8 -*-
"""MMF1922.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab

## MMF1922 Data Science
Author: Zhuoran Li, Yuanliufang Tao, Liu Xin
Date: October 29, 2020
"""

# SKLEARN is a useful tool to implement machine learning
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, log_loss, classification_report)

from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import SMOTE

from sklearn import metrics
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# read csv file
data = pd.read_csv('Data.csv')

# create a copy
data_copy = data

# preview the data
data.head(5)

# check null value
# caution: never having null value in Machine Learning
data.isna().sum()

# variable type check
data.dtypes

# Pearson correlation matrix
# heatmap
numerical = ['Age', 'Attrition', 'DailyRate', 'DistanceFromHome', 
             'Education', 'EmployeeNumber', 'EnvironmentSatisfaction',
             'HourlyRate', 'JobInvolvement', 'JobLevel', 'JobSatisfaction',
             'MonthlyIncome', 'MonthlyRate', 'NumCompaniesWorked',
             'PercentSalaryHike', 'PerformanceRating', 'RelationshipSatisfaction',
             'StockOptionLevel', 'TotalWorkingYears',
             'TrainingTimesLastYear', 'WorkLifeBalance', 'YearsAtCompany',
             'YearsInCurrentRole', 'YearsSinceLastPromotion','YearsWithCurrManager']

plt.figure(figsize=(30,30))
cor = data[numerical].corr()
sns.heatmap(cor, annot=False, cmap=plt.cm.Reds)
plt.show()

# transform the categorical variables into numreical
# so that data can be learned
string_var = ['BusinessTravel', 'Department', 'EducationField', 'Gender', 'JobRole', 'MaritalStatus', 'Over18', 'OverTime']
le = preprocessing.LabelEncoder()
for i in string_var:
    le.fit(data_copy[i])
    data_copy[i] = le.transform(data_copy[i])

# review the transformed data -> DONE cleaning data
# notice: since not neural network, do not need to normalize data
data.head(5)

# data visualization
# noticing that there might be an imbalance data problem
pd.value_counts(data['Attrition']).plot.bar()
plt.title('Target histogram Default', fontsize=20)

ax = plt.subplot(111)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
ax.set_xlabel('Attrition', fontsize=20)
ax.set_ylabel('Frequency', fontsize=20)

data['Attrition'].value_counts()

# split data into TARGET (y) and FEATURES (x)
# set 20% of the data as test set.
y = data_copy[['Attrition']]
x = data_copy.drop(columns = ['Attrition'])
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

# random forest classification WITHOUT any treat on imbalance data
# prior imbalance dataset treatments
clf = RandomForestClassifier(n_estimators = 100, 
                             bootstrap = True, max_features = 'sqrt')
clf.fit(x_train,y_train)
predict = clf.predict(x_test)

# result of accuracy, precision, recall, f1 score
# treat 'Yes' as positive target
# recall = 0.14
print("Accuracy score: {}".format(accuracy_score(y_test, predict)))
print("="*60)
print(classification_report(y_test, predict))

#################################################
## Treat imbalance dataset using UNDERSAMPLING ##
#################################################
rus = RandomUnderSampler(random_state=0)
x_resampled, y_resampled = rus.fit_sample(x, y)

# target data visualization after undersampling
pd.value_counts(y_resampled[:,0]).plot.bar()
plt.title('Target histogram after undersampling', fontsize=20)

plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.xlabel('Attrition', fontsize=20)
plt.ylabel('Frequency', fontsize=20)
data['Attrition'].value_counts()

# undersampling
# Split train, test again
x_train_1, x_test_1, y_train_1, y_test_1 = \
train_test_split(x_resampled, y_resampled, test_size=0.2, random_state=0)
# predict again
clf.fit(x_train_1,y_train_1)
predict_undersampling = clf.predict(x_test_1)

# undersampling Result
# recall = 0.87
# notice that there might be different recall score each time you train
# but it should be larger than prior recall
print("Accuracy score: {}".format(accuracy_score(y_test_1, predict_undersampling)))
print("="*60)
print(classification_report(y_test_1, predict_undersampling))

################################################
## Treat imbalance dataset using SMOTE METHOD ##
################################################
sm = SMOTE(random_state=2)
X_train_SMOTE, y_train_SMOTE = sm.fit_resample(x_train, y_train)

# target data visualization after SMOTE
pd.value_counts(y_train_SMOTE).plot.bar()
plt.title('Target histogram after SMOTE', fontsize=20)

plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.xlabel('Attrition', fontsize=20)
plt.ylabel('Frequency', fontsize=20)
pd.value_counts(y_train_SMOTE)

# SMOTE
# Split train, test again
x_train_2, x_test_2, y_train_2, y_test_2 = train_test_split(X_train_SMOTE, y_train_SMOTE, test_size=0.2, random_state=0)
# Predict again
clf.fit(x_train_2,y_train_2)
predict_SMOTE = clf.predict(x_test_2)

# SMOTE Result
# recall = 0.89
# notice that there might be different recall score each time you train
# it should be larger than undersampling
print("Accuracy score: {}".format(accuracy_score(y_test_2, predict_SMOTE)))
print("="*60)
print(classification_report(y_test_2, predict_SMOTE))

########################################################
####################### ROC ############################
########################################################

###################### Original ######################

# prepare data used by ROC
y_score = clf.fit(x_train, y_train).predict_proba(x_test)

## Tranform the target into interger
le = preprocessing.LabelEncoder()
le.fit(y_test)
y_test_encoded = le.transform(y_test)

## Prepare data for drawing ROC
fpr, tpr, thresholds = metrics.roc_curve(y_test_encoded, y_score[:, 1])
roc_auc = metrics.auc(fpr, tpr)

# Undersampling
y_score_under = clf.fit(x_train_1,y_train_1).predict_proba(x_test_1)
le_1 = preprocessing.LabelEncoder()
le_1.fit(y_test_1)
y_test_encoded_1 = le_1.transform(y_test_1)

fpr_under, tpr_under, thresholds_under = metrics.roc_curve(y_test_encoded_1, y_score_under[:, 1])
roc_auc_under = metrics.auc(fpr_under, tpr_under)

# SMOTE
y_score_SMOTE = clf.fit(x_train_2,y_train_2).predict_proba(x_test_2)
le_2 = preprocessing.LabelEncoder()
le_2.fit(y_test_2)
y_test_encoded_2 = le_2.transform(y_test_2)

fpr_SMOTE, tpr_SMOTE, thresholds_SMOTE = metrics.roc_curve(y_test_encoded_2, y_score_SMOTE[:, 1])
roc_auc_SMOTE = metrics.auc(fpr_SMOTE, tpr_SMOTE)

def drawRocMix(roc_auc,fpr,tpr, roc_auc_1, fpr_1,tpr_1, roc_auc_2, fpr_2,tpr_2):
    plt.subplots(figsize=(7, 5.5))
    plt.plot(fpr, tpr, color='lightblue', lw=2, label='ROC curve default (area = %0.2f) ' % roc_auc)
    plt.plot(fpr_1, tpr_1, color='blue', lw=2, label='ROC curve undersampling (area = %0.2f) ' % roc_auc_1)
    plt.plot(fpr_2, tpr_2, color='darkblue', lw=2, label='ROC curve SMOTE (area = %0.2f) ' % roc_auc_2)
    plt.plot([0, 1], [0, 1], color='grey', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve')
    plt.legend(loc="lower right")
    plt.show()
drawRocMix(roc_auc, fpr, tpr, roc_auc_under, fpr_under, tpr_under, roc_auc_SMOTE, fpr_SMOTE, tpr_SMOTE)

