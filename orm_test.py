import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, select, String, Numeric, URL
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from decimal import Decimal

#env file inladen
load_dotenv()

#haal variablen uit .env
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
name = os.getenv("DB_NAME")

#URL maken zodat ik geen f-string nodig heb dit is voor bepaalde characters in wachtwoorden zodat de url niet breekt.
url_object = URL.create("postgresql+psycopg2", username=user, password=password, host=host, port=port, database=name)

#engine maken start van iedere sqlalchemy app het is de "home base"
engine = create_engine(url_object)

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
    weight: Mapped[Decimal] = mapped_column(Numeric)

#data selecteren - sessie maken - select query - resultaten ophalen met for loop
#1 sessie maken
with Session(engine) as session:
    #2 query maken
    workouts = session.scalars(select(Workout)).all()

    #3 loop resultaten ophalen
    for w in workouts:
        print(f"{w.exercise} - {w.weight}")

    #workout toevoegen handmatig
    #nieuwe object maken met de klasse Workout en de waardes toevoegen
    new_workout = Workout(date="10-11-2026",
                          exercise="front lever",
                          sets=1,
                          reps=5,
                          weight=Decimal("65"))
    #obj toevoegen met session.add + committen(opslaan)
    session.add(new_workout)
    session.commit()

    #workout ophalen met session.get() endaarna reps veranderen en commit
    workout = session.get(Workout, 19)
    if workout is not None:
        workout.reps = 3
        session.commit()
    else:
        print("workout bestaat niet om aan te passen!")

    #workout verwijderen met session.delete
    session.delete(workout)
    session.commit()
