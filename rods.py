from build123d import *
from ocp_vscode import *

from scipy.spatial import ConvexHull

rods = 3
extend = 2
make_cube = False

octarod = RegularPolygon(.25, 8 , rotation=45/2, major_radius=False)
hexarod =   RegularPolygon(.2, 6, rotation=30, major_radius=False)

rod_shape = hexarod

#build 3-axis
def build3(rods=rods, extend=extend, make_cube=make_cube, rod_shape=rod_shape):
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



def tetra(planes=False):
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
def build():

    planes = tetra(planes=True)

    pts = HexLocations(.5,rods-rods%2,rods)

    p0 = extrude(Compound(planes[0] * pts * rod_shape), extend+rods/2, both=True)
    p1 = extrude(Compound(planes[1] * Pos(3**(0.5)/4,-.25,0) * pts  * rod_shape), extend+rods/2, both=True)
    p2 = extrude(Compound(planes[2] * Pos(0,.5,0) * pts * rod_shape), extend+rods/2, both=True)
    p3 = extrude(Compound(planes[3] * Pos(3**.5/4,.25,0) * pts * rod_shape), extend+rods/2, both=True)

    r =planes[2]  * Rectangle(3,5)

    p0.color = Color('cyan')
    p1.color = Color('gray')
    p2.color = Color('magenta')
    p3.color = Color('yellow')

   
    return [p0,p1, p2, p3]



if __name__ == '__main__':
    # from make import make
    # make(Compound(build()))
    
    show(*build())
