"""Simple weld calculator for planar and 3d welds.

Axes
----
x = horizontal
y = vertical
z = out of screen (x cross y)

References
----------
1. Inertia Tensor Transformation
https://hepweb.ucsd.edu/ph110b/110b_notes/node24.html

2. Parallel Axis Theorem
https://en.wikipedia.org/wiki/Parallel_axis_theorem
"""

import numpy as np
from numpy import linalg as la


class WeldLine:
    """Single line weld"""

    def __init__(self, from_point, to_point, size, weld_type="fillet"):
        self._from_point = np.array([*from_point, 1])
        self._to_point = np.array([*to_point, 1])
        self.size = size
        self.weld_type = weld_type
        self._transform = np.eye(4)

    @property
    def from_point(self):
        return (self._transform @ self._from_point)[:2]

    @property
    def to_point(self):
        return (self._transform @ self._to_point)[:2]

    def translate(self, tx=0, ty=0):
        """Translate weld line in the x-y plane"""
        tmat = np.array([[1, 0, 0, tx],
                         [0, 1, 0, ty],
                         [0, 0, 1, 0],
                         [0, 0, 0, 1]
                         ]
                        )
        self._transform = self._transform @ tmat

    def rotateZ(self, angle=0):
        """Rotate weld line about the out of plane z axis"""
        ang = np.radians(angle)
        rmat = np.array([[np.cos(ang), -np.sin(ang), 0, 0],
                         [np.sin(ang), np.cos(ang), 0, 0],
                         [0, 0, 1, 0],
                         [0, 0, 0, 1]
                         ]
                        )
        self._transform = self._transform @ rmat

    def rmat(self):
        """The rotation matrix of the transform matrix"""
        return self._transform[:3, :3]

    def tarray(self):
        """The translation component of the transform matrix"""
        return self._transform[:2, 3]

    def center(self):
        """Center of weld line"""
        return (self.from_point + self.to_point) / 2

    def length(self):
        """Length of weld line (not coordinate system dependent)"""
        return la.norm(self.to_point - self.from_point)

    def throat(self):
        """Throat size of weld line"""
        if self.weld_type == "fillet":
            return 1/np.sqrt(2) * self.size

    def area(self):
        """Area of weld line"""
        return self.throat() * self.length()

    def inertia(self):
        """Inertia matrix w.r.t the center of the weld line and about axis
        located at the origin.

        See references [1] and [2].
        """
        Ix = (1/12) * self.length()**3
        Iy = 0
        Iz = Ix + Iy

        imat = np.array([[Ix, 0, 0],
                         [0, Iy, 0],
                         [0, 0, Iz]
                         ]
                        )

        R = np.array([*self.center(), 0])
        I = self.rmat() @ imat @ np.transpose(self.rmat())  # about cg

        return (I + self.length()*(np.dot(R, R)*np.eye(3) -
                np.outer(R, R))) * self.throat()

    def ixx(self):
        """Inertia of weld line about the x axis with respect to coordinate
        system locate at the center.
        """
        return self.inertia()[0, 0]

    def iyy(self):
        """Inertia of weld line about the y axis"""
        return self.inertia()[1, 1]

    def izz(self):
        """Inertia of weld line about the z axis"""
        return self.inertia()[2, 2]


class WeldGroup:
    """A planar weld group consisting of serveral weld lines with similar or
    varying weld sizes.
    """

    def __init__(self):
        self.weld_lines = []

    def add_weld_line(self, from_point, to_point, size, weld_type):
        wl = WeldLine(from_point, to_point, size, weld_type)
        self.weld_lines.append(wl)

    def center(self):
        # average of components in each direction
        xsum, ysum = 0, 0
        for weld_line in self.weld_lines:
            cx, cy = weld_line.center()
            xsum += cx
            ysum += cy

        ncoords = 2 * len(self.weld_lines)

        return xsum/ncoords, ysum/ncoords

    def length(self):
        """Length of weld group"""
        group_length = 0
        for weld_line in self.weld_lines:
            group_length += weld_line.length()

        return group_length

    def area(self):
        """Area of weld group"""
        group_area = 0
        for weld_line in self.weld_lines:
            group_area += weld_line.area()

        return group_area

    def ixx(self):
        group_ixx = 0
        for weld_line in self.weld_lines:
            group_ixx += weld_line.ixx()

        return group_ixx

    def iyy(self):
        group_iyy = 0
        for weld_line in self.weld_lines:
            group_iyy += weld_line.iyy()

        return group_iyy

    def izz(self):
        group_izz = 0
        for weld_line in self.weld_lines:
            group_izz += weld_line.izz()

        return group_izz


if __name__ == "__main__":
    wg = WeldGroup()
    wg.add_weld_line((-5, -5, 0), (-5, 5, 0), 0.25, "fillet")
    wg.add_weld_line((5, -5, 0), (5, 5, 0), 0.25, "fillet")

    print(wg.center())
    print(wg.length())
    print(wg.area())
    print(wg.ixx())

    # wl = WeldLine((-5, -5, 0), (-5, 5, 0), 0.25, "fillet")
    # wl = WeldLine((0, -5, 0), (0, 5, 0), 0.25, "fillet")
    # print(wl.center())
    # print(wl.length())
    # print(wl.area())
    # print(wl.ixx())
