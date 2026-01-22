from tkinter import *
from tkinter import PhotoImage
from tkinter.ttk import *
from tkinter.filedialog import *
from tkinter.messagebox import *
import os, struct, zlib, math

class Window:
    def __init__(self, title):
        self.root = Tk()
        self.root.title(title)
        screen_x = self.root.winfo_screenwidth()
        screen_y = self.root.winfo_screenheight()
        x, y = self.window_center(screen_x, screen_y)
        self.root.geometry(f"800x500+{x}+{y}")
        self.root.resizable(False, False)
        self.root.overrideredirect(True)
        self.image_path = None
        self.photo_image = None
        self.png_points1 = None
        self.png_points2 = None
        self.png_points3 = None
        self.png_points4 = None
        self.widgets()
        self.root.update()
    
    def window_center(self, x, y):
        x = (x-800)//2
        y = (y-500)//2
        return x, y

    def widgets(self):
        self.enrty1 = Entry(self.root)
        self.enrty1.place(relx = 0.04, rely = 0.04, relwidth = 0.05, relheight = 0.045)
        self.label1 = Label(self.root, text = "a")
        self.label1.place(relx = 0.01, rely = 0.04)
        self.button1 = Button(self.root, text = "Создать", command = self.create_octagon)
        self.button1.place(relx = 0.1, rely = 0.01, relwidth = 0.4, relheight = 0.1)
        self.button2 = Button(self.root, text = "Сохранить", command = self.saved_image)
        self.button2.place(relx = 0.55, rely = 0.01, relwidth = 0.4, relheight = 0.1)
        self.close_button = Button(self.root, text = "X", command = self.root.destroy)
        self.close_button.place(relx = 0.96, rely = 0.01, relwidth = 0.03, relheight = 0.05)
        self.canvas1 = Canvas(self.root, bg = "lightgray")
        self.canvas1.place(relx = 0.005, rely = 0.12, relwidth = 0.49, relheight = 0.43, anchor = "nw")
        self.canvas2 = Canvas(self.root, bg = "lightgray")
        self.canvas2.place(relx = 0.005, rely = 0.995, relwidth = 0.49, relheight = 0.43, anchor = "sw")
        self.canvas3 = Canvas(self.root, bg = "lightgray")
        self.canvas3.place(relx = 0.995, rely = 0.12, relwidth = 0.49, relheight = 0.43, anchor = "ne")
        self.canvas4 = Canvas(self.root, bg = "lightgray")
        self.canvas4.place(relx = 0.995, rely = 0.995, relwidth = 0.49, relheight = 0.43, anchor = "se")
    
    def run(self):
        self.root.mainloop()

    def create_octagon(self):
        self.canvas1.delete("all")
        self.canvas2.delete("all")
        self.canvas3.delete("all")
        self.canvas4.delete("all")
        self.png_points1 = None
        self.png_points2 = None
        self.png_points3 = None
        self.png_points4 = None
        try:
            a = float(self.enrty1.get())
            if a <= 0:
                showerror("введите корректное число")
                return
            canvas_width = self.canvas1.winfo_width()
            canvas_height = self.canvas1.winfo_height()
            r = a / (2 * math.tan(math.pi/8))
            R = a / (2 * math.sin(math.pi/8))
            self.png_points1 = [[{} for _ in range(canvas_width)] for _ in range(canvas_height)]
            self.png_points2 = [[{} for _ in range(canvas_width)] for _ in range(canvas_height)]
            self.png_points3 = [[{} for _ in range(canvas_width)] for _ in range(canvas_height)]
            self.png_points4 = [[{} for _ in range(canvas_width)] for _ in range(canvas_height)]
            for i in range(canvas_height):
                for j in range(canvas_width):
                    self.png_points1[i][j] = {1: "lightgray"}
                    self.png_points2[i][j] = {1: "lightgray"}
                    self.png_points3[i][j] = {1: "lightgray"}
                    self.png_points4[i][j] = {1: "lightgray"}
            self.create_octagons(R)
            self.equation_circle(r, "red"), self.equation_circle(R, "blue")
            self.parametric_circle(r, "red"), self.parametric_circle(R, "blue")
            self.Brezenham_circle(r, "red"), self.Brezenham_circle(R, "blue")
            self.built_in_circle(r, "red"), self.built_in_circle(R, "blue")
        except ValueError:
            showerror("введите корректное число")
            return
    
    def create_octagons(self, R):
        canvas_width = self.canvas1.winfo_width()
        canvas_height = self.canvas1.winfo_height()
        center_x = canvas_width // 2
        center_y = canvas_height // 2
        x1, x2 = center_x + R * math.cos(math.pi/8 + 1 * math.pi/4), center_x + R * math.cos(math.pi/8 + 2 * math.pi/4)
        x3, x4 = center_x + R * math.cos(math.pi/8 + 3 * math.pi/4), center_x + R * math.cos(math.pi/8 + 4 * math.pi/4)
        x5, x6 = center_x + R * math.cos(math.pi/8 + 5 * math.pi/4), center_x + R * math.cos(math.pi/8 + 6 * math.pi/4)
        x7, x8 = center_x + R * math.cos(math.pi/8 + 7 * math.pi/4), center_x + R * math.cos(math.pi/8 + 8 * math.pi/4)
        y1, y2 = center_y + R * math.sin(math.pi/8 + 1 * math.pi/4), center_y + R * math.sin(math.pi/8 + 2 * math.pi/4)
        y3, y4 = center_y + R * math.sin(math.pi/8 + 3 * math.pi/4), center_y + R * math.sin(math.pi/8 + 4 * math.pi/4)
        y5, y6 = center_y + R * math.sin(math.pi/8 + 5 * math.pi/4), center_y + R * math.sin(math.pi/8 + 6 * math.pi/4)
        y7, y8 = center_y + R * math.sin(math.pi/8 + 7 * math.pi/4), center_y + R * math.sin(math.pi/8 + 8 * math.pi/4)
        points = [x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6, x7, y7, x8, y8]
        self.canvas1.create_polygon(points, outline = "black", fill = "lightgray")
        self.canvas2.create_polygon(points, outline = "black", fill = "lightgray")
        self.canvas3.create_polygon(points, outline = "black", fill = "lightgray")
        self.canvas4.create_polygon(points, outline = "black", fill = "lightgray")
        self.raster_lines(*points[0:4], "black"), self.raster_lines(*points[2:6], "black"), self.raster_lines(*points[4:8], "black")
        self.raster_lines(*points[6:10], "black"), self.raster_lines(*points[8:12], "black"), self.raster_lines(*points[10:14], "black")
        self.raster_lines(*points[12:16], "black"), self.raster_lines(*points[14:16], *points[0:2], "black")

    def raster_lines(self, x1, y1, x2, y2, color):
        canvas_width = self.canvas1.winfo_width()
        canvas_height = self.canvas1.winfo_height()
        x1, y1, x2, y2 = int(round(x1)), int(round(y1)), int(round(x2)), int(round(y2))
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy
        while True:
            if 0 <= y1 < canvas_height and 0 <= x1 < canvas_width:
                self.png_points1[y1][x1] = {1: color}
                self.png_points2[y1][x1] = {1: color}
                self.png_points3[y1][x1] = {1: color}
                self.png_points4[y1][x1] = {1: color}
            if x1 == x2 and y1 == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

    def equation_circle(self, radius, color):
        canvas_width = self.canvas1.winfo_width()
        canvas_height = self.canvas1.winfo_height()
        center_x = canvas_width // 2
        center_y = canvas_height // 2
        for x in range(center_x - int(radius), center_x + int(radius) + 1):
            under = radius ** 2 - (x - center_x) ** 2
            if under >= 0:
                square_root = math.sqrt(under)
                y1 = center_y - square_root
                y2 = center_y + square_root
                self.canvas1.create_line(x, y1, x, y1 + 1, fill = color)
                self.canvas1.create_line(x, y2, x, y2 + 1, fill = color)
                if 0 <= y1 < canvas_height and 0 <= x < canvas_width:
                    self.png_points1[int(y1)][int(x)] = {1: color}
                if 0 <= y2 < canvas_height and 0 <= x < canvas_width:
                    self.png_points1[int(y2)][int(x)] = {1: color}
        for y in range(center_y - int(radius), center_y + int(radius) + 1):
            under = radius ** 2 - (y - center_y) ** 2
            if under >= 0:
                square_root = math.sqrt(under)
                x1 = center_x - square_root
                x2 = center_x + square_root
                self.canvas1.create_line(x1, y, x1 + 1, y, fill = color)
                self.canvas1.create_line(x2, y, x2 + 1, y, fill = color)
                if 0 <= y < canvas_height and 0 <= x1 < canvas_width:
                    self.png_points1[int(y)][int(x1)] = {1: color}
                if 0 <= y < canvas_height and 0 <= x2 < canvas_width:
                    self.png_points1[int(y)][int(x2)] = {1: color}

    def parametric_circle(self, radius, color):
        canvas_width = self.canvas1.winfo_width()
        canvas_height = self.canvas1.winfo_height()
        center_x = canvas_width // 2
        center_y = canvas_height // 2
        for i in range(361):
            t = 2 * math.pi * i / 360
            x = center_x + radius * math.cos(t)
            y = center_y - radius * math.sin(t)
            self.canvas2.create_line(x, y, x + 1, y, fill = color)
            if 0 <= y < canvas_height and 0 <= x < canvas_width:
                self.png_points2[int(y)][int(x)] = {1: color}
    
    def Brezenham_circle(self, radius, color):
        canvas_width = self.canvas1.winfo_width()
        canvas_height = self.canvas1.winfo_height()
        center_x = canvas_width // 2
        center_y = canvas_height // 2
        x = 0
        y = int(radius)
        d = 3 - 2 * radius
        while y >= x:
            points = [
            (center_x + x, center_y + y), (center_x - x, center_y + y),
            (center_x + x, center_y - y), (center_x - x, center_y - y),
            (center_x + y, center_y + x), (center_x - y, center_y + x),
            (center_x + y, center_y - x), (center_x - y, center_y - x)
            ]
            for px, py in points:
                self.canvas3.create_line(px, py, px + 1, py, fill = color)
                if 0 <= py < canvas_height and 0 <= px < canvas_width:
                    self.png_points3[int(py)][int(px)] = {1: color}
            x += 1
            if d > 0 :
                y -= 1
                d = d + 4 * (x - y) + 10
            else:
                d = d + 4 * x + 6
        
    def built_in_circle(self, radius, color):
        canvas_width = self.canvas1.winfo_width()
        canvas_height = self.canvas1.winfo_height()
        center_x = canvas_width // 2
        center_y = canvas_height // 2
        x1 = center_x - radius
        x2 = center_x + radius
        y1 = center_y - radius
        y2 = center_y + radius
        self.canvas4.create_oval(x1, y1, x2, y2, outline = color)
        for i in range(0, 1081, 1):
            t = 2 * math.pi * i / 1080
            x = int(center_x + radius * math.cos(t))
            y = int(center_y - radius * math.sin(t))
            if 0 <= y < canvas_height and 0 <= x < canvas_width:
                self.png_points4[y][x] = {1: color}

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
                        pixel_dict = png_points[i][j]
                        hex_color = pixel_dict.get(1, "lightgray")
                        if hex_color == "black":
                            r, g, b = 0, 0, 0
                        elif hex_color == "red":
                            r, g, b = 255, 0, 0
                        elif hex_color == "blue":
                            r, g, b = 0, 0, 255
                        else:
                            r, g, b = 211, 211, 211
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

    def saved_image(self):
        if not self.png_points1:
            showerror("Ошибка", "Сначала создайте ромб")
            return
        script_dir = os.path.dirname(os.path.abspath(__file__))
        save_dir = os.path.join(script_dir, "saved_octagons_and_her_circles")
        os.makedirs(save_dir, exist_ok=True)
        arrays = [
            (self.png_points1, "equation_circle"),
            (self.png_points2, "parametric_circle"),
            (self.png_points3, "Brezenhem_circle"),
            (self.png_points4, "Tkinter")
        ]
        saved_files = []
        for array, name in arrays:
            if array:
                filename = os.path.join(save_dir, f"rhomb_{name}.png")
                if self.write_png_from_points(array, filename):
                    saved_files.append(filename)
                else:
                    showerror("Ошибка", f"Не удалось сохранить {name}")
        if saved_files:
            showinfo("Успех", f"Сохранено {len(saved_files)} изображений в папку:\n{save_dir}")
        else:
            showerror("Ошибка", "Не удалось сохранить изображения")

window = Window("Обработчик изображений")
window.run()