import csv

TOTAL_WIDTH = 72
LEFT_X_MARGIN = 1.9775
BAR_GAP = 0.27


# Represents where node holes lie for a side of a key.
class KeyNodes: 
    def __init__(self, top_offset, bottom_offset):
        self.top_offset = top_offset
        self.bottom_offset = bottom_offset
    
    def __str__(self):
        return "(%.2f,%.2f)" % (self.bottom_offset, self.top_offset)

# Represents the dimensions for a key.
class KeyDimension:
    height: float
    width: float
    left_node: KeyNodes
    right_node: KeyNodes

    def __init__(self, height, width, left_node, right_node):
        self.height = height
        self.width = width
        self.left_node = left_node
        self.right_node = right_node

    def __str__(self):
        return ("dim(%.2fx%.2f)" % (self.width, self.height)) + " left" + str(self.left_node) + " right" + str(self.right_node) 

# Represents a specific key.
class Key: 
    index: int
    name: str
    rack: int
    dimension: KeyDimension

    def __init__(self, index, name, rack, dimension):
        self.index = index
        self.name = name
        self.rack = rack
        self.dimension = dimension    

    def __str__(self):
        return "[" + self.name + ": " + (str(self.dimension)) + "]"

class Keys:
    def __init__(self, naturals, accidentals):
        self.naturals = naturals
        self.accidentals = accidentals

    def __str__(self): 
        return "naturals:" + str([key.name for key in self.naturals]) + "\naccidentals: " + str([key.name for key in self.accidentals])

# Reads in a CSV file, and marshals the data into Key objects.
# CSV Format: 
# (index, name, rack, width, height, l_bottom_offset, l_top_offset, r_bottom_offset, r_top_offset)

def read_keys(filename):
    rows = read_csv(filename)[1:]

    naturals = []
    accidentals = []

    for row in rows:
        '''
        l_node = KeyNodes(float(row[5]), float(row[6]))
        r_node = KeyNodes(float(row[7]), float(row[8]))
        '''

        l_node = None
        r_node = None
        dimension = KeyDimension(float(row[4]), float(row[3]), l_node, r_node)

        key = Key(int(row[0]), row[1].strip(), int(row[2]), dimension)

        if key.rack == 0:
            naturals.append(key)
        else:
            accidentals.append(key)

    return Keys(naturals, accidentals)

# Returns raw CSV file data.
def read_csv(filename):
    rows = []
    with open(filename, newline='') as csvfile:
        keyreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in keyreader:
            rows.append(row)

    return rows




'''

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

    print("Natural L, R: ", naturals[0].l_bound, ", ", naturals[51].r_bound)
    print("Accidentals L, R: ", accidentals[1].l_bound, accidentals[49].r_bound)

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

'''