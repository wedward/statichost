from build123d import *
from ocp_vscode import *

from scipy.spatial import ConvexHull

rods = 3
extend = 2
make_cube = False

octarod = RegularPolygon(.25, 8 , rotation=45/2, major_radius=False)
hexarod =   RegularPolygon(.3, 6, rotation=30, major_radius=False)
quadrod = RegularPolygon(.2, 4, False)
cyl = Circle(.5)
rod_shape = hexarod

#build 3-axis
def build3(rods=3, extend=2,  rod_shape=octarod, spacing= 1.0, make_cube=False):
    pts = GridLocations(1.0*spacing,1.0*spacing,rods,rods)
    objs = pts * rod_shape
    for obj in objs[1:]:
        objs[0]+= obj

    z = extrude( objs[0], amount= (rods/2) + extend + spacing, both=True) 
    z.color=Color('blue')

    y = z.translate((0.5*spacing,0,0)).rotate(Axis.X, 90)
    y.color = Color('lawngreen')

    x = z.translate((0.5*spacing,0.5*spacing,0)).rotate(Axis.Y, 90)
    x.color = Color('red')

    if make_cube:
        cube = Box(rods-1,rods-1,rods-1)
        return Compound([obj & cube for obj in [x,y,z]] )
    
    else:
        return   [x,y,z]



def tetra(planes=True):
    tetrahedron_vertices = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
    hull = ConvexHull(tetrahedron_vertices).simplices.tolist()
    platonic_faces = []
    for face_vertex_indices in hull:
        corner_vertices = [tetrahedron_vertices[i] for i in face_vertex_indices]
        platonic_faces.append(Face(Wire.make_polygon(corner_vertices)))

    if planes:
        planes = [Plane(f) for f in platonic_faces]
        for p in planes: p.origin = (0,0,0)
        return planes
    
    return Solid(Shell(platonic_faces))

#build 4-axis
def build4(rods=3, extend=2.0, rod_shape=hexarod, spacing=1):

    planes = tetra()

    pts = HexLocations(1* spacing,rods-rods%2,rods)

    amt = (rods/2) + extend + spacing + 1

    p0 = extrude(Compound(planes[0] * Pos(3**(0.5)/2 * spacing, 0,0) * pts * rod_shape), amt, both=True)
    p1 = extrude(Compound(planes[1] * Pos(3**(0.5) * spacing,-.5 * spacing,0) * pts  * rod_shape), amt, both=True)
    p2 = extrude(Compound(planes[2] * Pos(0,.5 * spacing,0) * pts * rod_shape), amt, both=True)
    p3 = extrude(Compound(planes[3] * Pos(3**.5/2 * spacing, 1  * spacing,0) * pts * rod_shape), amt, both=True)



    p0.color = Color('magenta')
    p1.color = Color('gray')
    p2.color = Color('yellow')
    p3.color = Color('cyan')

   
    return [p0,p1, p2, p3 , ]


def build(axes):

    ## spacing = 1.63 ??

    match axes:
        case 3:
            show(*build3())
        case 4:
            show(*build4())
        case 7:
            show(*build4(2, spacing=1.63), *build3(2, rod_shape=quadrod, spacing=2) )
        case _:
            print('invalid')

    
    




if __name__ == '__main__':
    # from make import make
    # make(Compound(build())) 
    
    build(7)
