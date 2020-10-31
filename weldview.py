"""Weld viewer"""


from tkinter import *
from tkinter.ttk import Combobox

from weldcalc import WeldGroup, MultiWeldGroup


class Application(Frame):

    def __init__(self, master, multi_weld_group):
        Frame.__init__(self, master)
        self.master = master
        self.multi_weld_group = multi_weld_group
        self.master.title("Weldomatic")
        self._do_layout()

    def _do_layout(self):
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

        m1 = PanedWindow(orient=VERTICAL)
        m1.pack(fill=Y, expand=True, anchor="nw")
        top = Label(m1, text="Project Tree")
        bottom = Label(m1, text="Properties")
        m1.add(top)
        m1.add(bottom)

        m2 = PanedWindow()
        right = Label(m2, text="right pane")
        m2.add(right)
        m2.pack(fill=BOTH, expand=True)

        # create widgets
        # self.weldtree = Treeview(self, show="tree")
        # ybar = Scrollbar(self, orient=VERTICAL, command=self.weldtree.yview)
        # xbar = Scrollbar(self, orient=HORIZONTAL, command=self.weldtree.yview)
        # self.weldtree.configure(yscroll=ybar.set)

        # self.weldtree.heading("#0", text="Outline", anchor="w")
        # self.update_ui()
        # insert multi weld groups, weld groups and weldines
        # weldtree.insert("", "end", "Multi Weld Group", open=True)

        # pack
        # ybar.pack(side=RIGHT, fill=Y)
        # xbar.pack(side=BOTTOM, fill=X)
        # self.weldtree.pack(side=TOP, fill=X)
        self.pack()

    def update_ui(self):
        for i, weld_group in enumerate(self.multi_weld_group.weld_groups, 1):
            wg = self.weldtree.insert("", i, weld_group.name,
                                      text="WeldGroup %s" % weld_group.name)
            for weld_line in weld_group.weld_lines:
                self.weldtree.insert(wg, "end", "", text="WeldLine")


class OutlineWidget:
    pass


