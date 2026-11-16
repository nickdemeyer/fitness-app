from sqlalchemy import create_engine, select, String, Numeric, URL, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, relationship
from decimal import Decimal
from typing import Optional

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100))

    #python snelkoppeling met workouts en maaltijd lijsten/relaties leggen
    workouts: Mapped[list["Workout"]] = relationship(back_populates="user")
    meals: Mapped[list["Meal"]] = relationship(back_populates="user")

class Workout(Base):
    __tablename__ = "workouts"
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[str] = mapped_column(String(50))
    exercise: Mapped[str] = mapped_column(String(100))
    sets: Mapped[int] = mapped_column()
    reps: Mapped[int] = mapped_column()
    weight: Mapped[Decimal] = mapped_column(Numeric)
    #database koppeling
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)

    #python snelkoppeling
    user: Mapped[Optional["User"]] = relationship(back_populates="workouts")

    def to_dict(self):
        return {"id": self.id,
                "date": self.date,
                "exercise": self.exercise,
                "sets": self.sets,
                "reps": self.reps,
                "weight": float(self.weight),
                "user_id": self.user_id}

class Meal(Base):
    __tablename__ = "meals"
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(100))
    calories: Mapped[int] = mapped_column()
    protein: Mapped[int] = mapped_column()
    carbs: Mapped[int] = mapped_column()
    fats: Mapped[int] = mapped_column()
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)

    #python snelkoppeling
    user: Mapped[Optional["User"]] = relationship(back_populates="meals")

    def to_dict(self):
        return {"id": self.id,
                "date": self.date,
                "name": self.name,
                "calories": self.calories,
                "protein": self.protein,
                "carbs": self.carbs,
                "fats": self.fats,
                "user_id": self.user_id}