function Rect(width, height) {
    this.width = width;
    this.height = height;
}

function Point(x, y) {
    this.x = x;
    this.y = y;
}

function Frame (label, value, origin, area) {
    this.label = label;
    this.value = value;
    this.origin = origin;
    this.area = area;
}

function TreeMap() {
    this.frames = [];
}

TreeMap.prototype.push = function(data) {
    this.frames.push(data);
}

TreeMap.prototype.concat = function(data) {
    if (data instanceof TreeMap) {
        this.frames = this.frames.concat(data.frames);
    } else {
        throw "Argument to TreeMap.concat must be a TreeMap object";
    }
}

function BaseData() { }

BaseData.prototype.get_total = function() {
    throw "Not implemented";
};

BaseData.prototype.get_label = function() {
    return this.label;
};

function DataPoint(value, label) {
    if (value < 0) {
        throw "value arg to DataPoint constructor must be >= 0";
    }
    this.value = value;
    this.label = label;
}

// DataPoint inherits from BaseData
// see https://developer.mozilla.org/en/Introduction_to_Object-Oriented_JavaScript
DataPoint.prototype = new BaseData();
DataPoint.prototype.constructor = DataPoint;

DataPoint.prototype.get_total = function() {
    return this.value;
};

DataPoint.prototype.get_value = function() {
    return this.value;
};

DataPoint.prototype.get_label = function() {
    return this.label;
};

function Dataset(data, label) {
    this.data = [];
    this.label = label;
    this.total = null;
    
    for (var i = 0; i < data.length; i++) {
        var datum = data[i];
        var label = datum[0];
        var value = datum[1];
        
        if (this.label && label) {
            label = this.label + '.' + label;
        }
        
        if (value instanceof Array) {
            this._append_data(new Dataset(value, label));
        } else {
            this._append_data(new DataPoint(value, label));
        }
    }
    this.sort();
}

Dataset.prototype = new BaseData();
Dataset.prototype.constructor = Dataset;

Dataset.prototype.sort = function() {
    this.data.sort(
        function(a, b) {
            var a_total = a.get_total();
            var b_total = b.get_total();
            if (a_total < b_total) { return 1 };
            if (a_total > b_total) { return -1 };
            return 0;
        }
    )
};

Dataset.prototype._append_data = function(data) {
    this.data.push(data)
};

Dataset.prototype.append_data = function(data) {
    this._append_data(data);
    this.sort();
};

Dataset.prototype.get_total = function() {
    if (this.total == null) {
        total = 0;
        for (var i = 0; i < this.data.length; i++) {
            total = total + this.data[i].get_total();
        }
        this.total = total;
    }
    return this.total;
};

Dataset.prototype.treemap = function(area, origin, padding, threshold, flat) {
    origin      = origin || new Point(0,0);
    padding     = padding || 0;
    threshold   = threshold || 0;
    if (flat == null)
        flat = true;
    
    var total = this.get_total();
    var x = origin.x;
    var y = origin.y;
    var w = area.width;
    var h = area.height;
    
    var result = new TreeMap();
    
    for (var i = 0; i < this.data.length; i++) {
        var datum = this.data[i];
        var is_last = false;
        
        if (total < threshold) {
            var label_tokens = datum.label.split('.');
            label_tokens[-1] = "Others";
            label = label_tokens.join('.');
            datum = new DataPoint(total, label);
            is_last = true;
        }
        
        if (i == this.data.length - 1) {
            is_last = true;
        }
        
        var this_x = x;
        var this_y = y;
        var this_w = w;
        var this_h = h;
        
        var fixed_height = w > h;
        
        var proportion = datum.get_total() / total;
        total -= datum.get_total();
        
        if (fixed_height) {
            this_w  = Math.floor(w * proportion);
            w       = w - this_w;
            x       = x + this_w;
        } else {
            this_h  = Math.floor(h * proportion);
            h       = h - this_h;
            y       = y + this_h;
        }
        
        // add padding
        if (fixed_height && !is_last) {
            this_w -= padding;
        } else if (!fixed_height && !is_last) {
            this_h -= padding;
        }
        
        // sanity check: did we end up rendering a negative-sized frame?
        if (this_w < 0) {
            this_w = 0;
        }
        if (this_h < 0) {
            this_h = 0;
        }
        
        origin = new Point(this_x, this_y);
        area   = new Rect(this_w, this_h);
        
        if (datum instanceof DataPoint) {
            result.push(new Frame(datum.label, datum.value, origin, area));
        } else {
            var tmap = datum.treemap(area, origin, padding, threshold, flat);
            if (flat) {
                result.concat(tmap);
            } else {
                result.push(tmap);
            }
        }
    }
    
    return result;
}

Dataset.prototype.treemap_in_element = function(element_id, padding, threshold) {
    var element = document.getElementById(element_id);
    var w       = parseInt(window.getComputedStyle(element, null).getPropertyValue('width'));
    var h       = parseInt(window.getComputedStyle(element, null).getPropertyValue('height'));
    var area    = new Rect(w, h);
    var origin  = new Point(0, 0);
    
    if (padding == null) {
        padding = 0;
    }
    if (threshold == null) {
        threshold = 0;
    }
    
    var tm      = this.treemap(area, origin, padding, threshold, true);
    
    for (var i = 0; i < tm.frames.length; i++) {
      var frame = tm.frames[i];
      var div = document.createElement('div');
      div.style.position = "absolute";
      div.className     = "frame " + frame.label.replace('.', ' ');
      div.style.width   = frame.area.width;
      div.style.height  = frame.area.height;
      div.style.left    = frame.origin.x;
      div.style.top     = frame.origin.y;
      element.appendChild(div);
      
      var content = document.createElement('div');
      content.className = 'content';
      div.appendChild(content);

      var val = document.createElement('div');
      val.className = 'value';
      val.innerHTML = frame.value;
      content.appendChild(val);

      var lbl = document.createElement('div');
      lbl.className = 'label';
      lbl.innerHTML = frame.label;
      content.appendChild(lbl);
    }
}
