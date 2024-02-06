import copy
import random
import sys 
import pygame
import numpy as np

WIDTH , HEIGHT = 600, 600
ROWS , COLS = 3, 3
SQSIZE = 200
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
LINE_WIDTH = 15
CIRC_COLOR = (239, 231, 200)
CIRC_WIDTH = 15
RADIUS = SQSIZE //4
CROSS_COLOR = (66, 66, 66)
CROSS_WIDTH = 20
OFFSET = 50

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe AI')
screen.fill(BG_COLOR)

class Board:
    def __init__(self):
        self.squares = np.zeros((ROWS,COLS))
        self.empty_sqrs = self.squares 
        self.marked_sqrs = 0

    def final_state(self, show=False):
        # return 0 if no wins yet
        # return 1 if player 1 wins
        # return 2 if player 2 wins
        # print(self.squares)
        # vertical wins
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] !=0:
                if show:
                    color = CIRC_COLOR if self.squares[0][col] == 2 else CROSS_COLOR
                    iPos = (col*SQSIZE + SQSIZE//2, 20)
                    fPos = (col*SQSIZE + SQSIZE//2, HEIGHT-20)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[0][col]

        # horizontal wins
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] !=0:
                if show:
                    color = CIRC_COLOR if self.squares[row][0] == 2 else CROSS_COLOR
                    iPos = (20, row*SQSIZE + SQSIZE//2)
                    fPos = (WIDTH-20, row*SQSIZE + SQSIZE//2)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[row][0]      
            
        # desc diagonal
            if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
                if show:
                    color = CIRC_COLOR if self.squares[0][0] == 2 else CROSS_COLOR
                    iPos = (20, 20)
                    fPos = (WIDTH-20, HEIGHT-20)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[0][0]
        
        # desc diagonal
            if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
                if show:
                    color = CIRC_COLOR if self.squares[2][0] == 2 else CROSS_COLOR
                    iPos = (20, HEIGHT-20)
                    fPos = (WIDTH-20, 20)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[1][1]
            
        # no win yet
        return 0


    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs +=1

    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0
    
    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_sqr(row, col):
                    empty_sqrs.append((row,col))

        return empty_sqrs
    
    def isfull(self):
        return self.marked_sqrs==9
    
    def isempty(self):
        return self.marked_sqrs==0

class AI:
    def __init__(self, level=1, player=2): # level=0 random | level=1 AI
        self.level = level
        self.player = player

    def rnd(self, board):
        empty_sqrs = board.get_empty_sqrs()
        index = random.randrange(0, len(empty_sqrs))
        return empty_sqrs[index]
    
    def minimax(self, board, maximizing):
        #terminal case
        case = board.final_state()
    
        if case == 1:
            return 1, None # evalution , move
    
        if case == 2:
            return -1, None
        
        elif board.isfull():
            return 0, None
        
        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval = self.minimax(temp_board, False)[0]

                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move

        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 2)
                eval = self.minimax(temp_board, True)[0]

                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move

    def eval(self, main_board):
        
        #random choice
        if self.level==0:
            move = self.rnd(main_board)
            eval = 'random'
        
        # AI move
        else:
            eval, move =  self.minimax(main_board, False)
        
        print(f'Move chosen by AI is {move} with {eval} as the evaluation')
        return move

class Game:

    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1
        self.gamemode = 'ai' # pvp or ai
        self.running = True
        self.show_lines()

    def make_move(self, row, col):
        self.board.mark_sqr(row, col, self.player)
        self.draw_fig(row, col)
        self.next_turn()

    def show_lines(self):
        screen.fill(BG_COLOR)
        #vertical
        pygame.draw.line(screen, LINE_COLOR, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, ( WIDTH-SQSIZE, 0), (WIDTH-SQSIZE, HEIGHT), LINE_WIDTH)

        #horizontal
        pygame.draw.line(screen, LINE_COLOR, (0, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT-SQSIZE), (WIDTH, HEIGHT-SQSIZE ), LINE_WIDTH)

    def draw_fig(self, row, col):
        if self.player == 1:
            # draw cross
            # desc line
            start_desc = (col*SQSIZE + OFFSET, row*SQSIZE + OFFSET)
            end_desc = (col*SQSIZE + SQSIZE - OFFSET, row*SQSIZE + SQSIZE - OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)

            # asc line
            start_asc = (col*SQSIZE + SQSIZE - OFFSET, row*SQSIZE + OFFSET)
            end_asc = (col*SQSIZE + OFFSET, row*SQSIZE + SQSIZE - OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)


        else:
            # draw cirlce
            center = (col*SQSIZE + SQSIZE//2, row*SQSIZE + SQSIZE//2)
            pygame.draw.circle(screen, CIRC_COLOR, center, RADIUS, CIRC_WIDTH)

    def next_turn(self):
        self.player = self.player%2 +1

    def reset(self):
        self.__init__()

    def isOver(self):
        return self.board.final_state(show=True) !=0 or self.board.isfull()
    

def main():

    game = Game()
    board = game.board
    ai = game.ai

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1]//SQSIZE
                col = pos[0]//SQSIZE

                if board.empty_sqr(row, col) and game.running:
                    game.make_move(row, col)

                    if game.isOver():
                        game.running = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai
        
        if game.gamemode == 'ai' and game.player == ai.player and game.running:
            #updating screen
            pygame.display.update()
            row ,col = ai.eval(board)
            game.make_move(row, col)
    
            if game.isOver():
                game.running = False

        pygame.display.update()
 
main()