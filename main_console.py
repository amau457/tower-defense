# the main script for console visualisation of the game
import towers
import enemies
import players
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
            print("can't place here")
        else:
            self.board[y, x] = tower_id
        
    def print_board(self, enemy_list, tower_list, path_list):
        #visualisation of the board in console
        matrix_to_print = []
        entry = [' ' for _ in range(self.board.shape[1])] # for displaying entry arrow
        entry[path_list[0][0]+1] = '⇩' #we take the first element of path list as the entry
        out_y = path_list[-1][1] #position of the output of the board
        matrix_to_print.append("   ".join(entry))
        matrix_to_print.append(" | ".join([' ']+[str(k) for k in range(self.board.shape[1])]))

        # dict for quick search
        enemy_map = {(e.x, e.y): e for e in enemy_list if getattr(e, "hp", 1) > 0} #alive
        tower_map = {(t.x, t.y): t for t in tower_list}

        for i in range(self.board.shape[1]):
            line = []
            for j in range(self.board.shape[0]):
                # enemies
                e = enemy_map.get((j, i))
                if e is not None:
                    line.append(e.representation)
                    continue

                # towers
                t = tower_map.get((j, i))
                if t is not None:
                    line.append(t.representation)
                    continue

                # board
                val = self.board[i, j]
                if np.isposinf(val):
                    line.append('═')
                elif np.isneginf(val):
                    line.append('║')
                else:
                    if val == 0:
                        line.append(' ')
                    elif val > 0:
                        idx = int(val) - 1
                        line.append(tower_list[idx].representation)
                    elif val < 0:
                        idx = int(-val) - 1
                        line.append(enemy_list[idx].representation)
                    else:
                        line.append(' ')


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

                # the right char with respect to connection
            
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

def next_step(tower_list, enemy_list, path_list):
    # do all the actions of one step (attack, move)
    # first we make all the towers attack
    for id_tow, tower in enumerate(tower_list):
        if tower.cooldown == 0: #if not busy
            target = tower.find_target(enemy_list) # the target to target 
            if not target == None:
                target.hp -= tower.attack_damage
                tower.cooldown = tower.attack_speed
        else: #if busy
            tower.cooldown -= 1
    
    #then we make the enemies move
    path_lookup = {(px, py): orient for px, py, orient in path_list}

    # enemies move
    for enemy in enemy_list:
        if enemy.hp <= 0:
            continue  # dead don't move

        steps = int(enemy.speed)  # number of steps this turn
        for _ in range(steps):
            x, y = enemy.x, enemy.y
            orientation = path_lookup.get((x, y), None)
            if orientation is None:
                break

            if orientation == 1: # left to right
                enemy.x += 1
            elif orientation == -1:# up to down
                enemy.y += 1
            elif orientation == 2:# right to left
                enemy.x -= 1
            elif orientation == -2: # down to up
                enemy.y -= 1
            else:
                break
    return(tower_list, enemy_list, path_list)


def check_enemies_alive(enemy_list):
    #checks if there are still some enemies that are alive
    for enemy in enemy_list:
        if enemy.hp > 0:
            return(True)
    return(False)

def check_player_life(enemy_list, actual_board, player):
    # checks if the player has still some life
    # one enemy that cross the output = - one life
    for enemy in enemy_list:
        if enemy.x >= actual_board.x_size:
            if enemy.hp > 0:
                enemy.hp = 0
                player.health -= 1
    return(player.health)

def ask_action(player, actual_board, tower_list):
    test = True
    while test:
        print("possible actions:")
        print("continue, buy, sell")
        var = input("what do you want to do ?")
        if var == "continue":
            test = False

        elif var == "buy":
            print("towers:")
            print("soldier", "archer")
            var2 = input("which tower do you want to buy ?")
            x = int(input("x pos ?"))
            y = int(input("y pos ?"))
            if var2 == "soldier" or var2 == "archer":
                to_buy_tower = towers.tower_obj(var2, x, y)
                if player.buy(to_buy_tower):
                    tower_list.append(to_buy_tower)
                    actual_board.place_tower(len(tower_list)+1, x, y)
                    print('tower placed')
                    print('')
                else:
                    print('not enough money') #we will show the amounts later..
                    print('')
            else:
                print("tower does not exist")
        
        elif var == "sell":
            print("not implemented yet")
        
        else:
            print("unkown command")
    return(player, actual_board, tower_list) #not necessary but safe



def main():
    # main function to run the game
    # create a player
    player1 = players.player(0)
    # round 1
    #create board
    actual_board = board((5,5)) #5x5 board
    #spawn the player (link it to the board)
    player1.spawn(actual_board)

    #add path
    path_list = [(0, 0, -1), (0, 1, -1), (0, 2, 1), (1, 2, 1), (2, 2, 1), (3 ,2 ,1), (4 ,2 ,1)]
    actual_board.add_path(path_list)

    actual_board.print_board([], [], path_list) # to show to the player

    tower_list = []
    player1, actual_board, tower_list = ask_action(player1, actual_board, tower_list)

    # wave of the level (will be generated automatically later)
    enemy_list = [enemies.enemy_obj('walker', 0, 0, 0),
                   enemies.enemy_obj('runner', 0, 0, 1),]
    actual_board.print_board(enemy_list, tower_list, path_list)
    print('')
    player_life = check_player_life(enemy_list, actual_board, player1)
    while check_enemies_alive(enemy_list) and player_life >0: # while we still have enemies and player still alive
        tower_list, enemy_list, path_list = next_step(tower_list, enemy_list, path_list)
        actual_board.print_board(enemy_list, tower_list, path_list)
        player_life = check_player_life(enemy_list, actual_board, player1)
    print('')
    print('life of the player:')
    print(check_player_life(enemy_list, actual_board, player1))

                    

if __name__=="__main__":
    main()
