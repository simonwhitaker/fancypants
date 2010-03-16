class Area(object):
    def __init__(self, width, height):
        super(Area, self).__init__()
        self.width = width
        self.height = height

class Point(object):
    def __init__(self, x, y):
        super(Point, self).__init__()
        self.x = x
        self.y = y

class Frame(object):
    def __init__(self, label, value, origin, area):
        super(Frame, self).__init__()
        self.label = label
        self.value = value
        self.origin = origin
        self.area = area
    
    @property
    def width(self):
        return self.area.width
    
    @property
    def height(self):
        return self.area.height
    
    @property
    def x(self):
        return self.origin.x
    
    @property
    def y(self):
        return self.origin.y
    
    def __str__(self):
        return "%s (%s): (%s, %s), (%s, %s)" % (self.value, self.label, self.origin.x, self.origin.y, self.area.width, self.area.height)

class Dataset(object):
    def __init__(self, data):
        """
        Arguments:
            data: a list of (string, number) tuples
        """
        super(Dataset, self).__init__()
        self.data = data
        
        # Sort the data, largest to smallest
        self.data.sort(cmp=lambda a,b: cmp(b[1], a[1]))
    
    def treemap(self, area, origin=Point(0,0), padding=0, threshold=0):
        """
        treemap: returns a set of Frame objects that describe a treemap
        
        Arguments:
            area:      An Area object, describing the size of the treemap
            origin:    A Point object, describing the origin of the treemap in 2D space
            padding:   padding between the frames in the treemap (defaults to 0)
            threshold: if total < threshold, aggregate all remaining values into an "other" frame 
    
        Return value is a list of Frames:
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
        x, y = origin.x, origin.y
        w, h = area.width, area.height
        
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
            # Special case: if this is the last frame, reduce neither
            if fixed_height is True and not is_last:
                this_w -= padding
            
            if fixed_height is False and not is_last:
                this_h -= padding
            
            # Sanity check: did we end up rendering a negative-sized frame?
            if this_w < 0:
                this_w = 0
            if this_h < 0:
                this_h = 0
            
            this_frame = Frame(label=label, value=value, origin=Point(this_x, this_y), area=Area(this_w, this_h))
            result = result + [this_frame]
            if is_last:
                break
        
        return result

if __name__ == '__main__':
    ig = Dataset([('foo',50),('bar',50)])
    frames = ig.treemap(Area(300,200), padding=0)
    for f in frames:
        print f.label, f.value, f.x, f.y, f.width, f.height