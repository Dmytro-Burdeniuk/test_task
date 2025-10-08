from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


URL_DATABASE = ''

engine = create_engine(URL_DATABASE, echo=True, future=True)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    future=True
)


class Base(DeclarativeBase):
    pass