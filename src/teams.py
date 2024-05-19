import typing
from .hero import Warrior
from .goblin import Goblin

class Team:
    def __init__(self):
        self.teams_1 = []
        self.teams_2 = []

    def add_to_team1(self, hero: Warrior | Goblin):
        self.teams_1.append(hero)
        hero.team = self.teams_1
        hero.other_team = self.teams_2
    
    def add_to_team2(self, hero: Warrior | Goblin):
        self.teams_2.append(hero)
        hero.team = self.teams_2
        hero.other_team = self.teams_1
    
    def print_1(self):
        return self.teams_1
    
    def print_2(self):
        return self.teams_2



