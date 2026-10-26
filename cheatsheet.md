## table + columns maken postgresql:
    create table "name table"(
        hier vul je de collums in voor de table
        id, serial primary key -> telt op 1 - 2 - 3 altijd unique nummer
        date, varchar(50) -> betekent dat er max 50 tekens in veld kunnen
        integer, decimal(50.8kg),...
    );

    manueel iets toevoegen insert into tablename(columns) values (..., ///, ///);

    update query manueel:
    update meals
    set date = '09-10-2026'
    where id = 1;

    delete row manueel:
    delete from meals
    where id = 5;

## make connectie with .env:
    def __init__(self):
            #db connectie maken
            self.con = psycopg2.connect(
                        host = os.getenv(""),
                        database = os.getenv(""),
                        user = os.getenv(""),
                        password = os.getenv(""),
                        port = os.getenv("")
            )
            #cursor to communicate with the database
            self.cur = self.con.cursor()
            return


## selecting a column name with f string:
    query = f"update workouts set {field} = %s where id = %s"

## flask
    virtualenv name
    activate env: .\env\Scripts\Activate.ps1

    print goes to terminal, return goes back to the caller
    decimal becomes a quoted string in jsaon, and float() fixes it.
    a list of tuples becomes a list of dictionaries with a loop and dict(zip(columns, row)).

    - request.get_json(silent=True) returns None instead of crashing on bad input.
    - fetchone() returns None when nothing is found. cur.rowcount is 0 when nothing was changed.
    - Close the connection on every path, including early returns.

## flask get json values:
# data.get("sleutel") pakt de waarde achter de sleutel, of geeft None als die ontbreekt.

data = request.get_json(silent=True)

field = data.get("field")          # als json {"field": "duration"}, dan field = "duration"
new_value = data.get("new_value")  # als json {"new_value": 45}, dan new_value = 45
