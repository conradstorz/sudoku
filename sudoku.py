#!/env/python

"""
Accept input from user in the format of a sudoku puzzle solution. Input is stored as a list of lists. each of nine lists contains 9 single digits stored as integer. User may choose to enter complete solutions OR puzzles. Puzzles contain the digit zero to indicate unknown value for that position. Both puzzles and solutions are validated at the completetion of all digits being input.
"""

from readchar import readchar #functions readchar() and readkey()

acceptable_digits = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}

def get_digits(size=9):
  """
  accept digits from user to fill puzzle array.
  """
  print acceptable_digits
  puzzle = []
  for xarg in range(size):
    line = []
    for yarg in range(size):
      userchar = 99
      while userchar not in acceptable_digits:
        userchar = int(readchar())
      line += userchar
      print ' ' + userchar,
    puzzle += line
    print # carriage return, line feed
  return puzzle

def col_set(puzzle, position, size=9, inclusive=True):
  """
  return a set of the values in puzzle for the column defined inclusive of the position unless overridden
  """
  this_set = set()
  for xarg in range(size):
    if not inclusive and xarg != position[0]:
      this_set += puzzle[xarg][position[1]]
  return this_set

def row_set(puzzle, position, size=9):
  """
  return a set of the values in puzzle for the sector defined inclusive of the position unless overridden
  """
  this_set = set()
  given_sector = containing_sector(position)
  for xarg, yarg in given_sector:
    if not inclusive and [xarg, yarg] != position:
      this_set += puzzle[xarg][yarg]
  return this_set

def containing_sector(position, size=9):
  sector_coordinates_list = [[0, 0], [0, 1], [0, 2],
                             [1, 0], [1, 1], [1, 2],
                             [2, 0], [2, 1], [2, 2]]
  return sector_coordinates_list

def sector_set(puzzle, position, size=9, inclusive=True):
  """
  return a set of the values in puzzle for the sector defined inclusive of the position unless overridden
  """
  this_set = set()
  given_sector = containing_sector(position)
  for xarg, yarg in given_sector:
    if not inclusive and [xarg, yarg] != position:
      this_set += puzzle[xarg][yarg]
  return this_set

def valid_value(puzzle, position):
  """
  From given position determine the values in the corresponding column, row and sector.
  Return True if value of position does not appear otherwise in these groups.
  Value is also valid if equal to Zero
  """
  xarg, yarg = position
  value = puzzle[xarg][yarg]
  if value != 0:
    column = col_set(puzzle, position, inclusive=False)
    row = row_set(puzzle, position, inclusive=False)
    sector = sector_set(puzzle, position, inclusive=False)
    combined_sets = column + row + sector
    if value in combined_sets:
      return False
  return True

def validate_puzzle(puzzle, solved=True, size=9): #solved=False allows zero as a valid digit
  """
  True / False test of is puzzle complete.
  """
  digits = acceptable_digits
  for xarg in range(size):
    for yarg in range(size):
      position_value = puzzle[xarg][yarg]
      if solved and position_value == 0:
        return (xarg, yarg)
      if position_value in digits:
        if not valid_value(puzzle, [xarg, yarg]):
          return (xarg, yarg)
  return True

def save_puzzle(puzzle, filename, destination='./'):
  return filepath

def display_puzzle(puzzle, highlight=None, size=9):
  red = 255
  blue = 128
  for xarg in range(size):
    for yarg in range(size):
      if highlight == [xarg, yarg]:
        color = red
      else:
        color = blue
      print puzzle[xarg][yarg],
      if yarg == size-1:
        print #carriage return, linefeed
  print
  return

def ask_user(correction):
  import time
  escapekey = 'esc'
  print '>',
  correction = readkey()
  print correction
  time.sleep(10)
  if correction == escapekey:
    return False
  return True

def get_corrections(puzzle, pointer=(0, 0)):
  """
  take a puzzle list of lists and an optional pointer and accept changes to the array.
  """
  arrowup = 'up'
  arrowdn = 'down'
  arrowrt = 'right'
  arrowlf = 'left'

  def move_pointer(arrowkey):
    if arrowkey == arrowup:
      pass
    if arrowkey == arrowdn:
      pass
    if arrowkey == arrowrt:
      pass
    if arrowkey == arrowlf:
      pass

  display_puzzle(puzzle, highlight=pointer)
  while ask_user(correction):
    if correction in arrowkeys:
      pointer = move_pointer(correction)
    if correction in acceptable_digits:
      puzzle[pointer] = correction
    display_puzzle(puzzle, highlight=pointer)
    if valid_puzzle(puzzle):
      break

def main():
  user_input = []
  print 'Please enter a sudoku puzzle solution.'
  user_input = get_digits()
  print
  result = validate_puzzle(user_input)
  if not result:
    user_input = get_corrections(user_input, result)
  saved_puzzle_filename = save_puzzle(user_input, 'puzzle1')

if __name__ == '__main__':
  main()
