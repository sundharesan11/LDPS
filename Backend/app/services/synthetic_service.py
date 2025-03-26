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
    # MaritalStatusType
)
from app.core.config import get_settings

class SyntheticService:
    def __init__(self):
        # Define parameter ranges for synthetic data generation
        self.age_range = (18, 70)
        self.income_range = (25000, 150000)
        self.experience_range = (0, 50)
        self.current_job_years_range = (0, 50)
        self.current_house_years_range = (0, 50)
    
    def _generate_defaulter(self, index: int) -> LoanApplicationRequest:
        """Generate synthetic data for likely defaulter"""
        # Generate data
        data = LoanApplicationRequest(
            age=np.random.randint(self.age_range[0], self.age_range[0]*2),
            income=np.random.uniform(self.income_range[0], self.income_range[1]),
            current_house_years=int(np.random.randint(self.current_house_years_range[0], self.current_house_years_range[1])),
            current_job_years=int(np.random.randint(self.current_job_years_range[0], self.current_job_years_range[1])),
            experience=int(np.random.randint(0, 3)),
            home_ownership=np.random.choice([e.value for e in HomeOwnershipType]),
            car_ownership=np.random.choice([e.value for e in CarOwnership]),
            profession=np.random.choice([e.value for e in Profession]),
            state=np.random.choice([e.value for e in State])
        )
        print(f"\nDefaulter Entry #{index + 1}:")
        print(f"Age: {data.age}")
        print(f"Income: ₹{data.income:,.2f}")
        print(f"Experience: {data.experience} years")
        print(f"Current Job Years: {data.current_job_years}")
        print(f"Current House Years: {data.current_house_years}")
        print(f"Home Ownership: {data.home_ownership}")
        print(f"Car Ownership: {data.car_ownership}")
        print(f"Profession: {data.profession}")
        print(f"State: {data.state}")
        print("-" * 50)
        return data
    
    def _generate_non_defaulter(self, index: int) -> LoanApplicationRequest:
        """Generate synthetic data for likely non-defaulter"""
        # Generate data
        data = LoanApplicationRequest(
            age=np.random.randint(30, self.age_range[1]),
            income=np.random.uniform(self.income_range[0] * 1.5, self.income_range[1]),
            current_house_years=int(np.random.randint(self.current_house_years_range[0], self.current_house_years_range[1])),
            current_job_years=int(np.random.randint(self.current_job_years_range[0], self.current_job_years_range[1])),
            experience=int(np.random.randint(5, 50)),
            car_ownership=np.random.choice([e.value for e in CarOwnership]),
            home_ownership=np.random.choice([e.value for e in HomeOwnershipType]),
            profession=np.random.choice([e.value for e in Profession]),
            state=np.random.choice([e.value for e in State])
        )
        print(f"\nNon-Defaulter Entry #{index + 1}:")
        print(f"Age: {data.age}")
        print(f"Income: ₹{data.income:,.2f}")
        print(f"Experience: {data.experience} years")
        print(f"Current Job Years: {data.current_job_years}")
        print(f"Current House Years: {data.current_house_years}")
        print(f"Home Ownership: {data.home_ownership}")
        print(f"Car Ownership: {data.car_ownership}")
        print(f"Profession: {data.profession}")
        print(f"State: {data.state}")
        print("-" * 50)
        return data
    
    def generate(self, count: int = 1, default_ratio: Optional[float] = 0.3) -> List[LoanApplicationRequest]:
        """Generate synthetic loan application data"""
        print(f"\nGenerating {count} synthetic records with {default_ratio*100:.1f}% defaulters")
        print("=" * 50)
        
        synthetic_data = []
        
        # Calculate how many defaulters to generate
        num_defaulters = int(count * default_ratio)
        num_non_defaulters = count - num_defaulters
        
        print(f"Generating {num_defaulters} defaulters and {num_non_defaulters} non-defaulters")
        print("=" * 50)
        
        print("\nDEFAULTER ENTRIES:")
        print("=" * 50)
        # Generate defaulters
        for i in range(num_defaulters):
            synthetic_data.append(self._generate_defaulter(i))
        
        print("\nNON-DEFAULTER ENTRIES:")
        print("=" * 50)
        # Generate non-defaulters
        for i in range(num_non_defaulters):
            synthetic_data.append(self._generate_non_defaulter(i))
        
        # Shuffle the data
        np.random.shuffle(synthetic_data)
        
        # Print final summary
        print("\nSUMMARY:")
        print("=" * 50)
        print(f"Total entries generated: {len(synthetic_data)}")
        print(f"Defaulters: {num_defaulters}")
        print(f"Non-defaulters: {num_non_defaulters}")
        print("=" * 50)
        
        return synthetic_data

@lru_cache()
def get_synthetic_service() -> SyntheticService:
    """Factory function for SyntheticService (singleton pattern)"""
    return SyntheticService()