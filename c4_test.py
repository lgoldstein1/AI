import random
import copy

def play(n=None):
    if n is None:
        while True:
            try:
                n = int(input('Input the grid size: '))
            except ValueError:
                print('Invalid input')
                continue
            if n <= 0:
                print('Invalid input')
                continue
            break

    grids = [[0] * n for _ in range(n)]
    user = 1
    print('Current board:')
    print(*grids, sep='\n')

    while True:
        if(user == 1):
            user_input = get_input(user, grids, n)
        else:
            user_input = get_move(grids, n)
        place_piece(user_input, user, grids)
        print('Current board:')
        print(*grids, sep='\n')

        if (check_won(grids, user, n) or
                diagcheck_won(grids, user, n) or
                diagcheck_won(grids[::-1], user, n)):
            print('Player', user, 'has won')
            return

        if not any(0 in grid for grid in grids):
            return

        user = 2 if user == 1 else 1


def get_input(user, grids, n):
    instr = 'Input a slot player {0} from 1 to {1}: '.format(user, n)
    while True:
        try:
            user_input = int(input(instr))
        except ValueError:
            print('invalid input:', user_input)
            continue
        if 0 > user_input or user_input > n + 1:
            print('invalid input:', user_input)
        elif grids[0][user_input - 1] != 0:
            print('slot', user_input, 'is full try again')
        else:
            return user_input - 1

def place_piece(user_input, user, grids):
    if(user == 2):
        print("Computer is moving...")
    for grid in grids[::-1]:
        if(grid[user_input] == 0):
            grid[user_input] = user
            return

def test_place(user_input, user, grids):
    for grid in grids[::-1]:
        if(grid[user_input] == 0):
            grid[user_input] = user
            return grids

def check_won(grids, user, n):
    for i in range(n):
        consec_counter = 0
        for j in range(n):
            try:
                if grids[i][j] == user:
                    consec_counter += 1
                else:
                    consec_counter = 0
            except TypeError:
                print("i:" , i)
                print("j:", j)
            if (consec_counter >= 4):
                return True
    return False

def diagcheck_won(grids, user, n):
    for i in range(n):
        consec_counter = 0
        for j in range(n):
            if grids[j][i] == user:
                consec_counter += 1
            else:
                consec_counter = 0
            if consec_counter >= 4:
                return True
    if(all(grids[x][x] == user for x in range(4))):
        return True
    return False

def get_move(grids, n):
    temp = copy.deepcopy(grids)
    #check for winning moves
    for i in range(n):
        temp1 = copy.deepcopy(temp)
        temp2 = copy.deepcopy(temp)
        if(temp1[0][i] == 0) and (temp2[0][i] == 0):
            if (check_won(test_place(i,2, temp1),2,n) == True):
                print("winning move found!")
                return i
            elif (diagcheck_won(test_place(i,2,temp2),2,n) == True):
                print("winning move found!")
                return i
    #check if the other player can win
    for j in range(n):
        temp3 = copy.deepcopy(grids)
        temp4 = copy.deepcopy(grids)
        if (temp1[0][j] == 0):
            if check_won(test_place(j,1, temp3),1,n) == True:
                print("blocking winning move...")
                return j
            if diagcheck_won(test_place(j, 1, temp4), 1, n) == True:
                print("blocking winning move...")
                return j

    #calculate best move
    possible_moves = []
    potential = []
    eval_dict = {}
    for i in range(n):
        if(temp[0][i] == 0):
            potential.append(i)
    #if there are no potential moves, play a random space
    if (len(potential) == 0):
        move = random.randint(0, n)
        try:
            while(temp[0][move] != 0):
                move = random.randint(0, n)
                return move
        except IndexError:
            print("move: ", move)
    else:
        vert_inc = 0
        for q in range(n):
            eval_dict[q] = 0
        for j in range(n):
            if(temp[i][j] == 2) and (vert_inc == 0):
                eval_dict[i] += 1
                vert_inc = 1
        for k in range(n):
            if(k > 0):
                if(temp[k][i-1] == 2):
                    eval_dict[i] += 1
            if (k < n):
                if (temp[k][i - 1] == 2):
                    eval_dict[i] += 1
    if eval_dict:
        highest = max(eval_dict.values())
        for key in eval_dict:
            if eval_dict[key] == highest:
                possible_moves.append(key)


    possible_valid = 0
    #make sure possible moves are valid
    for z in possible_moves:
        if(temp[0][z] == 0):
            possible_valid = 1
    if(possible_valid == 0):
        move = random.randint(0,n)
        try:
            while(temp[0][move] != 0):
                move = random.randint(0,n)
            return move
        except IndexError:
            print("move: ", move)
    print("eval_dict:" , eval_dict)
    move = random.choice(possible_moves)
    while(temp[0][move] != 0):
        move = random.choice(possible_moves)
    return move

if __name__ == '__main__':
    play()