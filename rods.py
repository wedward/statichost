from build123d import *
from ocp_vscode import *

rods = 3
extend = 2
make_cube = False
rod_shape =     RegularPolygon(.25, 8, rotation=45/2, major_radius=False)


def build(rods=rods, extend=extend, make_cube=make_cube, rod_shape=rod_shape):
    pts = GridLocations(1,1,rods,rods)
    objs = pts * rod_shape
    for obj in objs[1:]:
        objs[0]+= obj

    z = extrude( objs[0], amount= (rods/2) + extend, both=True) 
    z.color=Color('blue')

    y = z.translate((.5,0,0)).rotate(Axis.X, 90)
    y.color = Color('lawngreen')

    x = z.translate((.5,.5,0)).rotate(Axis.Y, 90)
    x.color = Color('red')

    if make_cube:
        cube = Box(rods-1,rods-1,rods-1)
        return Compound([obj & cube for obj in [x,y,z]] )
    
    else:
        return   [x,y,z] 

if __name__ == '__main__':
    show(*build())
