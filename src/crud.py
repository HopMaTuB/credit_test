from fastapi import Depends,HTTPException,status,UploadFile
from sqlalchemy.orm import Session
from src.db import get_db
from src.models import Credit,Payment,Plan
from datetime import date
import datetime
from io import BytesIO
import pandas as pd

def get_user_credits(user_id: int, db: Session = Depends(get_db)):
    user_credits = db.query(Credit).filter(Credit.user_id == user_id).all()    
    
    if not user_credits:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User credits not found")
    result = []
    today = date.today()

    for credit in user_credits:
        is_closed = credit.actual_return_date is not None
        credit_data = {
            "issuance_date": credit.issuance_date,
            "is_closed": is_closed
        }
        if is_closed:
            credit_data.update({
                "return_date": credit.return_date,
                "body": credit.body,
                "percent": credit.percent,
                "total_payments": credit.body + credit.percent
            })        
        else:
                try:
                    overdue_days = (today - credit.return_date).days if today > credit.return_date else 0
                    payment_amount = get_user_payments(credit.id,db)
                    total_percent = get_total_percent(user_id, db)
                    credit_data.update({
                        "return_deadline": credit.return_date,
                        "days_overdue": overdue_days or 0,
                        "Issue_amount": credit.body,
                        "accured_interest": credit.percent,
                        "amount_of_payments": payment_amount,
                        "total_percents": total_percent
                        })
                except Exception as e:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{e}")          
        
        result.append(credit_data)

    
    return result

def get_user_payments(credit_id: int, db: Session ):
    user_payment = db.query(Payment).filter(Payment.credit_id == credit_id).all()

    if not user_payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User payments not found")
    
    total_sum = sum(p.sum for p in user_payment)
    return total_sum

def get_total_percent(user_id: int, db: Session):
    total_percent = db.query(Credit).filter(Credit.user_id == user_id).all()
    if not total_percent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User credits not found")
    
    total_percent = sum(c.percent for c in total_percent)
    return total_percent
                      
def plans_insert(file: UploadFile, db: Session = Depends(get_db)):
    print(f"Received file: {file.filename}, Content-Type: {file.content_type}")

    try:
        file.file.seek(0) 
        df = pd.read_excel(BytesIO(file.file.read()), engine="openpyxl")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid Excel file: {str(e)}")

    expected_columns = {"місяць плану", "назва категорії плану", "сума"}

    if not expected_columns.issubset(df.columns):
        raise HTTPException(status_code=400, detail="Invalid columns")

    plans = []

    for _, row in df.iterrows():
        for _, row in df.iterrows():
            try:
                plan_month = pd.to_datetime(row["місяць плану"]).date()
                
                if plan_month.day != 1:
                    raise ValueError(f"Invalid month format: day is not 1 ({plan_month})")
                    
            except ValueError as e:
                print(f"Error parsing date: {row['місяць плану']}, error: {str(e)}")
                raise HTTPException(status_code=400, detail=f"Invalid month format: {row['місяць плану']}")

        category = row["назва категорії плану"]
        amount = row["сума"]

        if pd.isna(amount):
            raise HTTPException(status_code=400, detail="Invalid amount")

        plans.append(Plan(period=plan_month, category_id=category, sum=amount))
    
    db.add_all(plans)
    db.commit()
    
    return {"message": "Plans inserted successfully"}