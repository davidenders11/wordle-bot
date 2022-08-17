import numpy as np
import random as random
import pygame
from pygame.locals import *

# Word list
with open("sgb-words.txt", "r") as tf:
    words = tf.read().split('\n')

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
final_word = words[random.randrange(1,5758)].upper() # Winning word!
guess_counter = 0
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
# -------- Helper Functions ----------- #
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

def gradeWord():
  """Grades word if complete word has been typed, else does nothing"""
  global current_col
  global guess_counter
  temp_final = final_word
  if current_col != 5: return # character counter should be at 5 if word done
  green_counter = 0 
  guess = ''.join([game_board[guess_counter][col][0] for col in range(5)])
  for ind in range(0, 5):
    if temp_final[ind] == guess[ind]: # Right letter in right spot
      print(guess[ind] + " is in " + final_word + " at that location!")
      game_board[guess_counter][ind][1] = GREEN
      green_counter += 1
    elif temp_final[ind] in guess: # Right letter in wrong spot
      print(temp_final[ind] + " is in " + final_word + " at a different location!")
      game_board[guess_counter][ind][1] = YELLOW
    temp_final = setCharToNull(temp_final, ind) # Avoid double-counting letters
  if green_counter == 5:
    print("You won on guess number " + str(guess_counter + 1) + "!")
    return
  # Next guess!
  current_col = 0
  guess_counter = guess_counter + 1 if guess_counter < 5 else guess_counter


# -------- Main Program Loop ----------- #
print(final_word)
running = True
clock = pygame.time.Clock() # Used to manage how fast the screen updates
while running:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT or \
        (event.type == KEYDOWN and event.key == K_ESCAPE):
          running = False # end game if quit
        elif event.type == pygame.KEYDOWN:
          if event.key == K_BACKSPACE: # delete last character
            deleteLast()
          elif event.key == K_RETURN: # check if word is correct
            gradeWord() 
          elif event.key in range(97,123): # type next letter in word
            addToBoard(event.unicode)
 
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
        



  
# # 5758 words in total
# print(len(words))

# # inputless function that chooses a 5 letter word at random from list
# # list is reset every time to contain all 5 letter words
# # 6 guesses to get the word

# def start_game():
#   temp_words = words
#   guess_counter = 0
#   final_word = temp_words[random.randrange(1,5758)]
#   print('chosen wordle word = ', final_word)
#   while(guess_counter < 6):

#     guess_counter += 1
#     print('Please enter guess #', guess_counter)
#     guess_word = input()
    
#     if (valid_guess(guess_word)):
#       print(guess_color(guess_word, final_word))
#     else:
#       guess_counter -=1
    
#     if (guess_word == final_word): # player wins
#         print('Congratulations, you win on guess #' + str(guess_counter) + ' of 6')
#         return

#   # if function gets here, player has lost
#   print('Sorry, try again next time. Correct word is: ' + final_word)

# # guess will take 5 letter word as input (alphabetical only)

# def valid_guess(word):
#   if ((word.isalpha()) and (len(word)==5)):
#     if ((word in words)):
#       return True
#   else:
#     print('please guess with a 5 letter word')
#     return False

# def guess_color(word, final_word):
#   color_list = ['black', 'black', 'black', 'black', 'black']
#   for index in range(5):
#     if(word[index] in final_word):
#       if(word[index] == final_word[index]):
#         color_list[index] = 'green'
#       else:
#         color_list[index] = 'yellow'
#     else:
#       color_list[index] = 'black'
#   return color_list

# start_game()