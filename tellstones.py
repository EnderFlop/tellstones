import time
import os
from sys import exit
import tkinter as tk
from tkinter import ttk

#Initalizing tkinter
root = tk.Tk() #Init frame
root.title("Tellstones") #Frame title
root.resizable(False,False) #Non-resizable
frame = tk.Frame(root, width=1280, height=500, background="#5B5956") #Size and background color
frame.grid(row=0, column=0, sticky="nesw") #Init grid
for y in range(16): #Init rows 0-15 for filling
  frame.grid_rowconfigure(y, weight=1)
for x in range(8): #Init columns 0-7 for buttons
  frame.grid_columnconfigure(x, weight=1)
frame.grid_propagate(False) #Disable window resizing for widgets
advance = tk.IntVar() #Var to track user input and return
string = tk.StringVar() #Same as advance, but a string

#ROW FORMATTING
#ROW 0-X is the tellstone line
#ROW X-14 is the task prompt.
#ROW 14 is the point tracker
#ROW 15 is the buttons home


class Tellstone:
  def __init__(self, name):
    self.name = name
    self.hidden = False
    self.is_on_mat = False
    self.mat_location = None


  def __str__(self):
    return f"{self.name}"


  def __repr__(self):
    return f"{self.name}"


  def hide(self):
    self.hidden = True


  def add_to_line(self, location):
    self.is_on_mat = True
    self.mat_location = location



