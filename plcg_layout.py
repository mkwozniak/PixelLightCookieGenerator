import tkinter as tk
import tkinter.font as font
import plcg_config as cfg
from os.path import abspath, join, dirname
from PIL import Image, ImageTk


class UI:
    # absolute resource paths
    path_icon = abspath(join(dirname(__file__), cfg.PATH_ICON))
    path_logo = abspath(join(dirname(__file__), cfg.PATH_LOGO))

    entries_width = 5
    labels_width = 10
    layout_padding_x = 8.0
    layout_padding_y = 8.0
    logo_size = (96, 16)
    logo_scale = 2

    clr_bg = "#373737"
    clr_font_default = "#EEEEEE"
    clr_error = "red"
    clr_entries_fg = "white"
    clr_entries_bg = "#303030"
    clr_titles_bg = "#202020"
    clr_btn_fg = "white"
    clr_btn_bg = "#303030"
    clr_img_bgs = {
        "Clear": (0, 0, 0, 0),
        "Black": (0, 0, 0, 255)
    }

    window: tk.Tk = tk.Tk()
    window_preview: tk.Toplevel = tk.Toplevel(window,
                                              background="black")
    fnt_type = cfg.UI_FONT
    fnt_sys_4 = font.Font(family=fnt_type,
                          size=4)
    fnt_sys_8 = font.Font(family=fnt_type,
                          size=8)
    fnt_sys_12 = font.Font(family=fnt_type,
                           size=12)

    img_icon: Image = None
    img_logo: Image = None
    img_logo_tk: ImageTk.PhotoImage = None

    eid_width = "Width"
    eid_height = "Height"
    eid_radius = "Radius"
    eid_offset_x = "Offset X"
    eid_offset_y = "Offset Y"
    eid_clr_r = "Color Red"
    eid_clr_g = "Color Green"
    eid_clr_b = "Color Blue"
    eid_clr_bg = "Background Color"
    eid_falloff_start = "Falloff Start"
    eid_falloff_power = "Falloff Power"
    eid_falloff_spread = "Falloff Spread"
    eid_preview_scale = "Preview Scale"
    eid_preview_padding = "Preview Window Padding"
    eid_status_msg = "Status Message"

    entry_ids: list[str] = [
        eid_width, eid_height, eid_radius,
        eid_offset_x, eid_offset_y,
        eid_clr_r, eid_clr_g, eid_clr_b,
        eid_falloff_start, eid_falloff_power, eid_falloff_spread,
        eid_preview_scale, eid_preview_padding,
    ]

    # track signed and byte type entries
    entry_ids_signed: set = {
        eid_offset_x, eid_offset_y,
    }

    entry_ids_byte: set = {
        eid_clr_r, eid_clr_g, eid_clr_b,
    }

    # entry string vars
    entry_strings: dict[str, tk.StringVar] = {
        eid_width: tk.StringVar(window, name=eid_width),
        eid_height: tk.StringVar(window, name=eid_height),
        eid_radius: tk.StringVar(window, name=eid_radius),
        eid_offset_x: tk.StringVar(window, name=eid_offset_x),
        eid_offset_y: tk.StringVar(window, name=eid_offset_y),
        eid_clr_r: tk.StringVar(window, name=eid_clr_r),
        eid_clr_g: tk.StringVar(window, name=eid_clr_g),
        eid_clr_b: tk.StringVar(window, name=eid_clr_b),
        eid_clr_bg: tk.StringVar(window, name=eid_clr_bg),
        eid_falloff_start: tk.StringVar(window, name=eid_falloff_start),
        eid_falloff_power: tk.StringVar(window, name=eid_falloff_power),
        eid_falloff_spread: tk.StringVar(window, name=eid_falloff_spread),
        eid_preview_scale: tk.StringVar(window, name=eid_preview_scale),
        eid_preview_padding: tk.StringVar(window, name=eid_preview_padding),
        eid_status_msg: tk.StringVar(window, name=eid_status_msg)
    }

    """ FRAMES """
    frame_menu = tk.Frame(window,
                          bg=clr_bg)

    frame_status = tk.Frame(window,
                            bg=clr_bg)

    frame_general = tk.Frame(window,
                             bg=clr_bg)

    frame_color = tk.Frame(window,
                           bg=clr_bg)

    frame_falloff = tk.Frame(window,
                             bg=clr_bg)

    frame_preview = tk.Frame(window,
                             bg=clr_bg)

    frame_credits = tk.Frame(window,
                             bg=clr_bg)

    """ LABELS """
    lbl_logo = tk.Label(frame_credits)

    lbl_status = tk.Label(frame_status,
                          text="",
                          fg=clr_font_default,
                          bg=clr_bg,
                          font=fnt_sys_8,
                          wraplength=cfg.WIN_WIDTH - layout_padding_x,
                          height=2,
                          textvariable=entry_strings[eid_status_msg])

    lbl_greeting = tk.Label(text=cfg.TXT_GREETING,
                            fg=clr_font_default,
                            bg=clr_titles_bg,
                            font=fnt_sys_8)

    lbl_github = tk.Label(frame_credits,
                          text=cfg.TXT_GITHUB,
                          fg=clr_font_default,
                          bg=clr_titles_bg,
                          font=fnt_sys_8)

    lbl_general_title = tk.Label(frame_general,
                                 text="General",
                                 fg=clr_font_default,
                                 bg=clr_titles_bg,
                                 height=1,
                                 font=fnt_sys_8)

    lbl_size = tk.Label(frame_general,
                        text="Size[W, H]",
                        fg=clr_font_default,
                        bg=clr_entries_bg,
                        width=20,
                        font=fnt_sys_8)

    lbl_offset = tk.Label(frame_general,
                          text="Offset[X, Y]",
                          fg=clr_font_default,
                          bg=clr_entries_bg,
                          width=20,
                          font=fnt_sys_8)

    lbl_radius = tk.Label(frame_general,
                          text="Radius",
                          fg=clr_font_default,
                          bg=clr_entries_bg,
                          width=10,
                          font=fnt_sys_8)

    lbl_color_title = tk.Label(frame_color,
                               text="Colors",
                               bg=clr_titles_bg,
                               fg=clr_font_default,
                               font=fnt_sys_8)

    lbl_color_r = tk.Label(frame_color, text="Red[255]",
                           fg="Red",
                           bg=clr_entries_bg,
                           width=12,
                           font=fnt_sys_8)
    lbl_color_g = tk.Label(frame_color, text="Green[255]",
                           fg="Green",
                           bg=clr_entries_bg,
                           width=12,
                           font=fnt_sys_8)
    lbl_color_b = tk.Label(frame_color, text="Blue[255]",
                           fg="Blue",
                           bg=clr_entries_bg,
                           width=12,
                           font=fnt_sys_8)

    lbl_falloff_title = tk.Label(frame_falloff,
                                 text="Falloff",
                                 fg=clr_font_default,
                                 bg=clr_titles_bg,
                                 height=1,
                                 width=48,
                                 font=fnt_sys_8)

    lbl_falloff_start = tk.Label(frame_falloff,
                                 text="Falloff Start",
                                 fg=clr_font_default,
                                 bg=clr_entries_bg,
                                 width=16,
                                 font=fnt_sys_8)

    lbl_falloff_power = tk.Label(frame_falloff,
                                 text="Falloff Power",
                                 fg=clr_font_default,
                                 bg=clr_entries_bg,
                                 width=16,
                                 font=fnt_sys_8)

    lbl_falloff_spread = tk.Label(frame_falloff,
                                  text="Falloff Spread",
                                  fg=clr_font_default,
                                  bg=clr_entries_bg,
                                  width=16,
                                  font=fnt_sys_8)

    lbl_background = tk.Label(frame_color,
                              text="Background",
                              fg=clr_font_default,
                              bg=clr_entries_bg,
                              width=12,
                              font=fnt_sys_8)

    # preview image label
    lbl_preview = tk.Label(window_preview)

    lbl_preview_title = tk.Label(frame_preview,
                                 text="Preview Options",
                                 fg=clr_font_default,
                                 bg=clr_titles_bg,
                                 height=1,
                                 width=48,
                                 font=fnt_sys_8)

    lbl_preview_scale = tk.Label(frame_preview,
                                 text="Preview Scale",
                                 fg=clr_font_default,
                                 bg=clr_entries_bg,
                                 width=20,
                                 font=fnt_sys_8)

    lbl_preview_size = tk.Label(frame_preview,
                                text="Preview Padding",
                                fg=clr_font_default,
                                bg=clr_entries_bg,
                                width=20,
                                font=fnt_sys_8)

    lbl_preview_note = tk.Label(frame_preview,
                                text="Only affects the preview window, not the generated image.\n "
                                     "Previews are best visible with a Black background.",
                                fg=clr_font_default,
                                bg=clr_entries_bg,
                                width=24,
                                wraplength=cfg.WIN_WIDTH - layout_padding_x,
                                font=fnt_sys_8)

    lbl_menu_title = tk.Label(frame_menu,
                              text="Menu",
                              bg=clr_titles_bg,
                              fg=clr_font_default,
                              font=fnt_sys_8)

    """ ENTRIES """
    entry_width = tk.Entry(frame_general,
                           fg=clr_entries_fg, bg=clr_entries_bg,
                           width=entries_width,
                           font=fnt_sys_8,
                           textvariable=entry_strings[eid_width])

    entry_height = tk.Entry(frame_general,
                            fg=clr_entries_fg, bg=clr_entries_bg,
                            width=entries_width,
                            font=fnt_sys_8,
                            textvariable=entry_strings[eid_height])

    entry_offset_x = tk.Entry(frame_general,
                              fg=clr_entries_fg, bg=clr_entries_bg,
                              width=entries_width,
                              font=fnt_sys_8,
                              textvariable=entry_strings[eid_offset_x])

    entry_offset_y = tk.Entry(frame_general,
                              fg=clr_entries_fg, bg=clr_entries_bg,
                              width=entries_width,
                              font=fnt_sys_8,
                              textvariable=entry_strings[eid_offset_y])

    entry_radius = tk.Entry(frame_general,
                            fg=clr_entries_fg, bg=clr_entries_bg,
                            width=entries_width,
                            font=fnt_sys_8,
                            textvariable=entry_strings[eid_radius])

    entry_clr_r = tk.Entry(frame_color,
                           fg=clr_entries_fg, bg=clr_entries_bg,
                           width=4,
                           font=fnt_sys_8,
                           textvariable=entry_strings[eid_clr_r])

    entry_clr_g = tk.Entry(frame_color,
                           fg=clr_entries_fg, bg=clr_entries_bg,
                           width=4,
                           font=fnt_sys_8,
                           textvariable=entry_strings[eid_clr_g])

    entry_clr_b = tk.Entry(frame_color,
                           fg=clr_entries_fg, bg=clr_entries_bg,
                           width=4,
                           font=fnt_sys_8,
                           textvariable=entry_strings[eid_clr_b])

    entry_falloff_start = tk.Entry(frame_falloff,
                                   fg=clr_entries_fg, bg=clr_entries_bg,
                                   width=entries_width,
                                   font=fnt_sys_8,
                                   textvariable=entry_strings[eid_falloff_start])

    entry_falloff_power = tk.Entry(frame_falloff,
                                   fg=clr_entries_fg, bg=clr_entries_bg,
                                   width=entries_width,
                                   font=fnt_sys_8,
                                   textvariable=entry_strings[eid_falloff_power])

    entry_falloff_spread = tk.Entry(frame_falloff,
                                    fg=clr_entries_fg, bg=clr_entries_bg,
                                    width=entries_width,
                                    font=fnt_sys_8,
                                    textvariable=entry_strings[eid_falloff_spread])

    entry_preview_scale = tk.Entry(frame_preview,
                                   fg=clr_entries_fg, bg=clr_entries_bg,
                                   width=entries_width,
                                   font=fnt_sys_8,
                                   textvariable=entry_strings[eid_preview_scale])

    entry_preview_padding = tk.Entry(frame_preview,
                                     fg=clr_entries_fg, bg=clr_entries_bg,
                                     width=entries_width,
                                     font=fnt_sys_8,
                                     textvariable=entry_strings[eid_preview_padding])

    """ BUTTONS """
    btn_generate = tk.Button(
        frame_menu,
        text="G E N E R A T E",
        fg=clr_btn_fg, bg=clr_btn_bg,
        font=fnt_sys_8,
        height=1,
        width=20,
    )

    btn_preview = tk.Button(
        frame_menu,
        text="P R E V I E W",
        fg=clr_btn_fg, bg=clr_btn_bg,
        font=fnt_sys_8,
        height=1,
        width=20,
    )

    btn_save = tk.Button(
        frame_menu,
        text="S A V E",
        fg=clr_btn_fg, bg=clr_btn_bg,
        font=fnt_sys_8,
        height=1,
        width=20,
    )

    """ LIST BOXES """
    listbox_color_bg = tk.Listbox(frame_color,
                                  fg=clr_entries_fg, bg=clr_entries_bg,
                                  height=2,
                                  width=6,
                                  font=fnt_sys_8,
                                  selectmode=tk.SINGLE,
                                  exportselection=False)

    """ CHECK BUTTONS """
    half_point_val = tk.BooleanVar(window)
    half_point_checkbox = tk.Checkbutton(frame_general,
                                         height=1,
                                         font=fnt_sys_8,
                                         text="Half Point Mode",
                                         bg=clr_entries_bg,
                                         fg=clr_font_default,
                                         selectcolor=clr_entries_bg,
                                         activebackground=clr_entries_bg,
                                         variable=half_point_val)

    def __init__(self):
        self.load_resources()
        self.setup_windows()
        self.setup_grid()

    def load_resources(self):
        # load images #
        self.img_icon = tk.PhotoImage(file=self.path_icon)
        self.img_logo = Image.open(self.path_logo)  # jump through some hoops to resize logo
        self.img_logo = self.img_logo.resize((self.logo_size[0] * self.logo_scale,
                                              self.logo_size[1] * self.logo_scale),
                                             Image.Resampling.NEAREST)
        self.img_logo_tk = ImageTk.PhotoImage(self.img_logo)
        self.img_logo.close()

    def setup_windows(self):
        # window setup #
        self.window.configure(background=self.clr_bg)
        self.window.title(cfg.WIN_TITLE)
        self.window.geometry(cfg.WIN_SIZE)
        self.window.resizable(0, 0)
        self.window.columnconfigure(0, weight=1)
        self.window.iconphoto(False, self.img_icon)
        self.window.wm_iconphoto(False, self.img_icon)

        # preview window setup #
        self.window_preview.title(cfg.WIN_TITLE + " Preview")
        self.window_preview.geometry(cfg.WIN_SIZE)
        self.window_preview.resizable(0, 0)
        self.window_preview.iconphoto(False, self.img_icon)
        self.window_preview.wm_iconphoto(False, self.img_icon)

    def setup_grid(self):
        # frames setup #
        self.configure_equal_columns(self.frame_menu, 4)
        self.frame_menu.grid(row=3,
                             sticky=tk.EW,
                             padx=self.layout_padding_x)

        self.configure_equal_columns(self.frame_status, 1)
        self.frame_status.grid(row=4,
                               sticky=tk.EW,
                               padx=self.layout_padding_x)

        self.configure_equal_columns(self.frame_general, 3)
        self.frame_general.grid(row=5,
                                sticky=tk.EW,
                                padx=self.layout_padding_x)

        self.configure_equal_columns(self.frame_color, 4)
        self.frame_color.grid(row=6,
                              sticky=tk.EW,
                              padx=self.layout_padding_x)

        self.configure_equal_columns(self.frame_falloff, 3)
        self.frame_falloff.grid(row=7,
                                sticky=tk.EW,
                                padx=self.layout_padding_x)

        self.configure_equal_columns(self.frame_preview, 4)
        self.frame_preview.grid(row=8,
                                sticky=tk.EW,
                                padx=self.layout_padding_x)

        self.configure_equal_columns(self.frame_credits, 1)
        self.frame_credits.grid(row=9,
                                sticky=tk.EW,
                                padx=self.layout_padding_x)

        # labels setup #
        self.lbl_logo.configure(image=self.img_logo_tk, bg=self.clr_bg)
        self.lbl_logo.grid(column=0,
                           row=1,
                           columnspan=4)
        self.lbl_github.grid(column=0,
                             row=0,
                             sticky=tk.EW,
                             pady=self.layout_padding_y)

        self.lbl_status.grid(column=0,
                             row=5,
                             rowspan=2,
                             columnspan=4,
                             sticky=tk.EW,
                             padx=self.layout_padding_x)

        self.lbl_greeting.grid(column=0,
                               row=0,
                               columnspan=4,
                               sticky=tk.EW,
                               pady=self.layout_padding_y,
                               padx=self.layout_padding_x)

        self.lbl_general_title.grid(column=0,
                                    row=0,
                                    columnspan=4,
                                    sticky=tk.EW,
                                    pady=self.layout_padding_y)

        self.lbl_size.grid(column=0,
                           row=1,
                           sticky=tk.W)

        self.lbl_offset.grid(row=1,
                             column=1,
                             sticky=tk.W)

        self.lbl_radius.grid(row=1,
                             column=2,
                             sticky=tk.W)

        self.lbl_color_title.grid(column=0,
                                  row=0,
                                  sticky=tk.EW,
                                  columnspan=4,
                                  pady=self.layout_padding_y)

        self.lbl_color_r.grid(column=0,
                              row=1,
                              sticky=tk.NW)
        self.lbl_color_g.grid(column=1,
                              row=1,
                              sticky=tk.NW)
        self.lbl_color_b.grid(column=2,
                              row=1,
                              sticky=tk.NW)

        self.lbl_background.grid(column=3,
                                 row=1,
                                 sticky=tk.NW)

        self.lbl_falloff_title.grid(column=0,
                                    row=0,
                                    sticky=tk.EW,
                                    pady=self.layout_padding_y,
                                    columnspan=3)

        self.lbl_falloff_start.grid(column=0,
                                    row=1,
                                    sticky=tk.NW)

        self.lbl_falloff_power.grid(column=1,
                                    row=1,
                                    sticky=tk.NW)

        self.lbl_falloff_spread.grid(column=2,
                                     row=1,
                                     sticky=tk.NW)

        # self.lbl_menu_title.grid(column=0,
        #                          row=0,
        #                          sticky=tk.EW,
        #                          pady=self.layout_padding_y,
        #                          columnspan=4)

        self.lbl_preview.grid(column=0,
                              row=0)

        self.lbl_preview_title.grid(column=0,
                                    row=0,
                                    sticky=tk.EW,
                                    pady=self.layout_padding_y,
                                    columnspan=4)

        self.lbl_preview_scale.grid(column=0,
                                    row=1,
                                    sticky=tk.NW)

        self.lbl_preview_size.grid(column=1,
                                   row=1,
                                   sticky=tk.NW)

        self.lbl_preview_note.grid(column=0,
                                   row=3,
                                   sticky=tk.EW,
                                   columnspan=4)

        # entries setup #
        self.entry_width.grid(column=0,
                              row=2,
                              sticky=tk.NW,
                              pady=self.layout_padding_y)

        self.entry_height.grid(column=0,
                               row=2)

        self.entry_offset_x.grid(column=1,
                                 row=2,
                                 sticky=tk.NW,
                                 pady=self.layout_padding_y)

        self.entry_offset_y.grid(column=1,
                                 row=2,
                                 pady=self.layout_padding_y)

        self.entry_radius.grid(column=2,
                               row=2,
                               sticky=tk.NW,
                               pady=self.layout_padding_y)

        self.entry_clr_r.grid(column=0,
                              row=2,
                              sticky=tk.NW,
                              pady=self.layout_padding_y)

        self.entry_clr_g.grid(column=1,
                              row=2,
                              sticky=tk.NW,
                              pady=self.layout_padding_y)

        self.entry_clr_b.grid(column=2,
                              row=2,
                              sticky=tk.NW,
                              pady=self.layout_padding_y)

        self.entry_falloff_start.grid(column=0,
                                      row=2,
                                      sticky=tk.NW,
                                      pady=self.layout_padding_y)

        self.entry_falloff_power.grid(column=1,
                                      row=2,
                                      sticky=tk.NW,
                                      pady=self.layout_padding_y)

        self.entry_falloff_spread.grid(column=2,
                                       row=2,
                                       sticky=tk.NW,
                                       pady=self.layout_padding_y)

        self.entry_preview_scale.grid(column=0,
                                      row=2,
                                      sticky=tk.NW,
                                      pady=self.layout_padding_y)

        self.entry_preview_padding.grid(column=1,
                                        row=2,
                                        sticky=tk.NW,
                                        pady=self.layout_padding_y)

        # buttons setup #

        self.btn_generate.grid(column=0,
                               row=2,
                               sticky=tk.NW)

        self.btn_preview.grid(column=1,
                              sticky=tk.NW,
                              row=2)

        self.btn_save.grid(column=2,
                           sticky=tk.NW,
                           row=2)

        # list boxes setup #
        self.listbox_color_bg.grid(column=3,
                                   row=2,
                                   sticky=tk.NW,
                                   pady=self.layout_padding_y)

        # check buttons setup #
        self.half_point_checkbox.grid(column=0,
                                      row=3,
                                      sticky=tk.NW,
                                      columnspan=4)

    def configure_equal_columns(self, frame: tk.Frame, num_columns: int):
        for x in range(num_columns):
            frame.columnconfigure(x, weight=1)
