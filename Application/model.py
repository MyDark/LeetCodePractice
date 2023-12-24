from sqlalchemy import create_engine, Column, Integer, String, DECIMAL, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from config import Config

Base = declarative_base()


class Expenses(Base):
    __tablename__ = 'expenses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, nullable=False, default=2024)
    month = Column(String(255), nullable=True)
    category = Column(String(255), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=True, default=0.00)
    total_in_month = Column(DECIMAL(10, 2), nullable=True, default=0.00)
    total_in_year = Column(DECIMAL(10, 2), nullable=True, default=0.00)


class Incomes(Base):
    __tablename__ = 'incomes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, nullable=False, default=2024)
    month = Column(String(255), nullable=False)
    exchange_rate = Column(DECIMAL(10, 4), nullable=True)
    income_usd = Column(DECIMAL(10, 2), nullable=True, default=0.00)
    income_uah = Column(DECIMAL(10, 2), nullable=True, default=0.00)
    single_tax = Column(DECIMAL(10, 2), nullable=True, default=0.00)
    ssc = Column(DECIMAL(10, 2), nullable=True, default=1474.00)
    total_taxes = Column(DECIMAL(10, 2), nullable=True, default=0.00)
    clean_income = Column(DECIMAL(10, 2), nullable=True, default=0.00)
    additional_income = Column(DECIMAL(10, 2), nullable=True, default=0.00)
    expenses = Column(DECIMAL(10, 2), nullable=True, default=0.00)
    total_left = Column(DECIMAL(10, 2), nullable=True, default=0.00)


class Accounts(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    currency = Column(String(255), nullable=False)
    balance = Column(DECIMAL(10, 2), nullable=True)


engine = create_engine(Config.DATABASE_URI)
Base.metadata.create_all(engine)
