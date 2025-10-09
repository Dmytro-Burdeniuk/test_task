from src.database import Base, engine
from src.models import *


Base.metadata.create_all(bind=engine)
print("Таблиці створені успішно")