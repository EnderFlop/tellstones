import time
import sys
import os

#Initalizing console clearer function.
clear = lambda: os.system("cls")

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
    stone = input("What stone would you like to place on the line? ")
    stone = stone.lower()
    if stone in stones_dict.keys():
      stone = stones_dict[stone]
    else:
      print(f"{stone} isn't a valid stone. Did you remember to put 'the' before it?")
      take_it_back_now_yall()
      return
    if stone.is_on_mat == True:
      print(f"{stone} is already on the line!")
      take_it_back_now_yall()
      return
    #If the line is empty, add the stone to the middle
    if self.string == " .  .  .  .  .  .  . ":
      location = 3
      self.line[location] = stone
      stone.add_to_line(location)
      self.update_line()
    else:
      #If the line isn't empty, get input from the user on whether to add the stone to the left or the right of the current line
      left_or_right = input(f"Add {stone} to the left or right of the current line? (l/r) ")
      #If it's left, add it to the left and move self.furthest_left to the left by 1. Check to see if there is space.
      if left_or_right == "l":
        if self.furthest_left > 0:
          self.line[self.furthest_left - 1] = stone
          stone.add_to_line(self.furthest_left - 1)
          self.furthest_left -= 1
          self.update_line()
        else:
          print("That's off the line!")
          take_it_back_now_yall()
      #If it's right, add it to the right and move self.furthest_right to the right by 1. Check to see if there is space.
      elif left_or_right == "r":
        if self.furthest_right < 6:
          self.line[self.furthest_right + 1] = stone
          stone.add_to_line(self.furthest_right + 1)
          self.furthest_right += 1
          self.update_line()
        else:
          print("That's off the line!")
          take_it_back_now_yall()
      elif left_or_right != "r" or "l":
        print("Not a valid input.")
        take_it_back_now_yall()

  
  def hide_stone(self):
    if not self.is_empty():
      #Asks for stone and makes sure it's on the line. If it is, it hides it.
      stone = input("What stone would you like to hide? ")
      stone = stone.lower()
      if stone in stones_dict.keys():
        stone = stones_dict[stone]
        if stone.is_on_mat == True:
          stone.hide()
          self.update_line()
        else:
          print("That stone isn't on the mat!")
          take_it_back_now_yall()
      else:
        print(f"{stone} isn't a valid stone. Did you remember to put 'the' before it?")
        take_it_back_now_yall()

  def swap_stones(self):
    #begin by iterating through the items in self.line and making sure there are at least 2 tellstones.
    tellstone_count = 0
    for index in range(7):
      if isinstance(self.line[index], Tellstone):
        tellstone_count += 1
    if tellstone_count >= 2:
      #Get the first stone to swap
      first_stone = input("What is the position of the first stone you would like to swap? ")
      try:
        first_stone = int(first_stone)
      except ValueError:
        print("Input must be a number!")
        take_it_back_now_yall()
        return
      if first_stone not in range(1,8):
        print("Please use a number 1-7")
        take_it_back_now_yall()
        return
      #The -1 is to change 1-7 to 0-6 for QoL.
      if isinstance(self.line[first_stone - 1], Tellstone):
        first_index = first_stone - 1
      else:
        print("There isn't a Tellstone there!")
        take_it_back_now_yall()
        return
      #Get the second stone to swap
      second_stone = input("What is the position of the other stone you would like to swap? ")
      try:
        second_stone = int(second_stone)
      except ValueError:
        print("Input must be a number!")
        take_it_back_now_yall()
        return
      if second_stone not in range(1,8):
        print("Please use a number 1-7")
        take_it_back_now_yall()
        return
      #The -1 is to change 1-7 to 0-6 for QoL.
      if isinstance(self.line[second_stone - 1], Tellstone):
        second_index = second_stone - 1
      else:
        print("There isn't a Tellstone there!")
        take_it_back_now_yall()
        return
      #Swaps the Tellstones and updates the line.
      self.line[first_index], self.line[second_index] = self.line[second_index], self.line[first_index]
      self.update_line()
    else:
      print("There aren't enough Tellstones to swap.")
      take_it_back_now_yall()


  def find_hidden_count(self):
    self.hidden_count = 0
    for item in line.line:
       if isinstance(item, Tellstone) and item.hidden == True:
        self.hidden_count += 1
    return self.hidden_count

  def peek(self):
    #Find how many hidden stones there are
    #If no hidden stones, end funct
    if self.find_hidden_count() <= 0:
      print("There are no hidden stones!")
      take_it_back_now_yall()
      return
    #If line is empty, end funct
    if self.is_empty():
      print("There are no hidden stones!")
      take_it_back_now_yall()
      return
    #If there wasn't a point last turn, only do position once.
    if next_player.point_last_turn == False:
      position = False
      #Asks for position on the line, then check to see if there is a stone there that is hidden.
      while position == False:
        position = input("What position would you like to peek at? ")
        position = self.peek_error_test(position)
      #The -1's in the line indexs are to change the input 1-7 to the index 0-6. Just for accessibility.
      if type(self.line[position - 1]) is Tellstone and self.line[position - 1].hidden == True:
        for second in [3,2,1]:
          #Dynamically displays a 3 second countdown.
          print(f"Only {current_player.name} should see this! Showing in {second} second(s).\r", sep=" ", end="", flush=True)
          time.sleep(1)
        input(f"The stone in position {position} is {self.line[position-1].name}. Press ENTER to continue.")
      else:
        print("There either isn't a Tellstone there or it isn't hidden.")
    #If there was a point last turn, you can peek at up to 3 stones.
    if next_player.point_last_turn == True:
      print(f"{next_player} scored a point last turn, so you can look at up to 3 stones.")
      #Ask the user how many stones they want to look at
      how_many_stones = False
      while how_many_stones == False:
        how_many_stones = input(f"There are currently {self.hidden_count} face-down stones. How many would you like to peek at (up to three)? ")
        how_many_stones = self.stones_count_error_test(how_many_stones)
      position_list = []
      #Ask the user what positions they want to peek at
      for i in range(1,how_many_stones + 1):
        position = False
        while position == False:
          position = input("What position would you like to peek at? ")
          position = self.peek_error_test(position)
        position_list.append(position)
      for second in [3,2,1]:
        #Dynamically displays a 3 second countdown.
        print(f"Only {current_player.name} should see this! Showing in {second} second(s).\r", sep=" ", end="", flush=True)
        time.sleep(1)
      #Displays the stones then waits for an input.
      print("\n")
      for index in position_list:
        print(f"The stone in position {index} is {self.line[index - 1]}.")
      input("Press ENTER to continue.")
    


  #Error test functions for the above peek function. Returns false and loops with a While loop if the input is invalid.
  def stones_count_error_test(self, stones_count):
    try:
      stones_count = int(stones_count)
    except:
      print("Input must be a number!")
      return False
    if stones_count not in range(1,4):
      print("Please use a number 1-3")
      return False
    if stones_count > self.hidden_count:
      print("There aren't that many hidden stones!")
      return False
    else:
      return stones_count
  
  def peek_error_test(self, position):
    try:
      position = int(position)
    except:
      print("Input must be a number!")
      return False
    if position not in range(1,8):
      print("Please use a number 1-7")
      return False
    else:
      return position
  #End error test functions

  def challenge(self):
    if not self.is_empty():
      #Asks for position on the line, then check to see if there is a stone there that is hidden.
      error_check = 0
      while error_check == 0:
        position = input(f"Which position stone are you challenging {next_player} to name? ")
        try:
          position = int(position)
          #real_index is the true index of the Tellstone.
          real_index = position - 1
        except ValueError:
          print("Input must be a number!")
          take_it_back_now_yall()
          return
        if position not in range(1,8):
          print("Please use a number 1-7")
          take_it_back_now_yall()
          return
        elif not line.line[real_index].hidden:
          print("That Tellstone isn't hidden!")
          take_it_back_now_yall()
        elif line.line[real_index] == " . ":
          print("There isn't a Tellstone there.")
          take_it_back_now_yall()
        else:
          error_check = 1
      opponent_guess = input(f"Alright {next_player.name}, what stone do you think is in that postion? ")
      opponent_guess = opponent_guess.lower()
      if opponent_guess in stones_dict.keys():
        opponent_guess = stones_dict[opponent_guess]
      if opponent_guess == line.line[real_index]:
        print(f"Correct! Your guess, and the token at position {position}, is {line.line[real_index]}.")
        next_player.points += 1
        input(f"{current_player} has {current_player.points} points, and {next_player} has {next_player.points} points. Press ENTER to continue.")
        #next line is redundant because the value is set to False as soon as their turn starts. There is nothing in the game for if YOU scored a point last turn.
        #next.player.point_last_turn = True
      else:
        print(f"Ooh, tough luck. The token in position {position} was actually {line.line[real_index]}.")
        current_player.gain_point()
        input(f"{current_player} has {current_player.points} points, and {next_player} has {next_player.points} points. Press ENTER to continue.")
      line.line[real_index].hidden = False
      line.update_line()

  def boast(self):
    if self.is_empty():
      return
    if self.find_hidden_count() <= 0:
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
    if response == "doubt":
      pass
    if response == "believe":
      print(f"{next_player} believes that {current_player} knows where all the pieces are, and gives up a point.")
      current_player.gain_point()
      input(f"{current_player} has {current_player.points} points, and {next_player} has {next_player.points} points. Press ENTER to continue.")
    if response == "boast":
      pass
      
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
  "the crown": crown,
  "the shield": shield,
  "the sword": sword,
  "the flag": flag,
  "the knight": knight,
  "the hammer": hammer,
  "the scales": scales
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

