import pickle
import numpy as np
import tensorflow as tf
from fastapi import Depends, HTTPException, status
from typing import Dict, List, Tuple
import os
from functools import lru_cache
import pandas as pd
from app.api.models import LoanApplicationRequest, ModelPrediction
from app.utils.data_preprocessing import Preprocessor
from app.core.config import get_settings

class ModelService:
    def __init__(self, model_dir: str):
        self.model_dir = model_dir
        self.model1 = None  # Random Forest
        self.model2 = None  # XGBoost
        self.model3 = None  # Neural Network
        self.preprocessor = None  # Preprocessor
        self.feature_names = None
        self._load_models()
    
    def _load_models(self):
        """Load all three models from saved files"""
        try:
            # Load model 1 (Random Forest)
            rf_path = os.path.join(self.model_dir, "random_forest_model.pkl")
            print(f"Loading Random Forest from: {rf_path}")
            with open(rf_path, "rb") as f:
                self.model1 = pickle.load(f)
                print("Random Forest loaded successfully")
            
            # Load model 2 (XGBoost)
            xgb_path = os.path.join(self.model_dir, "xgb_model.pkl")
            print(f"Loading XGBoost from: {xgb_path}")
            with open(xgb_path, "rb") as f:
                self.model2 = pickle.load(f)
                print("XGBoost loaded successfully")
            
            # Load model 3 (Neural Network)
            nn_path = os.path.join(self.model_dir, "neural_network_model.h5")
            print(f"Loading Neural Network from: {nn_path}")
            self.model3 = tf.keras.models.load_model(nn_path)
            print("Neural Network loaded successfully")

            # Load preprocessor
            preprocessor_path = os.path.join(self.model_dir, "preprocessor.pkl")
            print(f"Loading preprocessor from: {preprocessor_path}")
            try:
                with open(preprocessor_path, "rb") as f:
                    # Try to load with custom unpickler
                    class CustomUnpickler(pickle.Unpickler):
                        def find_class(self, module, name):
                            if module == "preprocessing":
                                module = "app.utils.data_preprocessing"
                            return super().find_class(module, name)
                    
                    self.preprocessor = CustomUnpickler(f).load()
                print("Preprocessor loaded successfully")
            except Exception as e:
                print(f"Error loading preprocessor: {str(e)}")
                print("Creating new preprocessor with default settings")
                self.preprocessor = Preprocessor()
                # Save the new preprocessor
                with open(preprocessor_path, "wb") as f:
                    pickle.dump(self.preprocessor, f)
                print("New preprocessor created and saved successfully")
            
            # Load feature names if available
            try:
                features_path = os.path.join(self.model_dir, "feature_names.pkl")
                print(f"Loading feature names from: {features_path}")
                with open(features_path, "rb") as f:
                    self.feature_names = pickle.load(f)
                    print("Feature names loaded successfully")
            except Exception as e:
                print(f"Warning: Could not load feature names: {str(e)}")
                self.feature_names = None
                
        except Exception as e:
            error_msg = f"Failed to load models: {str(e)}"
            print(error_msg)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=error_msg
            )
    
    def _preprocess_data(self, application: LoanApplicationRequest):
        """Preprocess the application data"""
        try:
            # Convert Pydantic model to DataFrame
            data_dict = application.dict()
            # Convert enum values to their string representations
            for key, value in data_dict.items():
                if hasattr(value, 'value'):
                    data_dict[key] = value.value
            
            df = pd.DataFrame([data_dict])
            
            # Rename columns to match expected format
            df = df.rename(columns={
                'home_ownership': 'house_ownership'
            })
            
            # Transform the data
            return self.preprocessor.transform(df)
        except Exception as e:
            error_msg = f"Preprocessing error: {str(e)}"
            print(error_msg)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=error_msg
            )
    
    def predict(self, application: LoanApplicationRequest) -> ModelPrediction:
        """Make prediction using all models and ensemble their results"""
        try:
            print(f"Application data: {application}")
            
            # Convert Pydantic model to DataFrame
            data_dict = application.dict()
            # Convert enum values to their string representations
            for key, value in data_dict.items():
                if hasattr(value, 'value'):
                    data_dict[key] = value.value
            
            df = pd.DataFrame([data_dict])
            
            # Rename columns to match expected format
            df = df.rename(columns={
                'home_ownership': 'house_ownership',
                'marital_status': 'marital_Status'
            })
            
            # Use the already loaded preprocessor
            print("Using preprocessor to transform data")
            X = self.preprocessor.transform(df)
            print(f"Preprocessed data shape: {X.shape}")
            
            # Get predictions from each model
            pred1 = int(self.model1.predict(X)[0])
            print(f"Random Forest prediction: {pred1}")
            
            pred2 = int(self.model2.predict(X)[0])
            print(f"XGBoost prediction: {pred2}")
            
            # For neural network, get raw probability and convert to binary
            prob3 = float(self.model3.predict(X)[0][0])
            pred3 = int(prob3 > 0.5)
            print(f"Neural Network prediction: {pred3} (probability: {prob3})")
            
            # Ensemble prediction (simple majority vote)
            predictions = [pred1, pred2, pred3]
            ensemble_pred = max(set(predictions), key=predictions.count)
            print(f"Ensemble prediction: {ensemble_pred}")
            
            # Get feature importance from model 1 if available
            feature_importance = None
            if hasattr(self.model1, "feature_importances_") and self.feature_names:
                importance = self.model1.feature_importances_
                feature_importance = {
                    name: float(imp) for name, imp in
                    zip(self.feature_names, importance)
                }
            
            return ModelPrediction(
                model1_prediction=pred1,
                model2_prediction=pred2,
                model3_prediction=pred3,
                ensemble_prediction=ensemble_pred,
                default_probability=prob3,
                feature_importance=feature_importance
            )
            
        except Exception as e:
            error_msg = f"Prediction error: {str(e)}"
            print(error_msg)
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=error_msg
            )

@lru_cache()
def get_model_service() -> ModelService:
    """Factory function for ModelService (singleton pattern)"""
    settings = get_settings()
    return ModelService(model_dir=settings.MODEL_DIR)