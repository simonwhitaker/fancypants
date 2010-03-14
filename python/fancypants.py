class Infographic(object):
    """docstring for Infographic"""
    def __init__(self, data):
        """
        Arguments:
            data:      a list of (string, number) tuples
        """
        super(Infographic, self).__init__()
        self.data = data
        
        # Sort the data, largest to smallest
        self.data.sort(cmp=lambda a,b: cmp(b[1], a[1]))


    def get_frames(self, area, origin=(0,0), padding=0, threshold=0):
        """
        get_frames: return a list of data tuples for an X-O-GRAM-style
        infographic.

        Arguments:
            area:      a tuple containing (width, height) of area to fill with infographic
            origin:    a tuple containing (x, y) coordinates of area to fill (defaults to 0,0)
            padding:   padding between the frames in the infographic (defaults to 0)
            threshold: if total < threshold, aggregate all remaining values into an "other" frame 
    
        Return value is a list of dictionaries:
    
            {
                'label'  : string,
                'value'  : number,
                'x'      : number,
                'y'      : number,
                'width'  : number,
                'height' : number,
            }
        """
    
        # TODO:
        # Enforce some sane threshold? Otherwise can get lots of tiny frames
        if len(self.data) == 0:
            raise Exception("Your infographic needs at least one data point!")
    
        total = 0.0
        # data validation
        for datum in self.data:
            # float() will raise a ValueError if the arg isn't a valid float
            temp = float(datum[1])
            total += temp
            if temp <= 0:
                raise ValueError("All data must contain positive values (%s, %.2f)" % (datum[0], datum[1]))
    
        # Coords for all of data
        x, y = origin
        w, h = area
        
        result = []
    
        for i in range(0, len(self.data)):
            is_last = False
            # If there's a threshold and what's left sums to less than the threshold,
            # aggregate all the remaining data under "Others"
            if total < threshold:
                label, value = ('Others', total)
                is_last = True
            # Otherwise, grab the next datum from data
            else:
                label, value = self.data[i]

            if i == len(self.data) - 1:
                is_last = True
    
            # Coords for this panel
            this_x, this_y  = x, y
            this_w, this_h  = w, h
            
            # If w > h then we'll fix the height to h and set
            # w to a proportion, else do the reverse
            fixed_height = w > h
    
            proportion = float(value) / total
            total -= value
    
            if fixed_height:
                this_w  = int(float(w) * proportion)
                w       = w - this_w
                x       = x + this_w
    
            else:
                this_h  = int(float(h) * proportion)
                h       = h - this_h
                y       = y + this_h
    
            # Adding the padding...
            # If we're working on a fixed height, reduce the height by another 1 * padding
            # If we're working on a fixed width, reduce the width likewise
            # Special case: if this is the last frame, reduce both
            if fixed_height is True and not is_last:
                this_w -= padding

            if fixed_height is False and not is_last:
                this_h -= padding

            # Sanity check: did we end up rendering a negative-sized frame?
            if this_w < 0:
                this_w = 0
            if this_h < 0:
                this_h = 0
    
            this_frame = {
                'label':    label, 
                'value':    value, 
                'x':        this_x, 
                'y':        this_y, 
                'width':    this_w,
                'height':   this_h
            }
            result = result + [this_frame]
            if is_last:
                break
        
        return result

if __name__ == '__main__':
    ig = Infographic([('foo',150),('bar',50)])
    frames = ig.get_frames((400,200), padding=5)
    for f in frames:
        print f