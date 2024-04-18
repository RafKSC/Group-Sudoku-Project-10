import pygame
import sys
from cell import Cell
from sudoku_generator import *


class Board:
    def __init__(self, width, height, screen, difficulty):  # initial parameters to class Board
        self.width = width
        self.height = height
        self.difficulty = difficulty
        self.screen = screen
        if difficulty == "easy":
            self.board = generate_sudoku(9, 30)     # easy creates 30 values to solve
        elif difficulty == "medium":
            self.board = generate_sudoku(9, 40)     # medium creates 40 values to solve
        elif difficulty == "hard":
            self.board = generate_sudoku(9, 50)     # hard creates 50 values to solve
        self.cells = [
            [Cell(self.board[i][j], i, j, screen) for j in range(9)]
            for i in range(9)
        ]
        self.original_board = [
            [0 for j in range(9)] for i in range(9)
        ]
        for i in range(9):
            for j in range(9):
                self.original_board[i][j] = self.board[i][j]    # nested for loop to compare boards
        print("self original board", self.original_board)

    def draw(self):     # draws outline of Sudoku grid with 3x3 boxes
        # horizontal portion of the board
        for i in range(0, 10):
            if i % 3 == 0:
                pygame.draw.line(self.screen, (0, 0, 0),
                            (0, i * 59),
                             (self.width, i * 59), LINE_WIDTH * 3)     # bigger line depth in every 3 rows
            else:
                pygame.draw.line(self.screen, (0, 0, 0),
                                 (0, i * 59),
                                 (self.width, i * 59), LINE_WIDTH)    # every other line will be regular width

        # vertical portion of the board
        for i in range(0, 10):
            if i % 3 == 0:
                pygame.draw.line(self.screen, (0, 0, 0),
                             (i * 67, 0),
                             (i * 67, HEIGHT - 68), LINE_WIDTH * 3)     # bigger line depth in every 3 columns
            else:
                pygame.draw.line(self.screen, (0, 0, 0),
                                 (i * 67, 0),
                                 (i * 67, HEIGHT - 68), LINE_WIDTH)     # every other line will be regular width
        count = 0
        for i in range(9):
            print("empty: ", count)
            for j in range(9):
                if self.cells[i][j].value == 0:
                    count += 1
                print(self.cells[i][j].value)
                self.cells[i][j].draw()
        print("empty: ", count)

        # textures for the functions
        button_font = pygame.font.Font(None, 25)
        # ** replace easy with reset, medium with restart, and hard for exit**
        game_mode_text_easy = button_font.render("Reset", 0, (255, 255, 255))
        game_mode_text_medium = button_font.render("Restart", 0, (255, 255, 255))
        game_mode_text_hard = button_font.render("Exit", 0, (255, 255, 255))
        easy_surface = pygame.Surface((90, game_mode_text_easy.get_size()[0]))
        medium_surface = pygame.Surface((90, game_mode_text_medium.get_size()[0] - 15))
        hard_surface = pygame.Surface((90, game_mode_text_hard.get_size()[0] + 13))
        easy_surface.fill(ORANGE_COLOR)
        medium_surface.fill(ORANGE_COLOR)
        hard_surface.fill(ORANGE_COLOR)
        easy_surface.blit(game_mode_text_easy, (25, 10))
        medium_surface.blit(game_mode_text_medium, (10, 10))
        hard_surface.blit(game_mode_text_hard, (25, 10))
        # get rectangle - place where you want it
        easy_rectangle = easy_surface.get_rect(
            center=(WIDTH // 2 - 125, HEIGHT // 2 + 270)
        )
        medium_rectangle = medium_surface.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 + 270)
        )
        hard_rectangle = hard_surface.get_rect(
            center=(WIDTH // 2 + 125, HEIGHT // 2 + 270)
        )
        self.screen.blit(easy_surface, easy_rectangle)
        self.screen.blit(medium_surface, medium_rectangle)
        self.screen.blit(hard_surface, hard_rectangle)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_rectangle.collidepoint(event.pos):
                    # ** replace easy with reset, medium with restart, and hard for exit**
                    # Checks if mouse is on easy button
                    self.reset_to_original()  # if the mouse is on the start button, we can return to main
                if medium_rectangle.collidepoint(event.pos):

                    return
                if hard_rectangle.collidepoint(event.pos):
                    sys.exit()

        pygame.display.update()

    def select(self, row, col):     # where user is able to mark the cell on the Sudoku board
        self.cells[row][col].selected = True

    def click(self, x, y):   # returns coordinates on terminal of (row, column)
        row = y//60
        col = x//67
        return row, col

    def clear(self):    # clears cell values of only what was originally blank
        for i in range(9):
            for j in range(9):
                if self.cells[i][j].selected:
                    if self.original_board[i][j] == 0:
                        self.cells[i][j].set_cell_value(0)

    def sketch(self, value):     # sets sketch value displayed on top left corner of the cell
        for i in range(9):
            for j in range(9):
                if self.cells[i][j].selected:
                    self.cells[i][j].set_sketched_value(value)
                    self.cells[i][j].draw()

    def place_number(self, value):   # sets value of the cell from the user input
        for i in range(9):
            for j in range(9):
                if self.cells[i][j].selected:
                    self.cells[i][j].set_cell_value(value)

    def reset_to_original(self):    # resets board
        for i in range(9):
            for j in range(9):
                if self.cells[i][j].sketched_value is not None and self.cells[i][j].sketched_value != 0:
                    self.cells[i][j].set_cell_value(0)
                    self.cells[i][j].set_sketched_value(0)

    def is_full(self):  # keeps track whether the board is full or not. Returns True when this is the case
        for i in range(9):
            for j in range(9):
                if self.cells[i][j].value == 0:
                    return False
        return True

    def update_board(self):     # makes sure to update the board with each of the user inputs for the cells
        for i in range(9):
            for j in range(9):
                self.board[i][j] = self.cells[i][j].value

    def find_empty(self):   # finds empty cell and outputs coordinates (row, column)
        for i in range(9):
            for j in range(9):
                if self.cells[i][j].value == 0 and self.cells[i][j].sketched_value is None:
                    return i, j

    def check_board(self):  # checks whether Sudoku was done successfully or not
        print("self.board check board", self.board)
        print(GLOBAL_SELF_CORRECT_BOARD)
        for i in range(9):
            for j in range(9):
                if GLOBAL_SELF_CORRECT_BOARD[i][j] != self.board[i][j]:
                    return False
        return True
