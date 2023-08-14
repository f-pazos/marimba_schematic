import svgwrite
import marimba



# The canvas is 10'. Each unit is a 16th. (10' * 12"/1' * 16) = 1920
SIZE = 1920

ORIGIN_Y = SIZE / 2
ORIGIN_X = SIZE / 5




class Stroke:
    def __init__(self, color, stroke_width, opacity):
        self.color = color
        self.stroke_width = stroke_width 
        self.opacity = opacity


def visualize():
    left_butt = marimba.Butt(4*16, 32*16, 16*16)
    right_butt = marimba.Butt(4*16, 16*16, 8*16)
    dwg = svgwrite.Drawing('test.svg', size=(SIZE, SIZE), profile='tiny')

    draw_axes(dwg)
    draw_rectangle(dwg, (0, -2*16), (74*16, 4*16))

    # draw_rectangle(dwg, (0, 0), (16*12, 32*12))
    draw_butt(dwg, left_butt, -4*16)
    draw_butt(dwg, right_butt, 74*16)
    dwg.save()


def draw_marimba(drawing, marimba): 
    return



def draw_butt(drawing, butt, x_offset): 
    sw_corner = (x_offset, -butt.y_offset)

    draw_rectangle(drawing, sw_corner, (butt.width, butt.height))
    return



# Draws a rectangle. The given coordinates are abstract coordinates, 
# not the screen ones. 
def draw_rectangle(drawing, sw_corner, dimensions, stroke=Stroke(svgwrite.rgb(0, 0, 0, 'RGB'), 5, 1)): 

    nc = normalize_coordinate(sw_corner)
    print(nc)

    drawing.add(
        drawing.rect(
            insert=(nc[0], nc[1]-dimensions[1]), 
            size=dimensions, 
            stroke=stroke.color, 
            stroke_width=stroke.stroke_width, 
            fill_opacity=0,
            opacity=stroke.opacity
            )
        )
    


def draw_axes(drawing): 
    blueprint_color = svgwrite.rgb(3, 182, 252, 'RGB')
    axis_stroke = Stroke(color(100, 100, 100), 2.5, 1)

    draw_line(drawing, (-SIZE, 0), (SIZE, 0), stroke=axis_stroke)
    draw_line(drawing, (0, -SIZE), (0, SIZE), stroke=axis_stroke)

    hash_stroke = Stroke(color(100, 100, 100), 1.5, .5)
    # Draw hashes every inch.  
    hashes = [16 * i for i in range (-120, 120)]
    for hash in hashes: 
        draw_line(drawing, (hash, -8), (hash, 8), stroke=hash_stroke)
        draw_line(drawing, (-8, hash), (8, hash), stroke=hash_stroke)

    grid_stroke = Stroke(blueprint_color, .5, 0.5)

    # draw the grid, every foot.
    grid_offsets = [12 * 16 * i for i in range(-10, 10)]
    for grid_offset in grid_offsets:
        draw_line(drawing, (-SIZE, grid_offset), (SIZE, grid_offset), stroke=grid_stroke) 
        draw_line(drawing, (grid_offset, -SIZE), (grid_offset, SIZE), stroke=grid_stroke)
    

def draw_line(
        drawing, 
        start_point, 
        end_point, 
        stroke=Stroke(svgwrite.rgb(0, 0, 0, 'RGB'), 10, 1)):

    drawing.add(
        drawing.line(
        normalize_coordinate(start_point), 
        normalize_coordinate(end_point),
        opacity= stroke.opacity,
        stroke = stroke.color,
        stroke_width = stroke.stroke_width
        ))


def normalize_coordinate(coords): 
    return (ORIGIN_X + coords[0], ORIGIN_Y - coords[1])


def color(r, g, b): 
    return svgwrite.rgb(r, g, b, 'RGB')