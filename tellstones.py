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
    stone = input("What stone would you like to hide? ")
    stone = stone.lower()
    if stone in stones_dict.keys():
      stone = stones_dict[stone]
      stone.hide()
      self.update_line()
    else:
      print(f"{stone} isn't a valid stone. Did you remember to put 'the' before it?")



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


#Game begins below
game_over = 0
while game_over == 0:
  print(line)
  user_input = input("What would you like to do? ")
  user_input = user_input.lower()
  if user_input == "help":
    print("""You can do the following actions:
    "Place" a stone from the pool onto the line, to the left or right of the current stones in play
    "Hide" a face-up stone that is on the line by turning it face-down.
    """)
  elif user_input == "place":
    line.add_stone()
  elif user_input == "hide":
    line.hide_stone()
  elif user_input == "exit":
    game_over = 1
  else:
    print("That's not a valid command.")
