from fastapi import APIRouter,Depends,Request,UploadFile
from typing import List
from sqlalchemy.orm import Session
from src.db import get_db
from src.schemas import Credits
from src.crud import get_user_credits,plans_insert


credit_router = APIRouter()
plans_inserts =  APIRouter()


@credit_router.get('/user_credits/{user_id}',response_model=List[Credits],response_model_exclude_none=True,status_code=200)
def get_user_credit(request:Request, user_id: int, db: Session = Depends(get_db)):
    return get_user_credits(user_id,db)

@plans_inserts.post('/plans_insert', status_code=200)
def upload_file(file: UploadFile,db: Session = Depends(get_db)):
    return plans_insert(file,db)
