import numpy as np
import pandas as pd
from typing import List, Optional
from fastapi import Depends
from functools import lru_cache

from app.api.models import (
    LoanApplicationRequest,
    HomeOwnershipType,
    EducationType,
    MaritalStatusType
)
from app.core.config import get_settings

class SyntheticService:
    def __init__(self):
        # Define parameter ranges for synthetic data generation
        self.age_range = (18, 70)
        self.income_range = (25000, 150000)
        self.loan_amount_range = (5000, 100000)
        self.loan_terms = [12, 24, 36, 48, 60]
        self.credit_score_range = (400, 850)
        self.employment_years_range = (0, 25)
        self.debt_to_income_range = (0.1, 0.6)
        
    def _generate_defaulter(self) -> LoanApplicationRequest:
        """Generate synthetic data for likely defaulter"""
        return LoanApplicationRequest(
            age=np.random.randint(self.age_range[0], self.age_range[1]),
            income=np.random.uniform(self.income_range[0], self.income_range[0] * 2),
            loan_amount=np.random.uniform(self.loan_amount_range[0] * 2, self.loan_amount_range[1]),
            loan_term=np.random.choice(self.loan_terms),
            credit_score=np.random.randint(self.credit_score_range[0], 650),
            employment_years=np.random.uniform(0, 3),
            debt_to_income=np.random.uniform(0.4, self.debt_to_income_range[1]),
            home_ownership=np.random.choice([HomeOwnershipType.RENT, HomeOwnershipType.MORTGAGE]).value,
            education=np.random.choice(list(EducationType)).value,
            marital_status=np.random.choice(list(MaritalStatusType)).value
        )
    
    def _generate_non_defaulter(self) -> LoanApplicationRequest:
        """Generate synthetic data for likely non-defaulter"""
        return LoanApplicationRequest(
            age=np.random.randint(30, self.age_range[1]),
            income=np.random.uniform(self.income_range[0] * 1.5, self.income_range[1]),
            loan_amount=np.random.uniform(self.loan_amount_range[0], self.loan_amount_range[1] * 0.7),
            loan_term=np.random.choice(self.loan_terms),
            credit_score=np.random.randint(650, self.credit_score_range[1]),
            employment_years=np.random.uniform(3, self.employment_years_range[1]),
            debt_to_income=np.random.uniform(self.debt_to_income_range[0], 0.4),
            home_ownership=np.random.choice([HomeOwnershipType.OWN, HomeOwnershipType.MORTGAGE]).value,
            education=np.random.choice([EducationType.BACHELOR, EducationType.MASTER, EducationType.PHD]).value,
            marital_status=np.random.choice(list(MaritalStatusType)).value
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