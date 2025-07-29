from build123d import *
from ocp_vscode import show

def getpts(depth):
    # holes = 3**(depth*2-2)
    squares = 3**depth
    holeper = squares//3
    num = lambda i: i * 2 - 1

    out = []
    for j in range(1,holeper+1):
        out.append( [ ( num(k) / (holeper*2) , num(j) / (holeper*2) ) 
                     for k in range(1,holeper+1) ])
    
    return out

def build(depth):
    poly = Polygon((0,0),(1,0),(1,1),(0,1), align=(Align.MIN, Align.MIN))
    for i in range(1, depth+1):
        locs = Locations(getpts(i))
        poly-= locs * Rectangle(1/3**i, 1/3**i)

    poly.locate(Location((-.5,-.5,-.5)))

    comp1 = extrude(poly, 1)
    comp2 = comp1.rotate(Axis.Y, 90)
    comp3 = comp1.rotate(Axis.X, 90)

    return comp3 & comp2 & comp1

show(build(2))




    




