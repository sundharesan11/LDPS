from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Union
from enum import Enum

class HomeOwnershipType(str, Enum):
    OWN = "OWN"
    RENT = "RENT"
    MORTGAGE = "MORTGAGE"

class EducationType(str, Enum):
    HIGH_SCHOOL = "HIGH_SCHOOL"
    BACHELOR = "BACHELOR"
    MASTER = "MASTER"
    PHD = "PHD"

class MaritalStatusType(str, Enum):
    SINGLE = "SINGLE"
    MARRIED = "MARRIED"
    DIVORCED = "DIVORCED"

class LoanApplicationRequest(BaseModel):
    age: int = Field(..., ge=18, le=100)
    income: float = Field(..., ge=0)
    loan_amount: float = Field(..., gt=0)
    loan_term: int = Field(..., gt=0)
    credit_score: int = Field(..., ge=300, le=850)
    employment_years: float = Field(..., ge=0)
    debt_to_income: float = Field(..., ge=0, le=1)
    home_ownership: HomeOwnershipType
    education: EducationType
    marital_status: MaritalStatusType

    class Config:
        schema_extra = {
            "example": {
                "age": 35,
                "income": 60000,
                "loan_amount": 15000,
                "loan_term": 36,
                "credit_score": 720,
                "employment_years": 5.5,
                "debt_to_income": 0.35,
                "home_ownership": "MORTGAGE",
                "education": "BACHELOR",
                "marital_status": "MARRIED"
            }
        }

class ModelPrediction(BaseModel):
    model1_prediction: int
    model2_prediction: int
    model3_prediction: int
    ensemble_prediction: int
    default_probability: float
    feature_importance: Optional[Dict[str, float]] = None

class SyntheticGenerationRequest(BaseModel):
    count: int = Field(1, ge=1, le=100)
    default_ratio: Optional[float] = Field(0.3, ge=0, le=1)