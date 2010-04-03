class Rect(object):
    def __init__(self, width, height):
        super(Rect, self).__init__()
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

class BaseData(object):
    """Base class for data objects"""
    def __init__(self):
        super(BaseData, self).__init__()
        self.label = None
        self.value = None
    
    def get_total(self):
        """Returns total value of the data object"""
        raise NotImplementedError()
    
    def get_label(self):
        return self.label

class DataPoint(BaseData):
    """docstring for DataPoint"""
    def __init__(self, value, label=None):
        super(DataPoint, self).__init__()
        
        if value < 0:
            raise ValueError("All data must contain positive values (%.2f, %s)" % (value, label))
        
        self.label = label
        self.value = value
    
    def get_total(self):
        return self.value
    
    def get_value(self):
        return self.value

class Dataset(object):
    def __init__(self, data, label=None):
        super(Dataset, self).__init__()
        self.data = []
        self.label = label
        self.total = None
        
        # print "Dataset ctor called with %s, %s" % (data, label)
        
        for datum in data:
            (label, value) = datum
            if self.label and label:
                label = "%s.%s" % (self.label, label)
            
            if (isinstance(value, list)):
                self._append_data(Dataset(value, label))
            else:
                self._append_data(DataPoint(value, label))
        
        # Sort the data, largest to smallest
        self.sort()
    
    def sort(self):
        # Sort the data, largest to smallest
        self.data.sort(cmp=lambda a,b: cmp(b.get_total(), a.get_total()))
    
    def _append_data(self, data):
        self.data.append(data)
        # Unset total so it gets recalculated on next call to get_total
        self.total = None
    
    def append_data(self, data):
        self._append_data(data)
        self.sort()
    
    def get_total(self):
        if self.total is None:
            total = 0
            for datum in self.data:
                total += datum.get_total()
            self.total = total
        return self.total
    
    def treemap(self, area, origin=Point(0,0), padding=0, threshold=0, flat=True):
        """
        treemap: returns a set of Frame objects that describe a treemap
        
        Arguments:
            area:      A Rect object, describing the size of the treemap
            origin:    A Point object, describing the origin of the treemap in 2D space
            padding:   padding between the frames in the treemap (defaults to 0)
            threshold: if total < threshold, aggregate all remaining values into an "other" frame 
            flat:      if nested data is provided, provide a flat array as output, rather
                       than nested arrays
    
        Return value is a list of Frames
        """
    
        # TODO:
        # Enforce some sane threshold? Otherwise can get lots of tiny frames
        if len(self.data) == 0:
            raise Exception("Your infographic needs at least one data point!")
    
        total = self.get_total()
    
        # Coords for all of data
        x, y = origin.x, origin.y
        w, h = area.width, area.height
        
        result = []
    
        for i in range(0, len(self.data)):
            try:
                datum = self.data[i]
            except IndexError:
                print "index %i out of range for data of length %i" % (i, len(data))
                raise IndexError
                
            is_last = False
            
            # If there's a threshold and what's left sums to less than the threshold,
            # aggregate all the remaining data under "Others"
            # print "checking threshold, comparing %i < %i" % (total, threshold)
            if total < threshold:
                label_tokens = datum.label.split('.')
                label_tokens[-1] = 'Others'
                label = '.'.join(label_tokens)
                datum = DataPoint(total, label)
                is_last = True
    
            if i == len(self.data) - 1:
                is_last = True
    
            # Coords for this panel
            this_x, this_y  = x, y
            this_w, this_h  = w, h
            
            # If w > h then we'll fix the height to h and set
            # w to a proportion, else do the reverse
            fixed_height = w > h
    
            proportion = float(datum.get_total()) / total
            total -= datum.get_total()
    
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
            
            origin = Point(this_x, this_y)
            area   = Rect(this_w, this_h)
            
            if (isinstance(datum, DataPoint)):
                result.append(Frame(label=datum.label, value=datum.value, origin=origin, area=area))
            else:
                tmap = datum.treemap(area, origin, padding=padding, flat=flat, threshold=threshold)
                if flat:
                    result = result + tmap
                else:
                    result.append(tmap)
            if is_last:
                break
        
        return result


if __name__ == '__main__':
    ig = Dataset(
        [
            ('foo', 50), 
            ('bar', 50),
            ('a', [
                ('foo', 20), 
                ('bar', 30),
                ('wibble', [
                    ('oof', 40),
                    ('boof', 50)
                ])
            ])
        ]
    )
    frames = ig.treemap(Rect(300,200), padding=0)
    for f in frames:
        print f

    print "-------------------------"

    ig.append_data(DataPoint(110, 'blah'))
    frames = ig.treemap(Rect(300,200), padding=0)
    for f in frames:
        print f
