import os

class Config:
    DATABASE_URI = os.getenv("DATABASE_URI", "mysql+mysqlconnector://test:test1@test2/test3")
