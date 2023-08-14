# Helper class to represent the dimensions of a marimba's frame.


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
    def __init__(self, left_offest, right_offset):
         return


# A marimba represents the dimensions for a marimba. The dimensions are  
# registered against the "origin" of the marimba, which is defined as the 
# the point in space where the  left butt transitions from the naturals to the
# naturals. The point is on the inside of the marimba. 
class Marimba: 
    def __init__(
            self,             
            midbeam_width,
            left_butt_height, 
            left_butt_width, 
            left_butt_offset, 
            right_butt_height, 
            right_butt_width,            
            right_butt_offset, 
    ):
            self.midbeam_width = midbeam_width
            self.left_butt = Butt(left_butt_width, left_butt_height, left_butt_offset)
            self.right_butt = Butt(right_butt_width, right_butt_height, right_butt_offset)
