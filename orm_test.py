import os
from dotenv import load_dotenv
import psycopg2
from sqlalchemy import create_engine, select, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

#env file inladen
load_dotenv()

#haal variablen uit .env
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
name = os.getenv("DB_NAME")

#engine maken start van iedere sqlalchemy app het is de "home base"
engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}")

#base class maken
class Base(DeclarativeBase):
    pass

class Workout(Base):
    __tablename__ = "workouts"