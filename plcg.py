import plcg_util as util
import plcg_config as cfg
from typing import Callable, Union
from dataclasses import dataclass
from PIL import Image, ImageTk
from time import time
from tkinter.filedialog import asksaveasfile
from plcg_layout import UI


@dataclass
class ImageOptions:
    width: int
    height: int
    center_x: int
    center_y: int
    radius: int
    half_pt_mode: bool
    color: tuple[int, int, int]
    color_bg: tuple[int, int, int]
    falloff_start: int
    falloff_power: int
    falloff_spread: int


class PixelLightCookieGenerator:
    ui: UI = None
    img: Image = None
    img_resized: Image = None  # for preview
    img_tk: ImageTk.PhotoImage = None  # for preview
    img_buffer: list = []
    img_valid: bool = False

    entries: dict[str, bool] = {}
    entry_data: dict[str, Union[int, bool, tuple[int, int, int]]] = {}
    entry_callbacks_success: dict[str, Callable[[str, int], None]] = {}
    entry_callbacks_failure: dict[str, Callable[[str], None]] = {}

    clg_window_rate: int = 32
    status_showing: bool = False
    status_clear_time: float = 3.5
    status_clear_timer: float = 0.0

    preview_open: bool = False
    preview_updated: bool = False

    anim_clear_time: float = 0.25
    anim_clear_timer: float = 0.0
    anim_curr: int = 0
    anim_max: int = 64
    anim_dir: int = 1
    anim_msg: str = "*"

    def __init__(self):
        t_start = time()
        util.log_msg(f"Initializing ...")
        self.init_layout()
        util.log_msg(f"Initialized Successfully in {time() - t_start}")

        self.ui.window.after(self.clg_window_rate, self.update)
        self.ui.window.mainloop()
        self.ui.window_preview.mainloop()

    def init_layout(self) -> None:
        self.ui = UI()
        # initialize all layout elements
        self.entry_init(self.ui.eid_width, cfg.DEFAULT_WIDTH)
        self.entry_init(self.ui.eid_height, cfg.DEFAULT_HEIGHT)
        self.entry_init(self.ui.eid_radius, cfg.DEFAULT_RADIUS)
        self.entry_init(self.ui.eid_offset_x, cfg.DEFAULT_OFFSET_X)
        self.entry_init(self.ui.eid_offset_y, cfg.DEFAULT_OFFSET_Y)
        self.entry_init(self.ui.eid_clr_r, cfg.DEFAULT_COLOR[0])
        self.entry_init(self.ui.eid_clr_g, cfg.DEFAULT_COLOR[1])
        self.entry_init(self.ui.eid_clr_b, cfg.DEFAULT_COLOR[2])
        self.entry_init(self.ui.eid_falloff_start, cfg.DEFAULT_FALLOFF_START)
        self.entry_init(self.ui.eid_falloff_power, cfg.DEFAULT_FALLOFF_POWER)
        self.entry_init(self.ui.eid_falloff_spread, cfg.DEFAULT_FALLOFF_SPREAD)
        self.entry_init(self.ui.eid_preview_scale, cfg.DEFAULT_PREVIEW_SCALE)
        self.entry_init(self.ui.eid_preview_padding, cfg.DEFAULT_PREVIEW_PADDING)

        # configure button callbacks
        self.ui.btn_preview.configure(command=self.preview_toggle)
        self.ui.btn_generate.configure(command=self.generate_image)
        self.ui.btn_save.configure(command=self.save_img_to_file)

        # configure other elements
        num_bg_colors = 0
        for key in self.ui.clr_img_bgs:
            self.ui.listbox_color_bg.insert(num_bg_colors + 1, key)
            num_bg_colors += 1
        self.ui.listbox_color_bg.select_set(1)
        self.ui.half_point_val.set(True)

        self.status_showing = False
        for x in range(self.anim_max):
            self.tick_anim_msg()

        self.ui.window_preview.geometry("256x256")
        self.ui.window_preview.withdraw()
        self.ui.window_preview.protocol("WM_DELETE_WINDOW", self.preview_close)

    def update(self) -> None:
        if self.status_showing:
            self.tick_clear_error()
        else:
            self.tick_anim()
        if not self.preview_updated and self.img_valid:
            self.generate_preview()
            self.preview_updated = True
        self.ui.window.after(self.clg_window_rate, self.update)

    def tick_clear_error(self) -> None:
        self.status_clear_timer += self.clg_window_rate
        if self.status_clear_timer >= (self.status_clear_time * 1000):
            self.ui.entry_strings[self.ui.eid_status_msg].set("")
            self.status_clear_timer = 0.
            self.status_showing = False
            self.ui.lbl_status.config(fg=self.ui.clr_font_default)

    def tick_anim(self) -> None:
        self.anim_clear_timer += self.clg_window_rate
        # fun little text animation which alternates between two symbols
        if self.anim_clear_timer >= (self.anim_clear_time * 1000):
            self.tick_anim_msg()
            self.ui.entry_strings[self.ui.eid_status_msg].set(self.anim_msg)
            self.anim_clear_timer = 0

    def tick_anim_msg(self) -> None:
        self.anim_dir = -1 if self.anim_dir == 1 else 1
        self.anim_msg += "." if self.anim_dir == 1 else "*"
        # slice first and last once maximum
        if len(self.anim_msg) > self.anim_max:
            self.anim_msg += "*"
            self.anim_msg = self.anim_msg[1:len(self.anim_msg) - 1]

    def display_error(self, error: str) -> None:
        self.status_clear_timer = 0.0
        self.ui.lbl_status.config(fg=self.ui.clr_error)
        self.ui.entry_strings[self.ui.eid_status_msg].set(error)
        self.status_showing = True

    def display_status(self, msg: str) -> None:
        self.status_clear_timer = 0.0
        self.ui.entry_strings[self.ui.eid_status_msg].set(msg)
        self.status_showing = True

    def entry_init(self, eid: str, val: Union[int, bool]) -> None:
        self.entry_set(eid, val)
        self.entry_hook(eid,
                        self.entry_set,
                        self.entry_fail,
                        self.entry_sanitize)

    def entry_hook(self, eid: str, callback_success, callback_fail, callback_write) -> None:
        if eid not in self.ui.entry_strings:
            util.log_msg(f"Cannot hook entry: {eid}. Data does not exist.")
            return
        # hook the entry to success, failure, and sanitize callbacks
        self.entry_callbacks_success[eid] = callback_success
        self.entry_callbacks_failure[eid] = callback_fail
        self.ui.entry_strings[eid].trace_add("write", callback_write)

    def entry_set(self, eid: str, entry_val: Union[int, bool]) -> None:
        self.ui.entry_strings[eid].set(str(entry_val))
        self.entry_data[eid] = entry_val
        self.entries[eid] = True

    def entry_sanitize(self, eid: str, index: str, mode: str) -> None:
        entry_val = self.ui.window.globalgetvar(eid)
        if len(entry_val) == 0:
            self.entries[eid] = False
            return
        if eid not in self.entry_data:
            util.log_msg(f"Cannot sanitize entry: {eid}. Data does not exist.")
            return

        t_val = type(self.entry_data[eid])
        if t_val is int:
            # eid in signed set can have preceding negative symbol
            if eid in self.ui.entry_ids_signed and entry_val == "-":
                return
            self.entry_check_cast(eid, util.try_cast_integer(entry_val))

    def entry_fail(self, eid: str) -> None:
        t_val = type(self.entry_data[eid])
        if t_val is int:
            if not self.entries[eid]:
                self.ui.entry_strings[eid].set("")
                self.entry_data[eid] = 0
            else:
                self.ui.entry_strings[eid].set(str(self.entry_data[eid]))
            if eid in self.ui.entry_ids_byte:
                self.display_error(f"{eid} must be a value between 0 and 255.")
                return
            if eid not in self.ui.entry_ids_signed:
                self.display_error(f"{eid} must be a positive integer value.")
                return
            self.display_error(f"{eid} must be an integer value.")
            return

    def entry_check_cast(self, eid: str, try_cast: (bool, int)) -> None:
        success = try_cast[0]
        val = try_cast[1]
        # invoke appropriate events on success or failure
        if success:
            if eid in self.ui.entry_ids_byte and (val > 255 or val < 0):
                self.entry_callbacks_failure[eid](eid)
                return
            self.entry_callbacks_success[eid](eid, val)
            return
        self.entry_callbacks_failure[eid](eid)

    def preview_toggle(self) -> None:
        if self.preview_open:
            self.preview_close()
            return
        if not self.img_valid:
            self.display_error(f"Preview Failed. No image generated.")
            return

        if not self.preview_updated:
            self.generate_preview()
        self.preview_open = True
        self.ui.window_preview.deiconify()

    def preview_close(self) -> None:
        self.ui.window_preview.withdraw()
        self.preview_open = False

    def save_img_to_file(self):
        if not self.img_valid:
            self.display_error(f"Save Failed. No image generated.")
            return
        new_file = asksaveasfile(mode='wb', initialfile='output_cookie.png',
                                 defaultextension=".png", filetypes=[("PNG Files", "*.png")])
        if new_file is None:
            self.display_error(f"Invalid path or file output.")
            return
        self.img.save(new_file, format="PNG")

    def entries_valid(self) -> bool:
        invalid_entries = ""
        for eid in self.ui.entry_ids:
            if eid not in self.entries:
                util.log_msg(f"Ignoring entry validation for: {eid}. Data does not exist.")
                continue
            if not self.entries[eid]:
                invalid_entries += f"{eid}, "
        if len(invalid_entries) > 0:
            self.display_error(f"Invalid Entries: {invalid_entries}")
            return False
        return True

    def entries_in_bounds(self, preview_entries=False) -> bool:
        if preview_entries:
            entry_preview_scale = self.entry_data[self.ui.eid_preview_scale]
            entry_preview_padding = self.entry_data[self.ui.eid_preview_padding]
            if entry_preview_scale < 1 or entry_preview_scale > cfg.MAX_PREVIEW_SCALE:
                self.display_error(f"{self.ui.eid_preview_scale} must be between 1 and {cfg.MAX_PREVIEW_SCALE}.")
                return False
            if entry_preview_padding < 0 or entry_preview_padding > cfg.MAX_PREVIEW_PADDING:
                self.display_error(f"{self.ui.eid_preview_padding} must be between 0 and {cfg.MAX_PREVIEW_PADDING}.")
                return False
            return True

        entry_width = self.entry_data[self.ui.eid_width]
        entry_height = self.entry_data[self.ui.eid_height]

        over_sized = entry_width > cfg.MAX_SIZE or entry_height > cfg.MAX_SIZE
        under_sized = entry_width <= 0 or entry_height <= 0
        if over_sized or under_sized:
            self.display_error(f"{self.ui.eid_width} and {self.ui.eid_height} "
                               f"must be between 1 and {cfg.MAX_SIZE}.")
            return False

        entry_radius = self.entry_data[self.ui.eid_radius]
        rad_over_sized = entry_radius >= entry_width or entry_radius >= entry_height
        rad_under_sized = entry_radius <= 0
        if rad_over_sized or rad_under_sized:
            self.display_error(f"{self.ui.eid_radius} must be between 1 "
                               f"and the width/height of your image.")
            return False

        entry_offset_x = self.entry_data[self.ui.eid_offset_x]
        entry_offset_y = self.entry_data[self.ui.eid_offset_y]
        x_out_range = entry_offset_x < -entry_width or entry_offset_x > entry_width
        y_out_range = entry_offset_y < -entry_height or entry_offset_y > entry_height
        if x_out_range or y_out_range:
            self.display_error(f"{self.ui.eid_offset_x} and {self.ui.eid_offset_y} must be in range of "
                               f"{self.ui.eid_width} and {self.ui.eid_height}.")
            return False

        if len(self.ui.listbox_color_bg.curselection()) == 0:
            self.display_error(f"You must select a {self.ui.eid_clr_bg}")
            return False

        return True

    def generate_preview(self):
        if not self.entries_valid() or not self.entries_in_bounds(preview_entries=True):
            util.log_msg("Preview Image generate failed. Entries invalid or out of bounds.")
            return
        resized_width = self.entry_data[self.ui.eid_width] * self.entry_data[self.ui.eid_preview_scale]
        resized_height = self.entry_data[self.ui.eid_height] * self.entry_data[self.ui.eid_preview_scale]
        self.img_resized = self.img.resize((resized_width, resized_height), Image.Resampling.NEAREST)
        self.img_tk = ImageTk.PhotoImage(self.img_resized)
        prev_w = resized_width + self.entry_data[self.ui.eid_preview_padding]
        prev_h = resized_height + self.entry_data[self.ui.eid_preview_padding]
        self.ui.window_preview.geometry(f"{prev_w}x{prev_h}")
        self.ui.lbl_preview.configure(image=self.img_tk)
        self.ui.lbl_preview.image = self.img_tk
        util.log_msg("Generated Preview Image")

    def generate_image(self) -> None:
        self.img_valid = False
        self.display_status("Starting Generation ...")
        if not self.entries_valid() or not self.entries_in_bounds():
            util.log_msg("Image generate failed. Entries invalid or out of bounds.")
            return

        cent_x = int(self.entry_data[self.ui.eid_width] / 2) + self.entry_data[self.ui.eid_offset_x]
        cent_y = int(self.entry_data[self.ui.eid_height] / 2) + self.entry_data[self.ui.eid_offset_y]
        color = (self.entry_data[self.ui.eid_clr_r],
                 self.entry_data[self.ui.eid_clr_g],
                 self.entry_data[self.ui.eid_clr_b])
        clr_bg_selection = self.ui.listbox_color_bg.get(self.ui.listbox_color_bg.curselection()[0])

        # create options and generate image
        options = ImageOptions(width=self.entry_data[self.ui.eid_width],
                               height=self.entry_data[self.ui.eid_height],
                               center_x=cent_x,
                               center_y=cent_y,
                               radius=self.entry_data[self.ui.eid_radius],
                               half_pt_mode=self.ui.half_point_val.get(),
                               color=color,
                               color_bg=self.ui.clr_img_bgs[clr_bg_selection],
                               falloff_power=self.entry_data[self.ui.eid_falloff_power],
                               falloff_spread=self.entry_data[self.ui.eid_falloff_spread],
                               falloff_start=self.entry_data[self.ui.eid_falloff_start])

        self.img = Image.new(cfg.FORMAT, (options.width, options.height), cfg.DEFAULT_BG)
        self.generate_buffer(options)
        self.img.putdata(self.img_buffer)
        self.img_valid = True
        self.preview_updated = False
        self.display_status("Finished Generating Successfully!")
        util.log_msg("Generated Final Image")

    def generate_buffer(self, opt: ImageOptions):
        self.display_status("Generating Buffer ...")
        new_buffer = util.clear_plcg_rgba_buffer(opt.width, opt.height)
        half_pt = .5 if opt.half_pt_mode else 0
        clr = opt.color
        clr_bg = opt.color_bg
        center_x = opt.center_x
        center_y = opt.center_y
        rad_squared = opt.radius * opt.radius
        bg_is_clear = clr_bg[3] == 0

        fall_z = 0
        rads = []
        fall_bright = 0
        # generate 1d falloff gradient
        for z in range(0, opt.radius, opt.falloff_spread):
            # increment the falloff only outside the start radius
            if z >= opt.falloff_start:
                fall_bright = (fall_z * opt.falloff_power)
                fall_z += opt.falloff_spread
            fall_bright = max(min(255, fall_bright), 0)
            # falloff radius power and its squared radius in tuple
            f_sq = z * z if opt.half_pt_mode else (z * z) - 1
            rads.append((fall_bright, f_sq))

        # iterate each pixel
        for y in range(opt.height):
            for x in range(opt.width):
                index = opt.width * y + x
                new_buffer[index] = clr_bg
                # squared distance from center to check if inside circle
                half_x = x + half_pt
                half_y = y + half_pt
                dx = center_x - half_x
                dy = center_y - half_y
                distance_squared = dx * dx + dy * dy
                if not distance_squared <= rad_squared:
                    continue

                # iterate falloff each pixel
                # there's probably a much more efficient way to do this
                # but it gets the job done
                for z in range(len(rads)):
                    f_dist = rads[z][1]
                    if distance_squared > f_dist:
                        falloff = rads[z][0]
                        if bg_is_clear:
                            # clear cookies use the alpha channel
                            new_buffer[index] = (clr[0], clr[1], clr[2], 255 - falloff)
                            continue
                        new_buffer[index] = (clr[0] - falloff, clr[1] - falloff, clr[2] - falloff, 255)

        self.img_buffer = new_buffer
