import svgwrite
import marimba
import key_data
import calculator



# The canvas is 10'. Each unit is a 16th. (10' * 12"/1' * 16) = 1920
SIZE = 1920

ORIGIN_Y = SIZE / 2
ORIGIN_X = SIZE / 5

FRACTION = 16

MARIMBA_WIDTH = 69

LEFT_POST_GAP = 1.75
BAR_GAP = .2943
class Stroke:
    def __init__(self, color, stroke_width, opacity):
        self.color = color
        self.stroke_width = stroke_width 
        self.opacity = opacity

DEFAULT_STROKE = Stroke(svgwrite.rgb(0, 0, 0, 'RGB'), 5, 1)

def visualize():

    left_butt = marimba.Butt(4*16, 32*16, 16*16)
    right_butt = marimba.Butt(4*16, 16*16, 8*16)

    keys = key_data.read_keys("jeezus_naturals.csv")


    mrm = marimba.MarimbaSchematic(
        MARIMBA_WIDTH, 
        marimba.Butt(3, 36, 18), 
        marimba.Butt(3, 14, 7), 
        [
            marimba.Beam(-2.09375, -1.5, 1), 
            marimba.Beam(-15.28125, -5.375, 1), 
            marimba.Beam(2.5625, 1.2625, 1), 
            marimba.Beam(14.75, 4.375, 1), 
        ],
            keys.naturals, 
            keys.accidentals
    )

    dwg = svgwrite.Drawing('test.svg', size=(SIZE, SIZE), profile='tiny')

    draw_axes(dwg)
    # draw_rectangle(dwg, (0, -2*16), (74*16, 4*16))

    # draw_rectangle(dwg, (0, 0), (16*12, 32*12))
    # draw_butt(dwg, left_butt, -4*16)
    # draw_butt(dwg, right_butt, 74*16)
    draw_marimba(dwg, mrm)
    dwg.save()


# Computes all possible adjustments and right post offsets within a the range 
# (search_start, search_end) with the given number of samples, and picks with 
# the lowest error. Error is computed as the sum of the squared errors of each 
# bar node. The return is the distance between the adjusted bar and the lower 
# bar.
def compute_best_dimensions(marimba, top_beam, lower_beam, keys, gap, search_start, search_end, samples):
    left_point = (0, lower_beam.left_offset)
    right_point = (marimba.midbeam_width, lower_beam.right_offset)

    best_error = 1000000000

    right_offset_start = 0
    right_offset_end = -10

    for i in range(samples): 
        if i % 10 == 0: 
            print(i)
            
        # right_offset = 10 * i / samples
        right_offset = right_offset_start + (i / (samples-1)) * (right_offset_end - right_offset_start)
        lower_beam.right_offset = right_offset
        right_point = (marimba.midbeam_width, right_offset)
        for j in range(samples): 
            adjustment = search_start + (search_end - search_start) * (j / (samples-1))
            width = marimba.midbeam_width

            lower_beam_mid_y = get_beam_y(lower_beam, width, width / 2)

            top_beam_mid_y = get_beam_y(top_beam, width, width / 2)

            default_distance = abs(lower_beam_mid_y) - abs(top_beam_mid_y)
            proposed_distance = default_distance + adjustment


            third_point = (width / 2, top_beam_mid_y - proposed_distance)

            coordinates = (left_point[1], third_point[0], third_point[1], right_point[0], right_point[1])
            a = calc_a(*coordinates)
            b = calc_b(*coordinates)
            c = calc_c(*coordinates)

            error = compute_error(a, b, c, marimba, top_beam, keys, gap)

            if error < best_error: 
                best_error = error 
                best_candidates = (right_offset, default_distance + adjustment)

    return best_candidates

