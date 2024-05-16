import numpy as np
import pandas as pd
import math
from sklearn.linear_model import LinearRegression
from sklearn import tree 
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.experimental import enable_iterative_imputer  # noqa
from sklearn.impute import IterativeImputer
from sklearn.metrics import r2_score
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor 


def dropNA(df, top_9=False):
    """
    Prepare the data for training, deal with NaNs. I think we also need to drop the 2014 years?
    """
    
    # remove commas in numeric columns
    for feature in df.columns:
        df[feature] = df[feature].apply(lambda x: x.replace(',', '') if isinstance(x, str) else x)

    # force numeric 
    numeric_cols = ['Cost Min Basket', 'Goat Price', 'Goat to Cereal', 'Maize Price', 'Rice Price', 'Sorghum Price', 'Wage Price', 'Arrivals']
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric)

    # make categorical columns
    df = df.astype({"Region": 'category', "District": 'category', "Month": 'category'})

    # drop less useful columns
    if top_9:
        keep_cols = ['Arrivals', 'Region', 'District', 'Month', 'Year', 'Rainfall', 'Conflict Fatalities', 'Conflict Incidents', 'Water Price', 'Goat Price']
        df = df[keep_cols]
        df = df.dropna()
    else:
        columns = ['Region', 'District','CDI','Month','Year','NDVI','Rainfall','Water Price',
            'Conflict Fatalities','Conflict Incidents','Cholera Deaths',
            'Cholera Cases','Malaria','Measles','Cost Min Basket',
            'Goat Price','Goat to Cereal','Maize Price','Rice Price',
            'Sorghum Price','Wage Price','Wage to Cereal', 'Arrivals']
        df = df[columns]
        df = df.dropna()
    
    # encode data that is not numerical
    encoder = LabelEncoder()
    encoder.fit(df['Region'])
    df['Region'] = encoder.transform(df['Region'])
    encoder.fit(df['District'])
    df['District'] = encoder.transform(df['District'])
    encoder.fit(df['Month'])
    df['Month'] = encoder.transform(df['Month'])

    return df

def impute(df, top_9=False):
    """
    Prepare the data for training, impute NaNs. I think we also need to drop the 2014 years?
    """
    
    # encode data that is not numerical
    encoder = LabelEncoder()
    encoder.fit(df['Region'])
    df['Region'] = encoder.transform(df['Region'])
    encoder.fit(df['District'])
    df['District'] = encoder.transform(df['District'])
    encoder.fit(df['Month'])
    df['Month'] = encoder.transform(df['Month'])
    
    # turn string numbers into floats
    features = ['CDI','Month','Year','NDVI','Rainfall','Water Price',
            'Conflict Fatalities','Conflict Incidents','Cholera Deaths',
            'Cholera Cases','Malaria','Measles','Cost Min Basket',
            'Goat Price','Goat to Cereal','Maize Price','Rice Price',
            'Sorghum Price','Wage Price','Wage to Cereal', 'Departures','Arrivals']
    for feature in features:
        df[feature] = df[feature].apply(lambda x: x.replace(',', '') if isinstance(x, str) else x)
    
    # actually impute
    imp = IterativeImputer(max_iter=10, random_state=0)
    array_imp = imp.fit_transform(df)
    df = pd.DataFrame(array_imp, columns=df.columns) 

    # drop less useful columns
    if top_9:
        keep_cols = ['Arrivals', 'Region', 'District', 'Month', 'Year', 'Rainfall', 'Conflict Fatalities', 'Conflict Incidents', 'Water Price', 'Goat Price']
        df = df[keep_cols]
    else:
        columns = ['Region', 'District','CDI','Month','Year','NDVI','Rainfall','Water Price',
            'Conflict Fatalities','Conflict Incidents','Cholera Deaths',
            'Cholera Cases','Malaria','Measles','Cost Min Basket',
            'Goat Price','Goat to Cereal','Maize Price','Rice Price',
            'Sorghum Price','Wage Price','Wage to Cereal', 'Arrivals']
        df = df[columns]
        
    return df


def classification_accuracy(y_true, y_pred):
    """
    Return the classification accuracy of the predicted labels.
    """
    if len(y_true) != len(y_pred):
        raise ValueError("Arrays must be of equal length")

    accuracy = np.sum(y_true == y_pred) / len(y_true)
    return accuracy


def evaluate_LR(X_train, y_train, X_test, y_test):
    LR = LinearRegression()
    LR.fit(X_train, y_train)
    
    # evaluate model based on bins
    true_bins = pd.cut(y_test['Arrivals'], bins=[float('-inf'), 1000, 5000, float('inf')], labels=[1, 2, 3], right=False)
    preds_bin = np.digitize(LR.predict(X_test), bins=[float('-inf'), 1000, 5000, float('inf')], right=False).flatten()

    score = LR.score(X_test, y_test)
    rmse = math.sqrt(mean_squared_error(LR.predict(X_test), y_test))
    accuracy = classification_accuracy(true_bins, preds_bin)
    
    print(f'score: {score}')
    print(f'rmse: {rmse}')
    print(f'classification accuracy: {accuracy}')
    print("\n")


def evaluate_RF(X_train, y_train, X_test, y_test):
    RF = RandomForestRegressor()
    RF.fit(X_train, y_train.ravel())

    # evaluate model based on bins
    true_bins = pd.cut(y_test['Arrivals'], bins=[0, 1000, 5000, float('inf')], labels=[1, 2, 3], right=False)
    preds_bin = np.digitize(RF.predict(X_test), bins=[0, 1000, 5000, float('inf')], right=False).flatten()
    
    score = RF.score(X_test, y_test)
    rmse = math.sqrt(mean_squared_error(RF.predict(X_test), y_test))
    accuracy = classification_accuracy(true_bins, preds_bin)
    
    print(f'score: {score}')
    print(f'rmse: {rmse}')
    print(f'classification accuracy: {accuracy}')
    print("\n")


def evaluate_DT(X_train, y_train, X_test, y_test):
    DT = DecisionTreeRegressor()
    DT.fit(X_train, y_train)

    # evaluate model based on bins
    true_bins = pd.cut(y_test['Arrivals'], bins=[0, 1000, 5000, float('inf')], labels=[1, 2, 3], right=False)
    preds_bin = np.digitize(DT.predict(X_test), bins=[0, 1000, 5000, float('inf')], right=False).flatten()

    score = DT.score(X_test, y_test)
    rmse = math.sqrt(mean_squared_error(DT.predict(X_test), y_test))
    accuracy = classification_accuracy(true_bins, preds_bin)
    
    print(f'score: {score}')
    print(f'rmse: {rmse}')
    print(f'classification accuracy: {accuracy}')
    print("\n")