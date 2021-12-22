class Key:
    def __init__(self, name, width, node_length, total_length, index):
        self.name = name
        self.width = width
        self.total_length = total_length
        self.node_length = node_length
        self.index = index
    
    def set_nodes(self, bottom_l, bottom_r, top_l, top_r):
        self.bottom_l = bottom_l
        self.bottom_r = bottom_r
        self.top_l = top_l
        self.top_r = top_r

    def __eq__(self, other):
        return self.index == other.index
    def __gt__(self, other):
        return (self.index - other.index) > 0
    def __ge__(self, other):
        return (self.index - other.index) >= 0
    def __lt__(self, other):
        return (self.index - other.index) < 0
    def __le__ (self, other):
        return (self.index - other.index) <= 0
