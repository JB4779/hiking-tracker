from datetime import datetime

# Input Helper Functions
def get_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_optional_float(prompt, current_value):
    while True:
        user_input = input(prompt)
        if user_input == "":
            return current_value
        try:
            return float(user_input)
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter an integer.")

def get_optional_int(prompt, current_value):
    while True:
        user_input = input(prompt)
        if user_input == "":
            return current_value
        try:
            return int(user_input)
        except ValueError:
            print("Invalid input. Please enter an integer.")

def get_date(prompt):
    while True:
        date_str = input(prompt)
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

def get_optional_date(prompt, current_value):
    while True:
        date_str = input(prompt)
        if date_str == "":
            return current_value
        try: 
            datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

def get_time(prompt):
    while True:
        time_str = input(prompt)

        try:
            hours, minutes = map(int, time_str.split(":"))
            
            if minutes < 0 or minutes > 59 or hours < 0:
                raise ValueError
            
            return hours * 60 + minutes
        
        except ValueError:
            print("Invalid time format. Please use HH:MM.")

def get_optional_time(prompt, current_value):
    while True:
        time_str = input(prompt)
        if time_str == "":
            return current_value
        try:
            hours, minutes = map(int, time_str.split(":"))

            if minutes < 0 or minutes > 59 or hours < 0:
                raise ValueError

            return hours * 60 + minutes

        except ValueError:
            print("Invalid time format. Please use HH:MM.")

def format_time(minutes):
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours:02}:{mins:02}"