class Line:
  def __init__(self):
    #self.line is a list of the stone in order, with a blank space if it is empty
    self.line = [" " for i in range(7)]
    #self.string is a string that is used for __repr__, that has a " . " for a blank spot, " Stone " for a hidden stone, and " (name) " for a visible stone.
    self.string = ""
    #The first stone will be placed in the middle, so set the current bounds to the middle of the list
    self.furthest_left = 3
    self.furthest_right = 3


  def __repr__(self):
    return (f"The line is currently:\n{self.string}")

  def is_empty(self):
    if self.string == " .  .  .  .  .  .  . ":
      print("The line is empty!")
      take_it_back_now_yall()
      return True
    return False

  #Updates self.string based on the current state of self.line
  def update_line(self):
    #Starts by resetting self.string
    self.string = ""
    #Iterates 7 times for the 7 spaces
    for i in range(7):
      #If the index is a Tellstone
      if type(self.line[i]) == Tellstone:
        #and it isn't hidden, add the name of the stone
        if self.line[i].hidden == False:
          self.string += " " + str(self.line[i]) + " "
        #if it is hidden, add the word "stone"
        if self.line[i].hidden == True:
          self.string += " Stone "
      #If it's not a Tellstone, just add a period to mark an empty spot
      else:
        self.string += " . "

  
  def add_stone(self):
    clear_window()
    update_instructions("Select a Tellstone to place on the line.")
    stone = stone_buttons("place")
    if self.string == " .  .  .  .  .  .  . ":
      location = 3
      self.line[location] = stone
      stone.add_to_line(location)
      self.update_line()
    else:
      #If the line isn't empty, get input from the user on whether to add the stone to the left or the right of the current line
      clear_window()
      update_instructions("Would you like it on the left or the right of the current stones?")
      left_or_right = left_right_buttons()
      #If it's left, add it to the left and move self.furthest_left to the left by 1. Check to see if there is space.
      if left_or_right == "Left":
        if self.furthest_left > 0:
          self.line[self.furthest_left - 1] = stone
          stone.add_to_line(self.furthest_left - 1)
          self.furthest_left -= 1
          self.update_line()
        else:
          take_it_back_now_yall()
      #If it's right, add it to the right and move self.furthest_right to the right by 1. Check to see if there is space.
      elif left_or_right == "Right":
        if self.furthest_right < 6:
          self.line[self.furthest_right + 1] = stone
          stone.add_to_line(self.furthest_right + 1)
          self.furthest_right += 1
          self.update_line()
        else:
          take_it_back_now_yall()

  
  def hide_stone(self):
    if not self.is_empty():
      #Asks for stone and makes sure it's on the line. If it is, it hides it.
      clear_window()
      update_instructions("Choose a stone to hide.")
      stone = hide_buttons()
      stone.hide()
      self.update_line()


  def swap_stones(self):
    clear_window()
    #Get the first stone to swap
    update_instructions("What is the position of the first stone you would like to swap?")
    first_stone = position_buttons(hidden = "swap")
    #Get the second stone to swap
    update_instructions("What is the position of the second stone you would like to swap?")
    second_stone = position_buttons(hidden = "swap", stone_index = first_stone)
    #Swaps the Tellstones and updates the line.
    self.line[first_stone], self.line[second_stone] = self.line[second_stone], self.line[first_stone]
    self.line[first_stone].mat_location = first_stone
    self.line[second_stone].mat_location = second_stone
    self.update_line()



  def peek(self):
    #If there wasn't a point last turn, only do position once.
    if next_player.point_last_turn == False:
      update_instructions("What position would you like to look at?")
      position = position_buttons("peek") #Hides non-Tellstones and visible stones
      clear_window()
      update_instructions(f"Only {current_player.name} should see this! Press continue when only you are looking.")
      confirm_button()
      clear_window()
      update_instructions(f"The stone in position {position + 1} is {self.line[position].name}.")
      confirm_button()
    #If there was a point last turn, you can peek at up to 3 stones.
    if next_player.point_last_turn == True:
      update_instructions(f"{next_player} scored a point last turn, so you can look at up to 3 stones.")
      confirm_button()
      _, hidden_stones = stones_on_mat() #Getting list of current hidden stones. Only second return is neccesary, "_" is a dummy
      num_hidden_stones = len(hidden_stones) #Number of hidden stones
      if num_hidden_stones > 3: #If there is more than 3, still only do 3
        num_hidden_stones = 3
      position_list = [] #List where the positions of chosen stones is stored
      position_string = "" #String printed at the end listing the positions and their stones
      for i in range(1,num_hidden_stones+1):
        clear_window()
        update_instructions(f"What position would you like to peek at? (Peek number {i})")
        position = position_buttons("peek", stones_list=position_list) #Hides non-Tellstones, visible stones, and stones already chosen
        position_list.append(position) #Adds the position chosen to the position_list
        position_string += f"The stone in position {position+1} is {line.line[position]}.\n" #Adds the stone and pos to the string
      update_instructions(f"Only {current_player.name} should see this! Press continue when only you are looking.") #Confirmation
      confirm_button()
      clear_window()
      update_instructions(position_string) #Prints the string of stones
      confirm_button()
    


  def challenge(self):
    if not self.is_empty():
      #Asks for position on the line, then check to see if there is a stone there that is hidden.
      clear_window()
      update_instructions(f"What position are you challenging {next_player} to name?")
      position = position_buttons(hidden="peek") #The peek draw funct also works for challenge's purpose
      clear_window()
      update_instructions(f"Ok {next_player}, what Tellstone do you think is there?")
      opponent_guess = stone_buttons() #This was originally (not hidden = disabled) but it's really funny to see someone pick a stone that is visible so
      clear_window()
      self.line[position].hidden = False #Shows stone and updates line
      self.update_line()
      if opponent_guess == line.line[position]: #If correct
        next_player.gain_point()
        update_instructions(f"Correct! Your guess, and the token at position {position}, is {line.line[position]}.\n{current_player} has {current_player.points} points, and {next_player} has {next_player.points} points.")
        confirm_button()
      else: #If incorrect
        current_player.gain_point()
        update_instructions(f"Ooh, tough luck. The token in position {position} was actually {line.line[position]}.\n{current_player} has {current_player.points} points, and {next_player} has {next_player.points} points.")
        confirm_button()

  def boast(self):
    if self.is_empty():
      return
    #if self.find_hidden_count() <= 0:
      print("There are no hidden stones dummy!")
      take_it_back_now_yall()
      return
    print(f"""{current_player} thinks they know all the face down stones! How do you repsond {next_player}?
    "Doubt" that they know all the pieces. If they name them all correctly, they instantly win. If they don't, you do!
    "Believe" that they probably do know all the pieces. This gives them one point, and they don't have to guess anything.
    "Boast" that YOU know all the pieces, and force {current_player} to either doubt or believe you.
    """)
    response = False
    while response == False:
      response = input("")
      response = self.boast_error_check(response)
    
    #This is the big boy function.
    if response == "doubt":
      print(f"{next_player} doesn't believe you know all the pieces {current_player}! Now you have to prove you do!")
      #Create list of hidden stone indexes
      hidden_list = [stone.mat_location for stone in self.line if isinstance(stone, Tellstone) and stone.hidden == True]
      print(self)
      correct_count = 0
      #For each index in the list
      for stone_index in hidden_list:
        #Get a guess from the user on what stone is in that position
        stone_guess = input(f"The Tellstone in position {stone_index + 1} is: ")
        stone_guess = stone_guess.lower()
        #If the guess is in the stone dictionary
        if stone_guess in stones_dict.keys():
          stone_guess = stones_dict[stone_guess]
        if self.line[stone_index] == stone_guess:
          #Print correct and update the line so that stone is now visible. Reprint the line and add 1 to correct_count
          print("Correct!")
          self.line[stone_index].hidden = False
          self.update_line()
          correct_count += 1
          print(self)
        #Otherwise, end the game. Reveal all stones, print the line, and give the other player an absurd amount of points to rub it in.
        else:
          input(f"\n\nTough luck. That Tellstone was {self.line[stone_index]}. {next_player} wins! Press ENTER to continue.\n\n")
          for value in stones_dict.values():
            value.hidden = False
          self.update_line()
          for i in range(9000):
            next_player.gain_point()
          break
      #If you manage to get them all right, you get a stupid amount of points and you win automatically.
      if correct_count == len(hidden_list):
        input(f"\n\nAmazing! {current_player} got them all right! They win! Press ENTER to continue.\n\n")
        for i in range(9000):
          current_player.gain_point()
    
    if response == "believe":
      print(f"{next_player} believes that {current_player} knows where all the pieces are, and gives up a point.")
      current_player.gain_point()
      input(f"{current_player} has {current_player.points} points, and {next_player} has {next_player.points} points. Press ENTER to continue.")



    #This is a sort of recursion, where next player counters with another boast, and two more options are presented.
    if response == "boast":
      print(f"{next_player} counters with their own boast!")
      print(f"""{current_player}, you can either:
    "Doubt" that they know all the pieces. If they name them all correctly, they instantly win. If they don't, you do!
    "Believe" that they probably do know all the pieces. This gives them one point, and they don't have to guess anything.
    """)
      response = False
      while response == False:
        response = input("")
        response = self.boast_error_check(response)
  
      if response == "doubt":
        print(f"{current_player} doesn't believe you know all the pieces {next_player}! Time to put your points where your mouth is.")
        #Create list of hidden stone indexes
        hidden_list = [stone.mat_location for stone in self.line if isinstance(stone, Tellstone) and stone.hidden == True]
        print(self)
        correct_count = 0
        #For each index in the list
        for stone_index in hidden_list:
          #Get a guess from the user on what stone is in that position
          stone_guess = input(f"The Tellstone in position {stone_index + 1} is: ")
          stone_guess = stone_guess.lower()
          #If the guess is in the stone dictionary
          if stone_guess in stones_dict.keys():
            stone_guess = stones_dict[stone_guess]
          if self.line[stone_index] == stone_guess:
            #Print correct and update the line so that stone is now visible. Reprint the line and add 1 to correct_count
            print("Correct!")
            self.line[stone_index].hidden = False
            self.update_line()
            correct_count += 1
            print(self)
          #Otherwise, end the game. Reveal all stones, print the line, and give the other player an absurd amount of points to rub it in.
          else:
            input(f"\n\nTough luck. That Tellstone was {self.line[stone_index]}. {current_player} wins! Press ENTER to continue.\n\n")
            for value in stones_dict.values():
              value.hidden = False
            self.update_line()
            for i in range(9000):
              current_player.gain_point()
            break
        #If you manage to get them all right, you get a stupid amount of points and you win automatically.
        if correct_count == len(hidden_list):
          input(f"\n\nAmazing! {next_player} got them all right! They win! Press ENTER to continue.\n\n")
          for i in range(9000):
            next_player.gain_point()
      
      if response == "believe":
        print(f"{current_player} believes that {next_player} knows where all the pieces are, and gives up a point.")
        next_player.gain_point()
        input(f"{current_player} has {current_player.points} points, and {next_player} has {next_player.points} points. Press ENTER to continue.")


  def boast_error_check(self, input):
    try:
      input = int(input)
      print("Not a valid option. Try again.")
      return False
    except:
      input = input.lower()
      if input == "doubt" or input == "believe" or input == "boast":
        return input
      else:
        print("Not a valid option. Try again.")
        return False
      

