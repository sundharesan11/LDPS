from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    PROJECT_NAME: str = "Loan Default Prediction"
    PROJECT_DESCRIPTION: str = "An Application to predict loan defaulters"
    DEBUG: bool = True
    PROJECT_VERSION: str = "v1"
    
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000"
    ]
    
    MODEL_1_PATH: str = rf"Backend\ml_models\random_forest_model.pkl"
    MODEL_2_PATH: str = rf"Backend\ml_models\xgboost_model.pkl"
    MODEL_3_PATH: str = rf"ml_models\model3.h5"

    class Config:
        env_file = ".env"  # Load from a .env file

# Global function to get settings
def get_settings():
    return Settings()