def compute_error(a, b, c, marimba, top_beam, keys, gap): 

    curr_x = 0
    error = 0 
    error_exp = 1.5
    for key in keys: 
        key = key.dimension
        top_beam_y = get_beam_y(top_beam, marimba.midbeam_width, curr_x)
        lower_beam_y = quadratic_of(curr_x, a, b, c)

        ideal_gap = key.height - key.nw_offset - key.sw_offset
        actual_gap = abs(lower_beam_y) - abs(top_beam_y)
        d_error = abs(ideal_gap - actual_gap)**error_exp
        error += d_error


        curr_x += key.width

        top_beam_y = get_beam_y(top_beam, marimba.midbeam_width, curr_x)
        lower_beam_y = quadratic_of(curr_x, a, b, c)

        ideal_gap = key.height - key.nw_offset - key.sw_offset
        actual_gap = abs(lower_beam_y) - abs(top_beam_y)

        error += abs(ideal_gap - actual_gap)**error_exp

        curr_x += gap


    return error






def draw_marimba(drawing, marimba): 
    # draw_butt(drawing, marimba.left_butt, -marimba.left_butt.width) 
    # draw_butt(drawing, marimba.right_butt, marimba.midbeam_width)

    # for beam in marimba.beams:
    #     draw_beam(drawing, marimba, beam)


    draw_beam(drawing, marimba, marimba.beams[0])


    (ideal_right_offset, ideal_mid_width)= compute_best_dimensions(marimba, marimba.beams[0], marimba.beams[1], marimba.naturals, BAR_GAP, -4, 4, 1000)

    # ideal_right_offset = -.114114114114114 
    # ideal_mid_width =7.822541291291291 

    # ideal_right_offset = 10

    print(ideal_right_offset, ideal_mid_width)
    # exit()

    print("the ideal offset is %s" % ideal_mid_width)

    adjustment_x = marimba.midbeam_width / 2

    marimba.beams[1].right_offset = ideal_right_offset

    upper_beam_y = get_beam_y(marimba.beams[0], marimba.midbeam_width, adjustment_x)
    lower_beam_y = get_beam_y(marimba.beams[1], marimba.midbeam_width, adjustment_x)

    adjustment_y = upper_beam_y - ideal_mid_width 

    draw_quadratic_beam(drawing, marimba, marimba.beams[1], adjustment_y, adjustment_x, 100)


    # draw_line(drawing, scale_dimensions((adjustment_x, beam_y)), scale_dimensions((adjustment_x, adjustment_y)))


    draw_naturals(drawing, marimba.naturals, marimba.beams[0], MARIMBA_WIDTH, LEFT_POST_GAP, BAR_GAP)

def get_beam_y(beam, width, x): 
    dy = beam.right_offset - beam.left_offset
    dx = width

    return beam.left_offset + (dy/dx)*x


def draw_naturals(drawing, keys, beam, marimba_width, l_gap, spacing): 
    current_x = l_gap
    for key in keys: 
        y = get_beam_y(beam, marimba_width, current_x)

        sw_corner = (current_x, y - key.dimension.height + key.dimension.nw_offset)
        dimensions = (key.dimension.width, key.dimension.height)

        draw_rectangle(drawing, scale_dimensions(sw_corner), scale_dimensions(dimensions), Stroke(svgwrite.rgb(0, 0, 0, 'RGB'), 1, 1))
        draw_nodes(drawing, sw_corner, key.dimension)
        current_x += spacing + key.dimension.width

    return


