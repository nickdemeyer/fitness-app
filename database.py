import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker

#env file inladen
load_dotenv()

#haal variablen uit .env
db_user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

#URL maken zodat ik geen f-string nodig heb dit is voor bepaalde characters in wachtwoorden zodat de url niet breekt.
url_object = URL.create("postgresql+psycopg2", username=db_user, password=password, host=host, port=port, database=db_name)

#engine maken start van iedere sqlalchemy app het is de "home base"
engine = create_engine(url_object)

SessionLocal = sessionmaker(bind=engine)