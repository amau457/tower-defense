# the main script for console visualisation of the game
import towers
import enemies
import numpy as np

class board:
    def __init__(self, size):
        self.x_size, self.y_size = size
        self.board = np.zeros(size, dtype=np.int32)

    def place_tower(self, tower_id, x, y):
        # place a tower on the board
        # the tower is represented by an index (its index in the global variable tower_list of all towers)
        # the id is alwayd id_list + 1 (to differentiate with 0)
        if self.board[y, x] != 0:
            return("can't place here")
        else:
            self.board[y, x] = tower_id

    def place_enemy(self, enemy_id, x, y):
        # place an enemy on the board
        # the enemy is represented by an index (its index in the global variable enemy_list of all enemies)
        # enemy_id = -enemy_id (we give negative value to make a diff with tower_ids)
        # the id is alwayd id_list - 1 (to differentiate with 0)
        if self.board[y, x] != 0:
            return("can't place here")
        else:
            self.board[y, x] = enemy_id
        
    def print_board(self, enemy_list, tower_list):
        #visualisation of the board in console
        for i in range(self.board.shape[1]):
            line = []
            for j in range(self.board.shape[0]):
                value = self.board[i, j]
                if value == 0:
                    line.append(' ')

                if value < 0: #enemy
                    line.append(enemy_list[-value-1].representation)

                if value > 0: #tower
                    line.append(tower_list[value-1].representation)
            print(" | ".join(line))

                    

if __name__=="__main__":
    actual_board = board((5,5)) #5x5 board
    tower_list = [towers.tower_obj('soldier', 3, 1), towers.tower_obj('archer', 2, 4)]
    for id, tow in enumerate(tower_list):
        actual_board.place_tower(id+1, tow.x, tow.y)
    actual_board.print_board([], tower_list)