def draw_nodes(drawing, sw_corner, key_dimension): 
    left_x = sw_corner[0]
    right_x = sw_corner[0] + key_dimension.width
    top_y = sw_corner[1] + key_dimension.height - key_dimension.nw_offset 
    right_bottom_y = sw_corner[1] + key_dimension.se_offset
    left_bottom_y = sw_corner[1] + key_dimension.sw_offset

    points = [(left_x, left_bottom_y), (left_x, top_y), (right_x, top_y), (right_x, right_bottom_y), (left_x, left_bottom_y)]
    scaled = [normalize_coordinate(scale_dimensions(p)) for p in points]

    # sw_node_offset = scale_dimensions((0, key_dimension.sw_offset))
    # sw_node_coords = (sw_corner[0] + sw_node_offset[0], sw_corner[1] + sw_node_offset[1])


    # mid_node_height = key_dimension.height - key_dimension.nw_offset - key_dimension.sw_offset

    drawing.add(
        drawing.polyline(
            scaled, 
            stroke=svgwrite.rgb(255,0,0,'RGB'), 
            stroke_width=2,
            opacity=1,
            fill="none"
       )
    )
    # draw_rectangle(drawing, sw_node_coords, scale_dimensions((key_dimension.width, mid_node_height)), Stroke(svgwrite.rgb(255, 0, 0, 'RGB'), 2, 1))


def draw_beam(drawing, marimba, beam):
    draw_line(drawing, scale_dimensions((0, beam.left_offset)), scale_dimensions((marimba.midbeam_width, beam.right_offset)))


# Draws a polyline that approximates a parabola such that the endpoints are the
# the same as the beam, but includes the point (adjustment_x, adjustment_y).
def draw_quadratic_beam(drawing, marimba, beam, adjustment_y, adjustment_x, samples): 
    # y = 7x^2 * 3x + 2
    # (0, 2), (1, 12), (2, 36)

    p0 = (0, beam.left_offset)
    p1 = (marimba.midbeam_width, beam.right_offset)
    p2 = (adjustment_x, adjustment_y)

    coordinates = (p0[1], p1[0], p1[1], p2[0], p2[1])

    a = calc_a(*coordinates)
    b = calc_b(*coordinates)
    c = calc_c(*coordinates)

    points = [] 
    curr_x = 0 
    dx = (marimba.midbeam_width / samples)
    for i in range(samples): 
        p = (curr_x, quadratic_of(curr_x, a, b, c))
        points.append(normalize_coordinate(scale_dimensions(p)))    
        curr_x += dx 


    drawing.add(
        drawing.polyline(
            points, 
            stroke=DEFAULT_STROKE.color, 
            opacity=DEFAULT_STROKE.opacity, 
            stroke_width=DEFAULT_STROKE.stroke_width,
            fill="none",

        )
    )

def quadratic_of(x, a, b, c): 
    return a*x*x + b*x + c

def calc_a(a, c, d, e, f): 
    return (f - calc_b(a, c, d, e, f)*e - a) / (e*e)

def calc_b(a, c, d, e, f): 
    # return (y2*y2 - (x2*(y3*y3-y1*y1))/x3 - y1*y1) / (x2*x2 - x3*x2)
    return (d  - c*c*(f-a)/(e*e) - a) / (c - c*c/e)

def calc_c(a, c, d, e, f): 
    return a



def draw_butt(drawing, butt, x_offset): 
    sw_corner = scale_dimensions((x_offset, -butt.y_offset))
    draw_rectangle(drawing, sw_corner, scale_dimensions((butt.width, butt.height)))
    return

# def draw_line(drawing, start, end, stroke=Stroke(svgwrite.rgb(0, 0, 0, 'RGB'), 5, 1)): 
#     drawing.add(
#         drawing.line(
#             normalize_coordinate(scale_dimensions(start)), 
#             normalize_coordinate(scale_dimensions(end)), 
#             stroke = stroke.color, 
#             stroke_width = stroke.stroke_width, 
#             opacity = stroke.opacity
#         )
#     )

# Draws a rectangle. The given coordinates are abstract coordinates, 
# not the screen ones. 
def draw_rectangle(drawing, sw_corner, dimensions, stroke=Stroke(svgwrite.rgb(0, 0, 0, 'RGB'), 5, 1)): 

    nc = normalize_coordinate(sw_corner)

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

def scale_dimensions(x): 
    return (x[0]*FRACTION, x[1]*FRACTION)