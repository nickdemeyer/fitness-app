import os
from dotenv import load_dotenv
import psycopg2
from sqlalchemy import create_engine, select, String, Numeric
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

#workout table
class Workout(Base):
    __tablename__ = "workouts"
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[str] = mapped_column(String(50))
    exercise: Mapped[str] = mapped_column(String(100))
    sets: Mapped[int] = mapped_column()
    reps: Mapped[int] = mapped_column()
    weight: Mapped[float] = mapped_column(Numeric)

#data selecteren - sessie maken - select query - resultaten ophalen met for loop
#1 sessie maken
with Session(engine) as session:
    #2 query maken
    workouts = session.scalars(select(Workout)).all()

    #3 loop resultaten ophalen
    for w in workouts:
        print(f"{w.exercise} - {w.weight}")