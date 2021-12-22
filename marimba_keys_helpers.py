import csv
import classes
import numpy as np

TOTAL_WIDTH = 72
LEFT_X_MARGIN = 1.9775
BAR_GAP = 0.5

def get_keys(filename):
    key_info = {}
    with open(filename, newline='') as csvfile:
        keyreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in keyreader:
            key_info[int(row[5])] = classes.Key(row[0], float(row[1]), float(row[3]), float(row[4]), int(row[5]))
    return key_info

def set_nodes(filename, keys):
    with open(filename, newline='') as csvfile:
        nodereader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in nodereader:
            keys[int(row[4])].set_nodes(float(row[0]), float(row[1]), float(row[3]), float(row[2]))

def get_naturals():
    return get_keys('naturals.csv')

def get_accidentals():
    return get_keys('accidentals.csv')
    
def set_x_bounds(naturals, accidentals):
    curr_x = LEFT_X_MARGIN

    for bar_index in naturals:
        bar = naturals[bar_index]

        bar.l_bound = curr_x
        bar.r_bound = curr_x + bar.width
        
        curr_x = bar.r_bound + BAR_GAP 

    for bar_index in accidentals:
        bar = accidentals[bar_index]
        
        adj_nat = naturals[bar.index-1]
        nat_right_bound = adj_nat.r_bound
        center_of_accidental = nat_right_bound + BAR_GAP/2
    
        bar.l_bound = center_of_accidental - bar.width / 2
        bar.r_bound = center_of_accidental + bar.width / 2

def set_y_bounds(naturals, accidentals):

    for bar_index in naturals:
        bar = naturals[bar_index]

        bar.u_bound = bar.top_l
        bar.d_bound = bar.u_bound- bar.total_length

    for bar_index in accidentals:
        bar = accidentals[bar_index]
        adj_bar = naturals[bar.index-1]

        bar.d_bound = adj_bar.u_bound + 0.85 - bar.bottom_r
        bar.u_bound = bar.d_bound + bar.total_length

def get_best_fit_lines(naturals, accidentals):
    lines = []

    j = 0
    for key_set in [naturals, accidentals]:
        ux = []
        dx = []
        uy = []
        dy = []

        for index in key_set:
            bar = key_set[index]

            uy.append(bar.unl_bound)
            uy.append(bar.unr_bound)
            ux.append(bar.l_bound)
            ux.append(bar.r_bound)

            dy.append(bar.dnl_bound)
            dy.append(bar.dnr_bound)
            dx.append(bar.l_bound)
            dx.append(bar.r_bound)


        lines.append((2*j+1, np.polyfit(ux, uy, 1).tolist()))
        lines.append((2*j, np.polyfit(dx, dy, 1).tolist()))

        j+= 1


    return lines
