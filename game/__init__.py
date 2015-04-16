# init. nothing is really here..
SIZE_OF_ONE_TILE = 100
path_for_images = {2**i : "pic/"+str(2**i)+".png" for i in range(1,14)}

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
