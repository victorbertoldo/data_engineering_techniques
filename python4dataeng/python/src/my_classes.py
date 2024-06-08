from datetime import datetime as dt, date
from dateutil.relativedelta import relativedelta

class MyAge:
    def __init__(self, date_of_birth, my_name):
        # __init__ is the constructor, it fill properties and uses self
        # your date of birth in the format YYYY-MM-DD
        self.__date_of_birth = dt.strptime(date_of_birth, "%Y-%m-%d")
        self.__my_name = my_name
        self.__my_age_in_years = relativedelta(date.today(), self.__date_of_birth).years
        
    def show_me_my_age(self):
        return f"{self.__my_name}, you are young, your age is only {self.__my_age_in_years} years old"
    
age = MyAge("1988-09-16", "Victor")
if __name__ == "__main__":
    print(age.show_me_my_age())