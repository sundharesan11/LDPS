from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Union
from enum import Enum

class HomeOwnershipType(str, Enum):
    OWN = "owned"
    RENT = "rented"
    MORTGAGE = "noown_norent"

class CarOwnership(str, Enum):
    YES = "yes"
    NO = "no"

class MaritalStatusType(str, Enum):
    SINGLE = "single"
    MARRIED = "married"


class Profession(str, Enum):
    MECHANICAL_ENGINEER = "Mechanical_engineer"
    SOFTWARE_DEVELOPER = "Software_Developer"
    TECHNICAL_WRITER = "Technical_writer"
    CIVIL_SERVANT = "Civil_servant"
    LIBRARIAN = "Librarian"
    ECONOMIST = "Economist"
    FLIGHT_ATTENDANT = "Flight_attendant"
    ARCHITECT = "Architect"
    DESIGNER = "Designer"
    PHYSICIAN = "Physician"
    FINANCIAL_ANALYST = "Financial_Analyst"
    AIR_TRAFFIC_CONTROLLER = "Air_traffic_controller"
    POLITICIAN = "Politician"
    POLICE_OFFICER = "Police_officer"
    ARTIST = "Artist"
    SURVEYOR = "Surveyor"
    DESIGN_ENGINEER = "Design_Engineer"
    CHEMICAL_ENGINEER = "Chemical_engineer"
    HOTEL_MANAGER = "Hotel_Manager"
    DENTIST = "Dentist"
    COMEDIAN = "Comedian"
    BIOMEDICAL_ENGINEER = "Biomedical_Engineer"
    GRAPHIC_DESIGNER = "Graphic_Designer"
    COMPUTER_HARDWARE_ENGINEER = "Computer_hardware_engineer"
    PETROLEUM_ENGINEER = "Petroleum_Engineer"
    SECRETARY = "Secretary"
    COMPUTER_OPERATOR = "Computer_operator"
    CHARTERED_ACCOUNTANT = "Chartered_Accountant"
    TECHNICIAN = "Technician"
    MICROBIOLOGIST = "Microbiologist"
    FASHION_DESIGNER = "Fashion_Designer"
    AVIATOR = "Aviator"
    PSYCHOLOGIST = "Psychologist"
    MAGISTRATE = "Magistrate"
    LAWYER = "Lawyer"
    FIREFIGHTER = "Firefighter"
    ENGINEER = "Engineer"
    OFFICIAL = "Official"
    ANALYST = "Analyst"
    GEOLOGIST = "Geologist"
    DRAFTER = "Drafter"
    STATISTICIAN = "Statistician"
    WEB_DESIGNER = "Web_designer"
    CONSULTANT = "Consultant"
    CHEF = "Chef"
    ARMY_OFFICER = "Army_officer"
    SURGEON = "Surgeon"
    SCIENTIST = "Scientist"
    CIVIL_ENGINEER = "Civil_engineer"
    INDUSTRIAL_ENGINEER = "Industrial_Engineer"
    TECHNOLOGY_SPECIALIST = "Technology_specialist"

class State(str, Enum):
    MADHYA_PRADESH = "madhya pradesh"
    MAHARASHTRA = "maharashtra"
    KERALA = "kerala"
    ODISHA = "odisha"
    TAMIL_NADU = "tamil nadu"
    GUJARAT = "gujarat"
    RAJASTHAN = "rajasthan"
    TELANGANA = "telangana"
    BIHAR = "bihar"
    ANDHRA_PRADESH = "andhra pradesh"
    WEST_BENGAL = "west bengal"
    HARYANA = "haryana"
    PUDUCHERRY = "puducherry"
    KARNATAKA = "karnataka"
    UTTAR_PRADESH = "uttar pradesh"
    HIMACHAL_PRADESH = "himachal pradesh"
    PUNJAB = "punjab"
    TRIPURA = "tripura"
    UTTARAKHAND = "uttarakhand"
    JHARKHAND = "jharkhand"
    MIZORAM = "mizoram"
    ASSAM = "assam"
    JAMMU_AND_KASHMIR = "jammu and kashmir"
    DELHI = "delhi"
    CHHATTISGARH = "chhattisgarh"
    CHANDIGARH = "chandigarh"
    MANIPUR = "manipur"
    SIKKIM = "sikkim"


class LoanApplicationRequest(BaseModel):
    age: int = Field(..., ge=18, le=100)
    income: float = Field(..., ge=0)
    experience: float = Field(..., ge = 0)
    current_job_years: float = Field(..., ge=0)
    current_house_years: float = Field(..., ge=0)
    home_ownership: HomeOwnershipType
    car_ownership: CarOwnership
    # marital_status: MaritalStatusType
    profession: Profession
    state: State

    class Config:
        schema_extra = {
            "example": {
                "age": 35,
                "income": 60000,
                "experience": 5.5,
                "home_ownership": "rented",
                "car_ownership": "yes",
                # "marital_Status": "married",
                "profession": "Engineer",
                "current_job_years": 1.2,
                "current_house_years": 2.4,
                "state": "kerala"
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