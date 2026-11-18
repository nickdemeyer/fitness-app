from models import User, Workout
from database import SessionLocal


with SessionLocal() as session:
    me = session.get(User, 1)
    if me is not None:
        print(me.username)
        for w in me.workouts:
            print(w.exercise)

    workout = session.get(Workout, 6)
    if workout is not None and workout.user is not None:
        print(workout.user.username)



    #2 query maken
    #workouts = session.scalars(select(Workout)).all()

    #3 loop resultaten ophalen
    #for w in workouts:
    #    print(f"{w.exercise} - {w.weight}")

    #workout toevoegen handmatig
    #nieuwe object maken met de klasse Workout en de waardes toevoegen
    #new_workout = Workout(date="10-11-2026",
    #                      exercise="front lever",
    #                      sets=1,
    #                      reps=5,
    #                      weight=Decimal("65"))
    #obj toevoegen met session.add + committen(opslaan)
    #session.add(new_workout)
    #session.commit()

    #workout ophalen met session.get() endaarna reps veranderen en commit
    #workout = session.get(Workout, 19)
    #if workout is not None:
    #    workout.reps = 3
    #    session.commit()
    #else:
    #    print("workout bestaat niet om aan te passen!")

    #workout verwijderen met session.delete
    #session.delete(workout)
    #session.commit()