import numpy as np
import random as random
import pygame
from pygame.locals import *
from hash_table import final_hash_table

# Word list
with open("sgb-words.txt", "r") as tf:
  words = tf.read().split('\n')

# Initialize running list of possible words
poss_sols = set([])
for row in range(5):
  for col in range(26):
    for word in final_hash_table[row][col]:
      poss_sols.add(word)

# Game colors and cell dimensions
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (44, 44, 44)
GREEN = (84, 141, 78)
YELLOW = (181,159,59)
WIDTH = 75
HEIGHT = 75
MARGIN = 5

# Initialize game variables
final_word = random.choice(words).upper() # winning word!
guess_counter = 0 # What row is the player at
current_col = 0
game_board = [[["", GREY] for width in range(5)] for height in range(6)] 
# 5 x 6 game board, each cell stores character (0 for empty) and color 

# Initialize pygame and set screen height, width, caption
pygame.init()
SCREEN_WIDTH = 405
SCREEN_HEIGHT = 485
SCREEN_SIZE = [SCREEN_WIDTH, SCREEN_HEIGHT]
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Wordle Game")
screen.fill(BLACK)

# -------- Game Helper Functions ----------- #
def deleteLast():
  """Decrement current_col to previous letter if there is one and clear that letter"""
  global current_col
  current_col = current_col - 1 if current_col > 0 else current_col
  game_board[guess_counter][current_col][0] = ""

def addToBoard(chr):
  """Adds typed character to next open space, or replaces last character if no open spaces"""
  global current_col
  current_col = 4 if current_col == 5 else current_col # replace last if no open
  game_board[guess_counter][current_col][0] = chr.upper()
  current_col = current_col + 1

def setCharToNull(word, ind):
  """Replaces the index we just visited with a space"""
  return word[0:ind] + " " + word[ind+1:]

def grade_word():
  """Grades word if complete word has been typed, else does nothing"""
  global current_col
  global guess_counter
  game_over = False # Use to end game loop when game is over
  final_copy = final_word # use this to modify correct word to avoid double-counting
  green_counter = 0 # player wins if equals 5
  guess = ''.join([game_board[guess_counter][col][0] for col in range(5)]) # create string from game_board row

  if current_col != 5: return # character counter should be at 5 if word done
  
  # Check for greens
  for ind in range(0, 5):
    if final_copy[ind] == guess[ind]: # Right letter in right spot
      print(guess[ind] + " is in the word at that location!")
      game_board[guess_counter][ind][1] = GREEN
      green_counter += 1
      final_copy = setCharToNull(final_copy, ind) # avoid double-counting

  for ind in range(0,5):
    # Check if we already marked green so greens don't get marked yellow
    if final_copy[ind] == ' ':
        pass
    elif guess[ind] in final_copy:
      print(guess[ind] + " is in the word at a different location!")
      game_board[guess_counter][ind][1] = YELLOW
      final_copy = setCharToNull(final_copy, final_copy.index(guess[ind])) # avoid double-counting
  
  if green_counter == 5:
    print("You won on guess number " + str(guess_counter + 1) + "!")
    game_over = True
    return game_over
  elif guess_counter == 5:
    print("You lost. Final word was " + final_word)
    game_over = True
    return game_over
  
def print_instructions():
  """Text-based terminal output instructions"""
  line1 = "\nWelcome to Wordle!\n\n"
  line2 = "Instructions: \n\n"
  line3 = "1. Type your five-letter guess. Press delete to edit, and return when finished with a word. \n\n"
  line4 = "2. Characters in the correct spot will highlight green. If a character is in the word but in the wrong spot, it will highlight yellow. \n\n"
  line5 = "3. Press the right arrow key to engage the solver."
  print(line1 + line2 + line3 + line4 + line5)
    

# -------- Solver Functions ----------- #
def let_ind(letter):
  """Maps character to bucket 0-25"""
  return ord(letter) - ord('A')

def reducer():
  """Intersects the running list of possible solutions with the new information from the last guess"""
  global poss_sols
  for position in range(5):
    # For characters marked green, we get the intersection of the running set of possible solutions with the set 
    # of all words that have that character in that position
    if game_board[guess_counter][position][1] == GREEN:
      poss_sols.intersection_update(final_hash_table[position][let_ind(game_board[guess_counter][position][0])])
    # For yellow chars, intersect remaining solutions w/ set of all words with that char. anywhere in word
    elif game_board[guess_counter][position][1] == YELLOW:
      yellows = set([])
      for pos in range(5):
        for word in final_hash_table[pos][let_ind(game_board[guess_counter][position][0])]:
          yellows.add(word)
      poss_sols.intersection_update(yellows)
    # For grey chars, intersect remaining solutions w/ set of all words w/o that char. in that position
    elif game_board[guess_counter][position][1] == GREY:
      poss_sols.difference_update(final_hash_table[position][let_ind(game_board[guess_counter][position][0])])
  
def pick_next():
  """Picks random word from set of possible remaining solutions and adds it to board"""
  best_guess = poss_sols.pop()
  print("Computer guessed: " + best_guess + "\n")
  for letter in range(5):
    game_board[guess_counter][letter][0] = best_guess[letter]
    

# -------- Main Program Loop ----------- #
print_instructions()
running = True
solve = False
clock = pygame.time.Clock() # Used to manage how fast the screen updates
while running:
    for event in pygame.event.get():  # User did something
      if event.type == pygame.QUIT or \
      (event.type == KEYDOWN and event.key == K_ESCAPE):
        running = False
      elif event.type == pygame.KEYDOWN:
        if event.key == K_RIGHT:
          solve = True
        elif event.key == K_BACKSPACE: # delete last character
          deleteLast()
        elif event.key == K_RETURN: # check if word is correct
          running = not grade_word() # grade_word() returns true if game is over
          # Next guess!
          if current_col == 5: # Return key does nothing if guess isn't complete
            current_col = 0
            guess_counter = guess_counter + 1 if guess_counter < 5 else guess_counter
        elif event.key in range(97,123): # type next letter in word
          addToBoard(event.unicode)
    if solve:
      pick_next()
      current_col = 5 # Needed to pass grade_word() check
      solve = not grade_word()
      pygame.time.delay(500)
      reducer()
      guess_counter = guess_counter + 1 if guess_counter < 5 else guess_counter
 
    # Set the screen background
    screen.fill(BLACK)
    
    # Draw the game_board
    for row in range(6):
        for col in range(5):
            # draw cells
            pygame.draw.rect(screen,
                             game_board[row][col][1],
                             [(MARGIN + WIDTH) * col + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])
            # draw characters
            font = pygame.font.SysFont(None, 30)
            text = font.render(game_board[row][col][0], True, WHITE)
            text_rect = text.get_rect(center=((MARGIN + WIDTH) * col + MARGIN + WIDTH/2, (MARGIN + HEIGHT) * row + MARGIN + HEIGHT/2))
            screen.blit(text, text_rect)
 
    # Limit to 60 frames per second
    clock.tick(60)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()