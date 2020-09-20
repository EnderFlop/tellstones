import time
import sys

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
      return
    if stone.is_on_mat == True:
      print(f"{stone} is already on the line!")
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
      #If it's right, add it to the right and move self.furthest_right to the right by 1. Check to see if there is space.
      elif left_or_right == "r":
        if self.furthest_right < 6:
          self.line[self.furthest_right + 1] = stone
          stone.add_to_line(self.furthest_right + 1)
          self.furthest_right += 1
          self.update_line()
        else:
          print("That's off the line!")
      elif left_or_right != "r" or "l":
        print("Not a valid input.")

  
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
      else:
        print(f"{stone} isn't a valid stone. Did you remember to put 'the' before it?")

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
        return
      if first_stone not in range(1,8):
        print("Please use a number 1-7")
        return
      #The -1 is to change 1-7 to 0-6 for QoL.
      if isinstance(self.line[first_stone - 1], Tellstone):
        first_index = first_stone - 1
      else:
        print("There isn't a Tellstone there!")
        return
      #Get the second stone to swap
      second_stone = input("What is the position of the other stone you would like to swap? ")
      try:
        second_stone = int(second_stone)
      except ValueError:
        print("Input must be a number!")
        return
      if second_stone not in range(1,8):
        print("Please use a number 1-7")
        return
      #The -1 is to change 1-7 to 0-6 for QoL.
      if isinstance(self.line[second_stone - 1], Tellstone):
        second_index = second_stone - 1
      else:
        print("There isn't a Tellstone there!")
        return
      #Swaps the Tellstones and updates the line.
      self.line[first_index], self.line[second_index] = self.line[second_index], self.line[first_index]
      self.update_line()
    else:
      print("There aren't enough Tellstones to swap.")


  def peek(self):
    if not self.is_empty():
      #Asks for position on the line, then check to see if there is a stone there that is hidden.
      position = input("What position would you like to peek at? ")
      try:
        position = int(position)
      except ValueError:
        print("Input must be a number!")
        return
      if position not in range(1,8):
        print("Please use a number 1-7")
        return
      #The -1's in the line indexs are to change the input 1-7 to the index 0-6. Just for accessibility.
      if type(line.line[position - 1]) is Tellstone and line.line[position - 1].hidden == True:
        for second in [3,2,1]:
          #Dynamically displays a 3 second countdown.
          print(f"Only {current_player.name} should see this! Showing in {second} second(s).\r", sep=" ", end="", flush=True)
          time.sleep(1)
        input(f"The stone in position {position} is {line.line[position-1].name}. Press enter to continue.")
        #Moves cursor up 2 lines and erases position text. Doesn't work in cmd.
        sys.stdout.write("\033[F")
        sys.stdout.write("\033[F")
        print("\r\n")
      else:
        print("There either isn't a Tellstone there or it isn't hidden.")
  
  def challenge(self):
    if not self.is_empty():
      #Asks for position on the line, then check to see if there is a stone there that is hidden.
      position = input(f"Which position stone are you challenging your opponent to name, {current_player.name}? ")
      try:
        position = int(position)
        #real_index is the true index of the Tellstone.
        real_index = position - 1
      except ValueError:
        print("Input must be a number!")
        return
      if position not in range(1,8):
        print("Please use a number 1-7")
        return
      elif not line.line[real_index].hidden:
        print("That Tellstone isn't hidden!")
      elif line.line[real_index] == " . ":
        print("There isn't a Tellstone there.")
      else:
        opponent_guess = input(f"Alright {next_player.name}, what token do you think is in that postion? ")
        opponent_guess = opponent_guess.lower()
        if opponent_guess in stones_dict.keys():
          opponent_guess = stones_dict[opponent_guess]
        if opponent_guess == line.line[real_index]:
          print(f"Correct! Your guess, and the token at position {position}, is {line.line[real_index]}.")
          next_player.points += 1
        else:
          print(f"Ooh, tough luck. The token in position {position} was actually {line.line[real_index]}.")
        line.line[real_index].hidden = False
        line.update_line()

  def boast(self):
    pass

      

class Player:
  def __init__(self, name):
    self.name = name
    self.points = 0
  def gain_point(self):
    self.points += 1



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


#Game begins below
game_over = 0
player_turn = 0
while game_over == 0:
  print(line)
  #Alternate player turns.
  if player_turn % 2 == 0:
    current_player = player_one
    next_player = player_two
  else:
    current_player = player_two
    next_player = player_one
  if current_player.points == 3:
    print(f"Game over! {current_player.name} reached 3 points!")
    game_over = 1
  user_input = input(f"What would you like to do {current_player.name}? You have {current_player.points} points. ")
  user_input = user_input.lower()
  if user_input == "help":
    print("""You can do the following actions:
    "Place" a stone from the pool onto the line, to the left or right of the current stones in play
    "Hide" a face-up stone that is on the line by turning it face-down.
    "Swap" two stones around.
    "Peek" at a stone that is currently hidden.
    "Challenge" your opponent to name any face-down stone.
    "Boast" that you know all the face-down stones for an instant victory!
    """)
  elif user_input == "place":
    line.add_stone()
  elif user_input == "hide":
    line.hide_stone()
  elif user_input == "swap":
    line.swap_stones()
  elif user_input == "peek":
    line.peek()
  elif user_input == "challenge":
    line.challenge()
  elif user_input == "boast":
    line.boast()
  elif user_input == "debug":
    debug_input = input("Cheaters never prosper :( ")
    if debug_input == "list":
      for i in range(7):
        print(line.line[i])
    if debug_input == "fill":
      index = 0
      for value in stones_dict.values():
        value.is_on_mat = True
        line.line[index] = value
        index += 1
      line.update_line()
    else:
      print("Not a valid debugging command.")
  elif user_input == "exit":
    game_over = 1
  else:
    print("That's not a valid command.")
  player_turn += 1

