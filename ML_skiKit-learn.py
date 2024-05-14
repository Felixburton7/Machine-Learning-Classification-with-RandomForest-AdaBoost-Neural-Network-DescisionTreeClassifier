
# -*- coding: utf-8 -*-
"""ML Classfication of Students/k-Nearest Neighbors/RandomForest.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1zZhjkzy0pSpU5JPbwbJygtWtTmiruvwL

# **Kaggle HW5: Felix Burton**

**Remember to write your team name above, which MUST match your team name on Kaggle!!** Assignments without a team name will receive a 0/40 on the "accuracy on test data" component of this assignment's grade.
"""

from sklearn.neural_network import MLPClassifier
from sklearn.tree import plot_tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import lightgbm as lgb
from sklearn.metrics import confusion_matrix
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics
from sklearn.model_selection import train_test_split
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.dummy import DummyClassifier
import pandas as pd
import requests
from google.colab import drive
drive.mount('/content/drive')

"""### **Load the Data**"""

# This cell is necessary only if you are running on Google Colab. It downloads the files to your
# Colab instance so you don't have to upload them here.


def save_file(url, file_name):
    r = requests.get(url)
    with open(file_name, 'wb') as f:
        f.write(r.content)


save_file('https://courses.cs.washington.edu/courses/cse416/23sp/homeworks/hw5/edx_train.csv',
          'edx_train.csv')
save_file('https://courses.cs.washington.edu/courses/cse416/23sp/homeworks/hw5/edx_test.csv',
          'edx_test.csv')

df_test = pd.read_csv('edx_test.csv')
df_train = pd.read_csv('edx_train.csv')


"""### **Sample Code: Random Classifier**

**NOTE**: This classifier **DOES NOT** count as one of the 2 required for this assignment! It is merely here to illstrate how to submit your predictions.

See the Kaggle assignment (Data tab) for a description of each column in the dataset. You are creating a classifier to predict whether or not a student will get certified, stored in the `"certified"` column.
"""


target = "certified"  # target column

# This classifier returns labels sampled uniformly at random
df_train = pd.read_csv('edx_train.csv')
dummy_model = DummyClassifier(strategy="uniform")
dummy_model.fit(df_train.drop(target, axis=1), df_train[target])

"""The code below generates predictions on the test set, and outputs the predictions into a CSV file."""

# Generate predictions on the test set
df_test = pd.read_csv('edx_test.csv')
predictions = dummy_model.predict(df_test)

# Save your predictions as a CSV
# to_save = df_test[['userid_DI']].copy()
# to_save.loc[:, 'certified'] = predictions
# to_save.to_csv('submission.csv', index=False)

# See below for instructions on how to upload submission.csv to Kaggle,
# in order to evaluate your model and get points.

"""### **[5 Pts] Model Comparison**

**Instructions**: Run at least 2 different classification models. The classification models we have learned in class are: [Logistic Regression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html), [k-Nearest Neighbors](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html), [Decision Trees](https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html), [Random Forests](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html), and [AdaBoost](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.AdaBoostClassifier.html), [Neural Networks](https://scikit-learn.org/stable/modules/neural_networks_supervised.html). For each model, try at least 2 different hyperparameter settings.

Then, make one or more visualizations that let you compare the models you trained. Sample visualizations you can make include confusion matrices, or graphs of train and validation accuracy/error. See past section and homework code for how to make these visualizations.
"""

# Decision Tree: First classification Model
# Import the necessary libraries


# Inspecting Data
df_train = pd.read_csv('edx_train.csv')
df_train.columns

features = ['course_id', 'registered', 'viewed', 'explored', 'final_cc_cname_DI', 'LoE_DI', 'YoB', 'gender',
            'start_time_DI', 'last_event_DI', 'nevents', 'ndays_act', 'nplay_video',
            'nchapters', 'nforum_posts']

target = 'certified'
# Extract the feature columns and target column
df_train = df_train[features + [target]]
# df_train.head()


