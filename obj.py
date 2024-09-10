import random
import tkinter as tk
from tkinter import messagebox
from scipy.spatial.distance import cityblock

class ChessGame:
    def __init__(self, root, size, cell_size):
        self.root = root
        self.size = size
        self.cell_size = cell_size
        self.canvas = tk.Canvas(root, width=size * cell_size, height=size * cell_size)
        self.canvas.pack()
        self.label = tk.Label(root, text="Use arrow keys to move")
        self.label.pack()

        self.count = 0
        self.goal_position = (random.randint(0, size - 1), random.randint(0, size - 1))
        self.player_position = (random.randint(0, size - 1), random.randint(0, size - 1))
        self.dt_start = self.distance(self.player_position, self.goal_position)

        self.draw_chessboard()
        self.draw_chess(self.player_position)
        self.update_status(f"Initial distance: {self.dt_start}")

        root.bind("<Up>", lambda event: self.move("N"))
        root.bind("<Down>", lambda event: self.move("S"))
        root.bind("<Left>", lambda event: self.move("W"))
        root.bind("<Right>", lambda event: self.move("E"))

    def draw_chessboard(self):
        for row in range(self.size):
            for col in range(self.size):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2)

    def draw_chess(self, pos):
        x, y = pos
        x1 = y * self.cell_size + 10
        y1 = x * self.cell_size + 10
        x2 = x1 + self.cell_size - 20
        y2 = y1 + self.cell_size - 20
        self.canvas.create_oval(x1, y1, x2, y2, fill="red", tags="chess_piece")

    def move(self, direction):
        x, y = self.player_position
        if direction == "N" and x > 0:
            self.player_position = (x - 1, y)
        elif direction == "S" and x < self.size - 1:
            self.player_position = (x + 1, y)
        elif direction == "W" and y > 0:
            self.player_position = (x, y - 1)
        elif direction == "E" and y < self.size - 1:
            self.player_position = (x, y + 1)
        else:
            self.update_status("Move out of bounds! Try again.")
            return
        self.update_game()

    def distance(self, a, b):
        return cityblock(a, b)

    def update_game(self):
        self.count += 1
        dt_end = self.distance(self.player_position, self.goal_position)
        if dt_end < self.dt_start:
            self.update_status(f"Good choice, closer! Distance: {dt_end}")
        else:
            self.update_status(f"Bad choice, farther! Distance: {dt_end}")
        self.dt_start = dt_end
        self.canvas.delete("chess_piece")
        self.draw_chess(self.player_position)
        if self.player_position == self.goal_position:
            self.game_over()

    def update_status(self, message):
        self.label.config(text=message)

    def game_over(self):
        messagebox.showinfo("Game Over", f"You found the salary in {self.count} steps!")
        self.root.quit()

root = tk.Tk()
root.title("Chess Game")
size = random.randint(5, 20)
cell_size = 50

game = ChessGame(root, size, cell_size)

root.mainloop()
