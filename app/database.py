from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Получение URL базы данных из переменных окружения (указанных в docker-compose.yml)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/blog_db")

# Создание подключения к базе данных
engine = create_engine(DATABASE_URL)

# Создание фабрики сессий для взаимодействия с базой данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Определение базового класса для моделей SQLAlchemy
Base = declarative_base()

# Создание функции для получения сессии базы данных, чтобы использовать ее в зависимости FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
