from random import uniform
SIZE_OF_ONE_TILE = 100
CHANCE_FOR_TWO_OR_FOUR = ((2,9), (4,1))
PROB_FOR_TWO_NORMALIZED = CHANCE_FOR_TWO_OR_FOUR[0][1] / (CHANCE_FOR_TWO_OR_FOUR[0][1] + CHANCE_FOR_TWO_OR_FOUR[1][1])
AFTER_FOR_NEW_TURN = 50
path_for_images = {2**i : "pic/"+str(2**i)+".png" for i in range(1,14)}

def weighted_choice(choices = CHANCE_FOR_TWO_OR_FOUR):
    total = sum(w for c, w in choices)
    r = uniform(0, total)
    upto = 0
    for c, w in choices:
        if upto + w > r:
            return c
        upto += w
    assert False, "Shouldn't get here"

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
        
        
