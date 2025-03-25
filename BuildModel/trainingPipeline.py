import sys
import os
import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import roc_curve, roc_auc_score
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import load_model
from sklearn.metrics import roc_curve, auc
from bm_preprocessing import Preprocessor, preprocess_for_prediction
from sklearn.model_selection import cross_val_score, train_test_split, StratifiedKFold


def rf_train_pipeline(data_train, y_train, data_test, y_test):
    # Initialize the preprocessor
    preprocessor = Preprocessor()
    
    # Fit and transform the training data with SMOTE
    trainData, trainLabels = preprocessor.fit_transform(data_train, y_train, apply_smote=True)
    
    # Transform the test data with SMOTE
    testData, testLabels = preprocessor.transform(data_test, y_test, apply_smote=True)
    
    # Save the preprocessor for later use
    with open("preprocessor.pkl", "wb") as f:
        pickle.dump(preprocessor, f)
    # preprocessor.save("preprocessor.pkl")
    
    rf_optimum_params = {'criterion': 'gini', 'max_depth': 50, 'n_estimators': 800}
    
    rf_clf = RandomForestClassifier(
        n_estimators=rf_optimum_params['n_estimators'], 
        criterion=rf_optimum_params['criterion'], 
        max_depth=rf_optimum_params['max_depth'],  
        random_state=42,
        n_jobs=-1
    )
    
    # Train the model
    rf_clf.fit(trainData, trainLabels)

    print("Best AUC score on optimum parameters is: {}"\
                                    .format( round(roc_auc_score(testLabels,rf_clf.predict_proba(testData)[:, 1]), 5)))
    
    # Save the model
    with open("random_forest_model.pkl", "wb") as f:
        pickle.dump(rf_clf, f)
    
    return preprocessor, rf_clf


def xgb_train_pipeline(data_train, y_train, data_test, y_test):
    # Initialize the preprocessor
    preprocessor = Preprocessor()
    
    # Fit and transform the training data with SMOTE
    trainData, trainLabels = preprocessor.fit_transform(data_train, y_train, apply_smote=True)
    
    # Transform the test data with SMOTE
    testData, testLabels = preprocessor.transform(data_test, y_test, apply_smote=True)
    
    # Save the preprocessor for later use
    with open("preprocessor.pkl", "wb") as f:
        pickle.dump(preprocessor, f)

    optimum_params={'booster': 'gbtree', 'eval_metric': 'auc', 'max_depth': 50, 'n_estimators': 800, 'objective': 'binary:logistic', 'predictor': 'cpu_predictor', 'tree_method': 'hist'}

    xgb_clf = XGBClassifier(n_estimators= optimum_params['n_estimators'],
                                max_depth=optimum_params['max_depth'],
                                eval_metric='auc',
                                random_state=42,
                                n_jobs= -1,
                                verbosity = 1
                                )
    xgb_clf.fit(trainData, trainLabels)
    print("Best AUC score on optimum parameters is: {}"\
                                    .format( round(roc_auc_score(testLabels,xgb_clf.predict_proba(testData)[:, 1]), 5)))

    # Save the model
    with open("xgb_model.pkl", "wb") as f:
        pickle.dump(xgb_clf, f)
    
    return preprocessor, xgb_clf

def neuralnetwork(data_train, y_train, data_test, y_test):

    preprocessor = Preprocessor()
    
    # Fit and transform the training data with SMOTE
    trainData, trainLabels = preprocessor.fit_transform(data_train, y_train, apply_smote=True)
    
    # Transform the test data with SMOTE
    testData, testLabels = preprocessor.transform(data_test, y_test, apply_smote=True)

    with open("preprocessor.pkl", "wb") as f:
        pickle.dump(preprocessor, f)

    nn_model = Sequential([
        Dense(128, activation='relu', input_shape=(trainData.shape[1],)),
        Dropout(0.3),
        Dense(64, activation='relu'),
        Dropout(0.2),
        Dense(32, activation='relu'),
        Dense(1, activation='sigmoid')  # Output layer for binary classification
    ])

    # Compile the model
    nn_model.compile(optimizer=Adam(learning_rate=0.001),
                    loss='binary_crossentropy',
                    metrics=['AUC'])

    # Train the model
    nn_model.fit(trainData, trainLabels, validation_data=(testData, testLabels), epochs=10, batch_size=32)

    test_loss, test_auc = nn_model.evaluate(testData, testLabels)
    print(f"Test Loss: {test_loss:.4f}")
    print(f"Test AUC-ROC: {test_auc:.4f}")

    nn_model.save("neural_network_model.h5")

    return nn_model

def predict_with_pipeline(new_data):
    """
    Process new data and make predictions using the saved model.
    
    Parameters:
    new_data: pandas DataFrame with the same structure as training data
    
    Returns:
    predictions: Model predictions
    """
    # Preprocess the new data
    processed_data = preprocess_for_prediction(new_data, preprocessor_path="preprocessor.pkl")
    # Load the saved model
    with open("random_forest_model.pkl", "rb") as f:
        model1 = pickle.load(f)
    # Make predictions
    prediction1 = model1.predict(processed_data)
    
    with open("xgb_model.pkl", "rb") as f:
        model2 = pickle.load(f)
    # Make predictions
    prediction2 = model2.predict(processed_data)

    
    nn_loaded = load_model("neural_network_model.h5")
    prediction3 = (nn_loaded.predict(processed_data) >= 0.5).astype(int)

    return prediction1, prediction2, prediction3

# Example of how you'd use this with a single new record
def predict_single_record():
    
    new_data = pd.DataFrame({
        
        'profession': ['engineer'],
        'house_ownership': ['rented'],
        'state': ['Kerala'],
        'income': [750000],
        'age': [35],
        'current_house_years': [2],
        'experience': [10],
        'current_job_years': [5],
        'marital_status': ['married'],
        'car_ownership': ['yes']
    })
    prediction1, prediction2, prediction3 = predict_with_pipeline(new_data)
    
    return prediction1, prediction2, prediction3


if __name__ == '__main__':

    data = pd.read_csv("processed_training_data.csv")

    y_true=data['risk_flag']
    #using stratify=y_true to have equal number of datapoints both in train and test datasets 
    data_train, data_test, y_train,  y_test = train_test_split(data.drop('risk_flag', axis=1), y_true, 
                                                            stratify=y_true, test_size=0.3)
    data_train=data_train.reset_index(drop=True)
    data_test=data_test.reset_index(drop=True)
    y_train=y_train.reset_index(drop=True)
    y_test=y_test.reset_index(drop=True)

    # preprocessor, model = rf_train_pipeline(data_train, y_train, data_test, y_test)
    preprocessor, model = xgb_train_pipeline(data_train, y_train, data_test, y_test)
    # nn_model = neuralnetwork(data_train, y_train, data_test, y_test)

    a, b, c = predict_single_record()
    print(a, b, c)
    pass
