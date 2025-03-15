from sqlalchemy import Column,Integer,String,Date,ForeignKey
from sqlalchemy.orm import DeclarativeBase
from src.db import engine

class Base(DeclarativeBase):
	pass

class User(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True)
    login = Column(String(50))
    registration_date = Column(Date)

class Dictionary(Base):
    __tablename__ = 'Dictionary'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))

class Payment(Base):
    __tablename__ = 'Payments'

    id = Column(Integer, primary_key=True)
    sum = Column(Integer)
    payment_date = Column(Date)
    credit_id = Column(Integer,ForeignKey("Credits.id"))
    type_id = Column(Integer, ForeignKey("Dictionary.id"))

class Credit(Base):
    __tablename__ = 'Credits'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("Users.id"))
    issuance_date = Column(Date)
    return_date = Column(Date)
    actual_return_date = Column(Date,default=None)
    body = Column(Integer)
    percent = Column(Integer)

class Plan(Base):
    __tablename__ = 'Plans'

    id = Column(Integer, primary_key=True)
    period = Column(Date)
    sum = Column(Integer)
    category_id = Column(Integer, ForeignKey("Dictionary.id"))



Base.metadata.create_all(bind=engine)