class Player:
  def __init__(self, name):
    self.name = name
    self.points = 0
    self.point_last_turn = False
  def __repr__(self):
    return self.name
  def gain_point(self):
    self.points += 1
    self.point_last_turn = True



#Initalizing all the stones
crown = Tellstone("The Crown")
shield = Tellstone("The Shield")
sword = Tellstone("The Sword")
flag = Tellstone("The Flag")
knight = Tellstone("The Knight")
hammer = Tellstone("The Hammer")
scales = Tellstone("The Scales")

#Initalizing dict of strings to class names:
stones_dict = {
  "The Crown": crown,
  "The Shield": shield,
  "The Sword": sword,
  "The Flag": flag,
  "The Knight": knight,
  "The Hammer": hammer,
  "The Scales": scales,
}


#Initalizing Line and updating it to make self.list and self.string have the correct values for an empty board.
line = Line()
line.update_line()

#Initalizing players
player_one = Player("Player One")
player_two = Player("Player Two")

#Player turn variable
global player_turn
player_turn = 0

#Player turn function so only certain commands advance the turn.
def player_turn_advance():
  global player_turn
  player_turn += 1

#For if a player messes up an input, it doesnt advance the turn.
def take_it_back_now_yall():
  input("Press ENTER to continue.")
  global player_turn
  player_turn -= 1