def visualize_confusion_matrix(test, pred, score):
    cm = confusion_matrix(test, pred)
    plt.figure(figsize=(9, 9))
    sns.heatmap(cm, annot=True, fmt=".3f", linewidths=.5,
                square=True, cmap='Blues_r')
    plt.ylabel('Actual label')
    plt.xlabel('Predicted label')
    all_sample_title = 'Accuracy Score: {0}'.format(score)
    plt.title(all_sample_title, size=15)


# Lets one hot encode this.
df_train = pd.get_dummies(df_train)
features = list(df_train.columns)
features.remove('certified')
# features

# Defining wieghts
# class_weights = {'explored': 2, 'viewed': 2, 'certified': 1}  # Increase weight for 'explored' and 'viewed'
# class_weights = {0: 1, 1: 2}  # Testing different hyperparameters
# Standard train Test Split to start with
train_val, test_data = train_test_split(df_train, test_size=0.1)
train_data, validation_data = train_test_split(train_val, test_size=0.2)

# Take care of the missing values

# Instantiate the imputer with the 'most_frequent' strategy
imputer = SimpleImputer(strategy='most_frequent')

# Fit the imputer on the training data and transform both training and validation data
train_data_imputed = imputer.fit_transform(train_data[features])
validation_data_imputed = imputer.transform(validation_data[features])

# Drop rows with missing values from both training and validation data
train_data_clean = train_data.dropna(subset=features)
validation_data_clean = validation_data.dropna(subset=features)

# Created a decision tree with a max_depth of 4 and random_state = 7


dt = DecisionTreeClassifier(max_depth=4, random_state=7)

# Fit the training data to decision tree
dt.fit(train_data_clean[features], train_data_clean[target])

# Let's see and visualize how our predictions look
dt_y_pred = dt.predict(validation_data_clean[features])
dt_score = dt.score(
    validation_data_clean[features], validation_data_clean[target])
visualize_confusion_matrix(validation_data_clean[target], dt_y_pred, dt_score)


# Handle missing values
imputer = SimpleImputer(strategy='most_frequent')
train_data[features] = imputer.fit_transform(train_data[features])
validation_data[features] = imputer.transform(validation_data[features])
test_data[features] = imputer.transform(test_data[features])

# Define sample weights based on 'viewed' and 'explored' features
sample_weight = np.ones(len(train_data))
sample_weight += train_data['viewed'] * 10  # Adjust the multiplier as needed
sample_weight += train_data['explored'] * 10  # Adjust the multiplier as needed

# Create and train the Decision Tree classifier with sample weights
dt = DecisionTreeClassifier(max_depth=4, random_state=7)
dt.fit(train_data[features], train_data[target], sample_weight=sample_weight)

# Predict on the validation set
dt_y_pred = dt.predict(validation_data[features])

# Evaluate the model
dt_accuracy = accuracy_score(validation_data[target], dt_y_pred)
print("Decision Tree Accuracy:", dt_accuracy)

