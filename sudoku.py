#!/env/python

"""
Accept input from user in the format of a sudoku puzzle solution. Input is stored as a list of lists. each of nine lists contains 9 single digits stored as integer. User may choose to enter complete solutions OR puzzles. Puzzles contain the digit zero to indicate unknown value for that position. Both puzzles and solutions are validated at the completetion of all digits being input.
"""

from readchar import readchar #functions readchar() and readkey()

acceptable_digits = frozenset(range(10))

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
        userchar = readchar()
      line += userchar
      print ' ' + userchar,
    puzzle.append(line)
    print # carriage return, line feed
  return puzzle

def col_set(puzzle, position, size=9, inclusive=True):
  """
  return a set of the values in puzzle for the column defined inclusive of the position unless overridden
  """
  this_set = set()
  for xarg in range(size):
    if not inclusive and xarg != position[0]:
      this_set = this_set.union({puzzle[xarg][position[1]]})
  return this_set

def row_set(puzzle, position, size=9, inclusive=True):
  """
  return a set of the values in puzzle for the sector defined inclusive of the position unless overridden
  """
  this_set = set()
  #print puzzle
  for yarg in range(size):
    if not inclusive and yarg != position[1]:
      #print (position[0], yarg)
      this_set = this_set.union({puzzle[position[0]][yarg]})
  #print this_set
  return this_set

def containing_sector(position, size=9):
  sector_coordinates_list = [(0, 0), (0, 3), (0, 6),
                             (3, 0), (3, 3), (3, 6),
                             (6, 0), (6, 3), (6, 6),]
  block_offset_list = [(0, 0), (0, 1), (0, 2),
                       (1, 0), (1, 1), (1, 2),
                       (2, 0), (2, 1), (2, 2),]                           
  for xarg, yarg in sector_coordinates_list:
    for xoffset, yoffset in block_offset_list:
      (xptr, yptr) = (xarg + xoffset, yarg + yoffset)
      if (xptr, yptr) == position:
        sector_members_list = []
        for xoffset, yoffset in block_offset_list:
          pointer = (xarg + xoffset, yarg + yoffset)
          sector_members_list.add(pointer)
        return sector_members_list

def sector_set(puzzle, position, size=9, inclusive=True):
  """
  return a set of the values in puzzle for the sector defined inclusive of the position unless overridden
  """
  this_set = set()
  given_sector = containing_sector(position)
  for xarg, yarg in given_sector:
    if not inclusive and (xarg, yarg) != position:
      this_set = this_set.union({puzzle[xarg][yarg]})
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
    combined_sets = column.union(row.union(sector))
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
      print (xarg,yarg), ':', position_value, '  ',
      if solved and position_value == 0:
        print 'Zero digit @:',
        return (xarg, yarg)
      if position_value in digits:
        if not valid_value(puzzle, [xarg, yarg]):
          print 'Invalid digit @:',
          return (xarg, yarg)
  return True

def lense_valid(board): 
  """
  solution lifted from codewars.com site written by user Gravitational Lense (Lense)
  member of the Clan: Rensselaer Polytechnic Institute
  This function scans all row and colummns and sectors(Groups) and returns True/False based on 
  wether each block of nine entries correctly contains one entry of each digit from 1 - 9
  (EDIT: this solutiom is flawed)
  """
  rows = [set() for x in range(9)]
  cols = [set() for x in range(9)]
  groups = [set() for x in range(9)]
  for col in range(9):
    for row in range(9):
      rows[row].add(board[row][col])
      cols[col].add(board[row][col])
      groups[col/3+(row/3)*3].add(board[row][col])
  for blocks in  (rows, cols, groups):
    for block in blocks:
      #print block
      if len(block) != 9:
        return False
  return True

def conradical_valid(board): #board[i][j]
  """
  this was my solution for the codewars.com problem
  """
  boardvalid = True
    # check columns
  for col in range(9):
    sumtotal = 0
    for row in range(9):
      sumtotal += board[row][col]
    if sumtotal != 45: 
      boardvalid = False
  # check rows
  for row in range(9):
    sumtotal = 0
    for col in range(9):
      sumtotal += board[row][col]
    if sumtotal != 45: 
      boardvalid = False
  # check regions
  for indx in range(3):
    for jarg in range(3):
      sumtotal = 0
      for col in range(3):
        for row in range(3):
          sumtotal += board[indx*3+row][jarg*3+col]
      if sumtotal != 45: 
        boardvalid = False
  return boardvalid

def torofoggi_valid(board):
  """
  sloution provided by user torofoggi of codewars.com (EDIT: this solutiom is flawed)
  """
  parts = [set() for _ in xrange(27)]
  for xarg, row in enumerate(board):
    for yarg, element in enumerate(row):
      parts[(xarg / 3) * 3 + yarg / 3].add(element) # regions
      parts[yarg + 9].add(element) # columns
      parts[xarg + 18].add(element) # rows
  #for indx in range(27):
  #  print parts[indx]
  return True if [len(part) for part in parts].count(9) == 27 else False

def elcoban_valid(board):
    for k in range(9):
        if sorted([board[k][i] for i in range(9)]) != range(1,10):
            return False
        if sorted([board[i][k] for i in range(9)]) != range(1, 10):
            return False
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            if sorted([board[i + r][j + c] for r in range(3) for c in range(3)]) != range(1, 10):
                return False
    return True

def stfin_valid(board):
    digits = set(range(1,10))
    for row in board:
        if set(row) != digits:
            return False
    for i in digits:
        column = [board[j][i-1] for j in range(0,len(board))]
        if set(column) != digits:
            return False
    for k in [0,3,6]:
        for l in [0,3,6]:
            square = [board[i+k][j+l] for i in [0,1,2] for j in [0,1,2]]
            if set(square) != digits:
                return False
    return True

def werneckpaiva_valid(board):
  """
  solution provided by Ricardo (werneckpaiva) of Clan:Globo.com
    on codewars.com (EDIT: this solutiom is flawed)
  """
  for indx in xrange(0, 9):
    (row, col, blk) = (set(), set(), set())
    for jndx in xrange(0, 9):
      row.add(board[indx][jndx]) 
      col.add(board[jndx][indx])
      blk.add(board[0 + jndx / 3][((indx * 3) % 9) + jndx % 3])
    #print row
    #print col
    #print blk
    if len(row)!=9 or len(col)!=9 or len(blk)!=9:
      return False
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
  correction = readchar()
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
  arrowkeys = {arrowup, arrowdn, arrowrt, arrowlf}

  def move_pointer(arrowkey):
    if arrowkey == arrowup:
      pass
    if arrowkey == arrowdn:
      pass
    if arrowkey == arrowrt:
      pass
    if arrowkey == arrowlf:
      pass

  correction = ''
  display_puzzle(puzzle, highlight=pointer)
  while ask_user(correction):
    if correction in arrowkeys:
      pointer = move_pointer(correction)
    if int(correction) in acceptable_digits:
      puzzle[pointer] = int(correction)
    display_puzzle(puzzle, highlight=pointer)
    result = validate_puzzle(puzzle)
    if result:
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
