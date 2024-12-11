from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import time
time.sleep(20)

# Replace with your MySQL credentials
DATABASE_URL = "mysql+pymysql://sa:sa_password123@172.21.0.2/taskmanagement"

engine = create_engine(DATABASE_URL, connect_args={'connect_timeout': 20})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
