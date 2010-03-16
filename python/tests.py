from fancypants import Area, Dataset, Point
import unittest

class TestDataset(unittest.TestCase):
    """Unit tests for the Dataset class"""

    def setUp(self):
        """docstring for setUp"""
        pass
    
    def tearDown(self):
        """docstring for tearDown"""
        pass
    
    def testTreeMap(self):
        data = [('a', 100), ('b', 150), ('c', 250)]
        area = Area(300,200)

        # will generate a treemap like this:
        # 
        # +------------+------------+
        # |   c        |  b         |
        # | (150x200)  | (150x120)  |
        # |            |            |
        # |            +------------+
        # |            |  a         |
        # |            | (150x80)   |
        # +------------+------------+
        
        ds = Dataset(data)
        tm = ds.treemap(area)
        
        expected = [
          # [x,   y,   w,   h,   val, lbl]
            [0,   0,   150, 200, 250, 'c'],
            [150, 0,   150, 120, 150, 'b'],
            [150, 120, 150, 80,  100, 'a']
        ]
        
        for i in range(0, len(expected)):
            self.assertEqual(tm[i].origin.x,    expected[i][0])
            self.assertEqual(tm[i].origin.y,    expected[i][1])
            self.assertEqual(tm[i].area.width,  expected[i][2])
            self.assertEqual(tm[i].area.height, expected[i][3])
            self.assertEqual(tm[i].value,       expected[i][4])
            self.assertEqual(tm[i].label,       expected[i][5])
                                
            # test properties
            self.assertEqual(tm[i].x,           expected[i][0])
            self.assertEqual(tm[i].y,           expected[i][1])
            self.assertEqual(tm[i].width,       expected[i][2])
            self.assertEqual(tm[i].height,      expected[i][3])

if __name__ == '__main__':
    unittest.main()