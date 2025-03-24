from pydantic_settings import BaseSettings
from typing import List, ClassVar
import os


class Settings(BaseSettings):
    PROJECT_NAME: str = "Loan Default Prediction"
    PROJECT_DESCRIPTION: str = "An Application to predict loan defaulters"
    DEBUG: bool = True
    PROJECT_VERSION: str = "v1"
    
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000"
    ]
    # Get the absolute path to the ml_models directory
    # BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    BASE_DIR: ClassVar[str] = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    MODEL_DIR: str = os.path.join(BASE_DIR, "ml_models")
    MODEL_1_PATH: str = "random_forest_model.pkl"
    MODEL_2_PATH: str = "xgb_model.pkl"
    MODEL_3_PATH: str = "neural_network_model.h5"
    PREPROCESSOR_PATH: str = "preprocessor.pkl"

    class Config:
        env_file = ".env"  # Load from a .env file

# Global function to get settings
def get_settings():
    return Settings()
