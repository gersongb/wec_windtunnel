# Author: Gerson Garsed-Brand
# Date: June 2023
# Description: class definitions for a team

class Team:
    def __init__(self, name, colour):
        self.name = name
        self.cars = []
        self.aeromap = None
        self.colour = colour

    def set_aeromap(self, Aeromap):
        self.aeromap = Aeromap
   
    def add_car(self, Car):
        self.cars.append(Car)

  
class Car:
    def __init__(self, team, number):
        self.team = team
        self.number = number


