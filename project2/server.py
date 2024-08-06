import tkinter as tk
from tkinter import messagebox
import numpy as np
from socket import *
from threading import Thread

ROW_COUNT = 7
COLUMN_COUNT = 6
player_turn = 1
game_over = False
board = np.zeros((ROW_COUNT, COLUMN_COUNT))
window = tk.Tk()
buttons = []
waiting_for_turn = False
s = socket(AF_INET, SOCK_STREAM)

def create_gui():
    global window, buttons
    window.title("Connect 4")
    window.geometry("450x550")
    note_label = tk.Label(window, text="Player 1 (Red) 'X' ", font=("Helvetica", 12, "bold"))
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
    global player_turn, game_over, waiting_for_turn
    if game_over or waiting_for_turn or player_turn != 1:  # Player 1's turn
        return
    waiting_for_turn = True  # Set waiting_for_turn to True to indicate waiting for the other player's turn
    for i in range(ROW_COUNT - 1, -1, -1):
        if board[i][column] == 0:
            board[i][column] = player_turn
            buttons[i][column].config(text="X", bg="red")
            send_play(column)
            if check_win(player_turn):
                game_over = True
                show_end_message(player_turn)
            player_turn = 2  # Switch to Player 2's turn
            break

def check_win(player):
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == player and board[r][c + 1] == player and board[r][c + 2] == player and board[r][c + 3] == player:
                return True
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == player and board[r + 1][c] == player and board[r + 2][c] == player and board[r + 3][c] == player:
                return True
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == player and board[r + 1][c + 1] == player and board[r + 2][c + 2] == player and board[r + 3][c + 3] == player:
                return True
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == player and board[r - 1][c + 1] == player and board[r - 2][c + 2] == player and board[r - 3][c + 3] == player:
                return True
    return False

def send_reset():
    reset_msg = "RESET"
    reset_msg_encoded = reset_msg.encode()
    c.send(reset_msg_encoded)

def reset_game():
    global board, game_over, player_turn, waiting_for_turn
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    game_over = False
    player_turn = 1
    waiting_for_turn = False  # Reset waiting_for_turn when resetting the game
    for i in range(ROW_COUNT):
        for j in range(COLUMN_COUNT):
            buttons[i][j].config(text="", bg="blue")
    # Send reset message to the client
    send_reset()

def show_end_message(winner):
    
    play_again = messagebox.showinfo("Game Over", "Player " + str(player_turn) + " wins!")
    window.destroy()
    c.close()
    

def send_play(column):
    column_str = str(column)
    column_str_encoded = column_str.encode()
    c.send(column_str_encoded)

def handle_play(column):
    global player_turn, waiting_for_turn
    waiting_for_turn = False  # Set waiting_for_turn to False when handling the other player's move
    column = int(column)
    for i in range(ROW_COUNT - 1, -1, -1):
        if board[i][column] == 0:
            board[i][column] = player_turn
            buttons[i][column].config(text="O", bg="yellow")
            if check_win(player_turn):
                game_over = True
                show_end_message(player_turn)
            player_turn = 1  # Switch to Player 1's turn
            break

def apply_play(p):
    p = p.decode()
    p = int(p)
    handle_play(p)

def receive_message(c):
    while True:
        p = c.recv(10)
        apply_play(p)

def run():
    window.mainloop()

if __name__ == "__main__":
    create_gui()

    s.bind(('127.0.0.1', 6556))
    s.listen(5)
    c = None

    def handle_client():
        global c
        c, ad = s.accept()
        receive = Thread(target=receive_message, args=[c,])
        receive.start()

    def receive_message(c):
        try:
            while True:
                p = c.recv(10)
                apply_play(p)
        except ConnectionAbortedError:
            print("Connection closed by the client.")

    acc = Thread(target=handle_client)
    acc.start()
    run()
