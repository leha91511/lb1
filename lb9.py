from tkinter import *
from tkinter import PhotoImage
from tkinter.ttk import *
from tkinter.filedialog import *
from tkinter.messagebox import *
import os, struct, zlib
import math
import random

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
        self.segments = None
        self.Sutherland_Cohen_png_points = None
        self.middle_point_png_points = None
        self.simple_clipping_png_points = None
        self.widgets()
        self.root.after(200, self.check_and_create_default_image)
    
    def window_center(self, x, y, window_x, window_y):
        x = (x - window_x) // 2
        y = (y - window_y) // 2
        return x, y

    def widgets(self):
        self.button_exit = Button(self.root, text = "X", command = self.root.destroy)
        self.button_exit.place(relx = 0.97, rely = 0.005, relwidth = 0.025, relheight = 0.05)
        #кнопки и подписи
        self.label_pos = Label(self.root, text = "выберите центр для отсечения:")
        self.label_pos.place(relx = 0.01, rely = 0.005)
        self.label_x = Label(self.root, text = "x")
        self.label_x.place(relx = 0.14, rely = 0.005)
        self.x_point = Spinbox(self.root, from_ = 0, to = 400, increment = 1, width = 5, font = "Calibri")
        self.x_point.place(relx = 0.15, rely = 0.005, relwidth = 0.05, relheight = 0.025)
        self.label_x = Label(self.root, text = "y")
        self.label_x.place(relx = 0.2, rely = 0.005)
        self.y_point = Spinbox(self.root, from_ = 0, to = 500, increment = 1, width = 5, font = "Calibri")
        self.y_point.place(relx = 0.21, rely = 0.005, relwidth = 0.05, relheight = 0.025)
        self.label_select = Label(self.root, text = "Выберите кол-во отрезков (N):")
        self.label_select.place(relx = 0.01, rely = 0.03)
        self.spinbox_select = Spinbox(self.root, from_ = 1, to = 20, increment = 1, width = 5, font = "Calibri")
        self.spinbox_select.place(relx = 0.15, rely = 0.03, relwidth = 0.05, relheight = 0.025)
        self.label_square = Label(self.root, text = "выберите размеры для отсечения:")
        self.label_square.place(relx = 0.26, rely = 0.005)
        self.label_a = Label(self.root, text = "a")
        self.label_a.place(relx = 0.4, rely = 0.005)
        self.a_len = Spinbox(self.root, from_ = 1, to = 400, increment = 1, width = 5, font = "Calibri")
        self.a_len.place(relx = 0.41, rely = 0.005, relwidth = 0.05, relheight = 0.025)
        self.label_a = Label(self.root, text = "b")
        self.label_a.place(relx = 0.4, rely = 0.03)
        self.b_len = Spinbox(self.root, from_ = 1, to = 500, increment = 1, width = 5, font = "Calibri")
        self.b_len.place(relx = 0.41, rely = 0.03, relwidth = 0.05, relheight = 0.025)
        self.button_rand_gen = Button(self.root, text = "Сгенерировать N отрезков", command = self.segment_generat)
        self.button_rand_gen.place(relx = 0.46, rely = 0.005, relwidth = 0.15, relheight = 0.05)
        self.x_point.set(0)
        self.y_point.set(0)
        self.a_len.set(1)
        self.b_len.set(1)
        self.spinbox_select.set(1)
        self.button_clipping = Button(self.root, text = "Отсечь", command = self.clipping_all)
        self.button_clipping.place(relx = 0.61, rely = 0.005, relwidth = 0.15, relheight = 0.05)
        self.button_saved_all = Button(self.root, text = "Сохранить результат", command = self.saved_image_all)
        self.button_saved_all.place(relx = 0.76, rely = 0.005, relwidth = 0.15, relheight = 0.05)
        #оригиналное изображение
        self.frame_orig_image = Frame(self.root)
        self.frame_orig_image.place(relx = 0.005, rely = 0.06, relwidth = 0.49, relheight = 0.46)
        self.canvas_orig_image = self.create_canvas(self.frame_orig_image)
        #алгоритм Сазерленда-Коэна
        self.frame_Sutherland_Cohen_image = Frame(self.root)
        self.frame_Sutherland_Cohen_image.place(relx = 0.5, rely = 0.06, relwidth = 0.49, relheight = 0.46)
        self.canvas_Sutherland_Cohen_image = self.create_canvas(self.frame_Sutherland_Cohen_image)
        #алгоритм разбиения средней точкой
        self.frame_middle_point_image = Frame(self.root)
        self.frame_middle_point_image.place(relx = 0.005, rely = 0.53, relwidth = 0.49, relheight = 0.46)
        self.canvas_middle_point_image = self.create_canvas(self.frame_middle_point_image)
        #простой алгоритм отсечение
        self.frame_simple_clipping_image = Frame(self.root)
        self.frame_simple_clipping_image.place(relx = 0.5, rely = 0.53, relwidth = 0.49, relheight = 0.46)
        self.canvas_simple_clipping_image = self.create_canvas(self.frame_simple_clipping_image)
    
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
                    if self.segments:
                        self.draw_segments_on_original()
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
            margin = max(self.orig_img_width, self.orig_img_height) // 2
            canvas.config(scrollregion = (-margin, -margin, self.orig_img_width + margin, self.orig_img_height + margin))
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

    def check_and_create_default_image(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        default_path = os.path.join(script_dir, "nothing.png")
        if not os.path.exists(default_path):
            try:
                white_points = []
                for y in range(500):
                    row = []
                    for x in range(400):
                        row.append(("#aaaaaa", (x, y)))
                    white_points.append(row)
                self.write_png_from_points(white_points, default_path)
                print(f"Создан файл: {default_path}")
            except Exception as e:
                print(f"Ошибка при создании файла: {str(e)}")
                showerror("Ошибка", f"Не удалось создать изображение: {str(e)}")
                return
        self.image_path = default_path
        try:
            self.photo_image = PhotoImage(file=default_path)
            self.orig_img_width = self.photo_image.width()
            self.orig_img_height = self.photo_image.height()
            self.orig_png_points = self.getPixelArray()
            self.display_image(self.canvas_orig_image, self.orig_png_points)
            if self.segments:
                self.draw_segments_on_original()
        except Exception as e:
            print(f"Ошибка при загрузке nothing.png: {str(e)}")
            showerror("Ошибка", f"Не удалось загрузить изображение: {str(e)}")

    def get_clipping_window(self):
        try:
            center_x = int(self.x_point.get())
            center_y = int(self.y_point.get())
            half_width = int(self.a_len.get()) // 2
            half_height = int(self.b_len.get()) // 2
            x1 = center_x - half_width
            y1 = center_y - half_height
            x2 = center_x + half_width
            y2 = center_y + half_height
            x1 = max(0, min(400, x1))
            y1 = max(0, min(500, y1))
            x2 = max(0, min(400, x2))
            y2 = max(0, min(500, y2))
        
            return x1, y1, x2, y2
        except Exception as e:
            print(f"Ошибка при получении окна отсечения: {e}")
            return 150, 200, 250, 300

    def segment_generat(self):
        try:
            n = int(self.spinbox_select.get())
            segments = []
            for _ in range(n):
                x1 = round(random.uniform(-0.5, 1.5), 5)
                y1 = round(random.uniform(-0.5, 1.5), 5)
                x2 = round(random.uniform(-0.5, 1.5), 5)
                y2 = round(random.uniform(-0.5, 1.5), 5)
                segments.append((x1, y1, x2, y2))
            self.segments = segments
            if hasattr(self, 'orig_img_width') and hasattr(self, 'orig_img_height'):
                self.display_image(self.canvas_orig_image, self.orig_png_points)
                self.draw_segments_on_original()
        except Exception as e:
            showerror("Ошибка", f"Не удалось сгенерировать отрезки: {str(e)}")

    def draw_segments_on_original(self):
        if not hasattr(self, 'orig_img_width') or not hasattr(self, 'orig_img_height'):
            return
        x1, y1, x2, y2 = self.get_clipping_window()
        self.canvas_orig_image.create_rectangle(x1, y1, x2, y2, outline="blue", width=2)
        if self.segments:
            for x1, y1, x2, y2 in self.segments:
                px1 = int(x1 * self.orig_img_width)
                py1 = int(y1 * self.orig_img_height)
                px2 = int(x2 * self.orig_img_width)
                py2 = int(y2 * self.orig_img_height)
                self.canvas_orig_image.create_line(px1, py1, px2, py2, fill="red", width=2)

    def validate_window(self):
        try:
            x = int(self.x_point.get())
            y = int(self.y_point.get())
            a = int(self.a_len.get())
            b = int(self.b_len.get())
            half_a = a / 2
            half_b = b / 2
            if x - half_a < 0:
                showerror("Ошибка", f"Окно отсечения выходит за левую границу!\n" f"При x={x}, a={a} левая граница = {x - half_a}")
                return False
            if x + half_a > 400:
                showerror("Ошибка", f"Окно отсечения выходит за правую границу!\n" f"При x={x}, a={a} правая граница = {x + half_a}")
                return False
            if y - half_b < 0:
                showerror("Ошибка", f"Окно отсечения выходит за верхнюю границу!\n"f"При y={y}, b={b} верхняя граница = {y - half_b}")
                return False
            if y + half_b > 500:
                showerror("Ошибка", f"Окно отсечения выходит за нижнюю границу!\n"f"При y={y}, b={b} нижняя граница = {y + half_b}")
                return False
            return True
        except Exception as e:
            showerror("Ошибка", f"Ошибка при проверке окна: {e}")
            return False

    def clipping_all(self):
        if not hasattr(self, 'orig_img_width') or not hasattr(self, 'orig_img_height'):
            showerror("Ошибка", "Сначала выберите изображение")
            return
        if not self.segments:
            showerror("Ошибка", "Сначала сгенерируйте отрезки")
            return
        if not self.validate_window():
            return
        self.root.update()
        self.Sutherland_Cohen()
        self.root.update()
        self.middle_point()
        self.root.update()
        self.simple_clipping()

    def draw_line_to_points(self, points_array, x1, y1, x2, y2, color_rgb):
        x1 = int(round(x1))
        y1 = int(round(y1))
        x2 = int(round(x2))
        y2 = int(round(y2))
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy
        while True:
            if 0 <= x1 < self.orig_img_width and 0 <= y1 < self.orig_img_height:
                r, g, b = color_rgb
                hex_color = f"#{r:02x}{g:02x}{b:02x}"
                points_array[y1][x1] = (hex_color, (x1, y1))
            if x1 == x2 and y1 == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

    def compute_code(self, x, y, x_min, y_min, x_max, y_max):
        code = 0
        if x < x_min:
            code |= 1
        elif x > x_max:
            code |= 2
        if y < y_min:
            code |= 4
        elif y > y_max:
            code |= 8
        return code

    def Sutherland_Cohen(self):
        x_min, y_min, x_max, y_max = self.get_clipping_window()
        self.display_image(self.canvas_Sutherland_Cohen_image, self.orig_png_points)
        self.Sutherland_Cohen_png_points = []
        for y in range(self.orig_img_height):
            row = []
            for x in range(self.orig_img_width):
                row.append(("#ffffff", (x, y)))
            self.Sutherland_Cohen_png_points.append(row)
        for x1_norm, y1_norm, x2_norm, y2_norm in self.segments:
            x1 = int(x1_norm * self.orig_img_width)
            y1 = int(y1_norm * self.orig_img_height)
            x2 = int(x2_norm * self.orig_img_width)
            y2 = int(y2_norm * self.orig_img_height)
            code1 = self.compute_code(x1, y1, x_min, y_min, x_max, y_max)
            code2 = self.compute_code(x2, y2, x_min, y_min, x_max, y_max)
            while True:
                if code1 == 0 and code2 == 0:
                    self.canvas_Sutherland_Cohen_image.create_line(x1, y1, x2, y2, fill="green", width=2)
                    self.draw_line_to_points(self.Sutherland_Cohen_png_points, x1, y1, x2, y2, (0, 255, 0))
                    break
                if code1 & code2 != 0:
                    break
                if code1 != 0:
                    code = code1
                    x_out, y_out = x1, y1
                else:
                    code = code2
                    x_out, y_out = x2, y2
                if code & 1:
                    x_int = x_min
                    y_int = y1 + (y2 - y1) * (x_min - x1) / (x2 - x1) if (x2 - x1) != 0 else y1
                elif code & 2:
                    x_int = x_max
                    y_int = y1 + (y2 - y1) * (x_max - x1) / (x2 - x1) if (x2 - x1) != 0 else y1
                elif code & 4:
                    y_int = y_min
                    x_int = x1 + (x2 - x1) * (y_min - y1) / (y2 - y1) if (y2 - y1) != 0 else x1
                elif code & 8:
                    y_int = y_max
                    x_int = x1 + (x2 - x1) * (y_max - y1) / (y2 - y1) if (y2 - y1) != 0 else x1
                x_int = int(x_int)
                y_int = int(y_int)
                if code == code1:
                    x1, y1 = x_int, y_int
                    code1 = self.compute_code(x1, y1, x_min, y_min, x_max, y_max)
                else:
                    x2, y2 = x_int, y_int
                    code2 = self.compute_code(x2, y2, x_min, y_min, x_max, y_max)

    def middle_point(self):
        x_min, y_min, x_max, y_max = self.get_clipping_window()
        self.middle_point_png_points = []
        for y in range(self.orig_img_height):
            row = []
            for x in range(self.orig_img_width):
                row.append(("#ffffff", (x, y)))
            self.middle_point_png_points.append(row)
        recursion_depth = 0
        MAX_DEPTH = 100
        def midpoint_clip(x1, y1, x2, y2, eps=1.0):
            nonlocal recursion_depth
            recursion_depth += 1
            if recursion_depth > MAX_DEPTH:
                recursion_depth = 0
                return []
            code1 = self.compute_code(x1, y1, x_min, y_min, x_max, y_max)
            code2 = self.compute_code(x2, y2, x_min, y_min, x_max, y_max)
            if code1 == 0 and code2 == 0:
                return [(x1, y1, x2, y2)]
            if code1 & code2 != 0:
                return []
            if abs(x2 - x1) < eps and abs(y2 - y1) < eps:
                if code1 == 0:
                    return [(x1, y1, x2, y2)]
                elif code2 == 0:
                    return [(x1, y1, x2, y2)]
                else:
                    return []
            xm = (x1 + x2) / 2
            ym = (y1 + y2) / 2
            left_part = midpoint_clip(x1, y1, xm, ym, eps)
            right_part = midpoint_clip(xm, ym, x2, y2, eps)
            return left_part + right_part
        self.display_image(self.canvas_middle_point_image, self.orig_png_points)
        for x1_norm, y1_norm, x2_norm, y2_norm in self.segments:
            x1 = int(x1_norm * self.orig_img_width)
            y1 = int(y1_norm * self.orig_img_height)
            x2 = int(x2_norm * self.orig_img_width)
            y2 = int(y2_norm * self.orig_img_height)
            clipped_parts = midpoint_clip(x1, y1, x2, y2)
            for x1c, y1c, x2c, y2c in clipped_parts:
                self.canvas_middle_point_image.create_line(x1c, y1c, x2c, y2c, fill="green", width=2)
                self.draw_line_to_points(self.middle_point_png_points, x1c, y1c, x2c, y2c, (0, 255, 0))

    def simple_clipping(self):
        x_min, y_min, x_max, y_max = self.get_clipping_window()
        self.display_image(self.canvas_simple_clipping_image, self.orig_png_points)
        self.simple_clipping_png_points = []
        for y in range(self.orig_img_height):
            row = []
            for x in range(self.orig_img_width):
                row.append(("#ffffff", (x, y)))
            self.simple_clipping_png_points.append(row)
        for x1_norm, y1_norm, x2_norm, y2_norm in self.segments:
            x1 = int(x1_norm * self.orig_img_width)
            y1 = int(y1_norm * self.orig_img_height)
            x2 = int(x2_norm * self.orig_img_width)
            y2 = int(y2_norm * self.orig_img_height)
            def point_inside(x, y):
                return x_min <= x <= x_max and y_min <= y <= y_max
            p1_inside = point_inside(x1, y1)
            p2_inside = point_inside(x2, y2)
            if p1_inside and p2_inside:
                self.canvas_simple_clipping_image.create_line(x1, y1, x2, y2, fill="green", width=2)
                self.draw_line_to_points(self.simple_clipping_png_points, x1, y1, x2, y2, (0, 255, 0))
                continue
            if not p1_inside and not p2_inside:
                def line_intersects(x1, y1, x2, y2):
                    intersections = []
                    if x2 != x1:
                        t = (x_min - x1) / (x2 - x1)
                        if 0 <= t <= 1:
                            y_int = y1 + t * (y2 - y1)
                            if y_min <= y_int <= y_max:
                                intersections.append((x_min, y_int))
                    if x2 != x1:
                        t = (x_max - x1) / (x2 - x1)
                        if 0 <= t <= 1:
                            y_int = y1 + t * (y2 - y1)
                            if y_min <= y_int <= y_max:
                                intersections.append((x_max, y_int))
                    if y2 != y1:
                        t = (y_min - y1) / (y2 - y1)
                        if 0 <= t <= 1:
                            x_int = x1 + t * (x2 - x1)
                            if x_min <= x_int <= x_max:
                                intersections.append((x_int, y_min))
                    if y2 != y1:
                        t = (y_max - y1) / (y2 - y1)
                        if 0 <= t <= 1:
                            x_int = x1 + t * (x2 - x1)
                            if x_min <= x_int <= x_max:
                                intersections.append((x_int, y_max))
                    return intersections
                intersections = line_intersects(x1, y1, x2, y2)
                if len(intersections) >= 2:
                    def dist_from_start(x, y):
                        return ((x - x1)**2 + (y - y1)**2)**0.5
                    intersections.sort(key=lambda p: dist_from_start(p[0], p[1]))
                    ix1, iy1 = intersections[0]
                    ix2, iy2 = intersections[1]
                    self.canvas_simple_clipping_image.create_line(ix1, iy1, ix2, iy2, fill="green", width=2)
                    self.draw_line_to_points(self.simple_clipping_png_points, ix1, iy1, ix2, iy2, (0, 255, 0))
                continue
            if p1_inside and not p2_inside:
                intersections = []
                if x2 != x1:
                    t = (x_min - x1) / (x2 - x1)
                    if 0 <= t <= 1:
                        y_int = y1 + t * (y2 - y1)
                        if y_min <= y_int <= y_max:
                            intersections.append((x_min, y_int))
                if x2 != x1:
                    t = (x_max - x1) / (x2 - x1)
                    if 0 <= t <= 1:
                        y_int = y1 + t * (y2 - y1)
                        if y_min <= y_int <= y_max:
                            intersections.append((x_max, y_int))
                if y2 != y1:
                    t = (y_min - y1) / (y2 - y1)
                    if 0 <= t <= 1:
                        x_int = x1 + t * (x2 - x1)
                        if x_min <= x_int <= x_max:
                            intersections.append((x_int, y_min))
                if y2 != y1:
                    t = (y_max - y1) / (y2 - y1)
                    if 0 <= t <= 1:
                        x_int = x1 + t * (x2 - x1)
                        if x_min <= x_int <= x_max:
                            intersections.append((x_int, y_max))
                if intersections:
                    ix, iy = intersections[0]
                    self.canvas_simple_clipping_image.create_line(x1, y1, ix, iy, fill="green", width=2)
                    self.draw_line_to_points(self.simple_clipping_png_points, x1, y1, ix, iy, (0, 255, 0))
        
            if not p1_inside and p2_inside:
                intersections = []
                if x2 != x1:
                    t = (x_min - x1) / (x2 - x1)
                    if 0 <= t <= 1:
                        y_int = y1 + t * (y2 - y1)
                        if y_min <= y_int <= y_max:
                            intersections.append((x_min, y_int))
                if x2 != x1:
                    t = (x_max - x1) / (x2 - x1)
                    if 0 <= t <= 1:
                        y_int = y1 + t * (y2 - y1)
                        if y_min <= y_int <= y_max:
                            intersections.append((x_max, y_int))
                if y2 != y1:
                    t = (y_min - y1) / (y2 - y1)
                    if 0 <= t <= 1:
                        x_int = x1 + t * (x2 - x1)
                        if x_min <= x_int <= x_max:
                            intersections.append((x_int, y_min))
                if y2 != y1:
                    t = (y_max - y1) / (y2 - y1)
                    if 0 <= t <= 1:
                        x_int = x1 + t * (x2 - x1)
                        if x_min <= x_int <= x_max:
                            intersections.append((x_int, y_max))
                if intersections:
                    ix, iy = intersections[0]
                    self.canvas_simple_clipping_image.create_line(ix, iy, x2, y2,fill="green", width=2)
                    self.draw_line_to_points(self.simple_clipping_png_points, ix, iy, x2, y2, (0, 255, 0))

    def saved_image_all(self):
        self.saved_image("Sutherland_Cohen")
        self.saved_image("middle_point")
        self.saved_image("simple_clipping")

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