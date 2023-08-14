import key_data
import calculator

L_POS = 2.0
R_POS = 67.25

def compute_dimensions():
    keys = key_data.read_keys("key_data_new.csv")

    post_to_post = R_POS - L_POS
    nat_width = calculator.width_all_bars(keys.naturals)

    # The space in which the keys lie; from the left of the bottom A2 to the 
    # right of the C7.
    total_space = post_to_post - nat_width

    num_nats = len(keys.naturals)

    print("Space:", post_to_post)
    print("bars sum: ", nat_width)
    print("sum gap space: ", total_space)
    print("number of naturals: ", num_nats)

    # The gap is the between each bar. 
    gap_per_bar = total_space / num_nats
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

    coord = L_POS
    i = 0
    supports = [(0, "init", coord)]

    for key in keys.naturals:
        coord += gap_per_bar
        coord += key.dimension.width
        i += 1

        supports.append((i, key.name, coord))

    for support in supports: 
        print(support[0], support[1], "{:.3f}".format(support[2]), "",calculator.convert_to_imperial(support[2], 32), sep="\t")