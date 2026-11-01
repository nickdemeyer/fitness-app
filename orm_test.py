from sqlalchemy import create_engine, select, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

class base(DeclarativeBase):
    pass

class pet(base):
    __tablename__ = "pets"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))

engine = create_engine("sqlite:///:memory:")
base.metadata.create_all(engine)

with Session(engine) as session:
    session.add(pet(name="Rex"))
    session.commit()
    pets = session.scalars(select(pet)).all()
    print(pets[0].name)