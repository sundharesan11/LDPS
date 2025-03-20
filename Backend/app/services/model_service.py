import pickle
import numpy as np
import tensorflow as tf
from fastapi import Depends
from typing import Dict, List, Tuple
import os
from functools import lru_cache

from app.api.models import LoanApplicationRequest, ModelPrediction
from app.utils.preprocessing import preprocess_application
from app.core.config import get_settings

class ModelService:
    def __init__(self, model_dir: str):
        self.model_dir = model_dir
        self.model1 = None  # Random Forest
        self.model2 = None  # XGBoost
        self.model3 = None  # Neural Network
        self.feature_names = None
        self._load_models()
    
    def _load_models(self):
        """Load all three models from saved files"""
        try:
            # Load model 1 (Random Forest)
            with open(os.path.join(self.model_dir, "model1.pkl"), "rb") as f:
                self.model1 = pickle.load(f)
            
            # Load model 2 (XGBoost)
            with open(os.path.join(self.model_dir, "model2.pkl"), "rb") as f:
                self.model2 = pickle.load(f)
            
            # Load model 3 (Neural Network)
            self.model3 = tf.keras.models.load_model(
                os.path.join(self.model_dir, "model3.h5")
            )
            
            # Load feature names if available
            try:
                with open(os.path.join(self.model_dir, "feature_names.pkl"), "rb") as f:
                    self.feature_names = pickle.load(f)
            except:
                self.feature_names = None
                
        except Exception as e:
            raise Exception(f"Failed to load models: {str(e)}")
    
    def predict(self, application: LoanApplicationRequest) -> ModelPrediction:
        """Make prediction using all models and ensemble their results"""
        # Preprocess the application data
        X = preprocess_application(application, self.feature_names)
        
        # Get predictions from each model
        pred1 = int(self.model1.predict(X)[0])
        pred2 = int(self.model2.predict(X)[0])
        
        # For neural network, get raw probability and convert to binary
        prob3 = float(self.model3.predict(X)[0][0])
        pred3 = int(prob3 > 0.5)
        
        # Ensemble prediction (simple majority vote)
        predictions = [pred1, pred2, pred3]
        ensemble_pred = max(set(predictions), key=predictions.count)
        
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

@lru_cache()
def get_model_service() -> ModelService:
    """Factory function for ModelService (singleton pattern)"""
    settings = get_settings()
    return ModelService(model_dir=settings.MODEL_DIR)