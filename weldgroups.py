"""Some common weld groups.


For pictorial representation see website below:

    https://structx.com/weld_groups.html
"""

from math import sin, cos, radians

from weldcalc import WeldGroup


class Single(WeldGroup):

    def __init__(self, name=None, height=5, size=0.25, weld_type="fillet"):
        super(Single, self).__init__(name=None, size=size, weld_type=weld_type)
        h = height
        self.add_weld_line((0, -h/2), (0, h/2))


class Parallel(WeldGroup):

    def __init__(self, name="Parallel", base=5, height=5, size=0.25,
                 weld_type="fillet"):
        super(Parallel, self).__init__(name=name, size=size,
                                       weld_type=weld_type)
        b, h = base, height
        self.add_weld_line((-b/2, -h/2), (-b/2, h/2))
        self.add_weld_line((b/2, -h/2), (b/2, h/2))


class Angle(WeldGroup):

    def __init__(self, name="Angle", base=5, height=5, size=0.25,
                 weld_type="fillet"):
        super(Angle, self).__init__(name=name, size=size, weld_type=weld_type)
        b, h = base, height
        self.add_weld_line((-b/2, -h/2), (-b/2, h/2))
        self.add_weld_line((-b/2, h/2), (b/2, h/2))


class Rectangle(WeldGroup):

    def __init__(self, name="Rectangle", base=5, height=5, size=0.25,
                 weld_type="fillet"):
        super(Rectangle, self).__init__(name=name, size=size,
                                        weld_type=weld_type)
        b, h = base, height
        self.add_weld_line((-b/2, -h/2), (-b/2, h/2))
        self.add_weld_line((b/2, -h/2), (b/2, h/2))
        self.add_weld_line((-b/2, h/2), (b/2, h/2))
        self.add_weld_line((-b/2, -h/2), (b/2, -h/2))


class Tee(WeldGroup):

    def __init__(self, name="Tee", B=3, H=5, S=0.25, t=0.25, size=0.25,
                 weld_type="fillet"):
        super(Tee, self).__init__(name=name, size=size, weld_type=weld_type)
        b, h = B, H
        tw, tf = S, t
        self.add_weld_line((-tw/2, -h/2), (-tw/2, h/2-tf))
        self.add_weld_line((tw/2, -h/2), (tw/2, h/2-tf))
        self.add_weld_line((-b/2, h/2), (b/2, h/2))


class Circle(WeldGroup):

    def __init__(self, name="Circle", radius=5, size=0.25, weld_type="fillet"):
        super(Circle, self).__init__(name=name, size=size, weld_type=weld_type)
        nol = 100           # approximating weld lines
        ang = 360 / nol     # individual sector angle
        R = radius

        from_point = R*cos(radians(0)), R*sin(radians(0))
        for a in Circle.frange(ang, 360, ang):
            to_point = R*cos(radians(a)), R*sin(radians(a))
            self.add_weld_line(from_point, to_point)
            from_point = to_point
        # last point
        to_point = R*cos(radians(360)), R*sin(radians(360))
        self.add_weld_line(from_point, to_point)

    @staticmethod
    def frange(start, stop, increment):
        # floating point range
        while start < stop:
            yield start
            start += increment


class PartialI(WeldGroup):
    def __init__(self, name="PartialI", B=3, H=5, S=0.25, t=0.25, size=0.25,
                 weld_type="fillet"):
        super(PartialI, self).__init__(name=name, size=size,
                                       weld_type=weld_type)
        b, h = B, H
        tw, tf = S, t

        self.add_weld_line((-tw/2, -h/2+tf), (-tw/2, h/2-tf))
        self.add_weld_line((tw/2, -h/2+tf), (tw/2, h/2-tf))

        self.add_weld_line((-b/2, h/2), (b/2, h/2))
        self.add_weld_line((-b/2, -h/2), (b/2, -h/2))


if __name__ == "__main__":
    rect = Rectangle()
    rect.plot()

    # circle = Circle()
    # circle.plot()

    # para = Parallel()
    # para.plot()

    # ang = Angle()
    # ang.plot()

    # tee = Tee()
    # tee.plot()

    # parti = PartialI()
    # parti.plot()

