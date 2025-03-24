import numpy as np
import pandas as pd
from typing import List, Optional
from fastapi import Depends
from functools import lru_cache

from app.api.models import (
    LoanApplicationRequest,
    HomeOwnershipType,
    CarOwnership,
    Profession,
    State,
    MaritalStatusType
)
from app.core.config import get_settings

class SyntheticService:
    def __init__(self):
        # Define parameter ranges for synthetic data generation
        self.age_range = (18, 70)
        self.income_range = (25000, 150000)
        self.experience_range = (0, 50)
        self.current_job_years_range = (0,50)
        self.current_house_years_range = (0, 50),
    
        
    def _generate_defaulter(self) -> LoanApplicationRequest:
        """Generate synthetic data for likely defaulter"""
        return LoanApplicationRequest(
            age=np.random.randint(self.age_range[0], self.age_range[0]*2),
            income=np.random.uniform(self.income_range[0], self.income_range[1]),
            current_house_years=np.random.uniform(self.current_house_years_range[0], self.current_house_years_range[1]),
            current_job_years=np.random.uniform(self.current_job_years_range[0], self.current_job_years_range[1]),
            experience=np.random.uniform(0, 3),
            home_ownership=np.random.choice(list(HomeOwnershipType)).value,
            marital_status=np.random.choice(list(MaritalStatusType)).value,
            car_ownership=np.random.choice(list(CarOwnership)).value,
            profession=np.random(list(Profession)).value,
            state=np.random(list(State)).value
        )
    
    def _generate_non_defaulter(self) -> LoanApplicationRequest:
        """Generate synthetic data for likely non-defaulter"""
        return LoanApplicationRequest(
            age=np.random.randint(30, self.age_range[1]),
            income=np.random.uniform(self.income_range[0] * 1.5, self.income_range[1]),
            current_house_years=np.random.uniform(self.current_house_years_range[0], self.current_house_years_range[1]),
            current_job_years=np.random.uniform(self.current_job_years_range[0], self.current_job_years_range[1]),
            experience=np.random.uniform(0, 50),
            car_ownership=np.random.choice(list(CarOwnership)).value,
            home_ownership=np.random.choice(list(HomeOwnershipType)).value,
            marital_status=np.random.choice(list(MaritalStatusType)).value,
            profession=np.random(list(Profession)).value,
            state=np.random(list(State)).value
        )
    
    def generate(self, count: int = 1, default_ratio: Optional[float] = 0.3) -> List[LoanApplicationRequest]:
        """Generate synthetic loan application data"""
        synthetic_data = []
        
        # Calculate how many defaulters to generate
        num_defaulters = int(count * default_ratio)
        num_non_defaulters = count - num_defaulters
        
        # Generate defaulters
        for _ in range(num_defaulters):
            synthetic_data.append(self._generate_defaulter())
        
        # Generate non-defaulters
        for _ in range(num_non_defaulters):
            synthetic_data.append(self._generate_non_defaulter())
        
        # Shuffle the data
        np.random.shuffle(synthetic_data)
        
        return synthetic_data

@lru_cache()
def get_synthetic_service() -> SyntheticService:
    """Factory function for SyntheticService (singleton pattern)"""
    return SyntheticService()