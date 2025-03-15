from pydantic import BaseModel
from typing import Optional
from datetime import date

class Credits(BaseModel):
    issuance_date: Optional[date] = None
    is_closed: bool = None
    return_date: Optional[date] = None
    body: Optional[int] = None
    percent: Optional[int] = None
    total_payments: Optional[int] = None
    return_deadline: Optional[date] = None
    days_overdue: Optional[int] = None
    issue_amount: Optional[int] = None
    accured_interest: Optional[int] = None
    amount_of_payments: Optional[int] = None
    total_percents: Optional[int] = None
    