#      ::BUTTON DRAW FUNCTIONS BELOW::
global x_spread
x_spread = 6
global row
row = 15
def position_buttons(hidden=None, stone_index=None, stones_list=[]): #Writes number 1-7 for the 7 postions.
  global x_spread
  global row
  for i in range(7):
    button = tk.Button(frame, text=str(i+1), command=lambda i=i:[advance.set(i)])
    button.grid(padx=x_spread, row=row, column=i, sticky="nsew")
    if hidden == "swap": #In the swap funct, if the pos isn't a Tellstone, disable
      if not isinstance(line.line[i], Tellstone) or stone_index == i:
        button["state"] = "disabled"
    elif hidden == "peek": #In the peek funct, if the pos isnt hidden, or if the pos has already been choses in the 3 pos peek, disable. Also used for Challenge
      if not isinstance(line.line[i], Tellstone) or line.line[i].hidden == False or i in stones_list:
        button["state"] = "disabled"
  button.wait_variable(advance)
  return advance.get()

def hide_buttons(): #This only writes the buttons for the visible stones on the line in their positions, so as not to give away any hints.
  column = 0
  global x_spread
  global row
  for stone in line.line:
    if isinstance(stone, Tellstone):
      if stone.is_on_mat == True:
        if stone.hidden == False:
          stone_name = stone.name
          button = tk.Button(frame, text=stone, command=lambda stone_name=stone_name:[string.set(stone_name)])
          button.grid(padx=x_spread, row=row, column=column, sticky= "nsew")
    column += 1
  button.wait_variable(string)
  return stones_dict[string.get()]

