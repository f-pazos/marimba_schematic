import key_data
import calculator

L_POS = 1.75
R_POS = 67.25


def compute_dimensions(keys, beam_length, left_offset, right_offset):
    post_to_post = beam_length - left_offset - right_offset 
    nat_width = calculator.width_all_bars(keys)


    # The space in which the keys lie; from the left of the bottom A2 to the 
    # right of the C7.
    total_space = post_to_post - nat_width

    num_nats = len(keys)

    print("Space:", post_to_post)
    print("bars sum: ", nat_width)
    print("sum gap space: ", total_space)
    print("number of naturals: ", num_nats)

    # The gap is the between each bar. Note, there is half a gap on either side 
    # of the last keys, so the number of gaps is equal to the number of bars.
    gap_per_bar = total_space / (num_nats)

    print("gap per bar:", gap_per_bar)

    # ---- 
    # Here, we calculate the coordinate of each post, measured from the joint
    # of the support beam and the marimbutt. 
    # 
    # The post needs to be at the midpoint of the space, so for each we add
    # .5*GAP + bar_width + .5*GAP.
    # 
    # ... i suppose that we could also just add GAP + bar_width to calculate 
    # the offset. This would be more necessary if we decided to implement 
    # non-constant gaps. I don't actually think we want to do that; although 
    # I'm honestly not positive about that. 

    curr_x = left_offset 
    i = 0
    # supports = [(0, "init", coord)]
    supports = []
    posts_x = []

    for key in keys:
        posts_x.append(curr_x)
        curr_x += gap_per_bar / 2
        supports.append([i, key.name, curr_x, curr_x + key.dimension.width])
        curr_x += key.dimension.width + gap_per_bar/2
        i += 1

    posts_x.append(curr_x)

    # for support in [support for support in supports if support[0] == -1]: 
        # print('index: %s, bar: %s, left_x: %s, right_x: %s' % (support[0], support[1], calculator.convert_to_imperial(support[2]), calculator.convert_to_imperial(support[3])))
    
    for x in posts_x: 
        print('x %.4f: %s' % (x, calculator.convert_to_imperial(x)))


# 
# print_beam_measurements calculates the adjusted x measurements of the beam. 
# 
# To do this, we first assume the right and left posts are exactly at their 
# corresponding offsets. Using the marimba width, we can use this to deduce 
# the x positions of the right and left posts; call them x_l and x_r.
#
# From this, we find the horizontal coordinate of the post x, and then to find 
# the correct measurement along the beam, we find the arc length from x_l to x, 
# normalize it as a proportion of the arc length from x_l to x_r, and scale that
# to fit between the the left and right offset on the beam length. 

def print_beam_measurements(quadratic_beam, keys, left_offset, right_offset, beam_length, marimba_width): 
    x_l = left_offset 
    x_r = marimba_width - right_offset 

    post_to_post_arc_length = quadratic_beam.arc_length(x_l, x_r)

    sum_of_bars = calculator.width_all_bars(keys)
    post_to_post_measurement = beam_length - left_offset - right_offset

    bar_gap = (x_r - x_l - sum_of_bars) / len(keys)

    curr_x = x_l

    post_measurements = []

    for key in keys: 
        arc_distance = quadratic_beam.arc_length(x_l, curr_x) 
        post_measurements.append(left_offset + post_to_post_measurement*(arc_distance/post_to_post_arc_length))

        curr_x += bar_gap + key.dimension.width

    arc_distance = quadratic_beam.arc_length(x_l, curr_x)
    print("x_r %s, curr_x %s" %(x_r, curr_x))

    post_measurements.append(left_offset + post_to_post_measurement*(arc_distance/post_to_post_arc_length))

    for x in post_measurements: 
        print('x %.4f: %s' % (x, calculator.convert_to_imperial(x)))


    # right_point = quadratic_beam.y(w)
    # left_point = quadratic_beam.y(0)

    # slope = (right_point-left_point)/w
    # intercept = left_point
    # linear_beam = Line(slope, intercept)

    # full_linear_length = linear_beam.arc_length(0, w)
    # full_quadratic_length = quadratic_beam.arc_length(0, w)

    # for x in post_x_coordinates: 
    #     linear_dimension = linear_beam.arc_length(0, x) / full_linear_length * beam_measurement
    #     quadratic_dimension = quadratic_beam.arc_length(0, x) / full_quadratic_length * beam_measurement
    #     delta = linear_dimension - quadratic_dimension 

    #     print("original_x: %s \t| linear: %s \t| quadratic: %s \t| delta: %s" % (conv_imp(x), conv_imp(linear_dimension), conv_imp(quadratic_dimension),conv_imp(abs(delta))))