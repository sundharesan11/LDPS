from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.api.models import (
    LoanApplicationRequest,
    ModelPrediction,
    SyntheticGenerationRequest
)
from app.services.model_service import ModelService, get_model_service
from app.services.synthetic_service import SyntheticService, get_synthetic_service

router = APIRouter()

@router.post("/predict", response_model=ModelPrediction)
async def predict_loan_default(
    application: LoanApplicationRequest,
    model_service: ModelService = Depends(get_model_service)
):
    """
    Predict loan default probability using the ensemble of models
    """
    try:
        prediction = model_service.predict(application)
        return prediction
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction error: {str(e)}"
        )

@router.post("/generate-synthetic", response_model=List[LoanApplicationRequest])
async def generate_synthetic_data(
    request: SyntheticGenerationRequest,
    synthetic_service: SyntheticService = Depends(get_synthetic_service)
):
    """
    Generate synthetic loan application data
    """
    try:
        synthetic_data = synthetic_service.generate(
            count=request.count,
            default_ratio=request.default_ratio
        )
        return synthetic_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Synthetic data generation error: {str(e)}"
        )

@router.post("/predict-synthetic", response_model=List[ModelPrediction])
async def predict_with_synthetic(
    request: SyntheticGenerationRequest,
    synthetic_service: SyntheticService = Depends(get_synthetic_service),
    model_service: ModelService = Depends(get_model_service)
):
    """
    Generate synthetic data and predict loan default in one step
    """
    try:
        # Generate synthetic data
        synthetic_data = synthetic_service.generate(
            count=request.count,
            default_ratio=request.default_ratio
        )
        
        # Make predictions
        predictions = [model_service.predict(application) for application in synthetic_data]
        
        # Return both synthetic data and predictions
        return predictions
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Synthetic prediction error: {str(e)}"
        )