#Game begins below
game_over = 0
while game_over == 0:
  clear()
  print(line)
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
  if current_player.points == 3:
    print(f"Game over! {current_player.name} reached 3 points!")
    game_over = 1
  user_input = input(f"What would you like to do {current_player.name}? You have {current_player.points} points. ")
  user_input = user_input.lower()
  if user_input == "help":
    input("""You can do the following actions:
    "Place" a stone from the pool onto the line, to the left or right of the current stones in play
    "Hide" a face-up stone that is on the line by turning it face-down.
    "Swap" two stones around.
    "Peek" at a stone that is currently hidden.
    "Challenge" your opponent to name any face-down stone.
    "Boast" that you know all the face-down stones for an instant victory!
    Press ENTER to continue.
    """)
  elif user_input == "place":
    line.add_stone()
    player_turn_advance()
  elif user_input == "hide":
    line.hide_stone()
    player_turn_advance()
  elif user_input == "swap":
    line.swap_stones()
    player_turn_advance()
  elif user_input == "peek":
    line.peek()
    player_turn_advance()
  elif user_input == "challenge":
    line.challenge()
    player_turn_advance()
  elif user_input == "boast":
    line.boast()
    player_turn_advance()
  elif user_input == "debug":
    debug_input = input("Cheaters never prosper :( ")
    if debug_input == "list":
      for i in range(7):
        print(line.line[i])
    elif debug_input == "fill":
      index = 0
      for value in stones_dict.values():
        value.is_on_mat = True
        line.line[index] = value
        index += 1
      line.update_line()
    elif debug_input == "hide":
      for value in stones_dict.values():
        value.hidden = True
      line.update_line()
    elif debug_input == "give point":
      next_player.gain_point()
    elif debug_input == "get point":
      current_player.gain_point()
    else:
      input("Not a valid debugging command. ENTER to continue. ")
  elif user_input == "exit":
    game_over = 1
  else:
    input("That's not a valid command. ENTER to continue. ")