class WeldLineDetailsWidget(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master

        coord_frame = LabelFrame(self, text="Coordinates")
        # from point coordinate widgets
        from_point_frame = LabelFrame(coord_frame, text="Start")
        self.from_x_var = StringVar()
        self.from_y_var = StringVar()
        from_x_label = Label(from_point_frame, text="x")
        from_x_entry = Entry(from_point_frame, textvariable=self.from_x_var,
                             justify=RIGHT)
        from_y_label = Label(from_point_frame, text="y")
        from_y_entry = Entry(from_point_frame, textvariable=self.from_y_var,
                             justify=RIGHT)
        # layout
        from_x_label.grid(row=0, column=0)
        from_x_entry.grid(row=0, column=1)
        from_y_label.grid(row=1, column=0)
        from_y_entry.grid(row=1, column=1)
        from_point_frame.pack()


        # from point coordinate widgets
        to_point_frame = LabelFrame(coord_frame, text="Stop")
        self.to_x_var = StringVar()
        self.to_y_var = StringVar()
        to_x_label = Label(to_point_frame, text="x")
        to_x_entry = Entry(to_point_frame, textvariable=self.to_x_var,
                           justify=RIGHT)
        to_y_label = Label(to_point_frame, text="y")
        to_y_entry = Entry(to_point_frame, textvariable=self.to_y_var,
                           justify=RIGHT)
        # layout
        to_x_label.grid(row=0, column=0)
        to_x_entry.grid(row=0, column=1)
        to_y_label.grid(row=1, column=0)
        to_y_entry.grid(row=1, column=1)
        to_point_frame.pack()

        coord_frame.pack()

        # weld size widgets
        size_frame = LabelFrame(self, text="Size")
        self.size_var = StringVar()
        size_label = Label(size_frame, text="tw")
        size_entry = Entry(size_frame, textvariable=self.size_var,
                           justify=RIGHT)
        size_label.grid(row=0, column=0)
        size_entry.grid(row=0, column=1)
        size_frame.pack()


        # weld type widgets
        type_frame = LabelFrame(self, text="Type")
        self.type_var = StringVar()
        type_combobox = Combobox(type_frame, textvariable=self.type_var,
                                 justify=RIGHT)
        type_combobox["values"] = (" Fillet",)
        type_combobox.grid(row=0, column=0)
        type_combobox.current()
        type_frame.pack()

        self.pack(anchor="nw")


class WeldGroupDetailsWidget(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master

        header_label = Label(self, text="Weld Group Details")

        # weld size widgets
        general_frame = LabelFrame(self, text="General")

        name_label = Label(general_frame, text="Name")
        self.name_var = StringVar()
        name_entry = Entry(general_frame, textvariable=self.name_var,
                           justify=RIGHT)

        type_label = Label(general_frame, text="Type")
        self.type_var = StringVar()
        type_combobox = Combobox(general_frame, textvariable=self.type_var,
                                 justify=RIGHT)
        type_combobox["values"] = (" Fillet",
                                   " Groove",)
        type_combobox.current()

        self.size_var = StringVar()
        size_label = Label(general_frame, text="Size (tw)", anchor="e")
        size_entry = Entry(general_frame, textvariable=self.size_var,
                           justify=RIGHT)

        name_label.grid(row=0, column=0)
        name_entry.grid(row=0, column=1)
        type_label.grid(row=1, column=0)
        type_combobox.grid(row=1, column=1)
        size_label.grid(row=2, column=0)
        size_entry.grid(row=2, column=1)

        # transformation
        transform_frame = LabelFrame(self, text="Transformation")
        translate_frame = LabelFrame(transform_frame, text="Translation")
        rotate_frame = LabelFrame(transform_frame, text="Rotation")

        # from point coordinate widgets
        self.translate_x_var = StringVar()
        self.translate_y_var = StringVar()
        self.translate_z_var = StringVar()

        self.rotate_x_var = StringVar()
        self.rotate_y_var = StringVar()
        self.rotate_z_var = StringVar()

        translate_x_label = Label(translate_frame, text="Translate X ")
        translate_x_entry = Entry(translate_frame, textvariable=self.translate_x_var,
                                  justify=RIGHT)

        translate_y_label = Label(translate_frame, text="Translate Y ")
        translate_y_entry = Entry(translate_frame, textvariable=self.translate_y_var,
                                  justify=RIGHT)

        translate_z_label = Label(translate_frame, text="Translate Z ")
        translate_z_entry = Entry(translate_frame, textvariable=self.translate_z_var,
                                  justify=RIGHT)

        # layout
        translate_x_label.grid(row=0, column=0)
        translate_x_entry.grid(row=0, column=1)
        translate_y_label.grid(row=1, column=0)
        translate_y_entry.grid(row=1, column=1)
        translate_z_label.grid(row=2, column=0)
        translate_z_entry.grid(row=2, column=1)


        rotate_x_label = Label(rotate_frame, text="    Rotate X ")
        rotate_x_entry = Entry(rotate_frame, textvariable=self.rotate_x_var,
                               justify=RIGHT)
        rotate_y_label = Label(rotate_frame, text="    Rotate Y ")
        rotate_y_entry = Entry(rotate_frame, textvariable=self.rotate_y_var,
                               justify=RIGHT)
        rotate_z_label = Label(rotate_frame, text="    Rotate Z ")
        rotate_z_entry = Entry(rotate_frame, textvariable=self.rotate_z_var,
                               justify=RIGHT)

        apply_button = Button(transform_frame, text="Apply")
        reset_button = Button(transform_frame, text="Reset")

        # layout
        rotate_x_label.grid(row=0, column=0)
        rotate_x_entry.grid(row=0, column=1)
        rotate_y_label.grid(row=1, column=0)
        rotate_y_entry.grid(row=1, column=1)
        rotate_z_label.grid(row=2, column=0)
        rotate_z_entry.grid(row=2, column=1)


        # plot setting controls
        plot_frame = LabelFrame(self, text="Plot Ctrl")

        self.xlim_min_var = StringVar()
        xlim_min_label = Label(plot_frame, text="XLim Min")
        xlim_min_entry = Entry(plot_frame, textvariable=self.xlim_min_var,
                                  justify=RIGHT)
        self.xlim_max_var = StringVar()
        xlim_max_label = Label(plot_frame, text="XLim Max")
        xlim_max_entry = Entry(plot_frame, textvariable=self.xlim_max_var,
                                justify=RIGHT)


        self.ylim_min_var = StringVar()
        ylim_min_label = Label(plot_frame, text="YLim Min")
        ylim_min_entry = Entry(plot_frame, textvariable=self.ylim_min_var,
                                  justify=RIGHT)
        self.ylim_max_var = StringVar()
        ylim_max_label = Label(plot_frame, text="YLim Min")
        ylim_max_entry = Entry(plot_frame, textvariable=self.ylim_max_var,
                                  justify=RIGHT)


        self.color_var = StringVar()
        color_label = Label(plot_frame, text="Color")
        color_display_button = Button(plot_frame, text="                     ",
                                      background="red")


        style_label = Label(plot_frame, text="Style")
        self.style_var = StringVar()
        style_combobox = Combobox(plot_frame, textvariable=self.style_var,
                                 justify=RIGHT)
        style_combobox["values"] = (" Solid",
                                    " Dotted",
                                    " Dashed",
                                    " DashDot",)
        style_combobox.current()

        scale_factor_label = Label(plot_frame, text="Size Factor")
        scale_factor_scale = Scale(plot_frame, from_=1, to=5,
                                   orient=HORIZONTAL)



        # layout
        xlim_min_label.grid(row=0, column=0)
        xlim_min_entry.grid(row=0, column=1)
        xlim_max_label.grid(row=0, column=2)
        xlim_max_entry.grid(row=0, column=3)

        ylim_min_label.grid(row=1, column=0)
        ylim_min_entry.grid(row=1, column=1)
        ylim_max_label.grid(row=1, column=2)
        ylim_max_entry.grid(row=1, column=3)

        style_label.grid(row=2, column=0)
        style_combobox.grid(row=2, column=1)
        color_label.grid(row=3, column=0)
        color_display_button.grid(row=3, column=1)
        scale_factor_label.grid(row=4, column=0)
        scale_factor_scale.grid(row=4, column=1)


        header_label.pack(anchor="nw")
        general_frame.pack(anchor="nw", expand=True, fill=X)
        translate_frame.pack(anchor="nw", expand=True, fill=X)
        rotate_frame.pack(anchor="nw", expand=True, fill=X)
        reset_button.pack(side=RIGHT)
        apply_button.pack(side=RIGHT)
        transform_frame.pack(expand=True, fill=X)
        plot_frame.pack()

        self.pack()


class GraphWidget:
    pass


if __name__ == "__main__":
    wg1 = WeldGroup(size=0.25, weld_type="fillet")
    wg1.add_weld_line((-2.5, -5), (-2.5, 5))
    wg1.add_weld_line((2.5, -5), (2.5, 5))
    wg1.add_weld_line((-2.5, 5), (2.5, 5))
    wg1.add_weld_line((-2.5, -5), (2.5, -5))

    wg2 = WeldGroup(size=0.5, weld_type="fillet")
    wg2.add_weld_line((-2.5, -5), (-2.5, 5))
    wg2.add_weld_line((2.5, -5), (2.5, 5))
    wg2.add_weld_line((-2.5, 5), (2.5, 5))
    wg2.add_weld_line((-2.5, -5), (2.5, -5))
    wg2.translate(0, 5, 5)
    wg2.rotateX(90)

    mwg = MultiWeldGroup()
    mwg.add_weld_group(wg1)
    mwg.add_weld_group(wg2)

    win = Tk()
    win.geometry("350x200")
    details = WeldGroupDetailsWidget(win)
    mainloop()
