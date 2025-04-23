from pydantic import BaseModel, EmailStr
from typing import List, Optional

class DecisionMaker(BaseModel):
    name: str
    role: str
    linkedin: Optional[str] = ""

class Lead(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = ""
    website: Optional[str] = ""
    address: Optional[str] = ""
    industry: Optional[str] = ""
    number_of_employees: Optional[int] = 0
    annual_revenue: Optional[str] = ""

    decision_makers: List[DecisionMaker] = []
    recent_news: List[str] = []
    source_links: List[str] = []

    funding_stage: Optional[str] = ""
    ipo_status: Optional[str] = ""
