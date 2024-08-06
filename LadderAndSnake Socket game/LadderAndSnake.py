import tkinter as tk
from tkinter import messagebox
import random

board = {
    1: 38,
    4: 14,
    8: 30,
    21: 42,
    28: 74,
    50: 67,
    71: 92,
    80: 99,
    32: 10,
    34: 6,
    48: 26,
    63: 18,
    88: 24,
    95: 56,
    97: 78
}

def roll_dice():
    result = random.randint(1, 6)
    label_dice_result.config(text=f"Dice Result: {result}")
    return result

def move_player(player, steps):
    new_position = player + steps
    if new_position > 100:
        player = new_position - steps
    else:
        player = new_position
    if player in board:
        player = board[player]
    return player


def is_game_over(player):
    return player == 100


def handle_player_turn():
    global current_player
    global player1_position
    global player2_position

    steps = roll_dice()
    if current_player == 1:
        player1_position = move_player(player1_position, steps)
        if is_game_over(player1_position):
            messagebox.showinfo("Game Over", "Congratulations! Score 100 Player 1 'blue' wins!")
            play_again = messagebox.askyesno("Play Again?", "Do you want to play again?")
            if play_again:
                reset_game()
            else:
                window.destroy()  
        else:
            update_player_position_buttons()
            label_player1_position.config(text=f"Player 1 'blue' Score ({steps}) : {player1_position}")
            current_player = 2
            label_current_player.config(text="Current Player: Player 2 'red'")
    else:
        player2_position = move_player(player2_position, steps)
        if is_game_over(player2_position):
            messagebox.showinfo("Game Over", "Congratulations! Score 100 Player 2 'red' wins!")
            play_again = messagebox.askyesno("Play Again?", "Do you want to play again?")
            if play_again:
                reset_game()
            else:
                window.destroy()  
        else:
            update_player_position_buttons()
            label_player2_position.config(text=f"Player 2 'red' Score ({steps}) : {player2_position}")
            current_player = 1
            label_current_player.config(text="Current Player: Player 1 'blue'")


def reset_game():
    global player1_position
    global player2_position
    global current_player
    
    player1_position = 0
    player2_position = 0
    current_player = 1
    update_player_position_buttons()
    label_current_player.config(text="Current Player: Player 1 'blue'")
    label_player1_position.config(text="Player 1 'blue' Score : 0")
    label_player2_position.config(text="Player 2 'red' Score : 0")



def update_player_position_buttons():
    button_player1.config(bg="blue" )
    button_player2.config(bg="red" )
    button_player1.grid(row=9 - player1_position // 10, column=player1_position % 10)
    button_player2.grid(row=9 - player2_position // 10, column=player2_position % 10)



window  = tk.Tk()
window.title("Snake and Ladder Game")
window.configure(bg="lightblue")  



label_player = tk.Label(window , text="player 1 window")
label_player.grid(row=17, columnspan=10)

current_player1 = tk.Button(window , text="", width=1, height=1 ,bg="blue", state=tk.DISABLED)
current_player1.grid(row=12, columnspan=7)

current_player2 = tk.Button(window , text="", width=1, height=1 ,bg="red", state=tk.DISABLED)
current_player2.grid(row=13, columnspan=7)

label_current_player = tk.Label(window , text="Current Player: Player 1 'blue'")
label_current_player.grid(row=11, columnspan=10)

label_player1_position = tk.Label(window , text="Player 1 'blue' Position Score (0) : 0")
label_player1_position.grid(row=12, columnspan=10)

label_player2_position = tk.Label(window , text="Player 2 'red' Position Score (0) : 0")
label_player2_position.grid(row=13, columnspan=10)

button_roll_dice = tk.Button(window , text="Roll Dice", command=handle_player_turn)
button_roll_dice.grid(row=15, columnspan=2)

label_dice_result = tk.Label(window , text="Dice Result: ")
label_dice_result.grid(row=16, columnspan=2)

button_reset = tk.Button(window , text="Reset Game",bg="black",fg="white",width=9, height=2 ,command=reset_game)
button_reset.grid(row=15, column=8)



buttons_board = [[tk.Button(window , text="", width=6, height=2, state=tk.DISABLED,bg="lightblue") for _ in range(10)] for _ in range(10)]

counter = 0
for i in range(10):
    for j in range(10):
        buttons_board[i][j].config(text=str(counter),font=("bold"))
        buttons_board[i][j].grid(row=9-i, column=j)
        counter += 1


buttons_board[0][1].config(text="1-->38",bg="#90EE90")
buttons_board[0][4].config(text="4-->14",bg="#90EE90")
buttons_board[0][8].config(text="8-->30",bg="#90EE90")
buttons_board[2][1].config(text="21-->42",bg="#90EE90")
buttons_board[2][8].config(text="28-->74",bg="#90EE90")
buttons_board[5][0].config(text="50-->67",bg="#90EE90")
buttons_board[7][1].config(text="71-->92",bg="#90EE90")
buttons_board[8][0].config(text="80-->99",bg="#90EE90")
buttons_board[3][2].config(text="32-->10",bg="#FFB6C1")
buttons_board[3][4].config(text="34-->6",bg="#FFB6C1")
buttons_board[4][8].config(text="48-->26",bg="#FFB6C1")
buttons_board[6][3].config(text="63-->18",bg="#FFB6C1")
buttons_board[8][8].config(text="88-->24",bg="#FFB6C1")
buttons_board[9][5].config(text="95-->56",bg="#FFB6C1")
buttons_board[9][7].config(text="97-->78",bg="#FFB6C1")
    

button_player1 = tk.Button(window , text="", width=4, height=2, state=tk.DISABLED)
button_player2 = tk.Button(window , text="", width=4, height=2, state=tk.DISABLED)

player1_position = 0
player2_position = 0
current_player = 1

update_player_position_buttons()
window.mainloop()




