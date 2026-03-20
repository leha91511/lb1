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
        self.afin_png_points = None
        self.repl_png_points = None
        self.func_png_points = None
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
        #афинное изображение
        self.button_afin_image = Button(self.root, text = "Афинное преобразование", command = self.afin_transform)
        self.button_afin_image.place(relx = 0.5, rely = 0.005, relwidth = 0.12, relheight = 0.05)
        self.frame_afin_image = Frame(self.root)
        self.frame_afin_image.place(relx = 0.5, rely = 0.06, relwidth = 0.49, relheight = 0.44)
        self.canvas_afin_image = self.create_canvas(self.frame_afin_image)
        self.label_afin = Label(self.root, text = "Выберите угол наклона")
        self.label_afin.place(relx = 0.62, rely = 0.005, relwidth = 0.11, relheight = 0.025)
        self.angle_afin = Spinbox(self.root, from_ = -360, to = 360, width = 10, font = "Calibri")
        self.angle_afin.place(relx = 0.67, rely = 0.03, relwidth = 0.05, relheight = 0.025)
        self.label_afin = Label(self.root, text = "Выберите смещение по x")
        self.label_afin.place(relx = 0.74, rely = 0.005, relwidth = 0.11, relheight = 0.025)
        self.x_afin = Spinbox(self.root, from_ = -1000, to = 1000, width = 10, font = "Calibri")
        self.x_afin.place(relx = 0.85, rely = 0.005, relwidth = 0.05, relheight = 0.025)
        self.label_afin = Label(self.root, text = "Выберите смещение по y")
        self.label_afin.place(relx = 0.74, rely = 0.03, relwidth = 0.11, relheight = 0.025)
        self.y_afin = Spinbox(self.root, from_ = -1000, to = 1000, width = 10, font = "Calibri")
        self.y_afin.place(relx = 0.85, rely = 0.03, relwidth = 0.05, relheight = 0.025)
        self.button_saved_afin_image = Button(self.root, text = "Сохранить", command = lambda: self.saved_image('afin'))
        self.button_saved_afin_image.place(relx = 0.905, rely = 0.005, relwidth = 0.06, relheight = 0.05)
        #восстановленное изображение
        self.button_repl_image = Button(self.root, text = "Обратное преобразование", command = self.replicate_afin_transform)
        self.button_repl_image.place(relx = 0.005, rely = 0.5, relwidth = 0.2, relheight = 0.05)
        self.frame_repl_image = Frame(self.root)
        self.frame_repl_image.place(relx = 0.005, rely = 0.55, relwidth = 0.49, relheight = 0.44)
        self.canvas_repl_image = self.create_canvas(self.frame_repl_image)
        self.button_saved_repl_image = Button(self.root, text = "Сохранить", command = lambda: self.saved_image('repl'))
        self.button_saved_repl_image.place(relx = 0.21, rely = 0.5, relwidth = 0.15, relheight = 0.05)
        #функциональное преобразование
        self.button_func_image = Button(self.root, text = "Функциональное преобразование", command = self.func_transform)
        self.button_func_image.place(relx = 0.5, rely = 0.5, relwidth = 0.2, relheight = 0.05)
        self.frame_func_image = Frame(self.root)
        self.frame_func_image.place(relx = 0.5, rely = 0.55, relwidth = 0.49, relheight = 0.44)
        self.canvas_func_image = self.create_canvas(self.frame_func_image)
        self.button_saved_func_image = Button(self.root, text = "Сохранить", command = lambda: self.saved_image('func'))
        self.button_saved_func_image.place(relx = 0.71, rely = 0.5, relwidth = 0.15, relheight = 0.05)

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

    def afin_transform(self):
        if not self.orig_png_points:
            showerror("Ошибка", "Сначала выберите изображение")
            return
        try:
            if not self.x_afin.get() or not self.y_afin.get() or not self.angle_afin.get():
                showerror("Ошибка", "Введите значения во все поля")
                return
            dx = float(self.x_afin.get())
            dy = float(self.y_afin.get())
            angle = math.radians(float(self.angle_afin.get()))
            self.dx, self.dy, self.angle = dx, dy, angle
            cos_fi = math.cos(angle)
            sin_fi = math.sin(angle)
            transitional_massive = []
            min_x = 0
            min_y = 0
            max_x = 0
            max_y = 0
            for line in self.orig_png_points:
                row = []
                for color, (px, py) in line:
                    new_x = cos_fi * px + -sin_fi * py + dx
                    new_y = sin_fi * px + cos_fi * py + dy
                    new_x = int(round(new_x))
                    new_y = int(round(new_y))
                    min_x = min(min_x, new_x)
                    min_y = min(min_y, new_y)
                    max_x = max(max_x, new_x)
                    max_y = max(max_y, new_y)
                    row.append((color, (new_x, new_y)))
                transitional_massive.append(row)
            self.afin_png_points = []
            height = max_y - min_y + 1
            width = max_x - min_x + 1
            for y in range(height):
                row = []
                for x in range(width):
                    orig_x = x + min_x
                    orig_y = y + min_y
                    row.append(("#ffffff", (orig_x, orig_y)))
                self.afin_png_points.append(row)
            for line in transitional_massive:
                for color, (x, y) in line:
                    array_x = x - min_x
                    array_y = y - min_y
                    if 0 <= array_y < height and 0 <= array_x < width:
                        self.afin_png_points[array_y][array_x] = (color, (x, y))
            self.display_image(self.canvas_afin_image, self.afin_png_points)
        except Exception as e:
            showerror("Ошибка", f"Ошибка при аффинном преобразовании: {str(e)}")

    def replicate_afin_transform(self):
        if not self.afin_png_points:
            showerror("Ошибка", "Нет афинного изображения")
            return
        try:
            dx = self.dx
            dy = self.dy
            angle = self.angle
            cos_fi = math.cos(angle)
            sin_fi = math.sin(angle)
            transitional_massive = []
            min_x = 0
            min_y = 0
            max_x = 0
            max_y = 0
            for line in self.afin_png_points:
                row = []
                for color, (px, py) in line:
                    if color == "#ffffff" or color == "#FFFFFF":
                        continue
                    new_x = cos_fi * px + sin_fi * py - sin_fi * dy - cos_fi * dx
                    new_y = - sin_fi * px + cos_fi * py - cos_fi * dy + sin_fi * dx
                    new_x = int(round(new_x))
                    new_y = int(round(new_y))
                    min_x = min(min_x, new_x)
                    min_y = min(min_y, new_y)
                    max_x = max(max_x, new_x)
                    max_y = max(max_y, new_y)
                    row.append((color, (new_x, new_y)))
                transitional_massive.append(row)
            self.repl_png_points = []
            height = max_y - min_y + 1
            width = max_x - min_x + 1
            for y in range(height):
                row = []
                for x in range(width):
                    orig_x = x + min_x
                    orig_y = y + min_y
                    row.append(("#ffffff", (orig_x, orig_y)))
                self.repl_png_points.append(row)
            for line in transitional_massive:
                for color, (x, y) in line:
                    array_x = x - min_x
                    array_y = y - min_y
                    if 0 <= array_y < height and 0 <= array_x < width:
                        self.repl_png_points[array_y][array_x] = (color, (x, y))
            self.display_image(self.canvas_repl_image, self.repl_png_points)
        except Exception as e:
            showerror("Ошибка", f"Ошибка при обратном аффинном преобразовании: {str(e)}")

    def func_transform(self):
        if not self.orig_png_points:
            showerror("Ошибка", "Сначала выберите изображение")
            return
        try:
            transitional_massive = []
            max_x = 0
            max_y = 0
            for line in self.orig_png_points:
                row = []
                for color, (px, py) in line:
                    new_x = px ** (3 / 7)
                    new_x = int(round(new_x))
                    max_x = max(max_x, new_x)
                    max_y = py
                    row.append((color, (new_x, py)))
                transitional_massive.append(row)
            self.func_png_points = []
            width = max_x + 1
            height = max_y + 1
            for y in range(height):
                row = []
                for x in range(width):
                    row.append(("#ffffff", (x, y)))
                self.func_png_points.append(row)
            for line in transitional_massive:
                for color, (x, y) in line:
                    self.func_png_points[y][x] = (color, (x, y))
            self.display_image(self.canvas_func_image, self.func_png_points)
        except Exception as e:
            showerror("Ошибка", f"Ошибка при функциональном преобразовании: {str(e)}")

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