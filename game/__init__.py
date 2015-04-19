from random import uniform
SIZE_OF_ONE_TILE = 100
CHANCE_FOR_TWO_OR_FOUR = ((2,9), (4,1))
PROB_FOR_TWO_NORMALIZED = CHANCE_FOR_TWO_OR_FOUR[0][1] / (CHANCE_FOR_TWO_OR_FOUR[0][1] + CHANCE_FOR_TWO_OR_FOUR[1][1])
AFTER_FOR_NEW_TURN = 1
path_for_images = {2**i : "pic/"+str(2**i)+".png" for i in range(1,14)}
CORNERS = ((0,0), (0,3), (3,0), (3,3))
BOUNDARYx0 = tuple([(i, 0) for i in range(4)] )
BOUNDARYx3 = tuple([(i, 3) for i in range(4)] )
BOUNDARYy0 = tuple([(0, i) for i in range(4)] )
BOUNDARYy3 = tuple([(3, i) for i in range(4)] )
BOUNDARYS = (BOUNDARYx0, BOUNDARYx3, BOUNDARYy0, BOUNDARYy3)
def weighted_choice(choices = CHANCE_FOR_TWO_OR_FOUR):
    total = sum(w for c, w in choices)
    r = uniform(0, total)
    upto = 0
    for c, w in choices:
        if upto + w > r:
            return c
        upto += w
    assert False, "Shouldn't get here"

def flipping30(input):
    ''' flip 0x3 , 1x2 '''
    return (3-i for i in input)

class Directions:
    NORTH = 'North'
    SOUTH = 'South'
    EAST = 'East'
    WEST = 'West'
    dxdy = {NORTH : (0,-1),
            SOUTH : (0,1),
            EAST  : (1,0),
            WEST  : (-1,0)
            }
    
    @staticmethod
    def generator():
        yield Directions.NORTH
        yield Directions.EAST
        yield Directions.SOUTH
        yield Directions.WEST
        
        
