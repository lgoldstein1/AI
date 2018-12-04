import pygame, random, copy

print("loading trash talk module...")

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 170, 255)
DARKBLUE = (0, 0, 153)
YELLOW = (255, 255, 0)

pygame.init()

# Set the width and height of the screen [width, height]
size = (700, 700)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Connect 4")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# initialize the board as a stack
row1 = [0, 0, 0, 0, 0]
row2 = [0, 0, 0, 0, 0]
row3 = [0, 0, 0, 0, 0]
row4 = [0, 0, 0, 0, 0]
row5 = [0, 0, 0, 0, 0]

grids = [row1, row2, row3, row4, row5]
user = 1

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True


    # --- Game logic should go here


    # ---Buttons-----
    def button(x, y, w, h, ic, ac, num):
        if(user == 1):
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            if x + w > mouse[0] > x and y + h > mouse[1] > y:
                pygame.draw.rect(screen, ac, (x, y, w, h))

                if click[0] == 1:
                    onclick(num)

            else:
                pygame.draw.rect(screen, ic, (x, y, w, h))
        else:
            num = get_move(grids, 5)
            onclick(num)

        if (check_won(grids, 1, 5) or
                diagcheck_won(grids, 1, 5) or
                diagcheck_won(grids[::-1], 1, 5)):
            for a in range(5):
                for b in range(5):
                    grids[a][b] = 1
            screen.fill(RED)
            font = pygame.font.SysFont('Calibri', 50, True, False)
            text = font.render("Congratulations cheater", True, WHITE)
            screen.blit(text, [250, 100])
        elif (check_won(grids, 2, 5) or
                diagcheck_won(grids, 2, 5) or
                diagcheck_won(grids[::-1], 2, 5)):
            for a in range(5):
                for b in range(5):
                    grids[a][b] = 2
            screen.fill(BLACK)
            font = pygame.font.SysFont('Calibri', 50, True, False)
            text = font.render("YOU LOSE", True, WHITE)
            screen.blit(text, [250, 100])
        return





    def test_place(user_input, user, grids):
        for grid in grids[::-1]:
            if (grid[user_input] == 0):
                grid[user_input] = user
                return grids


    def check_won(grids, user, n=5):
        for i in range(n):
            consec_counter = 0
            for j in range(n):
                try:
                    if grids[i][j] == user:
                        consec_counter += 1
                    else:
                        consec_counter = 0
                except TypeError:
                    print("i:", i)
                    print("j:", j)
                if (consec_counter >= 4):
                    return True
        return False


    def diagcheck_won(grids, user, n=5):
        for i in range(n):
            consec_counter = 0
            for j in range(n):
                if grids[j][i] == user:
                    consec_counter += 1
                else:
                    consec_counter = 0
                if consec_counter >= 4:
                    return True
        if (all(grids[x][x] == user for x in range(4))):
            return True
        return False


    def get_move(grids, n=5):
        temp = copy.deepcopy(grids)
        # check for winning moves
        for i in range(n):
            temp1 = copy.deepcopy(temp)
            temp2 = copy.deepcopy(temp)
            if (temp1[0][i] == 0) and (temp2[0][i] == 0):
                if (check_won(test_place(i, 2, temp1), 2, n) == True):
                    print("winning move found!")
                    return i
                elif (diagcheck_won(test_place(i, 2, temp2), 2, n) == True):
                    print("winning move found!")
                    return i
        # check if the other player can win
        for j in range(n):
            temp3 = copy.deepcopy(grids)
            temp4 = copy.deepcopy(grids)
            if (temp1[0][j] == 0):
                if check_won(test_place(j, 1, temp3), 1, n) == True:
                    print("blocking winning move...")
                    return j
                if diagcheck_won(test_place(j, 1, temp4), 1, n) == True:
                    print("blocking winning move...")
                    return j

        # calculate best move
        possible_moves = []
        potential = []
        eval_dict = {}
        for i in range(n):
            if (temp[0][i] == 0):
                potential.append(i)
        # if there are no potential moves, play a random space
        if (len(potential) == 0):
            found = 0
            move = random.randint(0, 4)
            try:
                while(found == 0):
                    if (temp[0][move] != 0):
                        move = random.randint(0, 4)
                    else:
                        return move
                return move
            except IndexError:
                print("move: ", move)
        else:
            vert_inc = 0
            for q in range(n):
                eval_dict[q] = 0
            for j in range(n):
                if (temp[i][j] == 2) and (vert_inc == 0):
                    eval_dict[i] += 1
                    vert_inc = 1
            for k in range(n):
                if (k > 0):
                    if (temp[k][i - 1] == 2):
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
        # make sure possible moves are valid
        for z in possible_moves:
            if (temp[0][z] == 0):
                possible_valid = 1
        if (possible_valid == 0):
            move = random.randint(0, 4)
            found = 0
            try:
                while(found == 0):
                    if (temp[0][move] != 0):
                        move = random.randint(0, 4)
                    else:
                        return move
                return move
            except IndexError:
                print("move potential: ", move)
        move = random.choice(possible_moves)
        while (temp[0][move] != 0):
            move = random.choice(possible_moves)
        return move

    def colorswitch(int):
        colors = [WHITE, RED, BLACK]
        return colors[int]


    def onclick(num):
        global user
        if (user == 2):
            print("Computer is moving...")
        for grid in grids[::-1]:
            if (grid[num] == 0):
                grid[num] = user
                if(user == 1):
                    user = 2
                    return
                elif(user == 2):
                    user = 1
                    return


    # --- Screen-clearing code goes here

    screen.fill(BLUE)

    pygame.draw.rect(screen, DARKBLUE, [145, 150, 400, 400])
    pygame.draw.polygon(screen, BLACK, [[145, 550], [125, 575], [545, 550], [570, 575]])

    # column1
    y = 475
    x = 470

    # buttons for columns
    button(150, 120, 70, 20, YELLOW, RED, 0)

    button(230, 120, 70, 20, YELLOW, RED, 1)

    button(310, 120, 70, 20, YELLOW, RED, 2)

    button(390, 120, 70, 20, YELLOW, RED, 3)

    button(470, 120, 70, 20, YELLOW, RED, 4)

    for j in range(4,-1,-1):
        for i in range(4,-1,-1):
            pygame.draw.ellipse(screen, colorswitch(grids[i][j]), [x, y, 70, 70])


            y -= 80
        x -= 80
        y = 475

    # --- Drawing code should go here

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(7)

# Close the window and quit.
pygame.quit()