import key_data
import calculator

L_POS = 1.75
R_POS = 67.25

def compute_dimensions():
    # keys = key_data.read_keys("key_data_new.csv")

    natural_keys = key_data.read_keys("jeezus_naturals.csv").naturals
    post_to_post = R_POS - L_POS
    nat_width = calculator.width_all_bars(natural_keys)

    # The space in which the keys lie; from the left of the bottom A2 to the 
    # right of the C7.
    total_space = post_to_post - nat_width

    num_nats = len(natural_keys)

    print("Space:", post_to_post)
    print("bars sum: ", nat_width)
    print("sum gap space: ", total_space)
    print("number of naturals: ", num_nats)

    # The gap is the between each bar. 
    gap_per_bar = total_space / (num_nats - 1)
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

    curr_x = L_POS
    i = 0
    # supports = [(0, "init", coord)]
    supports = []

    for key in natural_keys:
        supports.append([i, key.name, curr_x, curr_x + key.dimension.width])
        curr_x += gap_per_bar + key.dimension.width
        i += 1

    for support in supports: 
        print('index: %s, bar: %s, left_x: %s, right_x: %s' % (support[0], support[1], calculator.convert_to_imperial(support[2]), calculator.convert_to_imperial(support[3])))