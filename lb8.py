from tkinter import *
from tkinter import PhotoImage
from tkinter.ttk import *
from tkinter.filedialog import *
from tkinter.messagebox import *
import os, struct, zlib
import math

class Window:
    def __init__(self, title):
        self.root = Tk()
        self.root.title(title)
        screen_x = self.root.winfo_screenwidth()
        screen_y = self.root.winfo_screenheight()
        window_x = int(screen_x * 0.9)
        window_y = int(screen_y * 0.9)
        x, y = self.window_center(screen_x, screen_y, window_x, window_y)
        self.root.geometry(f"{window_x}x{window_y}+{x}+{y}")
        self.root.resizable(False, False)
        self.root.overrideredirect(True)
        self.image_path = None
        self.photo_image = None
        self.orig_png_points = None
        self.nearest_png_points = None
        self.bilinear_png_points = None
        self.bicubic_png_points = None
        self.widgets()
    
    def window_center(self, x, y, window_x, window_y):
        x = (x - window_x) // 2
        y = (y - window_y) // 2
        return x, y
    
    def widgets(self):
        self.button_exit = Button(self.root, text = "X", command = self.root.destroy)
        self.button_exit.place(relx = 0.97, rely = 0.005, relwidth = 0.025, relheight = 0.05)
        #оригиналное изображение
        self.button_orig_image = Button(self.root, text = "Выбрать картинку", command = self.select_image)
        self.button_orig_image.place(relx = 0.005, rely = 0.005, relwidth = 0.15, relheight = 0.05)
        self.frame_orig_image = Frame(self.root)
        self.frame_orig_image.place(relx = 0.005, rely = 0.06, relwidth = 0.49, relheight = 0.44)
        self.canvas_orig_image = self.create_canvas(self.frame_orig_image)
        #указатели для афинного преобразования
        self.label_afin = Label(self.root, text = "Выберите угол наклона")
        self.label_afin.place(relx = 0.16, rely = 0.005, relwidth = 0.11, relheight = 0.025)
        self.angle_afin = Spinbox(self.root, from_ = -360, to = 360, width = 10, font = "Calibri")
        self.angle_afin.place(relx = 0.21, rely = 0.03, relwidth = 0.05, relheight = 0.025)

        self.label_afin = Label(self.root, text = "Масштаб по x")
        self.label_afin.place(relx = 0.27, rely = 0.005, relwidth = 0.07, relheight = 0.025)
        self.scale_x = Spinbox(self.root, from_ = 0.1, to = 5, increment = 0.1, width = 5, font = "Calibri")
        self.scale_x.place(relx = 0.335, rely = 0.005, relwidth = 0.05, relheight = 0.025)

        self.label_afin = Label(self.root, text = "Масштаб по y")
        self.label_afin.place(relx = 0.27, rely = 0.03, relwidth = 0.07, relheight = 0.025)
        self.scale_y = Spinbox(self.root, from_ = 0.1, to = 5, increment = 0.1, width = 5, font = "Calibri")
        self.scale_y.place(relx = 0.335, rely = 0.03, relwidth = 0.05, relheight = 0.025)

        self.label_afin = Label(self.root, text = "Скос по x")
        self.label_afin.place(relx = 0.39, rely = 0.005, relwidth = 0.05, relheight = 0.025)
        self.skew_x = Spinbox(self.root, from_ = -2, to = 2, increment = 0.1, width = 5, font = "Calibri")
        self.skew_x.place(relx = 0.44, rely = 0.005, relwidth = 0.05, relheight = 0.025)

        self.label_afin = Label(self.root, text = "Скос по y")
        self.label_afin.place(relx = 0.39, rely = 0.03, relwidth = 0.05, relheight = 0.025)
        self.skew_y = Spinbox(self.root, from_ = -2, to = 2, increment = 0.1, width = 5, font = "Calibri")
        self.skew_y.place(relx = 0.44, rely = 0.03, relwidth = 0.05, relheight = 0.025)

        self.scale_x.set(1.0)
        self.scale_y.set(1.0)
        self.skew_x.set(0.0)
        self.skew_y.set(0.0)
        self.angle_afin.set(0)
        #интерполяция по ближайшему соседу
        self.button_nearest_image = Button(self.root, text = "Интерполяция по ближайшему соседу", command = self.nearest_neighbor_interpolation)
        self.button_nearest_image.place(relx = 0.5, rely = 0.005, relwidth = 0.2, relheight = 0.05)
        self.frame_nearest_image = Frame(self.root)
        self.frame_nearest_image.place(relx = 0.5, rely = 0.06, relwidth = 0.49, relheight = 0.44)
        self.canvas_nearest_image = self.create_canvas(self.frame_nearest_image)
        self.button_saved_nearest_image = Button(self.root, text = "Сохранить", command = lambda: self.saved_image('nearest'))
        self.button_saved_nearest_image.place(relx = 0.71, rely = 0.005, relwidth = 0.15, relheight = 0.05)
        #билинейная интерполяция
        self.button_bilinear_image = Button(self.root, text = "Билинейная интерполяция", command = self.bilinear_interpolation)
        self.button_bilinear_image.place(relx = 0.005, rely = 0.5, relwidth = 0.2, relheight = 0.05)
        self.frame_bilinear_image = Frame(self.root)
        self.frame_bilinear_image.place(relx = 0.005, rely = 0.55, relwidth = 0.49, relheight = 0.44)
        self.canvas_bilinear_image = self.create_canvas(self.frame_bilinear_image)
        self.button_saved_bilinear_image = Button(self.root, text = "Сохранить", command = lambda: self.saved_image('bilinear'))
        self.button_saved_bilinear_image.place(relx = 0.21, rely = 0.5, relwidth = 0.15, relheight = 0.05)
        #бикубическаая интерполяция
        self.button_bicubic_image = Button(self.root, text = "Бикубическаая интерполяция", command = self.bicubic_interpolation)
        self.button_bicubic_image.place(relx = 0.5, rely = 0.5, relwidth = 0.2, relheight = 0.05)
        self.frame_bicubic_image = Frame(self.root)
        self.frame_bicubic_image.place(relx = 0.5, rely = 0.55, relwidth = 0.49, relheight = 0.44)
        self.canvas_bicubic_image = self.create_canvas(self.frame_bicubic_image)
        self.button_saved_bicubic_image = Button(self.root, text = "Сохранить", command = lambda: self.saved_image('bicubic'))
        self.button_saved_bicubic_image.place(relx = 0.71, rely = 0.5, relwidth = 0.15, relheight = 0.05)

    def create_canvas(self, frame):
        canvas = Canvas(frame, bg = "white")
        scrollbar_x = Scrollbar(frame, orient = HORIZONTAL, command = canvas.xview)
        scrollbar_y = Scrollbar(frame, orient = VERTICAL, command = canvas.yview)
        canvas.grid(row = 0, column = 0, sticky="nsew")
        scrollbar_y.grid(row = 0, column = 1, sticky = "ns")
        scrollbar_x.grid(row = 1, column = 0, sticky = "ew")
        frame.grid_rowconfigure(0, weight = 1)
        frame.grid_columnconfigure(0, weight = 1)
        canvas.configure(xscrollcommand = scrollbar_x.set, yscrollcommand = scrollbar_y.set)
        canvas.scrollbar_x = scrollbar_x
        canvas.scrollbar_y = scrollbar_y
        return canvas

    def scrollbar_x(self, frame, canvas):
        xbar = Scrollbar(frame, orient = HORIZONTAL, command = canvas.xview)
        xbar.place(relx = 0, rely = 1, relheight = 1, anchor = "ne", width = 17)
        return xbar
        
    def scrollbar_y(self, frame, canvas):
        ybar = Scrollbar(frame, orient = VERTICAL, command = canvas.yview)
        ybar.place(relx = 1, rely = 0, relwidth = 0.95, anchor = "sw", width = 17)
        return ybar

    def run(self):
        self.root.mainloop()
    
    def select_image(self):
        file_types = [
            ("Поддерживаемые форматы", "*.png *.ppm"),
            ("PNG файлы", "*.png"),
            ("PPM файлы", "*.ppm"),
            ("Все файлы", "*.*")]
        file_path = askopenfilename(title = "Выбрать изображение", filetypes = file_types)
        if file_path:
            self.image_path = file_path
            file_ext = os.path.splitext(file_path)[1].lower()
            supported_formats = ['.png', '.ppm']
            if file_ext in supported_formats:
                try:
                    self.photo_image = PhotoImage(file = file_path)
                    self.orig_img_width = self.photo_image.width()
                    self.orig_img_height = self.photo_image.height()
                    self.orig_png_points = self.getPixelArray()
                    self.display_image(self.canvas_orig_image, self.orig_png_points)
                except Exception as e:
                    print(f"Ошибка в select_image: {str(e)}")
                    showerror("Ошибка")
            else: showerror("формат не поддерживается")
    
    def display_image(self, canvas, points):
        try:
            if not points:
                showerror("Ошибка", "Нет изображения")
                return
            min_x = 0
            min_y = 0
            max_x = 0
            max_y = 0
            for line in points:
                for color, (x, y) in line:
                    min_x = min(min_x, x)
                    min_y = min(min_y, y)
                    max_x = max(max_x, x)
                    max_y = max(max_y, y)
            orig_width = max_x - min_x + 1
            orig_height = max_y - min_y + 1
            canvas_width = max_x + 1
            canvas_height = max_y + 1
            offset_x = 0
            offset_y = 0
            if min_x < 0:
                offset_x = abs(min_x)
                canvas_width = max_x + offset_x + 1
            if min_y < 0:
                offset_y = abs(min_y)
                canvas_height = max_y + offset_y + 1
            img = PhotoImage(width = orig_width, height = orig_height)
            for y in range(orig_height):
                for x in range(orig_width):
                    img.put("#ffffff", (x, y))
            for line in points:
                for color, (orig_x, orig_y) in line:
                    img_x = orig_x - min_x
                    img_y = orig_y - min_y
                    if 0 <= img_x < orig_width and 0 <= img_y < orig_height:
                        img.put(color, (img_x, img_y))
            canvas.delete("all")
            left_bound = min(0, min_x)
            top_bound = min(0, min_y)
            image_in_scroll_x = left_bound if min_x < 0 else 0
            image_in_scroll_y = top_bound if min_y < 0 else 0
            canvas.create_image(image_in_scroll_x, image_in_scroll_y, anchor = "nw", image = img)
            canvas.image_ref = img
            canvas.config(scrollregion = (image_in_scroll_x, image_in_scroll_y, canvas_width, canvas_height))
            canvas.xview_moveto(-image_in_scroll_x)
            canvas.yview_moveto(-image_in_scroll_y)
        except Exception as e:
            print(f"Ошибка в display_image: {str(e)}")
            raise Exception(f"Ошибка загрузки изображения: {str(e)}")

    def getPixelArray(self):
        if not self.photo_image:
            return None
        try:
            width = self.orig_img_width
            height = self.orig_img_height
            png_points = []
            for y in range(height):
                row = []
                for x in range(width):
                    try:
                        color = self.photo_image.get(x, y)
                        if isinstance(color, tuple):
                            if len(color) >= 3:
                                r, g, b = color[0], color[1], color[2]
                                hex_color = f"#{r:02x}{g:02x}{b:02x}"
                            else:
                                hex_color = "#FFFFFF"
                        elif isinstance(color, str):
                            hex_color = color
                        else:
                            hex_color = "#FFFFFF"
                        pixel_dict = hex_color
                        row.append((pixel_dict, (x, y)))
                    except:
                        row.append(("#FFFFFF", (x, y)))
                png_points.append(row)
            return png_points
        except Exception as e:
            print(f"Ошибка при создании массива: {e}")
            return None

    def nearest_neighbor_interpolation(self):
        if not self.orig_png_points:
            showerror("Ошибка", "Сначала выберите изображение")
            return
        try:
            if not self.scale_x.get() or not self.scale_y.get() or not self.skew_x.get() or not self.skew_y.get() or not self.angle_afin.get():
                showerror("Ошибка", "Введите значения во все поля")
                return
            angle = math.radians(float(self.angle_afin.get()))
            scale_x_val = float(self.scale_x.get())
            scale_y_val = float(self.scale_y.get())
            skew_x_val = float(self.skew_x.get())
            skew_y_val = float(self.skew_y.get())
            self.angle = angle
            self.scale_x_val, self.scale_y_val = scale_x_val, scale_y_val
            self.skew_x_val, self.skew_y_val = skew_x_val, skew_y_val
            cos_fi = math.cos(angle)
            sin_fi = math.sin(angle)
            height_orig = len(self.orig_png_points)
            width_orig = len(self.orig_png_points[0])
            corners = [(0, 0), (width_orig - 1, 0), (0, height_orig - 1), (width_orig - 1, height_orig - 1)]
            min_x = 0
            min_y = 0
            max_x = 0
            max_y = 0
            for px, py in corners:
                rotated_x = cos_fi * px + -sin_fi * py
                rotated_y = sin_fi * px + cos_fi * py
                scaled_x = rotated_x * scale_x_val
                scaled_y = rotated_y * scale_y_val
                skewed_x = scaled_x + skew_x_val * scaled_y
                skewed_y = scaled_y + skew_y_val * scaled_x
                new_x = skewed_x
                new_y = skewed_y
                min_x = min(min_x, new_x)
                min_y = min(min_y, new_y)
                max_x = max(max_x, new_x)
                max_y = max(max_y, new_y)
            min_x = int(math.floor(min_x))
            min_y = int(math.floor(min_y))
            max_x = int(math.ceil(max_x))
            max_y = int(math.ceil(max_y))
            width = max_x - min_x + 1
            height = max_y - min_y + 1
            det = 1 - skew_x_val * skew_y_val
            self.nearest_png_points = []
            for y in range(height):
                row = []
                for x in range(width):
                    res_x = x + min_x
                    res_y = y + min_y
                    scaled_x = (res_x - skew_x_val * res_y) / det
                    scaled_y = (res_y - skew_y_val * res_x) / det
                    rotated_x = scaled_x / scale_x_val
                    rotated_y = scaled_y / scale_y_val
                    src_x = cos_fi * rotated_x + sin_fi * rotated_y
                    src_y = -sin_fi * rotated_x + cos_fi * rotated_y
                    nearest_x = int(round(src_x))
                    nearest_y = int(round(src_y))
                    if 0 <= nearest_x < width_orig and 0 <= nearest_y < height_orig:
                        color = self.orig_png_points[nearest_y][nearest_x][0]
                    else:
                        color = "#ffffff"
                    row.append((color, (res_x, res_y)))
                self.nearest_png_points.append(row)
            self.display_image(self.canvas_nearest_image, self.nearest_png_points)
        
        except Exception as e:
            showerror("Ошибка", f"Ошибка при интерполяции ближайшего соседа: {str(e)}")

    def bilinear_interpolation(self):
        if not self.orig_png_points:
            showerror("Ошибка", "Сначала выберите изображение")
            return
        try:
            if not self.scale_x.get() or not self.scale_y.get() or not self.skew_x.get() or not self.skew_y.get() or not self.angle_afin.get():
                showerror("Ошибка", "Введите значения во все поля")
                return
            angle = math.radians(float(self.angle_afin.get()))
            scale_x_val = float(self.scale_x.get())
            scale_y_val = float(self.scale_y.get())
            skew_x_val = float(self.skew_x.get())
            skew_y_val = float(self.skew_y.get())
            self.angle = angle
            self.scale_x_val, self.scale_y_val = scale_x_val, scale_y_val
            self.skew_x_val, self.skew_y_val = skew_x_val, skew_y_val
            cos_fi = math.cos(angle)
            sin_fi = math.sin(angle)
            height_orig = len(self.orig_png_points)
            width_orig = len(self.orig_png_points[0])
            corners = [(0, 0), (width_orig - 1, 0), (0, height_orig - 1), (width_orig - 1, height_orig - 1)]
            min_x = 0
            min_y = 0
            max_x = 0
            max_y = 0
            for px, py in corners:
                rotated_x = cos_fi * px + -sin_fi * py
                rotated_y = sin_fi * px + cos_fi * py
                scaled_x = rotated_x * scale_x_val
                scaled_y = rotated_y * scale_y_val
                skewed_x = scaled_x + skew_x_val * scaled_y
                skewed_y = scaled_y + skew_y_val * scaled_x
                new_x = skewed_x
                new_y = skewed_y
                min_x = min(min_x, new_x)
                min_y = min(min_y, new_y)
                max_x = max(max_x, new_x)
                max_y = max(max_y, new_y)
            min_x = int(math.floor(min_x))
            min_y = int(math.floor(min_y))
            max_x = int(math.ceil(max_x))
            max_y = int(math.ceil(max_y))
            width = max_x - min_x + 1
            height = max_y - min_y + 1
            det = 1 - skew_x_val * skew_y_val
            self.bilinear_png_points = []
            for y in range(height):
                row = []
                for x in range(width):
                    res_x = x + min_x
                    res_y = y + min_y
                    scaled_x = (res_x - skew_x_val * res_y) / det
                    scaled_y = (res_y - skew_y_val * res_x) / det
                    rotated_x = scaled_x / scale_x_val
                    rotated_y = scaled_y / scale_y_val
                    src_x = cos_fi * rotated_x + sin_fi * rotated_y
                    src_y = -sin_fi * rotated_x + cos_fi * rotated_y
                    x0 = int(math.floor(src_x))
                    y0 = int(math.floor(src_y))
                    x1 = x0 + 1
                    y1 = y0 + 1
                    a = src_x - x0
                    b = src_y - y0
                    if (0 <= x0 < width_orig and 0 <= x1 < width_orig and 
                        0 <= y0 < height_orig and 0 <= y1 < height_orig):
                        c00 = self.orig_png_points[y0][x0][0]
                        c10 = self.orig_png_points[y0][x1][0]
                        c01 = self.orig_png_points[y1][x0][0]
                        c11 = self.orig_png_points[y1][x1][0]

                        def hex_to_rgb(hex_color):
                            hex_color = hex_color[1:]
                            return (int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16))
    
                        r00, g00, b00 = hex_to_rgb(c00)
                        r10, g10, b10 = hex_to_rgb(c10)
                        r01, g01, b01 = hex_to_rgb(c01)
                        r11, g11, b11 = hex_to_rgb(c11)
                        r = int((1 - a) * (1 - b) * r00 + a * (1 - b) * r10 + (1 - a) * b * r01 + a * b * r11)
                        g = int((1 - a) * (1 - b) * g00 + a * (1 - b) * g10 + (1 - a) * b * g01 + a * b * g11)
                        b = int((1 - a) * (1 - b) * b00 + a * (1 - b) * b10 + (1 - a) * b * b01 + a * b * b11)
                        r = max(0, min(255, r))
                        g = max(0, min(255, g))
                        b = max(0, min(255, b))
                        color = f"#{r:02x}{g:02x}{b:02x}"
                    else:
                        color = "#ffffff"
                    row.append((color, (res_x, res_y)))
                self.bilinear_png_points.append(row)
            self.display_image(self.canvas_bilinear_image, self.bilinear_png_points)
        except Exception as e:
            showerror("Ошибка", f"Ошибка при билинейной интерполяции: {str(e)}")

    def bicubic_interpolation(self):
        if not self.orig_png_points:
            showerror("Ошибка", "Сначала выберите изображение")
            return
        try:
            if not self.scale_x.get() or not self.scale_y.get() or not self.skew_x.get() or not self.skew_y.get() or not self.angle_afin.get():
                showerror("Ошибка", "Введите значения во все поля")
                return
            angle = math.radians(float(self.angle_afin.get()))
            scale_x_val = float(self.scale_x.get())
            scale_y_val = float(self.scale_y.get())
            skew_x_val = float(self.skew_x.get())
            skew_y_val = float(self.skew_y.get())
            self.angle = angle
            self.scale_x_val, self.scale_y_val = scale_x_val, scale_y_val
            self.skew_x_val, self.skew_y_val = skew_x_val, skew_y_val
            cos_fi = math.cos(angle)
            sin_fi = math.sin(angle)
            height_orig = len(self.orig_png_points)
            width_orig = len(self.orig_png_points[0])
            corners = [(0, 0), (width_orig - 1, 0), (0, height_orig - 1), (width_orig - 1, height_orig - 1)]
            min_x = 0
            min_y = 0
            max_x = 0
            max_y = 0
            for px, py in corners:
                rotated_x = cos_fi * px + -sin_fi * py
                rotated_y = sin_fi * px + cos_fi * py
                scaled_x = rotated_x * scale_x_val
                scaled_y = rotated_y * scale_y_val
                skewed_x = scaled_x + skew_x_val * scaled_y
                skewed_y = scaled_y + skew_y_val * scaled_x
                new_x = skewed_x
                new_y = skewed_y
                min_x = min(min_x, new_x)
                min_y = min(min_y, new_y)
                max_x = max(max_x, new_x)
                max_y = max(max_y, new_y)
            min_x = int(math.floor(min_x))
            min_y = int(math.floor(min_y))
            max_x = int(math.ceil(max_x))
            max_y = int(math.ceil(max_y))
            width = max_x - min_x + 1
            height = max_y - min_y + 1
            det = 1 - skew_x_val * skew_y_val
            self.bicubic_png_points = []
            for y in range(height):
                row = []
                for x in range(width):
                    res_x = x + min_x
                    res_y = y + min_y
                    scaled_x = (res_x - skew_x_val * res_y) / det
                    scaled_y = (res_y - skew_y_val * res_x) / det
                    rotated_x = scaled_x / scale_x_val
                    rotated_y = scaled_y / scale_y_val
                    src_x = cos_fi * rotated_x + sin_fi * rotated_y
                    src_y = -sin_fi * rotated_x + cos_fi * rotated_y
                    if 1 <= src_x < width_orig - 2 and 1 <= src_y < height_orig - 2:
                        color = self.bicubic_interpolate_pixel(self.orig_png_points, src_x, src_y, height_orig, width_orig)
                    else:
                        color = "#ffffff"
                    row.append((color, (res_x, res_y)))
                self.bicubic_png_points.append(row)
            self.display_image(self.canvas_bicubic_image, self.bicubic_png_points)
        except Exception as e:
            showerror("Ошибка", f"Ошибка при бикубической интерполяции: {str(e)}")

    def bicubic_interpolate_pixel(self, img, x, y, height_orig, width_orig):
        x0 = int(math.floor(x))
        y0 = int(math.floor(y))
        p = []
        for dy in range(-1, 3):
            for dx in range(-1, 3):
                ix = x0 + dx
                iy = y0 + dy
                if 0 <= ix < width_orig and 0 <= iy < height_orig:
                    hex_color = img[iy][ix][0]
                    hex_color = hex_color[1:]
                    r = int(hex_color[0:2], 16)
                    g = int(hex_color[2:4], 16)
                    b = int(hex_color[4:6], 16)
                    p.append((r, g, b))
                else:
                    p.append((255, 255, 255))
        r_vals = [p[i][0] for i in range(16)]
        g_vals = [p[i][1] for i in range(16)]
        b_vals = [p[i][2] for i in range(16)]
        a = x - x0
        b = y - y0
        r_row = []
        g_row = []
        b_row = []
        for i in range(4):
            r_row.append(self.cubic_interpolate(r_vals[i*4:(i+1)*4], a))
            g_row.append(self.cubic_interpolate(g_vals[i*4:(i+1)*4], a))
            b_row.append(self.cubic_interpolate(b_vals[i*4:(i+1)*4], a))
        r = self.cubic_interpolate(r_row, b)
        g = self.cubic_interpolate(g_row, b)
        b = self.cubic_interpolate(b_row, b)
        r = max(0, min(255, int(r)))
        g = max(0, min(255, int(g)))
        b = max(0, min(255, int(b)))
        return f"#{r:02x}{g:02x}{b:02x}"

    def cubic_interpolate(self, p, x):
        return p[1] + 0.5 * x * (p[2] - p[0] + x * (2.0 * p[0] - 5.0 * p[1] + 4.0 * p[2] - p[3] + x * (3.0 * (p[1] - p[2]) + p[3] - p[0])))

    def saved_image(self, text):
        if not self.image_path:
            showerror("Ошибка", "Сначала загрузите изображение")
            return
        try:
            directory = os.path.dirname(self.image_path)
            filename = os.path.basename(self.image_path)
            name, ext = os.path.splitext(filename)
            output_filename = f"{name}_{text}.png"
            output_path = os.path.join(directory, output_filename)
            counter = 1
            while os.path.exists(output_path):
                output_filename = f"{name}_{text}_{counter}.png"
                output_path = os.path.join(directory, output_filename)
                counter += 1
            png_points = getattr(self, f"{text}_png_points", None)
            self.write_png_from_points(png_points, output_path)
        except Exception as e:
            showerror("Ошибка", f"Не удалось сохранить изображение: {str(e)}")

    def write_png_from_points(self, png_points, filename):
        try:
            if not png_points:
                return False
                
            height = len(png_points)
            width = len(png_points[0]) if height > 0 else 0
            
            if width == 0 or height == 0:
                return False

            with open(filename, 'wb') as file:
                file.write(b'\x89PNG\r\n\x1a\n')
                ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
                ihdr_length = struct.pack('>I', 13)
                ihdr_type = b'IHDR'
                ihdr_crc = struct.pack('>I', zlib.crc32(ihdr_type + ihdr_data))
                file.write(ihdr_length)
                file.write(ihdr_type)
                file.write(ihdr_data)
                file.write(ihdr_crc)
                raw_data = bytearray()
                for i in range(height):
                    raw_data.append(0)
                    for j in range(width):
                        hex_color =  png_points[i][j][0]
                        hex_color = hex_color[1:]
                        r = int(hex_color[0:2], 16)
                        g = int(hex_color[2:4], 16)
                        b = int(hex_color[4:6], 16)
                        raw_data.append(r)
                        raw_data.append(g)
                        raw_data.append(b)
                compressed = zlib.compress(bytes(raw_data))
                idat_length = struct.pack('>I', len(compressed))
                idat_type = b'IDAT'
                idat_crc = struct.pack('>I', zlib.crc32(idat_type + compressed))
                file.write(idat_length)
                file.write(idat_type)
                file.write(compressed)
                file.write(idat_crc)
                iend_length = struct.pack('>I', 0)
                iend_type = b'IEND'
                iend_crc = struct.pack('>I', zlib.crc32(iend_type))
                file.write(iend_length)
                file.write(iend_type)
                file.write(iend_crc)
            return True
        except Exception as e:
            print(f"Ошибка при создании PNG: {e}")
            return False

window = Window("Обработчик изображений")
window.run()