import os
import psycopg2
from dotenv import load_dotenv

load_dotenv() #load in the memory

class MealTracker:
    def __init__(self):
        