def confirm_button(): #Simple funct that draws a massive continue button. Just used to show instuctional text and wait for user to understand.
  global row
  button = tk.Button(frame, text="Continue", command=lambda:[advance.set(1)])
  button.grid(row=row, column=0, columnspan=8, sticky="nsew")
  button.wait_variable(advance)

def stone_buttons(hidden=None): #This writes the 7 stones as buttons. It takes an arg, and disables certain buttons accordingly
  column = 0
  global x_spread
  global row
  for name, value in stones_dict.items():
    button = tk.Button(frame, text=name, command=lambda name=name:[string.set(name)])
    button.grid(padx=x_spread, row=row, column=column, sticky="nsew")
    if hidden == "place": #If it's already on the mat, disable
      if value.is_on_mat == True:
        button["state"] = "disabled"
    column += 1
  button.wait_variable(string)
  return stones_dict[string.get()]

def left_right_buttons(): #These are the buttons that let you choose left or right when you place a stone.
  global x_spread
  global row
  left = tk.Button(frame, text="Left", command=lambda:[string.set("Left")])
  left.grid(padx=x_spread, row=row, column=0, sticky="nsew", columnspan=4)
  right = tk.Button(frame, text="Right", command=lambda:[string.set("Right")])
  right.grid(padx=x_spread, row=row, column=4, sticky="nsew", columnspan=4)
  if line.furthest_left == 0:
    left["state"] = "disabled"
  if line.furthest_right == 6:
    right["state"] = "disabled"
  left.wait_variable(string)
  return string.get()

def action_buttons(): #This creates and places all of the buttons used for declaring your first action. Also follows logic to disable unusable buttons
  global x_spread
  global row
  global string
  #Prints a help message on the left of the screen that stays there for the next action
  help = tk.Button(frame, text="Help", command=lambda:[update_instructions("""You can do the following actions:
"Place" a stone from the pool onto the line, to the left or right of the current stones in play
"Hide" a face-up stone that is on the line by turning it face-down.
"Swap" two stones around.
"Peek" at a stone that is currently hidden.
"Challenge" your opponent to name any face-down stone.
"Boast" that you know all the face-down stones for an instant victory!"""), advance.set(1), string.set("True")])
  help.grid(padx=x_spread, row=row, column=0, sticky="nsew")

  stones_list, hidden_stones_list = stones_on_mat() #Get a list the length of either the stones on the mat or the hidden stones.

  place = tk.Button(frame, text="Place", command=lambda:[line.add_stone(), advance.set(1)])
  place.grid(padx=x_spread, row=row, column=1, sticky="nsew")
  if len(stones_list) == 7: #If there are 7 stones on the mat, disable
    place["state"] = "disabled"

  hide = tk.Button(frame, text="Hide", command=lambda:[line.hide_stone(), advance.set(1)])
  hide.grid(padx=x_spread, row=row, column=2, sticky="nsew")
  if len(stones_list) == 0 or len(hidden_stones_list) == len(stones_list): #If there are 0 stones or all the stones are hidden, disable
    hide["state"] = "disabled"
  
  swap = tk.Button(frame, text="Swap", command=lambda:[line.swap_stones(), advance.set(1)])
  swap.grid(padx=x_spread, row=row, column=3, sticky="nsew") 
  if len(stones_list) <= 1: #If there is less than 2 stones, disable
    swap["state"] = "disabled"


  peek = tk.Button(frame, text="Peek", command=lambda:[line.peek(), advance.set(1)])
  peek.grid(padx=x_spread, row=row, column=4, sticky="nsew")
  if len(hidden_stones_list) == 0: #If there are no hidden stones, disable
    peek["state"] = "disabled"

  challenge = tk.Button(frame, text="Challenge", command=lambda:[line.challenge(), advance.set(1)])
  challenge.grid(padx=x_spread, row=row, column=5, sticky="nsew")
  if len(hidden_stones_list) == 0: #If there are no hidden stones, disable
    challenge["state"] = "disabled"

  boast = tk.Button(frame, text="Boast", command=lambda:[line.boast(), advance.set(1)])
  boast.grid(padx=x_spread, row=row, column=6, sticky="nsew")
  if len(hidden_stones_list) == 0: #If there are no hidden stones, disable
    boast["state"] = "disabled"


  exit = tk.Button(frame, text="Exit", command=lambda:[root.destroy(), advance.set(1)])
  exit.grid(padx=x_spread, row=row, column=7, sticky="se")
  help.wait_variable(advance)

