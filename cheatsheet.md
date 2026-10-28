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
• Het is de internetstandaard: Data versturen naar een API (of dat nu workouts of meals zijn) gebeurt altijd als JSON.
• De vaste vertaling: Flask zet die JSON binnenkomende data altijd om naar een Python dictionary via request.get_json(). Er zit geen geheime logica achter.
• De buitenwereld (Postman/frontend) stuurt data als JSON naar jouw Flask-server.
• request.get_json() is de vertaler van Flask: het pakt die binnenkomende JSON-tekst en zet het om in een handige Python dictionary.
• Hierna kun je de data in Python gebruiken via bijvoorbeeld data["name"] of data["calories"].


field = data.get("field")          # als json {"field": "duration"}, dan field = "duration"
new_value = data.get("new_value")  # als json {"new_value": 45}, dan new_value = 45

## flask gebruikt standaard json dus dit is wat ik moet doen
    • De database geeft een tuple (een kale rij zonder labels).
    • Flask vereist een dictionary om de data automatisch te kunnen vertalen naar JSON.
    • JSON werkt met sleutel-waarde-paren, zodat de frontend (of Postman) de data begrijpt (bijv. "calories": 500).
    syntax: dict(zip(columns, row)) voegt twee losse lijsten samen tot één dictionary
    float() maakt van een tekst of getal een kommagetal bv wanneer je 50.5 uit database moet halen oplossing: workout["weight"] = float(workout["weight"])


## 🚗 De reis van de maaltijd-data (van Postman naar de Database):

1. Stap 1: De Buitenwereld (JSON)
	• De gebruiker typt in Postman een tekstje met de maaltijd. Omdat het internet geen Python begrijpt, typen ze dit in JSON (een universele tekst-standaard).
	• Jasje: Een platte tekststream.
2. Stap 2: De Uitsmijter (Python Dictionary)
	• Flask vangt die JSON-tekst op. Met request.get_json() vertaalt Flask die tekst naar een Python Dictionary (data = {...}).
	• Waarom? Nu kan jouw Python-code heel makkelijk met if-statements controleren of de naam niet leeg is en de getallen niet negatief zijn.
	• Jasje: Een Python Dictionary met sleutels en waarden.
3. Stap 3: De Kluis (PostgreSQL Database)
	• Als de data is goedgekeurd, stuur je de losse waarden uit die dictionary (data["name"], data["calories"]) door naar je database-methode (add_meal).
	• Jouw code stopt die losse waarden in een SQL-query (INSERT INTO meals...) en schiet ze zo de database in.
	• Jasje: Een tabel met rijen en kolommen.

📋 En hoe reist de data terug (als je een maaltijd opvraagt via GET)?

Precies de omgekeerde weg!
1. Database: Geeft een tuple (een kale rij met data zonder labels, bijv: (1, 'Kip', 500)).
2. Jouw Code: Plakt met dict(zip(columns, row)) de labels er weer aan vast om er een Python Dictionary van te maken ({"id": 1, "name": "Kip"}).
3. Flask: Vertaalt die dictionary met jsonify() weer terug naar JSON, zodat Postman of de app het netjes op het scherm kan tonen.
