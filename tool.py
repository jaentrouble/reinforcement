import random
from constants import *

def randposlist(n : int, width : int, height : int):
    """
    randposlist
    n : number of positions in the list
    """
    direction = random.randint(0,3)
    body = []
    if direction == RIGHT :
        head = randpos(n-1,width-1, 0, height-1)
        body.append(head.copy())
        for i in range(n-1) :
            new = head.copy()
            new[0] -= i+1
            body.append(new)
    elif direction == LEFT :
        head = randpos(0,width-n, 0, height-1)
        body.append(head.copy())
        for i in range(n-1) :
            new = head.copy()
            new[0] += i+1
            body.append(new)
    elif direction == UP :
        head = randpos(0,width-1, 0, height-n)
        body.append(head.copy())
        for i in range(n-1) :
            new = head.copy()
            new[1] += i+1
            body.append(new)
    elif direction == DOWN :
        head = randpos(0,width-1, n-1, height-1)
        body.append(head.copy())
        for i in range(n-1) :
            new = head.copy()
            new[0] -= i+1
            body.append(new)

    return body, direction

def randpos (xmin : int, xmax : int, ymin : int, ymax : int ) :
    """
    randpos
    [randint(xmin, xmax), randint(ymin, ymax)]
    """
    return [random.randint(xmin,xmax), random.randint(ymin, ymax)]