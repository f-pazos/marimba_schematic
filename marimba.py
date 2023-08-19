# Helper class to represent the dimensions of a marimba's frame.

import key_data

# A butt represents the dimensions of a butt. 
# - y_offset is the measure from the bottom of the butt to the origin of the 
# marimba.
class Butt: 
    def __init__(self, width, height, y_offset):
        self.width = width
        self.height = height
        self.y_offset = y_offset 

# A beam represents a cross beam. The offset parameters measure how far the 
# bottom of the beam is on the frame. 
class Beam: 
    def __init__(self, left_offset, right_offset, width):
         self.left_offset = left_offset
         self.right_offset = right_offset
         self.width = width


# A marimba represents the dimensions for a marimba. The dimensions are  
# registered against the "origin" of the marimba, which is defined as the 
# the point in space where the  left butt transitions from the naturals to the
# naturals. The point is on the inside of the marimba. 
class MarimbaSchematic: 
    def __init__(
            self,             
            midbeam_width,
            left_butt, 
            right_butt, 
            beams, 
            naturals, 
            accidentals
    ):
            self.midbeam_width = midbeam_width
            self.left_butt = left_butt            
            self.right_butt = right_butt 
            self.beams = beams
            self.naturals = naturals
            self.accidentals = accidentals