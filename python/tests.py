from fancypants import Rect, Dataset, Point
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
        area = Rect(300,200)

        # will generate a treemap like this:
        # 
        # (0,0)+------------+------------+
        #      |   c        |  b         |
        #      | (150x200)  | (150x120)  |
        #      |            |            |
        #      |            +------------+
        #      |            |  a         |
        #      |            | (150x80)   |
        #      +------------+------------+
        
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

    def testNestedTreeMap(self):
        data = [
            ('a', [('p', 10),  ('q', 40)]),
            ('b', [('r', 150), ('s', 50)])
        ]
        area = Rect(250,200)

        # will generate a treemap like this:
        # 
        # (0,0)+--------------+------------+
        #      |              |            |
        #      |   b.r        |  a.q       |
        #      | (200x150)    | (50x160)   |
        #      |              |            |
        #      +--------------+            |
        #      |              +------------+
        #      |   b.s        | a.p        |
        #      | (200x50)     | (50x40)    |
        #      +--------------+------------+

        ds = Dataset(data)
        tm = ds.treemap(area)
        
        expected = [
          # [x,   y,   w,   h,   val,  lbl]
            [0,   0,   200, 150, 150, 'b.r'],
            [0,   150, 200, 50,  50,  'b.s'],
            [200, 0,   50,  160, 40,  'a.q'],
            [200, 160, 50,  40,  10,  'a.p'],
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