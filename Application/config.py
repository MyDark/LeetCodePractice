import os


class Config:
    DATABASE_URI = os.getenv("DATABASE_URI", "mysql+mysqlconnector://db_user:db_pass@db_host/db_name")
