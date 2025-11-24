# the main script for console visualisation of the game
import towers
import enemies
import numpy as np

class board:
    def __init__(self, size):
        self.x_size, self.y_size = size
        self.board = np.zeros(size, dtype=float)

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
        
    def print_board(self, enemy_list, tower_list, path_list):
        #visualisation of the board in console
        matrix_to_print = []
        entry = [' ' for _ in range(self.board.shape[1])] # for displaying entry arrow
        entry[path_list[0][0]+1] = '⇩' #we take the first element of path list as the entry
        out_y = path_list[-1][1] #position of the output of the board
        matrix_to_print.append("   ".join(entry))
        matrix_to_print.append(" | ".join([' ']+[str(k) for k in range(self.board.shape[1])]))
        for i in range(self.board.shape[1]):
            line = []
            for j in range(self.board.shape[0]):
                value = self.board[i, j]
                if value == 0:
                    line.append(' ')

                if value < 0 and value != np.inf and value != -np.inf: #enemy
                    line.append(enemy_list[-int(value)-1].representation)

                if value > 0 and value != np.inf and value != -np.inf: #tower
                    line.append(tower_list[int(value)-1].representation)
                
                if value == np.inf: #path horizontal
                    line.append('═')

                if value == -np.inf: #path horizontal
                    line.append('║')
            if i == out_y: 
                line.append('⇨')
            else:
                line.append(' ')
            matrix_to_print.append(" | ".join([str(i)]+line))

        matrix_to_print_corr = self.correct_print_board(matrix_to_print)
        for line in matrix_to_print_corr:
            print(line)
    
    @staticmethod
    def correct_print_board(matrix_to_print):
        #correct the list of value in matrix to print
        # the path must be ╚ ╝ ╔ ╗ with respect to what comes before and next
        header1 = matrix_to_print[0]
        header2 = matrix_to_print[1]
        rows = [line.split(" | ") for line in matrix_to_print[2:]]
        if not rows:
            return [header1, header2]

        indices = [parts[0] for parts in rows]
        grid = [parts[1:] for parts in rows]
        H = len(grid)
        W = len(grid[0]) if H > 0 else 0

        path_chars = {"═", "║", "╔", "╗", "╚", "╝"}

        def is_path(r, c):
            if 0 <= r < H and 0 <= c < W:
                return grid[r][c] in path_chars
            return False

        new_grid = [row[:] for row in grid]

        for r in range(H):
            for c in range(W):
                ch = grid[r][c]
                if ch not in path_chars:
                    # if ch is not a path
                    continue

                up = is_path(r-1, c)
                down = is_path(r+1, c)
                left = is_path(r, c-1)
                right = is_path(r, c+1)

                # choix du caractère selon les connexions
            
                if down and right:
                    new_ch = "╔"
                elif down and left:
                    new_ch = "╗"
                elif up and right:
                    new_ch = "╚"
                elif up and left:
                    new_ch = "╝"
                else:
                    if left or right:
                        new_ch = "═"
                    else:
                        new_ch = "║"
                new_grid[r][c] = new_ch

        corrected = [header1, header2]
        for idx, row in zip(indices, new_grid):
            corrected.append(" | ".join([idx] + row))
        return(corrected)
    
        
    def add_path(self, path_list):
        # add the path (ie the path that the enemies follow)
        for path in path_list:
            #path is a tuple (x, y, orientation) with 1 left to right, 2 right to left, -1 up to down, -2 down to up
            x, y, orientation = path
            self.board[y, x] = np.inf*(orientation) #+- infinity



                    

if __name__=="__main__":
    actual_board = board((5,5)) #5x5 board
    tower_list = [towers.tower_obj('soldier', 3, 1), towers.tower_obj('archer', 2, 4)]
    for id, tow in enumerate(tower_list):
        actual_board.place_tower(id+1, tow.x, tow.y)
    path_list = [(0, 0, -1), (0, 1, -1), (0, 2, -1), (1, 2, 1), (2, 2, 1), (3 ,2 ,1), (4 ,2 ,1)]
    actual_board.add_path(path_list)
    actual_board.print_board([], tower_list, path_list)
