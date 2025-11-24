# all the classes of enemies (different from towers classes)
import numpy as np

def assign_type(type):
    # assign characteristics with respect to the type to an enemy
    all_enemies = {"walker": [20, 5], "runner": [10, 20]} #hp, speed,
    return(all_enemies[type])

class enemy_obj:
    def __init__(self, type, x, y):
        characteristics = assign_type(type)
        self.type = type
        self.hp, self.speed = characteristics
        # hp the hp of the enemy
        # speed is the speed of movement
        self.x = x #enemy position
        self.y = y
        
    def change_position(self, new_x, new_y):
        #change x,y to the next position of the enemy 
        self.x = new_x
        self.y = new_y
        
                

if __name__ == "__main__":
    simple_enemy1 = enemy_obj("walker", 0, 0)
    print(simple_enemy1.hp)
    print(simple_enemy1.speed)