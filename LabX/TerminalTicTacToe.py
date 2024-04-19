import os
import sys
import time
import random
import keyboard

class TerminalTicTacToe:
    def __init__(self, num_players, player_names, grid_size, player_symbols=None):
        if num_players < 2:
            raise ValueError("Number of players must be at least 2.")
        if num_players > 4:
            raise ValueError("Number of players cannot exceed 4.")
        if grid_size < 5:
            raise ValueError("Grid size must be at least 5.")
        if grid_size > 25:
            raise ValueError("Grid size cannot exceed 25.")

        self.num_players = num_players
        self.player_names = player_names
        self.grid_size = grid_size
        self.current_player_index = 0
        self.current_player = player_names[self.current_player_index]
        self.board = [[' ' for _ in range(grid_size)] for _ in range(grid_size)]
        self.symbols = ['#', '$', '%', '&']  # Default symbols for players
        if player_symbols is None:
            random.shuffle(self.symbols)
            self.player_symbols = {player: symbol for player, symbol in zip(player_names, self.symbols)}
        else:
            self.player_symbols = player_symbols
        self.moves_left = grid_size * grid_size

    def display_board(self, selected_row, selected_col):
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear the terminal
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                cell = f"| {self.board[i][j]} "
                if i == selected_row and j == selected_col:
                    cell = f"\033[7m{cell}\033[0m"  # Highlight selected cell
                print(cell, end="")
            print("|")
            print("_ _ " * self.grid_size + "_ _ ")

    def move_cursor(self, direction, current_row, current_col):
        if direction == 'up' and current_row > 0:
            return current_row - 1, current_col
        elif direction == 'down' and current_row < self.grid_size - 1:
            return current_row + 1, current_col
        elif direction == 'left' and current_col > 0:
            return current_row, current_col - 1
        elif direction == 'right' and current_col < self.grid_size - 1:
            return current_row, current_col + 1
        return current_row, current_col  # Return current position if movement is not possible

    def play(self):
        current_row, current_col = 0, 0
        while True:
            self.display_board(current_row, current_col)
            print(f"{self.current_player}'s turn. Use arrow keys to move, Enter to select.")
            key_pressed = keyboard.read_event(suppress=True).name
            if key_pressed == 'enter':
                result, winner, _ = self.make_move(current_row, current_col)
                if result == 'win':
                    self.display_board(current_row, current_col)
                    print(f"Congratulations {winner}! You won!")
                    break
                elif result == 'draw':
                    self.display_board(current_row, current_col)
                    print("It's a draw!")
                    break
            elif key_pressed in ['up', 'down', 'left', 'right']:
                current_row, current_col = self.move_cursor(key_pressed, current_row, current_col)

    def make_move(self, row, col):
        if self.board[row][col] != ' ':
            return 'occupied', None, []

        self.board[row][col] = self.player_symbols[self.current_player]
        self.moves_left -= 1

        if self.check_victory(row, col):
            return 'win', self.current_player, []

        if self.moves_left == 0:
            return 'draw', None, []

        self.current_player_index = (self.current_player_index + 1) % self.num_players
        self.current_player = self.player_names[self.current_player_index]
        return 'success', None, []

    def check_victory(self, row, col):
        symbol = self.board[row][col]
        min_symbols_for_victory = (self.grid_size + 1) // 2

        # Check horizontal
        count = 1
        for c in range(col + 1, self.grid_size):
            if self.board[row][c] == symbol:
                count += 1
            else:
                break
        for c in range(col - 1, -1, -1):
            if self.board[row][c] == symbol:
                count += 1
            else:
                break
        if count >= min_symbols_for_victory:
            return True

        # Check vertical
        count = 1
        for r in range(row + 1, self.grid_size):
            if self.board[r][col] == symbol:
                count += 1
            else:
                break
        for r in range(row - 1, -1, -1):
            if self.board[r][col] == symbol:
                count += 1
            else:
                break
        if count >= min_symbols_for_victory:
            return True

        # Check diagonal (top-left to bottom-right)
        count = 1
        for i in range(1, min(row, col) + 1):
            if self.board[row - i][col - i] == symbol:
                count += 1
            else:
                break
        for i in range(1, min(self.grid_size - row, self.grid_size - col)):
            if self.board[row + i][col + i] == symbol:
                count += 1
            else:
                break
        if count >= min_symbols_for_victory:
            return True

        # Check diagonal (top-right to bottom-left)
        count = 1
        for i in range(1, min(row, self.grid_size - col - 1) + 1):
            if self.board[row - i][col + i] == symbol:
                count += 1
            else:
                break
        for i in range(1, min(self.grid_size - row, col + 1)):
            if self.board[row + i][col - i] == symbol:
                count += 1
            else:
                break
        if count >= min_symbols_for_victory:
            return True

        return False

if __name__ == "__main__":
    num_players = int(input("Enter number of players (2 to 4): "))
    player_names = [input(f"Enter name for player {i+1}: ") for i in range(num_players)]
    grid_size = int(input("Enter grid size (5 to 25): "))

    game = TerminalTicTacToe(num_players, player_names, grid_size)
    game.play()
