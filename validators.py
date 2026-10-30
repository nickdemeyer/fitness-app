from datetime import datetime

def check_string_emptyfield(value):
    if type(value) is not str or value.strip() == "":
        return "No valid text or empty"
    return None

def check_date(value):
    if type(value) is not str:
        return "Fill in DD-MM-YYYY to be valid" 
    try:
        datetime.strptime(value, "%d-%m-%Y")   
    except ValueError:
        return "Fill in DD-MM-YYYY to be valid" 
    return None

def check_whole_number(value):
    if type(value) is not int or value <= 0:
        return "Must be a number"
    return None

def check_non_negative_number(value):
    if type(value) not in [int, float] or value < 0:
        return "Number must be 0 or higher"
    return None