def update_instructions(string):
  print_string = tk.Label(frame, text=string, background="#5B5956", anchor="w", justify=tk.LEFT)
  print_string.grid(row=row-2, rowspan=1, column=0, columnspan=8, sticky="w")

def stones_on_mat():
  return ["stone" for stone in line.line if isinstance(stone, Tellstone)], ["hidden stone" for stone in line.line if isinstance(stone, Tellstone) and stone.hidden == True]

global game_over
game_over = 0
global current_player
current_player = player_one
global next_player
next_player = player_two
#Game begins below
def gameplay_loop():
  global x_spread
  global row
  global game_over
  global current_player
  global next_player
  #Vars for button setup
  #Clear and print the line
  visible_line = tk.Label(frame, text=line, bg="#5B5956")
  visible_line.grid(row=0, rowspan=10, column=0, columnspan=8, sticky="ew")
  #Alternate player turns and turn their point_last_turn value to False.
  if player_turn % 2 == 0:
    current_player = player_one
    current_player.point_last_turn = False
    next_player = player_two
  else:
    current_player = player_two
    current_player.point_last_turn = False
    next_player = player_one
  #Check to see if a player has won
  if current_player.points >= 3:
    clear_window()
    update_instructions(f"Game over! {current_player.name} reached {current_player.points} points!")
    game_over = 1
  if next_player.points >= 3:
    clear_window()
    update_instructions(f"Game over! {next_player.name} reached {next_player.points} points!")
    game_over = 1
  #Reset var for input loop.
  if game_over == 0:
    background_label = tk.Label(frame, bg="#787774")
    background_label.grid(row=row-1, column=0, rowspan=2, columnspan=8, sticky="news")
    label = tk.Label(frame, text=f"What would you like to do {current_player}? You have {current_player.points} points. {next_player} has {next_player.points} points.", bg="#787774")
    label.grid(row=row-1, column=0, columnspan=8, sticky="new")
    action_buttons()
    if string.get() != "True": #If "Help" was the last action, don't clear the console. This gives the user a chance to read the text.
      clear_window()



def all_children(window):
    _list = window.winfo_children()
    for item in _list :
        if item.winfo_children() :
            _list.extend(item.winfo_children())
    return _list
def clear_window():
  global row
  widget_list = all_children(frame)
  for item in widget_list:
    if isinstance(item, tk.Button):
      item.grid_forget()
    grid_list = frame.grid_slaves(row=row-2, column=0)
    for widget in grid_list:
      widget.grid_forget()


while game_over == 0:
  gameplay_loop()
  if game_over == 1:
    play_again = input("Thank you for playing! Play again (y/n)? ")
    play_again = play_again.lower()
    if play_again == "y":
      #This is probably a shit way to do this but I hope it works.
      #Reinitalizing all the classes in order to reset them to default states.
      #Initalizing all the stones
      crown = Tellstone("The Crown")
      shield = Tellstone("The Shield")
      sword = Tellstone("The Sword")
      flag = Tellstone("The Flag")
      knight = Tellstone("The Knight")
      hammer = Tellstone("The Hammer")
      scales = Tellstone("The Scales")

      #Initalizing Line and updating it to make self.list and self.string have the correct values for an empty board.
      line = Line()
      line.update_line()

      #Initalizing players
      player_one = Player("Player One")
      player_two = Player("Player Two")

      player_turn = 0
      game_over = 0
    else:
      print("Goodbye!")
