import psycopg2

#making connection
connectie = psycopg2.connect(database = "dbname", user = "postgres", password = "pass", host = "localhost", port = "5432")

#cursor object
cur = connectie.cursor()

#insert
insert_query = """insert into workouts (date, exercise, sets, reps, weight) values(%s, %s, %s, %s, %s);"""
data = [("17/03/2026", "pulldown", 4, 10, 50), ("17/03/2026", "cable row", 4, 10, 35)]
cur.executemany(insert_query, data)
print("data inserted")
connectie.commit()

#print all workouts met select
sql = """select id, date, exercise, sets, reps, weight from workouts"""
cur.execute(sql)
rows = cur.fetchall()
for i in rows:
    print(f"id: {i[0]} - date: {i[1]} - exercise: {i[2]} - sets: {i[3]} - reps: {i[4]} - weight: {i[5]}")
