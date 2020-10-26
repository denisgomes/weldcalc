"""Weld property calculator for planar and 3d welds.

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

import tkinter
from itertools import groupby

import numpy as np
from numpy import linalg as la

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

from mpl_toolkits.mplot3d import Axes3D

import matplotlib.pyplot as plt


class WeldLine:
    """A single weld line.

    A weld line is created with respect to the local weld axis located at the
    origin (0, 0). Initially, the local weld line and 'global' weld group
    coordinate systems are at the same location. When a rotation is specified
    for the weld group, the weld line local and global coordinates are no
    longer aligned. Rotation of a weld line takes place with respect to the
    weld group coordinate system.

    Parameters
    ----------
    from_point : tuple
        From point (x1, y1) in object coordinates.

    to_point : tuple
        To point (x1, y1) in object coordinates.

    size : float
        Weld size.

    weld_type : str
        Type of weld. 'Fillet' for example.

    weld_group : WeldGroup
        Instance of a weld group.
    """

    def __init__(self, from_point, to_point, size, weld_type="fillet",
                 weld_group=None):
        self._from_point = np.array([*from_point, 0, 1])
        self._to_point = np.array([*to_point, 0, 1])
        self.size = size
        self.weld_type = weld_type
        self.weld_group = weld_group

    def transform(self):
        """The weld line object coordinate system, positioned at the center
        of the weld line.

        Y is up.
        X is to the right.
        Z is out of the screen.
        """
        from_point = self._from_point[:3]
        to_point = self._to_point[:3]
        _yaxis = to_point - from_point

        yaxis = _yaxis / np.linalg.norm(_yaxis)     # unit vector
        zaxis = np.array([0, 0, 1])
        xaxis = np.cross(yaxis, zaxis)
        center = (from_point + to_point) / 2

        tf = np.eye(4)
        tf[:3, 0] = xaxis
        tf[:3, 1] = yaxis
        tf[:3, 2] = zaxis
        tf[:3, 3] = center

        return tf

    @property
    def from_point(self):
        """The from point with respect to the weld group coordinate system"""
        return (self.weld_group.transform @ self._from_point)[:3]

    @property
    def to_point(self):
        """The to point with respect to the weld group coordinate system"""
        return (self.weld_group.transform @ self._to_point)[:3]

    def center(self):
        """Center of weld line with respect to the weld group coordinate
        system.
        """
        return (self.from_point + self.to_point) / 2

    def length(self):
        """Length of weld line"""
        return la.norm(self.to_point - self.from_point)

    def throat(self):
        """Throat size of weld line"""
        if self.weld_type == "fillet":
            return 1/np.sqrt(2) * self.size

    def area(self):
        """Area of weld line"""
        return self.throat() * self.length()

    def inertia(self):
        """Inertia matrix w.r.t weld line global coordinate system axes located
        at the center of the weld line (therefore no parallel axis theorem).
        """
        Ix = (1/12) * self.throat() * self.length()**3
        Iy = (1/12) * self.throat()**3 * self.length()
        Iz = Ix + Iy

        imat = np.array([[Ix, 0, 0],
                         [0, Iy, 0],
                         [0, 0, Iz]
                         ]
                        )

        rmat = self.rmat()

        I = rmat @ imat @ np.transpose(rmat)

        return I

    def rmat(self):
        return self.transform()[:3, :3]

    def ixx(self):
        """Inertia of weld line about the local x axis."""
        return self.inertia()[0, 0]

    def iyy(self):
        """Inertia of weld line about the local y axis"""
        return self.inertia()[1, 1]

    def izz(self):
        """Inertia of weld line about the local z axis"""
        return self.inertia()[2, 2]


class WeldGroup:
    """A planar weld group consisting of several weld lines with similar or
    different weld sizes.

    Parameters
    ----------
    name : str
        Name of weld group. A number of automatically assigned if not
        specified.
    """

    count = 0

    def __init__(self, name=None):
        self.name = name
        if self.name is None:
            self.name = str(WeldGroup.count)
            WeldGroup.count += 1

        self.weld_lines = []
        self._transform = np.eye(4)

    @property
    def transform(self):
        """Weld group transformation matrix"""
        return self._transform

    def add_weld_line(self, from_point, to_point, size, weld_type="fillet"):
        """Append a weld line to a group"""
        wl = WeldLine(from_point, to_point, size, weld_type, self)
        self.weld_lines.append(wl)

    def length(self):
        """Length of weld group"""
        group_length = 0
        for weld_line in self.weld_lines:
            group_length += weld_line.length()

        return group_length

    def cg(self):
        """Center of gravity of weld group. CG is based on the length of each
        weld line, similar to how the center of gravity of an area is based on
        the area.
        """
        cx, cy, cz = 0, 0, 0
        wt = 0
        for weld_line in self.weld_lines:
            cx += (weld_line.center()[0] * weld_line.length())
            cy += (weld_line.center()[1] * weld_line.length())
            cz += (weld_line.center()[2] * weld_line.length())
            wt += weld_line.length()

        return cx/wt, cy/wt, cz/wt

    def area(self):
        """Area of weld group"""
        group_area = 0
        for weld_line in self.weld_lines:
            group_area += weld_line.area()

        return group_area

    def translate(self, tx, ty, tz=0):
        """Translate weld group"""
        tmat = np.array([[1, 0, 0, tx],
                         [0, 1, 0, ty],
                         [0, 0, 1, tz],
                         [0, 0, 0, 1]
                         ]
                        )
        self._transform = self._transform @ tmat

    def rotateZ(self, angle):
        """Rotate weld group about the z axis"""
        ang = np.radians(angle)
        rmat = np.array([[np.cos(ang), -np.sin(ang), 0, 0],
                         [np.sin(ang), np.cos(ang), 0, 0],
                         [0, 0, 1, 0],
                         [0, 0, 0, 1]
                         ]
                        )
        self._transform = self._transform @ rmat

    def rotateX(self, angle=0):
        """Rotate weld group about the x axis"""
        ang = np.radians(angle)
        rmat = np.array([[1, 0, 0, 0],
                         [0, np.cos(ang), -np.sin(ang), 0],
                         [0, np.sin(ang), np.cos(ang), 0],
                         [0, 0, 0, 1]
                         ]
                        )
        self._transform = self._transform @ rmat

    def rotateY(self, angle=0):
        """Rotate weld group about the y axis"""
        ang = np.radians(angle)
        rmat = np.array([[np.cos(ang), 0, np.sin(ang), 0],
                         [0, 1, 0, 0],
                         [-np.sin(ang), 0, np.cos(ang), 0],
                         [0, 0, 0, 1]
                         ]
                        )
        self._transform = self._transform @ rmat

    def rmat(self):
        """The rotation component of the transform matrix"""
        return self._transform[:3, :3]

    def inertia(self):
        """Inertia matrix w.r.t the center of the weld line and about axis
        located at the origin.

        See references [1] and [2].
        """
        Ix, Iy, Iz = 0, 0, 0
        for weld_line in self.weld_lines:
            # distance to weld group cg
            R = np.array([*weld_line.center()]) - self.cg()
            rmat = self.rmat()

            # about the center
            I = rmat * weld_line.inertia() * np.transpose(rmat)

            # about parallel axis
            J = (I + weld_line.throat()*weld_line.length() *
                 (np.dot(R, R)*np.eye(3) - np.outer(R, R)))

            Ix += J[0, 0]
            Iy += J[1, 1]
            Iz += J[2, 2]

        imat = np.array([[Ix, 0, 0],
                         [0, Iy, 0],
                         [0, 0, Iz]
                         ]
                        )

        return imat

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

    def plot(self):
        root = tkinter.Tk()
        root.wm_title("Weld Group Properties")

        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.set_xlim(-10, 10)
        ax.set_ylim(-10, 10)
        ax.set_aspect("equal")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")

        # grid
        ax.grid()
        ax.minorticks_on()
        ax.grid(which='major', linestyle='-', linewidth='0.5', color='red')
        ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black')

        # orgin and cg points
        ax.scatter(*zip((0, 0), self.cg()[:2]))

        # texts
        ax.text(*self.cg()[:2], "CG")

        # coordinate arrows
        ax.arrow(0, 0, 1, 0, width=0.05)
        ax.arrow(0, 0, 0, 1, width=0.05)
        ax.text(1.25, 0, "X")
        ax.text(0, 1.25, "Y")

        # plot weld lines
        legend_labels = []
        legend_handles = []
        color_map = plt.get_cmap("gist_rainbow")
        kfunc = lambda wl: (wl.size, wl.weld_type)
        # need to sort to avoid unexpected results
        sorted_list = sorted(self.weld_lines, key=kfunc)
        for ((size, weld_type), weld_lines) in groupby(sorted_list, key=kfunc):
            color = color_map(np.random.rand())
            for i, weld_line in enumerate(weld_lines):
                xs, ys = zip(weld_line.from_point[:2], weld_line.to_point[:2])
                lines = ax.plot(xs, ys)

                lines[0].set_color(color)
                lines[0].set_linewidth(1+size)

            legend_handles.append(lines[0])
            legend_labels.append(r"$t_w=%s$, %s" % (size, weld_type))

        ax.legend(handles=legend_handles, labels=legend_labels, loc="best")

        # output property box
        textstr = '\n'.join((
            r'$L_w=%.3f$' % (self.length(), ),
            r'$A_w=%.3f$' % (self.area(), ),
            r'$I_{xcg}=%.3f$' % (self.ixx(), ),
            r'$I_{ycg}=%.3f$' % (self.iyy(), ),
            r'$I_{zcg}=%.3f$' % (self.izz(), ),
            r'$CG=(%.3f,%.3f,%.3f)$' % (*self.cg(), ),
            ))

        # these are matplotlib.patch.Patch properties
        props = dict(boxstyle='square', facecolor='wheat', alpha=0.5)

        # place a text box in upper left in axes coords
        ax.text(0.015, 0.985, textstr, transform=ax.transAxes, fontsize=10,
                verticalalignment='top', bbox=props)

        canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH,
                                    expand=1)

        toolbar = NavigationToolbar2Tk(canvas, root)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH,
                                    expand=1)

        def on_key_press(event):
            print("you pressed {}".format(event.key))
            key_press_handler(event, canvas, toolbar)

        canvas.mpl_connect("key_press_event", on_key_press)

        tkinter.mainloop()


class MultiWeldGroup:
    """A collection of weld groups in 3 dimensional space. Multiple planar weld
    groups are transformed to create a combined weld in 3d.

    Example
    -------
    Create a multi weld group consisting of two planar welds and plot.

    .. code-block:: python

        >>> wg1 = WeldGroup()
        >>> wg1.add_weld_line((-2.5, -5), (-2.5, 5), 0.25, "fillet")
        >>> wg1.add_weld_line((2.5, -5), (2.5, 5), 0.25, "fillet")
        >>> wg1.add_weld_line((-2.5, 5), (2.5, 5), 0.25, "fillet")
        >>> wg1.add_weld_line((-2.5, -5), (2.5, -5), 0.25, "fillet")

        >>> wg2 = WeldGroup()
        >>> wg2.add_weld_line((-2.5, -5), (-2.5, 5), 0.5, "fillet")
        >>> wg2.add_weld_line((2.5, -5), (2.5, 5), 0.5, "fillet")
        >>> wg2.add_weld_line((-2.5, 5), (2.5, 5), 0.25, "fillet")
        >>> wg2.add_weld_line((-2.5, -5), (2.5, -5), 1.25, "fillet")
        >>> wg2.translate(0, 5, 5)
        >>> wg2.rotateX(90)

        >>> mwg = MultiWeldGroup()
        >>> mwg.add_weld_group(wg1)
        >>> mwg.add_weld_group(wg2)
        >>> mwg.plot()
    """

    def __init__(self):
        self.weld_groups = []

    def add_weld_group(self, weld_group):
        self.weld_groups.append(weld_group)

    def length(self):
        group_length = 0
        for weld_group in self.weld_groups:
            group_length += weld_group.length()

        return group_length

    def area(self):
        group_area = 0
        for weld_group in self.weld_groups:
            group_area += weld_group.area()

        return group_area

    def cg(self):
        """CG of gravity of a multi weld group. CG is based on the total line
        length of each weld group, similar to the center of gravity of an area.
        """
        cx, cy, cz = 0, 0, 0
        wt = 0
        for weld_group in self.weld_groups:
            cx += (weld_group.cg()[0] * weld_group.length())
            cy += (weld_group.cg()[1] * weld_group.length())
            cz += (weld_group.cg()[2] * weld_group.length())
            wt += weld_group.length()

        return cx/wt, cy/wt, cz/wt

    def inertia(self):
        """Inertia matrix w.r.t the center of the weld line and about axis
        located at the global origin.

        See references [1] and [2].
        """
        Ix, Iy, Iz = 0, 0, 0
        for weld_group in self.weld_groups:
            # distance to multi weld group cg
            R = np.array([*weld_group.cg()]) - self.cg()

            rmat = np.eye(3)    # global coordinate

            # about the weld group cg
            I = rmat * weld_group.inertia() * np.transpose(rmat)

            # about parallel axis
            J = (I + weld_group.length() * (np.dot(R, R)*np.eye(3) -
                 np.outer(R, R)))

            Ix += J[0, 0]
            Iy += J[1, 1]
            Iz += J[2, 2]

        imat = np.array([[Ix, 0, 0],
                         [0, Iy, 0],
                         [0, 0, Iz]
                         ]
                        )

        return imat

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

    def plot(self):
        root = tkinter.Tk()
        root.wm_title("Multi-Weld Group Properties")

        # plot here
        fig = Figure(figsize=(5, 4), dpi=100)

        canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
        canvas.draw()

        ax = fig.add_subplot(111, projection="3d")
        ax.set_xlim(-10, 10)
        ax.set_ylim(-10, 10)
        ax.set_zlim(-10, 10)
        ax.set_aspect("equal")
        ax.set_proj_type("ortho")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")

        # grid
        ax.grid()
        ax.minorticks_on()
        ax.grid(which='major', linestyle='-', linewidth='0.5', color='red')
        ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black')

        # orgin and cg points
        ax.scatter(*zip((0, 0, 0), self.cg()))

        # texts
        ax.text(*self.cg(), "CG")

        # coordinate arrows
        ax.quiver(0, 0, 0, 1, 0, 0, length=1.0)
        ax.quiver(0, 0, 0, 0, 1, 0, length=1.0)
        ax.quiver(0, 0, 0, 0, 0, 1, length=1.0)
        ax.text(1.25, 0, 0, "X")
        ax.text(0, 1.25, 0, "Y")
        ax.text(0, 0, 1.25, "Z")

        # plot weld groups
        legend_labels = []
        legend_handles = []
        color_map = plt.get_cmap("gist_rainbow")
        for weld_group in self.weld_groups:
            color = color_map(np.random.rand())
            for weld_line in weld_group.weld_lines:
                xs, ys, zs = zip(weld_line.from_point, weld_line.to_point)
                lines = ax.plot(xs, ys, zs)

                lines[0].set_color(color)
                lines[0].set_linewidth(1+weld_line.size)

            legend_handles.append(lines[0])
            legend_labels.append(r"WeldGroup [%s]" % weld_group.name)

        ax.legend(handles=legend_handles, labels=legend_labels, loc="best")

        # output property box
        textstr = '\n'.join((
            r'$L_w=%.3f$' % (self.length(), ),
            r'$A_w=%.3f$' % (self.area(), ),
            r'$I_{xcg}=%.3f$' % (self.ixx(), ),
            r'$I_{ycg}=%.3f$' % (self.iyy(), ),
            r'$I_{zcg}=%.3f$' % (self.izz(), ),
            r'$CG=(%.3f,%.3f,%.3f)$' % (*self.cg(), ),
            ))

        # these are matplotlib.patch.Patch properties
        props = dict(boxstyle='square', facecolor='wheat', alpha=0.5)

        # place a text box in upper left in axes coords
        ax.text2D(0.015, 0.985, textstr, transform=ax.transAxes, fontsize=10,
                  verticalalignment='top', bbox=props)

        toolbar = NavigationToolbar2Tk(canvas, root)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH,
                                    expand=1)

        def on_key_press(event):
            print("you pressed {}".format(event.key))
            key_press_handler(event, canvas, toolbar)

        canvas.mpl_connect("key_press_event", on_key_press)

        tkinter.mainloop()


if __name__ == "__main__":
    wg1 = WeldGroup()
    wg1.add_weld_line((-2.5, -5), (-2.5, 5), 0.25, "fillet")
    wg1.add_weld_line((2.5, -5), (2.5, 5), 0.25, "fillet")
    wg1.add_weld_line((-2.5, 5), (2.5, 5), 0.25, "fillet")
    wg1.add_weld_line((-2.5, -5), (2.5, -5), 0.25, "fillet")

    # wg2 = WeldGroup()
    # wg2.add_weld_line((-2.5, -5), (-2.5, 5), 0.5, "fillet")
    # wg2.add_weld_line((2.5, -5), (2.5, 5), 0.5, "fillet")
    # wg2.add_weld_line((-2.5, 5), (2.5, 5), 0.25, "fillet")
    # wg2.add_weld_line((-2.5, -5), (2.5, -5), 1.25, "fillet")
    # wg2.translate(0, 5, 5)
    # wg2.rotateX(90)

    mwg = MultiWeldGroup()
    mwg.add_weld_group(wg1)
    # mwg.add_weld_group(wg2)
    mwg.plot()
