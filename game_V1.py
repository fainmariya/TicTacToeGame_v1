import datetime
import json
import os
from tkinter import *
from tkinter.ttk import *

FIRST_PLAYER_SYMBOL = 'x'
SECOND_PLAYER_SYMBOL = '0'
current_player = FIRST_PLAYER_SYMBOL
saved_games_files = []

def create_game_board():
    # create gameboard
    global game_board
    for elmnt in game_board_frame.grid_slaves():  # master - slave 
        elmnt.grid_remove()
    size = int(board_size.get())
    
    game_board = [
        [Entry(master = game_board_frame, width=2, justify=CENTER) for i in range(size)] 
        for j in range(size) 
        ]

    # populate game_board_frame 
    for row in range(size):
        for col in range(size):
            game_board[row][col].bind('<KeyRelease>', input_control )
            game_board[row][col].grid(column=col, row=row, ipadx=1, ipady=1, padx=2, pady=2)
           
def input_control(evnt):
    global current_player, game_board
    current_widget = evnt.widget
    errors.config(text="", foreground="black")
    field_value = current_widget.get()
    # check x or 0  entered
    if field_value != current_player:
        # alert message
        errors.config(text="Incorrect player", foreground="red")
        # cleanup field
        current_widget.delete(0, END) 
        return
    
    current_widget.config(state = 'disabled')
    
    if winner_found(): # true / false
        # disable board
        for row in game_board:
            for e in row:
                e.config(state="disabled") # state: Literal['normal', 'disabled', 'readonly']
        
        # print message
        winner.config(text=f'Winner found: {current_player}')
        
        return
    
    if current_player == FIRST_PLAYER_SYMBOL: current_player = SECOND_PLAYER_SYMBOL
    else: current_player = FIRST_PLAYER_SYMBOL
        
def winner_found():
    # check rows -> winner in row?
    for row in game_board:
        if row[0].get() == '': continue
        if len(set(map(lambda e: e.get(), row))) == 1: return True

    # check cols -> winner in column?
    for column_number in range(len(game_board)):
        # if game_board[0][column_number].get() == '': continue
        temp_list = [game_board[r][column_number].get() for r in range(len(game_board))]
        # print (temp_list)
        if temp_list.count(current_player) == len(game_board): return True

    # check diagonals    
    temp_list = [ game_board[i][i].get() for i in range(len(game_board))]      
    if temp_list.count(current_player) == len(game_board): return True
    #
    temp_list = [ game_board[i][len(game_board)-1-i].get() for i in range(len(game_board))]      
    if temp_list.count(current_player) == len(game_board): return True
    return False  # Winner not found

def save_game():
    # collect data - > dict
    game_data = {}
    d_string = datetime.datetime.now().strftime('%Y_%m_%d_%H-%M-%S')
    game_data.update({"date":d_string})
    game_data.update({"player1_name": player1_name.get()})
    game_data.update({"player2_name":player2_name.get()})
    game_data.update({"current_player":current_player})
    matrix = [
       [game_board[r][c].get() for c in range (len(game_board))]
        for r in range (len(game_board))
    ]
    game_data.update({"game_board":matrix})
    # write file
    
    file_name = os.path.join( 
                            os.path.dirname(__file__), 
                            f'game_{d_string}_{player1_name.get()}_{player2_name.get()}.json')
    with open(file_name, 'w') as f:
        json.dump(game_data, f, indent=4)

def saved_games_list():
    for next_file in os.scandir(os.path.dirname(__file__)):
        if next_file.name.count('game_', 0, 5) > 0:
            saved_games_files.append(next_file.name)        
    print (saved_games_files) 
    saved_files_combo.config(values=saved_games_files) 
    combo_files.set(saved_games_files[0])  

def load_selected_game(e):
    print(f'Loading geme from file: {combo_files.get()}')
   

root_window = Tk()
root_window.title("Tic tac toe game")
controls_frame = Frame()
game_board_frame = Frame()
stat_frame = Frame()

# root window grid:
root_window.grid_columnconfigure(0, weight=0)
root_window.grid_columnconfigure(1, weight=1)
root_window.grid_rowconfigure(0, weight=0)
root_window.grid_rowconfigure(1, weight=1)
controls_frame.grid(column=0, row=0, columnspan=2, sticky=(W, E))
game_board_frame.grid(column=1, row=1, sticky=(W,E,N,S))
stat_frame.grid(column=0, row=1, sticky=(W,E,N,S))

# populate controls frame
Label(controls_frame, text="Board size: ").pack(side=LEFT, anchor='center', ipadx=10, ipady=5, padx=20, pady=10)
board_size = Entry(controls_frame, width=2, justify=CENTER)

board_size.pack(side=LEFT, anchor='center', ipadx=1, ipady=1)

Button(controls_frame, text="Create game board", command=create_game_board).pack(side=LEFT, anchor='center', ipadx=10, ipady=5, padx=20, pady=10)
Button(controls_frame, text="Save current game", command=save_game).pack(side=LEFT, anchor='center', ipadx=10, ipady=5, padx=20, pady=10)
Button(controls_frame, text="Get saved games", command=saved_games_list).pack(side=LEFT, anchor='center', ipadx=10, ipady=5, padx=20, pady=10)
combo_files = StringVar()
saved_files_combo = Combobox(controls_frame, values=saved_games_files, textvariable=combo_files)
saved_files_combo.bind('<<ComboboxSelected>>', load_selected_game)
saved_files_combo.pack(side=LEFT, anchor='center', ipadx=10, ipady=5, padx=20, pady=10)

# populate stat_frame
errors = Label(stat_frame)
errors.pack(anchor=W)
winner = Label(stat_frame)
winner.pack(anchor=W)
Label(stat_frame, text="Player1 name: ").pack(anchor=W)
player1_name = Entry(stat_frame)
player1_name.pack(anchor=W, ipadx=10, ipady=5, padx=20, pady=10)
Label(stat_frame, text="Player2 name: ").pack(anchor=W)
player2_name = Entry(stat_frame)
player2_name.pack(anchor=W, ipadx=10, ipady=5, padx=20, pady=10)

root_window.mainloop()