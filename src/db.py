from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from load_env import MY_SQL_BD,MY_SQL_HOSTNAME,MY_SQL_PASSWORD,MY_SQL_PORT,MY_SQL_USERNAME


DATABASE_URL = f"mysql+mysqlconnector://{MY_SQL_USERNAME}:{MY_SQL_PASSWORD}@{MY_SQL_HOSTNAME}:{MY_SQL_PORT}/{MY_SQL_BD}"

engine = create_engine(DATABASE_URL,echo = True)
SessionLocal = sessionmaker(autocommit=False,bind = engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()