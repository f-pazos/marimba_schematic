

# Returns the width of all the bars with no spaces. 
def width_all_bars(rack):
    total = 0
    for key in rack:   
        total += key.dimension.width
    
    return total

# Returns a string representation of the measurement in imperial units; up to 
# the given precision. 
def convert_to_imperial(dim, prec=32) -> str: 
    d = dim//1

    r = dim%1
    num = round(prec*r)
    den = prec

    while num%2 == 0 and den > 1:
        num = num//2
        den = den//2


    return "{:.0f} {:.0f}/{:.0f}".format(d, num, den)
