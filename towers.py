# all the classes of towers (different from enemies classes)
import numpy as np

def assign_type(type):
    # assign characteristics with respect to the type to a tower
    all_towers = {"soldier": [20, 5, 1, 5], "archer": [10, 20, 1, 5]} #hp, range, attack_speed (/s), attack_damage
    return(all_towers[type])

class tower_obj:
    def __init__(self, type, x, y):
        characteristics = assign_type(type)
        self.type = type
        self.hp, self.range, self.attack_speed, self.attack_damage = characteristics
        # hp the hp of the tower
        # range the range of action
        # attack speed its speed in attack/s
        # attack damage, the amount of damages it does per attack
        self.priority = "first" # the priority in targeting
        # posible values: "first", "last", "closest"
        self.x = x #tower position
        self.y = y
    
    def change_priority(self, new_priority):
        #change the priority setting
        # posible values: "first", "last", "closest"
        self.priority = new_priority
    
    def distance2enemy(self, enemy):
        # returns the distance between tower and enemy
        res = np.sqrt((enemy.x-self.x)**2+(enemy.y-self.y)**2)
        return(res)

    def find_target(self, enemies):
        #finds the target to focus with respect to priority
        if len(enemies) == 0:
            # no enemies
            return(None)
        
        target = None
        for enemy in enemies:
            if self.distance2enemy(enemy) < self.range: #if the enemy is in the range
                if self.priority == "first":
                    # the target is the enemy the least advenced on the path
                    if target == None or target.order > enemy.order:
                        target = enemy
                
                if self.priority == "last":
                    # the target is the enemy the most advenced on the path
                    if target == None or target.order < enemy.order:
                        target = enemy

                if self.priority == "closest":
                    # the target is the closest to the tower
                    if target == None or self.distance2enemy(enemy) < self.distance2enemy(target):
                        target = enemy
        return(target)
                


if __name__ == "__main__":
    simple_tower1 = tower_obj("soldier", 0, 0)
    print(simple_tower1.hp)
    print(simple_tower1.range)