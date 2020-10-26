"""Some common weld groups.

https://structx.com/weld_groups.html
"""

from math import sin, cos, pi, radians

from weldcalc import WeldGroup


class Single(WeldGroup):

    def __init__(self, name=None, height=5, size=0.25, weld_type="fillet"):
        super(Single, self).__init__(name)
        h = height
        self.add_weld_line((0, -h/2), (0, h/2), size, weld_type)


class Parallel(WeldGroup):

    def __init__(self, name=None, base=5, height=5, size=0.25,
                 weld_type="fillet"):
        super(Parallel, self).__init__(name)
        b, h = base, height
        self.add_weld_line((-b/2, -h/2), (-b/2, h/2), size, weld_type)
        self.add_weld_line((b/2, -h/2), (b/2, h/2), size, weld_type)


class Angle(WeldGroup):

    def __init__(self, name=None, base=5, height=5, size=0.25,
                 weld_type="fillet"):
        super(Angle, self).__init__(name)
        b, h = base, height
        self.add_weld_line((0, 0), (0, h), size, weld_type)
        self.add_weld_line((0, h), (b, h), size, weld_type)


class Rectangle(WeldGroup):

    def __init__(self, name=None, base=5, height=5, size=0.25,
                 weld_type="fillet"):
        super(Rectangle, self).__init__(name)
        b, h = base, height
        self.add_weld_line((-b/2, -h/2), (-b/2, h/2), size, weld_type)
        self.add_weld_line((b/2, -h/2), (b/2, h/2), size, weld_type)
        self.add_weld_line((-b/2, h/2), (b/2, h/2), size, weld_type)
        self.add_weld_line((-b/2, -h/2), (b/2, -h/2), size, weld_type)


class Tee(WeldGroup):

    def __init__(self, name=None, B=3, H=5, S=0.25, t=0.25, size=0.25,
                 weld_type="fillet"):
        super(Tee, self).__init__(name)
        b, h = B, H
        tw, tf = S, t
        self.add_weld_line((-tw/2, 0), (-tw/2, h-tf), size, weld_type)
        self.add_weld_line((tw/2, 0), (tw/2, h-tf), size, weld_type)
        self.add_weld_line((-b/2, h), (b/2, h), size, weld_type)


class Circle(WeldGroup):

    def __init__(self, name=None, radius=5, size=0.25, weld_type="fillet"):
        super(Circle, self).__init__(name)
        nol = 100           # approximating weld lines
        ang = 360 / nol     # individual sector angle
        R = radius

        from_point = R*cos(radians(0)), R*sin(radians(0))
        for a in Circle.frange(ang, 360, ang):
            to_point = R*cos(radians(a)), R*sin(radians(a))
            self.add_weld_line(from_point, to_point, size, weld_type)
            from_point = to_point
        # last point
        to_point = R*cos(radians(360)), R*sin(radians(360))
        self.add_weld_line(from_point, to_point, size, weld_type)

    @staticmethod
    def frange(start, stop, increment):
        # floating point range
        while start < stop:
            yield start
            start += increment


if __name__ == "__main__":
    # rect = Rectangle()
    # rect.plot()

    # circle = Circle()
    # circle.plot()

    # para = Parallel()
    # para.plot()

    # ang = Angle()
    # ang.plot()

    tee = Tee()
    tee.plot()
