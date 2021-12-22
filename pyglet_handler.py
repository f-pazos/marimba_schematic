import pyglet
from pyglet.graphics.vertexattribute import create_attribute
from pyglet.shapes import Rectangle 
import math, random
from pyglet.window.key import R


global naturals, accidentals, MARIMBA_WIDTH

dimensions = {}

L_BOUND = 0.05
R_BOUND = 0.95

MARIMBA_HEIGHT = 34.25
SUPPORT_WIDTH = 0.75

LEFT_BUTT_WIDTH = 32.5
RIGHT_BUTT_WIDTH = 12.75

window = pyglet.window.Window(1920, 1080, "test")
batch = pyglet.graphics.Batch()
shapes = []


@window.event
def on_draw(): 
    window.clear()
    batch.draw()
    pyglet.image.get_buffer_manager().get_color_buffer().save('screenshot.png')
    
def add_shapes(lst):
    for shape in lst:
        shapes.append(shape)

def create_midpoint():
    line = pyglet.shapes.Line(0, window.height//2, window.width, window.height//2, 1, color=(255, 255, 255), batch=batch)
    line.opacity = 255
    return [line]

def create_bounds():
    l_bound = window.width * L_BOUND
    r_bound = window.width * R_BOUND

    u_bound = y_to_pixel(MARIMBA_HEIGHT / 2)
    d_bound = y_to_pixel(-1 * MARIMBA_HEIGHT / 2)

    l_line = pyglet.shapes.Line(l_bound, 0, l_bound, window.height, 1, color=(255, 255, 255), batch=batch)
    r_line = pyglet.shapes.Line(r_bound, 0, r_bound, window.height, 1, color=(255, 255, 255), batch=batch)
    u_line = pyglet.shapes.Line(0, u_bound, window.width, u_bound, 1, color=(255, 255, 255), batch=batch)
    d_line = pyglet.shapes.Line(0, d_bound, window.width, d_bound, 1, color=(255, 255, 255), batch=batch)

    l_line.opacity = 100
    r_line.opacity = 100
    u_line.opacity = 100
    d_line.opacity = 100

    add_shapes([l_line, r_line, u_line, d_line])

def create_keys():
    shapes = []

    color = (255, 0, 0)
    for index in naturals | accidentals :
        if index in naturals:
            key = naturals[index]
            color = (255, 0, 0)
        else:
            key = accidentals[index]
            color = (0, 255, 0)

        xbound = (key.r_bound, key.l_bound)
        ybound = (key.u_bound, key.d_bound)
        
        l_bound = x_to_pixel(xbound[0])
        r_bound = x_to_pixel(xbound[1])

        u_bound = y_to_pixel(ybound[0])
        d_bound = y_to_pixel(ybound[1])

        key.unl_bound = key.u_bound - key.top_l
        key.unr_bound = key.u_bound - key.top_r
        key.dnl_bound = key.d_bound + key.bottom_r
        key.dnr_bound = key.d_bound + key.bottom_l
    
        unl_bound = y_to_pixel(key.unl_bound)
        unr_bound = y_to_pixel(key.unr_bound)
        dnl_bound = y_to_pixel(key.dnl_bound)
        dnr_bound = y_to_pixel(key.dnr_bound)

        rectangle = pyglet.shapes.Polygon([l_bound, u_bound], [r_bound, u_bound], [r_bound, d_bound], [l_bound, d_bound], color=color, batch=batch)
        rectangle.opacity = 128

        top_node = pyglet.shapes.Line(l_bound, unl_bound, r_bound, unr_bound, 2, color = (0,0,0), batch = batch)
        top_node.opacity = 255

        bottom_node = pyglet.shapes.Line(l_bound, dnl_bound, r_bound, dnr_bound, 2, color = (0,0,0), batch = batch)
        bottom_node.opacity = 255

        shapes.append(rectangle)
        shapes.append(top_node)
        shapes.append(bottom_node)

    add_shapes(shapes)

def y_to_pixel(val):
    return int(val * INCH_TO_PIXEL_FACTOR + window.height / 2)

def x_to_pixel(val):
    return int(val * INCH_TO_PIXEL_FACTOR + L_BOUND * window.width)

    
def create_nodelines(lines):
    shapes = []

    color = (248, 168, 184) 

    for (index, line) in lines:
        lx = x_to_pixel(0)
        rx = x_to_pixel(MARIMBA_WIDTH)

        ly = y_to_pixel(line[1])
        ry = y_to_pixel(line[0] * MARIMBA_WIDTH + line[1])

        angle = math.atan2(line[0], 1)
        extra_y = math.cos(angle) * SUPPORT_WIDTH / 2 * INCH_TO_PIXEL_FACTOR

        ldim = line[1]
        rdim = line[0] * MARIMBA_WIDTH + line[1]
        extra_dim = math.cos(angle) * SUPPORT_WIDTH / 2
        
        print("LINE ", index)
        print("\tLEFT SIDE DIMENSIONS:")
        print("\t\tlower: ", ldim - extra_dim)
        print("\t\thigher: ", ldim + extra_dim)
        print("\tRIGHT SIDE DIMENSIONS: ")
        print("\t\tlower: ", rdim - extra_dim)
        print("\t\thigher: ", rdim + extra_dim)
        
        print("\tANGLE: ", angle / math.pi * 180)

        dimensions[index] = {}
        dimensions[index]["left_butt"] = (ldim - extra_dim, ldim + extra_dim)
        dimensions[index]["right_butt"] = (rdim - extra_dim, rdim + extra_dim)
        dimensions[index]["angle"] = angle / math.pi * 180

        line_shape = pyglet.shapes.Polygon([lx, ly + extra_y], [rx, ry + extra_y], [rx, ry - extra_y], [lx, ly - extra_y], color=color, batch=batch)
        line_shape.opacity = 128
        

        shapes.append(line_shape)

    add_shapes(shapes)

def draw_rectangle(l_bound, r_bound, d_bound, u_bound, color, opacity):
    shape = pyglet.shapes.Polygon(
        [x_to_pixel(l_bound), y_to_pixel(u_bound)], 
        [x_to_pixel(r_bound), y_to_pixel(u_bound)],
        [x_to_pixel(r_bound), y_to_pixel(d_bound)],
        [x_to_pixel(l_bound), y_to_pixel(d_bound)], 
        color=color, batch=batch)
    shape.opacity = opacity
    add_shapes([shape])

    pyglet.shapes.Polygon([l_bound, u_bound], [r_bound, u_bound], [r_bound, d_bound], [l_bound, d_bound], color=color, batch=batch)

def create_leftbutt():

    shapes = []

    d_bound = dimensions[0]["left_butt"][0] - 1.25 - .125 - 0.01 # To account for rounding width from 29.72 to 29.75
    u_bound = d_bound + LEFT_BUTT_WIDTH
    l_bound = -1.25
    r_bound = .75


    midpoint_1 = dimensions[1]["left_butt"][1] - 0.375
    midpoint_2 = dimensions[2]["left_butt"][1] - 0.375

    white = (255, 255, 255)
    orange = (255, 128, 0)

    draw_rectangle(l_bound, r_bound, d_bound, u_bound, white, 128)

    curr_bottom = d_bound
    for dy in [1.25, 1.125, 11.3125, 1.0625, 1.5, 1.5, 1.0625, 11.3125, 1.125, 1.25]:
        
        draw_rectangle(0, r_bound, curr_bottom, curr_bottom + dy, [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)], 255)
        curr_bottom += dy


                                                                    # LEFT BUTT DIMENSIONS
    # draw_rectangle(0, r_bound, d_bound, d_bound + 1.25, white, 255) # Lowest, 1.25" 
    # draw_rectangle(0, r_bound, d_bound + 1.25 + 1.125, midpoint_1 - 0.5, white, 255) # In between 0 and 1, 11.3125"
    # draw_rectangle(0, r_bound, midpoint_1 + 0.5625, d_bound + LEFT_BUTT_WIDTH / 2, white, 255) # In between 1 and mid, 1.5" 


    # draw_rectangle(0, r_bound, u_bound - LEFT_BUTT_WIDTH / 2, midpoint_2 - 0.5625, orange, 255) # Between mid and 2, 1.5"
    # draw_rectangle(0, r_bound, midpoint_2 + 0.5, u_bound - 1.25 - 1.125, orange, 255) # Between 2 and 3, 11,3125"
    # draw_rectangle(0, r_bound, u_bound - 1.25, u_bound, orange, 255) # Top, 1.25"

    print("LEFT_BUTT")
    print("\tBetween 0 and 1: ", midpoint_1 - 0.5 - (d_bound + 1.25 + 1.125))
    print("\tBetween 1 and mid: ", d_bound + LEFT_BUTT_WIDTH / 2 - (midpoint_1 + 0.5))
    print("\tBetween mid and 2: ", midpoint_2 - 0.5 - (u_bound - LEFT_BUTT_WIDTH / 2))
    print("\tBetween 2 and 3: ", u_bound - 1.25 - 1.125 - (midpoint_2 + 0.5))

