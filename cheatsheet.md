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
                        host = os.getenv("DB_HOST"),
                        database = os.getenv("DB_NAME"),
                        user = os.getenv("DB_USER"),
                        password = os.getenv("DB_PASSWORD"),
                        port = os.getenv("DB_PORT")
            )
            #cursor to communicate with the database
            self.cur = self.con.cursor()
            return
