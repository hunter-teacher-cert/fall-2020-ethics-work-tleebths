# Izagma Alonso &import random

MAXPOPULATION = 99
NUM_ROWS = 3
NUM_COLS = 6
NUM_DISTRICTS = 6

class Cell(object):   
    def __init__(self, population, district, vote):
        self.population = population
        self.district = district
        self.vote = vote


def totalPop():
  total = 0
  for i in range(NUM_ROWS):
    for j in range(NUM_COLS):
      total += purple_state[i][j].population
  return total
      

purple_state=[[ Cell( random.randint(1,MAXPOPULATION),1,random.randint(0,1) ) for i in range(NUM_COLS)] for j in range(NUM_ROWS)]


def displayState():
  print("Purple State:")
  for i in range(NUM_ROWS):
    print(i,end="\t")
    if i%2 == 0:
      start = 0
      end = NUM_COLS - 1
      change = 1
    else:
      start = NUM_COLS -1
      end = 0
      change = -1

    for j in range(start,end,change):
        print(purple_state[i][j].district, purple_state[i][j].population, purple_state[i][j].vote, end=",\t")
      
    print()

def oldDisplayState():
  print("Purple State:")
  for i in range(NUM_ROWS):
    print(i,end="\t")
    for j in range(NUM_COLS):
      print(purple_state[i][j].district, purple_state[i][j].population, purple_state[i][j].vote, end=",\t")
    print()


def simpleDistricts():
  districtCells = NUM_ROWS * NUM_COLS / NUM_DISTRICTS
  distNum = 1
  numCells = 0

  for i in range(NUM_ROWS):
    for j in range(NUM_COLS):
      purple_state[i][j].district = distNum
      numCells += 1
      if numCells >= districtCells:
        distNum += 1
        numCells = 0

  
def makeDistricts():
  targetPop = totalPop() / NUM_DISTRICTS
  districtCells = NUM_ROWS * NUM_COLS / NUM_DISTRICTS
  print("Target Population: ", targetPop)
  distNum = 1
  popSum = 0
  over = False
  numCells = 0

  for i in range(NUM_ROWS):
    for j in range(NUM_COLS):
      if (over and popSum + purple_state[i][j].population >= targetPop) or (numCells >= districtCells +1):
        distNum += 1
        if distNum > NUM_DISTRICTS:
          distNum = NUM_DISTRICTS
        print(popSum)
        purple_state[i][j].district = distNum
        popSum = purple_state[i][j].population
        over = False
        numCells = 1
      else:
        purple_state[i][j].district = distNum
        popSum += purple_state[i][j].population
        numCells += 1
        
        if (popSum >= targetPop) or (numCells >= districtCells +1):
          over = True
          distNum += 1
          if distNum > NUM_DISTRICTS:
            distNum = NUM_DISTRICTS
          print(popSum)
          popSum = 0
          numCells = 0

#simpleDistricts()
makeDistricts()
displayState()
