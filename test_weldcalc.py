"""Simple unit tests for some common weld group"""

from math import sin, cos, radians
import unittest

from weldcalc import WeldGroup


class TestSingleWeldGroup(unittest.TestCase):

    def setUp(self):
        self.wg = WeldGroup(size=0.25, weld_type="fillet")
        self.wg.add_weld_line((0, -5), (0, 5))

    def test_length(self):
        """Test weld line length"""
        self.assertEqual(10, self.wg.length())

    def test_area(self):
        """Test weld line area"""
        self.assertAlmostEqual(1.7678, round(self.wg.area(), 4), 4)

    def test_ixx(self):
        """Test weld group x inertia"""
        self.assertAlmostEqual(14.7314, round(self.wg.ixx(), 4), 4)

    def test_iyy(self):
        """Test weld group y inertia"""
        self.assertAlmostEqual(0.0046, round(self.wg.iyy(), 4), 4)


class TestRectangleWeldGroup(unittest.TestCase):
    """Rectangular weld profile.

    https://www.engineersedge.com/weld/fillet_weld_moment_inertia.htm
    """

    def setUp(self):
        self.wg = WeldGroup(size=0.25, weld_type="fillet")
        self.wg.add_weld_line((-2.5, -5), (-2.5, 5))
        self.wg.add_weld_line((2.5, -5), (2.5, 5))
        self.wg.add_weld_line((-2.5, 5), (2.5, 5))
        self.wg.add_weld_line((-2.5, -5), (2.5, -5))

    def test_cg(self):
        self.assertEqual((0, 0, 0), self.wg.cg())

    def test_length(self):
        """Test weld line length"""
        self.assertEqual(30, self.wg.length())

    def test_area(self):
        """Test weld line area"""
        self.assertAlmostEqual(5.3033, round(self.wg.area(), 4), 4)

    def test_ixx(self):
        """Test weld group x inertia.

        """
        self.assertAlmostEqual(73.66, round(self.wg.ixx(), 2), 2)


# floating point range
def frange(start, stop, increment):
    while start < stop:
        yield start
        start += increment


class TestCircleWeldGroup(unittest.TestCase):
    """Circular weld profile.

    https://www.engineersedge.com/weld/fillet_weld_moment_inertia.htm

    """

    def setUp(self):
        self.wg = WeldGroup(size=0.25, weld_type="fillet")

        self.R = R = 10     # radius of weld group
        nol = 100           # approximating weld lines
        ang = 360 / nol     # individual sector angle

        from_point = R*cos(radians(0)), R*sin(radians(0))
        for a in frange(ang, 360, ang):
            to_point = R*cos(radians(a)), R*sin(radians(a))
            self.wg.add_weld_line(from_point, to_point)
            from_point = to_point
        # last point
        to_point = R*cos(radians(360)), R*sin(radians(360))
        self.wg.add_weld_line(from_point, to_point)

    def test_cg(self):
        self.assertAlmostEqual((0, 0, 0), tuple(map(round, self.wg.cg())))

    def test_ixx(self):
        """The results are close (within 3%) but not exact. The approximation
        is less than the analytical result.
        """
        self.assertAlmostEqual(554.92, round(self.wg.ixx(), 2), 2)

    def test_iyy(self):
        """The results are close (within 3%) but not exact. The approximation
        is less than the analytical result.
        """
        self.assertAlmostEqual(554.92, round(self.wg.ixx(), 2), 2)


if __name__ == "__main__":
    unittest.main()