def create_rightbutt():

    shapes = []

    d_bound = dimensions[0]["right_butt"][0] - 1.25 - .125 - 0.02 # To account for rounding dimension
    u_bound = d_bound + RIGHT_BUTT_WIDTH
    l_bound = MARIMBA_WIDTH - 0.75
    r_bound = MARIMBA_WIDTH + 1.25


    midpoint_1 = dimensions[1]["right_butt"][1] - 0.375
    midpoint_2 = dimensions[2]["right_butt"][1] - 0.375

    white = (255, 255, 255)
    orange = (255, 128, 0)

    draw_rectangle(l_bound, r_bound, d_bound, u_bound, white, 128)
    
    curr_bottom = d_bound
    for dy in [1.125, 1.125, 2.25, 1.0625, 0.8125, 0.8125, 1.0625, 2.25, 1.125, 1.125]:
        
        draw_rectangle(l_bound, MARIMBA_WIDTH, curr_bottom, curr_bottom + dy, [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)], 255)
        curr_bottom += dy

    input(dimensions[1]["right_butt"][0] - dimensions[0]["right_butt"][1])
                                                                                # RIGHT BUTT DIMENSIONS
    # draw_rectangle(l_bound, MARIMBA_WIDTH, d_bound, d_bound + 1.125, white, 255) # Lowest
    # draw_rectangle(l_bound, MARIMBA_WIDTH, d_bound + 1.125 + 1.125, midpoint_1 - 0.5, white, 255) # In between 0 and 1
    # draw_rectangle(l_bound, MARIMBA_WIDTH, midpoint_1 + 0.5625, d_bound + RIGHT_BUTT_WIDTH / 2, white, 255) # In between 1 and mid

    # draw_rectangle(l_bound, MARIMBA_WIDTH, u_bound - RIGHT_BUTT_WIDTH / 2, midpoint_2 - 0.5625, orange, 255) # Between mid and 2
    # draw_rectangle(l_bound, MARIMBA_WIDTH, midpoint_2 + 0.5, u_bound - 1.125 - 1.125, orange, 255) # Between 2 and 3
    # draw_rectangle(l_bound, MARIMBA_WIDTH, u_bound - 1.125, u_bound, orange, 255) # Top 

    print("RIGHT_BUTT")
    print("\tBetween 0 and 1: ", midpoint_1 - 0.5 - (d_bound + 1.125 + 1.125))
    print("\tBetween 1 and mid: ", d_bound + RIGHT_BUTT_WIDTH / 2 - (midpoint_1 + 0.5))
    print("\tBetween mid and 2: ", midpoint_2 - 0.5 - (u_bound - RIGHT_BUTT_WIDTH / 2))
    print("\tBetween 2 and 3: ", u_bound - 1.125 - 1.1125 - (midpoint_2 + 0.5))


def set_keys(nats, accs):
    global naturals, accidentals, MARIMBA_WIDTH, INCH_TO_PIXEL_FACTOR
    naturals = nats
    accidentals = accs
    MARIMBA_WIDTH = nats[51].r_bound + 1.9775
    INCH_TO_PIXEL_FACTOR = window.width*(R_BOUND - L_BOUND) / MARIMBA_WIDTH

    print("Total Marimba Width: ", MARIMBA_WIDTH)


def run():
    pyglet.app.run()