# Visualize the confusion matrix
cm = confusion_matrix(validation_data[target], dt_y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot()
plt.title("Decision Tree Confusion Matrix")
plt.show()

# Generate predictions on the test set
# Generate predictions on the test set
df_test = pd.read_csv('edx_test.csv')
df_test.head()

# For the first classfication model, Part 2: I will be inroducing Boosting to try and improve my score I will be using LightGBM (Light Gradient Boosting Machine) an open-source gradient boosting framework developed by Microsoft

# Import the necessary libraries (I know this is repeated code but for my own clarity)

# Inspecting Data
df_train = pd.read_csv('edx_train.csv')
# Drop the User_id_column for training purposes
# Load the Iris dataset
X, y = df_train.drop(['certified', 'userid_DI'], axis=1), df_train.certified
# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)
# Should be without the columns
# X_train

# Encoding categorical features
cat_cols = X.select_dtypes(include=['object']).columns
label_encoders = {}
for col in cat_cols:
    le = LabelEncoder()
    X_train[col] = le.fit_transform(X_train[col])
    X_test[col] = le.fit_transform(X_test[col])
    df_test[col] = le.fit_transform(df_test[col])
    # check[col] = le.fit_transform(check[col])
    label_encoders[col] = le

# label_encoders
# X.columns
userid_DI = df_test.userid_DI
test = df_test.drop(['userid_DI'], axis=1)

# Create a training dataset.
# Create a LightGBM dataset
train_data = lgb.Dataset(X_train, label=y_train)
test_data = lgb.Dataset(X_test, label=y_test, reference=train_data)

# Specify parameters for the LightGBM classifier
params = {
    'boosting_type': 'gbdt',
    'objective': 'multiclass',
    'num_class': 2,
    'metric': 'multi_logloss',
    'num_leaves': 31,
    'learning_rate': 0.049,
    'feature_fraction': 0.9,
    'bagging_fraction': 0.8,
    'bagging_freq': 100,
    'verbose': 0
}

# Train the LightGBM classifier
num_round = 100
bst = lgb.train(params, train_data, num_round, valid_sets=[test_data])


# Make predictions on the test set
y_pred = bst.predict(X_test, num_iteration=bst.best_iteration)
y_pred_class = [int(pred.argmax()) for pred in y_pred]

# Evaluate the accuracy of the classifier
accuracy = accuracy_score(y_test, y_pred_class)
print("Accuracy:", accuracy)

# Save the best predictions (which is the certified column predictions)
predictions = bst.predict(test, num_iteration=bst.best_iteration)
predictions_c = [int(pred.argmax()) for pred in predictions]


# Save your predictions as a CSV
to_save = df_test[['userid_DI']].copy()
to_save.loc[:, 'certified'] = predictions_c
to_save.to_csv('submission.csv', index=False)
# to_save.head(10)

# See below for instructions on how to upload submission.csv to Kaggle,
# in order to evaluate your model and get points.

# Calculate predictions
predictions = bst.predict(X_test, num_iteration=bst.best_iteration)
predictions_c = [int(pred.argmax()) for pred in predictions]

# Compute confusion matrix
cm = confusion_matrix(y_test, predictions_c)

# Calculate accuracy score
accuracy = accuracy_score(y_test, predictions_c)

# Plot confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False)
plt.xlabel('Predicted labels')
plt.ylabel('True labels')
plt.title('Accuracy {0}'.format(accuracy))
plt.show()


# Tried a number of Hyperparameter settings and looked for the best ones using grid_search

# Perform grid search for Random Forest
param_grid = {
    'n_estimators': [50, 100, 200],  # Number of trees in the forest
    'max_depth': [None, 5, 10],       # Maximum depth of the trees
    # Minimum number of samples required to split a node
    'min_samples_split': [2, 5, 10]
}

# Instantiate the Random Forest classifier
rf = RandomForestClassifier(random_state=7)

# Create a GridSearchCV object
grid_search = GridSearchCV(
    estimator=rf, param_grid=param_grid, cv=5, scoring='accuracy', n_jobs=-1)

# Perform grid search on the training data
grid_search.fit(train_data_clean[features], train_data_clean[target])

# Get the best parameters and best score
best_params = grid_search.best_params_
best_score = grid_search.best_score_

print("Best Parameters:", best_params)
print("Best Score:", best_score)

# Use the best estimator to make predictions
best_rf = grid_search.best_estimator_
rf_y_pred = best_rf.predict(validation_data_clean[features])

# Evaluate the model
accuracy = accuracy_score(validation_data_clean[target], rf_y_pred)
print("Random Forest Accuracy:", accuracy)

# Visualize the decision tree
plt.figure(figsize=(20, 10))
plot_tree(best_rf.estimators_[0], feature_names=features, class_names=[
          '0', '1'], filled=True)
plt.title("Decision Tree Visualization")
plt.show()

# As a third model I tested a NN (just used sklearns as it should be of similar quality to PyTorch)

# Instantiate the Multi-layer Perceptron classifier
mlp = MLPClassifier(hidden_layer_sizes=(100, 50), activation='relu', solver='adam',
                    alpha=0.0001, batch_size='auto', learning_rate='constant',
                    learning_rate_init=0.001, max_iter=200, random_state=7)

# Train the neural network model
mlp.fit(train_data_clean[features], train_data_clean[target])

# Predict on the validation set
mlp_y_pred = mlp.predict(validation_data_clean[features])

# Evaluate the model
accuracy = accuracy_score(validation_data_clean[target], mlp_y_pred)
print("Neural Network Accuracy:", accuracy)

"""**Remember to submit your submissions CSV FILE on Kaggle!** 40 pts come from your accuracy on the private test data.

Attend section on Thurs 5/11 for a demo of how to uppload submissions to Kaggle. We also have screenshots below (ingore summer and homework number in pictures)

Step 1: See the list of files on Colab

![See Colab Files](https://courses.cs.washington.edu/courses/cse416/22su/homework/hw4/programming/1_colab_see_files.jpg)

Step 2: Download `submission.csv`

![Download Colab File](https://courses.cs.washington.edu/courses/cse416/22su/homework/hw4/programming/2_colab_download_file.jpg)

Step 3: Join the Kaggle competition.

![Join the Kaggle Competition](https://courses.cs.washington.edu/courses/cse416/22su/homework/hw4/programming/3_kaggle_join_competition.jpg)

Step 4: Enusre your team name in Kaggle matches the one at the top of this notebook!

![Check Team Name](https://courses.cs.washington.edu/courses/cse416/22su/homework/hw4/programming/4_kaggle_team_name.jpg)

Step 5: Upload `submission.csv` to Kaggle

![Upload submission.csv](https://courses.cs.washington.edu/courses/cse416/22su/homework/hw4/programming/6_kaggle_upload_submission.jpg)

### **Discussion**

#### **[7 Pts] Training the Models**

**Instructions**: Discuss what models you tried, and what you did to improve your initial predictions. Discuss what hyperparameters you tried, and which hyperparameters seemed important for your final model. Finally, discuss what you are inferring from the above visualiation(s).

Test

I explored a number of different models for this assignment and was impressed at the accuracy that even a simple Decision Tree (>97%) was able to achieve.

Decision Tree:

Hyperparameter tuning: To improve initial predictions, I increased used scikit-learns DecisionClassTreeClassifier, 'class_wieght' parameter. Additionally, I changed the max-depth (started high at 6) to 4 as I believe it was overfitting the training set. Additionally, I started by selecting the features that I thought were most relevant and then progressively added more. I found that using all the featured got me the best consistent results from the dataset.

Random Forest:

Hyperparameter Tuning: I used gridsearch to try and identify the best hyperparameters and iterate throught. As Random Forest is an ensemble method I also choose hyperparametrs which should be more generalizable.
Neural Network:

Light Gradient Boosting Machine:

Hyperparameter Tuning: This gave good results and I was able to test a number of different hyperparameters. I adjusted the learning rate and increased bagging to help generalizability. This led to an increase in the accuracy score against the test data.

Extra- Nueral Network: I tried this out of curiosity, and just in case it was much better than the other models for some reason!

#### **[3 Pts] Feature Selection**

**Instructions**: Discuss what features you used and whether you did some transformations on them. What features seemed important for your final model?

I adjusted the features iteratively, and found that in some cases the features 'viewed' and 'explored' led to better results and seemed important to the final model. However, I got the best results when I included all features that were available and using hyperparameter to adjust.

#### **[5 Pts] Ethical Implications**

**Instructions**: Consider and discuss the ethical implications of using the model you trained. Imagine you were hired to work as a data scientist for an online education platform (exciting, right?). They want to use your model to predict which students they should tailor their course material towards so they can maximize their profits. Their idea is to use the model to help predict which student groups (i.e. from specific countries or certain educational backgrounds) would make them the most money by getting the most participants to complete their paid certificate program. Are there any ethical considerations we should think about before acting on that plan?

Yes, there are several important considerations to take into account. Firstly, the model may inadvertently exacerbate existing biases present in the training data. For example, if students from certain countries or educational backgrounds historically had less access to resources, the model might unfairly disadvantage these groups by predicting lower success rates for them. Therefore, this reinforces inequality as if the model's predictions influence the allocation of resources, it could make existing educational inequalities worse. Students from less advantaged backgrounds might not receive the support they need to succeed, further entrenching educational disparities.
"""
