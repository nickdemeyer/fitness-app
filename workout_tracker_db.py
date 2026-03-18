import os
import psycopg2
from dotenv import load_dotenv
class WorkoutTracker:
    def __init__(self):
        load_dotenv()  #laad dotenv bestand met gegevens
        db_name = os.getenv('database')  
        db_user = os.getenv('user')      #env variables ophalen
        db_pass = os.getenv('password')
        db_host = os.getenv('host')
        db_port = os.getenv('port')

        #CONNECTIE MAKEN
        self.connectie = psycopg2.connect(dbname=db_name, user=db_user, password=db_pass, host=db_host, port=db_port)



