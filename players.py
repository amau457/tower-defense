# all the things to define player class
import numpy as np
import towers

class player:
    def __init__(self, id):
        self.money = 0
        self.health = 0
        self.level = 0
        self.board = None
        self.id = id #player id
    
    def spawn(self, board):
        #initialise all variables to a starting value (spawn player)
        self.money = 20
        self.health = 20
        self.level = 1
        self.board = board

    def buy(self, tower):
        #return true and update the price if we have enough money
        if self.money >= tower.price:
            self.money -= tower.price
            return(True)
        else:
            return(False)

