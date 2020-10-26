"""Weld viewer"""


from tkinter import *
from tkinter.ttk import *

from weldcalc import WeldGroup, MultiWeldGroup


class Application(Frame):

    def __init__(self, master, multi_weld_group):
        Frame.__init__(self, master)
        self.master = master
        self.multi_weld_group = multi_weld_group
        self.master.title("Weldomatic")
        self.init_ui()

    def init_ui(self):
        menubar = Menu(self.master)
        filemenu = Menu(menubar, tearoff=0)
        # filemenu.add_command(label="New", command=donothing)
        # filemenu.add_command(label="Open", command=donothing)
        # filemenu.add_command(label="Save", command=donothing)
        # filemenu.add_command(label="Save as...", command=donothing)
        # filemenu.add_command(label="Close", command=donothing)
        filemenu.add_separator()

        filemenu.add_command(label="Exit", command=self.master.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        self.master.config(menu=menubar)

        # create widgets
        self.weldtree = Treeview(self, show="tree")
        ybar = Scrollbar(self, orient=VERTICAL, command=self.weldtree.yview)
        # xbar = Scrollbar(self, orient=HORIZONTAL, command=self.weldtree.yview)
        self.weldtree.configure(yscroll=ybar.set)

        self.weldtree.heading("#0", text="Outline", anchor="w")
        self.update_ui()
        # insert multi weld groups, weld groups and weldines
        # weldtree.insert("", "end", "Multi Weld Group", open=True)

        # pack
        ybar.pack(side=RIGHT, fill=Y)
        # xbar.pack(side=BOTTOM, fill=X)
        self.weldtree.pack(side=TOP, fill=X)
        self.pack()

    def update_ui(self):
        for i, weld_group in enumerate(self.multi_weld_group.weld_groups, 1):
            wg = self.weldtree.insert("", i, weld_group.name,
                                      text="WeldGroup %s" % weld_group.name)
            for weld_line in weld_group.weld_lines:
                self.weldtree.insert(wg, "end", "", text="WeldLine")


if __name__ == "__main__":
    wg1 = WeldGroup()
    wg1.add_weld_line((-2.5, -5), (-2.5, 5), 0.25, "fillet")
    wg1.add_weld_line((2.5, -5), (2.5, 5), 0.25, "fillet")
    wg1.add_weld_line((-2.5, 5), (2.5, 5), 0.25, "fillet")
    wg1.add_weld_line((-2.5, -5), (2.5, -5), 0.25, "fillet")

    wg2 = WeldGroup()
    wg2.add_weld_line((-2.5, -5), (-2.5, 5), 0.5, "fillet")
    wg2.add_weld_line((2.5, -5), (2.5, 5), 0.5, "fillet")
    wg2.add_weld_line((-2.5, 5), (2.5, 5), 0.25, "fillet")
    wg2.add_weld_line((-2.5, -5), (2.5, -5), 1.25, "fillet")
    wg2.translate(0, 5, 5)
    wg2.rotateX(90)

    mwg = MultiWeldGroup()
    mwg.add_weld_group(wg1)
    mwg.add_weld_group(wg2)

    win = Tk()
    Application(win, mwg)
    mainloop()
