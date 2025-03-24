import pandas as pd
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
import pickle
import os
import sys

class Preprocessor:
    def __init__(self, fitted_scaler=None, categorical_encoders=None):
        """
        Initialize the preprocessor.
        
        Parameters:
        fitted_scaler: A fitted StandardScaler object (optional)
        categorical_encoders: Dictionary with fitted one-hot encoders for each category (optional)
        """
        self.scaler = fitted_scaler if fitted_scaler else StandardScaler()
        self.categorical_encoders = categorical_encoders if categorical_encoders else {}
        self.numerical_features = ['income', 'age', 'experience', 'current_job_years', 'current_house_years']
        self.categorical_features = ['house_ownership', 'profession', 'state', 'car_ownership', 'marital_Status']
    
    def fit(self, data):
        """
        Fit the preprocessor on training data.
        
        Parameters:
        data: pandas DataFrame containing all required features
        
        Returns:
        self: Fitted preprocessor
        """
        # Fit one-hot encoders for each categorical feature
        for feature in self.categorical_features:
            if feature in data.columns:
                self.categorical_encoders[feature] = pd.get_dummies(data[feature])
        
        # Extract numerical features
        numerical_data = data[self.numerical_features]
        
        # Combine all features for scaling
        encoded_data = self._encode_categories(data)
        
        # Fit the scaler
        self.scaler.fit(encoded_data)
        
        return self
    
    def _encode_categories(self, data):
        """
        Apply one-hot encoding to categorical features.
        
        Parameters:
        data: pandas DataFrame containing categorical features
        
        Returns:
        encoded_data: pandas DataFrame with encoded features
        """
        encoded_dfs = []
        
        # Encode each categorical feature
        for feature in self.categorical_features:
            if feature in data.columns:
                encoded = pd.get_dummies(data[feature])
                
                # Make sure all categories from training are present
                if feature in self.categorical_encoders:
                    # Get all columns from training data
                    expected_columns = self.categorical_encoders[feature].columns
                    
                    # Add missing columns with zeros
                    for col in expected_columns:
                        if col not in encoded.columns:
                            encoded[col] = 0
                    
                    # Ensure column order matches training data
                    encoded = encoded[expected_columns]
                
                encoded_dfs.append(encoded)
        
        # Add numerical features
        numerical_data = data[self.numerical_features]
        encoded_dfs.append(numerical_data)
        
        # Concatenate all features
        return pd.concat(encoded_dfs, axis=1)
    
    def transform(self, data, labels=None, apply_smote=False):
        """
        Transform data using the fitted preprocessor.
        
        Parameters:
        data: pandas DataFrame to transform
        apply_smote: Boolean indicating whether to apply SMOTE oversampling
        labels: Target labels, required if apply_smote is True
        
        Returns:
        transformed_data: Preprocessed numpy array
        transformed_labels: Oversampled labels if apply_smote is True
        """
        # Encode categorical features
        encoded_data = self._encode_categories(data)
        
        # Scale data
        scaled_data = self.scaler.transform(encoded_data)
        
        # Apply SMOTE if requested
        if apply_smote and labels is not None:
            over_sampler = SMOTE(random_state=2)
            oversampled_data, oversampled_labels = over_sampler.fit_resample(scaled_data, labels)
            return oversampled_data, oversampled_labels
        
        return scaled_data
    
    def fit_transform(self, data, labels=None, apply_smote=False):
        """
        Fit the preprocessor and transform the data in one step.
        
        Parameters:
        data: pandas DataFrame to fit and transform
        labels: Target labels, required if apply_smote is True
        apply_smote: Boolean indicating whether to apply SMOTE oversampling
        
        Returns:
        transformed_data: Preprocessed numpy array
        transformed_labels: Oversampled labels if apply_smote is True
        """
        self.fit(data)
        
        if apply_smote and labels is not None:
            return self.transform(data, apply_smote=True, labels=labels)
        
        return self.transform(data)
    
    def save(self, filename):
        """
        Save the preprocessor to a file using pickle.
        
        Parameters:
        filename: Path to save the preprocessor
        """
        with open(filename, 'wb') as f:
            pickle.dump(self, f)
    
    @classmethod
    def load(cls, filename):
        """
        Load a preprocessor from a file.
        
        Parameters:
        filename: Path to the saved preprocessor
        
        Returns:
        preprocessor: Loaded Preprocessor instance
        """
        with open(filename, 'rb') as f:
            return pickle.load(f)

def preprocess_for_prediction(data, preprocessor_path):
    """
    Preprocess new data for prediction using a saved preprocessor.
    
    Parameters:
    data: pandas DataFrame with new data
    preprocessor_path: Path to the saved preprocessor
    
    Returns:
    processed_data: Preprocessed numpy array ready for prediction
    """
    # Load the saved preprocessor
    with open(preprocessor_path, "rb") as f:
        preprocessor = pickle.load(f)
    
    # Transform the data
    processed_data = preprocessor.transform(data)
    return processed_data