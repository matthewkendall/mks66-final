import math
import numpy as np

## texture is of the form [D, type]
## D is a dictionary with all R,G,B pixel values: D = {(u,v) : (R,G,B)}
## type is a list
    ## type[0] is the type of texture: (e.g. 'box', 'cylinder', 'sphere')
    ## type[1], type[2], ... are the properties of the type of texture
        ## e.g. 'box' has width, depth, and height

texture = []
COORDS = 0
TYPE = 1
BOX = 0
CYLINDER = 1
SPHERE = 2

BOT = 0
TOP = 1
box_prop = {"is_box" : False, "box_num" : -1, "box_dim" : [-1, -1, -1], "box_loc" : -1}
box_num = -1
box_dim = [-1, -1, -1]
is_box = False


def texture_scanline(polygons, i, screen, zbuffer, texture):
    flip = False
    BOT = 0
    TOP = 2
    MID = 1

    points = [ (polygons[i][0], polygons[i][1], polygons[i][2]),
               (polygons[i+1][0], polygons[i+1][1], polygons[i+1][2]),
               (polygons[i+2][0], polygons[i+2][1], polygons[i+2][2]) ]

    # alas random color, we hardly knew ye
    #color = [0,0,0]
    #color[RED] = (23*(i/3)) %256
    #color[GREEN] = (109*(i/3)) %256
    #color[BLUE] = (227*(i/3)) %256

    points.sort(key = lambda x: x[1])
    x0 = points[BOT][0]
    z0 = points[BOT][2]
    x1 = points[BOT][0]
    z1 = points[BOT][2]
    y = int(points[BOT][1])

    distance0 = int(points[TOP][1]) - y * 1.0 + 1
    distance1 = int(points[MID][1]) - y * 1.0 + 1
    distance2 = int(points[TOP][1]) - int(points[MID][1]) * 1.0 + 1

    dx0 = (points[TOP][0] - points[BOT][0]) / distance0 if distance0 != 0 else 0
    dz0 = (points[TOP][2] - points[BOT][2]) / distance0 if distance0 != 0 else 0
    dx1 = (points[MID][0] - points[BOT][0]) / distance1 if distance1 != 0 else 0
    dz1 = (points[MID][2] - points[BOT][2]) / distance1 if distance1 != 0 else 0

    while y <= int(points[TOP][1]):
        if ( not flip and y >= int(points[MID][1])):
            flip = True

            dx1 = (points[TOP][0] - points[MID][0]) / distance2 if distance2 != 0 else 0
            dz1 = (points[TOP][2] - points[MID][2]) / distance2 if distance2 != 0 else 0
            x1 = points[MID][0]
            z1 = points[MID][2]

        # look into the difference
        # draw_line(int(x0), y, z0, int(x1), y, z1, screen, zbuffer, color)
        draw_scanline(int(x0), z0, int(x1), z1, y, screen, zbuffer, texture, polygons, i)
        x0+= dx0
        z0+= dz0
        x1+= dx1
        z1+= dz1
        y+= 1

# draws scanline in the correct order
# and retrieves color if necessary
def draw_scanline(x0, z0, x1, z1, y, screen, zbuffer, color, polygons, i):
    dist = abs(x1-x0)
    if x0 < x1:
        delta_x = 1
    else:
        delta_x = -1

    x = x0
    z = z0
    delta_z = (z1 - z0) / (x1 - x0 + 1) if (x1 - x0 + 1) != 0 else 0

    while dist >= 0:
        if is_texture:
            u,v = get_uv(x, y, z)
            color = get_color(u, v)

        plot(screen, zbuffer, color, x, y, z)
        x+= delta_x
        z+= delta_z
        dist -= 1




######################### MATH FUNCTIONS ################################
# gets (u,v) coordinates from (x,y,z) coordinates given type of texture map
def get_uv(x, y, z, polygons, i, texture):
    X,Y = convert_xy(x, y, z, polygons, i)

    if is_box:
        w,h,d = box_dim[0], box_dim[1], box_dim[2]
        # box_pair =
        return box_convert_uv(x, y, w, h, d, box_pair)


    pass


# converts a point in triangle back to standard basis representation
# coordinates in 3D are x0, y0, z0
# used for any type of texture
def convert_xy(x0, y0, z0, polygons, i):
    BOT = 0
    TOP = 2
    MID = 1
    points = [ (polygons[i][0], polygons[i][1], polygons[i][2]),
               (polygons[i+1][0], polygons[i+1][1], polygons[i+1][2]),
               (polygons[i+2][0], polygons[i+2][1], polygons[i+2][2]) ]

    points.sort(key = lambda x: x[1])
    A = [0, 0, 0]
    B = [0, 0, 0]

    A[0] = points[BOT][0] - points[MID][0]
    A[1] = points[BOT][1] - points[MID][1]
    A[2] = points[BOT][2] - points[MID][2]

    B[0] = points[TOP][0] - points[MID][0]
    B[1] = points[TOP][1] - points[MID][1]
    B[2] = points[TOP][2] - points[MID][2]

    m = np.matrix([ [A[0], B[0], 0],
                    [A[1], B[1], 0],
                    [A[2], B[2], 1]])
    m = m.I.getA()
    v = np.array([ [x0], [y0], [z0]])
    v = m.dot(v)

    return v[0][0],v[1][0]

# this function converts each triangle from the box into the correct
# location for the texture map
# returns a pair of homogenized coordinates u,v according to
# box location [box_num, BOT/TOP]
# and dimentions given pair of homogenized coordinates x,y
def box_convert_uv(x, y, w, h, d, box_pair):
    box_num = box_pair[0]
    box_loc = box_pair[1]
    BOT = 0
    TOP = 1
    box_x = box_num % 4
    box_y = box_num // 4

    dx1,dx2 = (h * 1.0) / (2*w + 2*h), (w * 1.0) / (2*w + 2*h)
    dx3,dx4 = dx1,dx2
    dy1,dy2,dy3 = (h * 1.0) / (2*h + d), (d * 1.0) / (2*h + d), (h * 1.0) / (2*h + d)

    move_x = 0
    move_y = 0

    # determine correct scaling and moving
    if box_x == 0:
        scale_x = dx1
        move_x = 0
    elif box_x == 1:
        scale_x = dx2
        move_x = dx1
    elif box_x == 2:
        scale_x = dx3
        move_x = dx1 + dx2
    else:
        scale_x = dx4
        move_x = dx1 + dx2 + dx3
    if box_y == 0:
        scale_y = dy1
        move_y = 0
    elif box_y == 1:
        scale_y = dy2
        move_y = dy1
    else:
        scale_y = dy3
        move_y = dy1 + dy2

    # do necessary reflections
    if box_num in {1,5,7,9}:
        if box_loc == TOP:
            x = 1-x
            y = 1-y
    elif box_num in {4,6}:
        # reflect about x=1/2
        x = 1-x
        if box_loc == TOP:
            x = 1-x
            y = 1-y
    else:
        return "Not correct box number (%d) % (box_num)"

    u = x * scale_x + move_x
    v = y * scale_y + move_y

    return u,v

# tests
# BOT,TOP = 0,1
# x,y = 0.5,0.5
# w,h,d = 1,1,1
# box_pair = [7,BOT]
# box_convert_uv(x,y,w,h,d, box_pair)
######################### /MATH FUNCTIONS ################################
