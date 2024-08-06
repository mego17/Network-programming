import tkinter as tk
from tkinter import messagebox
import numpy as np

ROW_COUNT = 7
COLUMN_COUNT = 6
player_turn = 1
game_over = False
board = np.zeros((ROW_COUNT, COLUMN_COUNT))
window = tk.Tk()
buttons = []

def create_gui():
    global window, buttons
    window.title("Connect 4")
    window.geometry("450x550")
    note_label = tk.Label(window, text="Player 1 (Red) - Player 2 (Yellow)", font=("Helvetica", 12, "bold"))
    note_label.grid(row=0, columnspan=COLUMN_COUNT)
    for i in range(ROW_COUNT):
        row = []
        for j in range(COLUMN_COUNT):
            button = tk.Button(window, command=lambda row=i, column=j: click(row, column), bg="blue", height=3, width=6)
            button.grid(row=i + 1, column=j)
            row.append(button)
        buttons.append(row)
    reset_button = tk.Button(window, text="Reset", bg="black", fg="white", width=5, height=1, command=reset_game)
    reset_button.grid(row=ROW_COUNT + 1, columnspan=COLUMN_COUNT)

def click(row, column):
    global player_turn, game_over
    if game_over:
        return
    for i in range(ROW_COUNT - 1, -1, -1):
        if board[i][column] == 0:
            board[i][column] = player_turn
            buttons[i][column].config(text="X" if player_turn == 1 else "O", bg="red" if player_turn == 1 else "yellow")
            if check_win():
                game_over = True
                show_end_message()
            player_turn = 3 - player_turn
            break

def check_win():
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == player_turn and board[r][c + 1] == player_turn and board[r][c + 2] == player_turn and board[r][c + 3] == player_turn:
                return True
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == player_turn and board[r + 1][c] == player_turn and board[r + 2][c] == player_turn and board[r + 3][c] == player_turn:
                return True
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == player_turn and board[r + 1][c + 1] == player_turn and board[r + 2][c + 2] == player_turn and board[r + 3][c + 3] == player_turn:
                return True
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == player_turn and board[r - 1][c + 1] == player_turn and board[r - 2][c + 2] == player_turn and board[r - 3][c + 3] == player_turn:
                return True

def reset_game():
    global board, game_over, player_turn
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    game_over = False
    player_turn = 1
    for i in range(ROW_COUNT):
        for j in range(COLUMN_COUNT):
            buttons[i][j].config(text="", bg="SystemButtonFace")

def show_end_message():
    global player_turn
    play_again = messagebox.askyesno("Game Over", "Player " + str(player_turn) + " wins!\nDo you want to play again?")
    if play_again:
        reset_game()
    else:
        window.destroy()

def run():
    window.mainloop()

if __name__ == "__main__":
    create_gui()
    run()
