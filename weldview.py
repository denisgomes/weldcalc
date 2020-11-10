"""User interface widgets"""

from base64 import b16encode
from tkinter import *
from tkinter import colorchooser
from tkinter.ttk import Combobox
import threading
import time

from weldcalc import WeldGroup, MultiWeldGroup
from utils import rgb_2_hex_color, hex_2_rgb_color

WELD_TYPES = ("fillet", "groove")
STYLES = ("solid", "dotted", "dashed", "dashdot")


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
        type_combobox["values"] = ("fillet",
                                   "groove",
                                   )
        type_combobox.grid(row=0, column=0)
        type_combobox.current()
        type_frame.pack()

        self.pack(anchor="nw")


class WeldGroupDetailsWidget(Frame):

    def __init__(self, master, weld_group):
        Frame.__init__(self, master)
        self.master = master
        self._do_layout()
        self.update(weld_group)     # sets weldgroup

    def _do_layout(self):
        main_frame = LabelFrame(self, text="Weld Group Details",
                                padx=3, pady=3)

        # weld size widgets
        general_frame = LabelFrame(main_frame, text="General", padx=3, pady=3)
        general_frame.columnconfigure(1, weight=1)

        name_label = Label(general_frame, text="Name")
        self.name_var = StringVar()
        name_entry = Entry(general_frame, textvariable=self.name_var,
                           justify=CENTER)

        type_label = Label(general_frame, text="Type")
        self.weld_type_var = StringVar()
        type_combobox = Combobox(general_frame,
                                 textvariable=self.weld_type_var,
                                 justify=CENTER,
                                 state="readonly")
        type_combobox["values"] = WELD_TYPES
        type_combobox.current()

        self.weld_size_var = StringVar()
        size_label = Label(general_frame, text="Size (tw)", anchor="e")
        self.size_entry = Entry(general_frame, textvariable=self.weld_size_var,
                                justify=CENTER)

        name_label.grid(row=0, column=0, sticky=E)
        name_entry.grid(row=0, column=1, sticky=E+W)
        type_label.grid(row=1, column=0, sticky=E)
        type_combobox.grid(row=1, column=1, sticky=E+W)
        size_label.grid(row=2, column=0, sticky=E)
        self.size_entry.grid(row=2, column=1, sticky=E+W)

        # transformation
        transform_frame = LabelFrame(main_frame, text="Transform", padx=3,
                                     pady=3)
        translate_frame = LabelFrame(transform_frame, text="Translation",
                                     padx=3, pady=3)
        translate_frame.columnconfigure(1, weight=1)
        rotate_frame = LabelFrame(transform_frame, text="Rotation (deg)",
                                  padx=3, pady=3)
        rotate_frame.columnconfigure(1, weight=1)

        # from point coordinate widgets
        self.translate_x_var = StringVar()
        self.translate_y_var = StringVar()
        self.translate_z_var = StringVar()

        self.rotate_x_var = StringVar()
        self.rotate_y_var = StringVar()
        self.rotate_z_var = StringVar()

        translate_x_label = Label(translate_frame, text="Translate X ")
        translate_x_entry = Entry(translate_frame,
                                  textvariable=self.translate_x_var,
                                  justify=CENTER)

        translate_y_label = Label(translate_frame, text="Translate Y ")
        translate_y_entry = Entry(translate_frame,
                                  textvariable=self.translate_y_var,
                                  justify=CENTER)

        translate_z_label = Label(translate_frame, text="Translate Z ")
        translate_z_entry = Entry(translate_frame,
                                  textvariable=self.translate_z_var,
                                  justify=CENTER)

        # layout
        translate_x_label.grid(row=0, column=0)
        translate_x_entry.grid(row=0, column=1, sticky=E+W)
        translate_y_label.grid(row=1, column=0)
        translate_y_entry.grid(row=1, column=1, sticky=E+W)
        translate_z_label.grid(row=2, column=0)
        translate_z_entry.grid(row=2, column=1, sticky=E+W)

        rotate_x_label = Label(rotate_frame, text="    Rotate X ")
        rotate_x_entry = Entry(rotate_frame, textvariable=self.rotate_x_var,
                               justify=CENTER)
        rotate_y_label = Label(rotate_frame, text="    Rotate Y ")
        rotate_y_entry = Entry(rotate_frame, textvariable=self.rotate_y_var,
                               justify=CENTER)
        rotate_z_label = Label(rotate_frame, text="    Rotate Z ")
        rotate_z_entry = Entry(rotate_frame, textvariable=self.rotate_z_var,
                               justify=CENTER)

        # apply_button = Button(transform_frame, text="Apply")
        transform_reset_button = Button(transform_frame, text="Reset",
                                        command=self.on_transform_reset_button)

        # layout
        rotate_x_label.grid(row=0, column=0, sticky=E)
        rotate_x_entry.grid(row=0, column=1, sticky=E+W)
        rotate_y_label.grid(row=1, column=0, sticky=E)
        rotate_y_entry.grid(row=1, column=1, sticky=E+W)
        rotate_z_label.grid(row=2, column=0, sticky=E)
        rotate_z_entry.grid(row=2, column=1, sticky=E+W)

        # plot setting controls
        plot_frame = LabelFrame(main_frame, text="Plot Ctrl", padx=3, pady=3)
        plot_frame.columnconfigure(1, weight=1)
        plot_frame.columnconfigure(3, weight=1)

        self.xlim_min_var = StringVar()
        xlim_min_label = Label(plot_frame, text="XLim Min")
        xlim_min_entry = Entry(plot_frame, textvariable=self.xlim_min_var,
                               justify=CENTER)
        self.xlim_max_var = StringVar()
        xlim_max_label = Label(plot_frame, text="XLim Max")
        xlim_max_entry = Entry(plot_frame, textvariable=self.xlim_max_var,
                               justify=CENTER)

        self.ylim_min_var = StringVar()
        ylim_min_label = Label(plot_frame, text="YLim Min")
        ylim_min_entry = Entry(plot_frame, textvariable=self.ylim_min_var,
                                  justify=CENTER)
        self.ylim_max_var = StringVar()
        ylim_max_label = Label(plot_frame, text="YLim Min")
        ylim_max_entry = Entry(plot_frame, textvariable=self.ylim_max_var,
                                  justify=CENTER)

        self.color_var = StringVar()
        color_label = Label(plot_frame, text="Color")
        self.color_display_button = Button(plot_frame, text=" ",
                                           background="black",
                                           command=self.on_color_display_button)

        style_label = Label(plot_frame, text="Style")
        self.style_var = StringVar()
        style_combobox = Combobox(plot_frame, textvariable=self.style_var,
                                  justify=CENTER, state="readonly")
        style_combobox["values"] = STYLES
        style_combobox.current()

        scale_factor_label = Label(plot_frame, text="Size\nFactor")
        self.scale_factor_scale = Scale(plot_frame, from_=1, to=5,
                                        orient=HORIZONTAL)

        plot_reset_button = Button(plot_frame, text="Reset",
                                   command=self.on_plot_reset_button)

        # layout
        xlim_min_label.grid(row=0, column=0, sticky=E)
        xlim_min_entry.grid(row=0, column=1, sticky=E+W)
        xlim_max_label.grid(row=0, column=2, sticky=E)
        xlim_max_entry.grid(row=0, column=3, sticky=E+W)

        ylim_min_label.grid(row=1, column=0, sticky=E)
        ylim_min_entry.grid(row=1, column=1, sticky=E+W)
        ylim_max_label.grid(row=1, column=2, sticky=E)
        ylim_max_entry.grid(row=1, column=3, sticky=E+W)

        style_label.grid(row=2, column=0, sticky=E)
        style_combobox.grid(row=2, column=1, sticky=E+W)
        color_label.grid(row=3, column=0, sticky=E)
        self.color_display_button.grid(row=3, column=1, sticky=E+W)
        scale_factor_label.grid(row=4, column=0, sticky=E)
        self.scale_factor_scale.grid(row=4, column=1, sticky=E+W)

        plot_reset_button.grid(row=5, column=0, sticky=W)

        weldgroup_apply_button = Button(main_frame, text="Apply",
            command=lambda: self.on_weld_group_apply_button(self.weld_group))


        main_frame.pack(anchor="nw")
        general_frame.pack(anchor="nw", expand=True, fill=X)
        translate_frame.pack(anchor="nw", expand=True, fill=X)
        rotate_frame.pack(anchor="nw", expand=True, fill=X)
        transform_reset_button.pack(side=LEFT)
        # apply_button.pack(side=RIGHT)
        transform_frame.pack(expand=True, fill=X)
        plot_frame.pack()
        weldgroup_apply_button.pack(fill=X, side=RIGHT)

        self.pack()

    def on_color_display_button(self):
        current_color = self.get_color_display_button_color()
        rgb, _ = colorchooser.askcolor(initialcolor=current_color)
        self.set_color_display_button_color(tuple(map(int, rgb)))

    def set_color_display_button_color(self, value):
        self.color_display_button.configure(background=rgb_2_hex_color(value))

    def get_color_display_button_color(self):
        return self.color_display_button.cget("background")

    def on_transform_reset_button(self):
        wg = self.weld_group

        tx, ty, tz = wg.translation
        self.translate_x_var.set(tx)
        self.translate_y_var.set(ty)
        self.translate_z_var.set(tz)

        rotx, roty, rotz = wg.rotation
        self.rotate_x_var.set(rotx)
        self.rotate_y_var.set(roty)
        self.rotate_z_var.set(rotz)

    def on_plot_reset_button(self):
        wg = self.weld_group
        xlim_min, xlim_max = wg.xlim
        ylim_min, ylim_max = wg.ylim

        self.xlim_min_var.set(xlim_min)
        self.xlim_max_var.set(xlim_max)
        self.ylim_min_var.set(ylim_min)
        self.ylim_max_var.set(ylim_max)

        self.style_var.set(wg.style)
        self.set_color_display_button_color(wg.color)
        self.scale_factor_scale.set(wg.scale)

    def update(self, weld_group):
        self.weld_group = wg = weld_group
        self.name_var.set(wg.name)
        self.weld_type_var.set(wg.weld_type)
        self.weld_size_var.set(wg.size)

        tx, ty, tz = wg.translation
        self.translate_x_var.set(tx)
        self.translate_y_var.set(ty)
        self.translate_z_var.set(tz)

        rotx, roty, rotz = wg.rotation
        self.rotate_x_var.set(rotx)
        self.rotate_y_var.set(roty)
        self.rotate_z_var.set(rotz)

        xlim_min, xlim_max = wg.xlim
        self.xlim_min_var.set(xlim_min)
        self.xlim_max_var.set(xlim_max)

        ylim_min, ylim_max = wg.ylim
        self.ylim_min_var.set(ylim_min)
        self.ylim_max_var.set(ylim_max)

        self.style_var.set(wg.style)
        self.set_color_display_button_color(wg.color)
        self.scale_factor_scale.set(wg.scale)

    def on_weld_group_apply_button(self, weld_group):
        wg = weld_group

        wg.name = self.name_var.get()
        wg.weld_type = self.weld_type_var.get()

        try:
            weld_size = float(self.weld_size_var.get())
            if weld_size < 0:
                raise ValueError
            wg.size = weld_size
        except ValueError:
            self.weld_size_var.set(wg.size)

        try:
            wg.translation = tuple(map(float, (self.translate_x_var.get(),
                                               self.translate_y_var.get(),
                                               self.translate_z_var.get())))
        except ValueError:
            tx, ty, tz = wg.translation
            self.translate_x_var.set(tx)
            self.translate_y_var.set(ty)
            self.translate_z_var.set(tz)

        try:
            wg.rotation = tuple(map(float, (self.rotate_x_var.get(),
                                            self.rotate_y_var.get(),
                                            self.rotate_z_var.get())))
        except ValueError:
            rotx, roty, rotz = wg.rotation
            self.rotate_x_var.set(rotx)
            self.rotate_y_var.set(roty)
            self.rotate_z_var.set(rotz)

        try:
            wg.xlim = tuple(map(float, (self.xlim_min_var.get(),
                                        self.xlim_max_var.get())))
        except ValueError:
            xlim_min, xlim_max = wg.xlim
            self.xlim_min_var.set(xlim_min)
            self.xlim_max_var.set(xlim_max)

        try:
            wg.ylim = tuple(map(float, (self.ylim_min_var.get(),
                                        self.ylim_max_var.get())))
        except ValueError:
            ylim_min, ylim_max = wg.ylim
            self.ylim_min_var.set(ylim_min)
            self.ylim_max_var.set(ylim_max)

        wg.style = self.style_var.get()
        wg.color = self.get_color_display_button_color()
        wg.scale = self.scale_factor_scale.get()


class WeldGroupPlotWidget:
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
    wg2.translation = (0, 5, 5)
    wg2.rotation = (90, 0, 0)
    wg2.update_transform()

    mwg = MultiWeldGroup()
    mwg.add_weld_group(wg1)
    mwg.add_weld_group(wg2)

    win = Tk()
    win.geometry("350x200")
    details = WeldGroupDetailsWidget(win, wg1)
    mainloop()
