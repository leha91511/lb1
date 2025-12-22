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
    
    def window_center(self, x, y):
        x = (x-800)//2
        y = (y-500)//2
        return x, y

    def widgets(self):
        self.enrty1 = Entry(self.root)
        self.enrty1.place(relx = 0.04, rely = 0.01, relwidth = 0.08, relheight = 0.045)
        self.label1 = Label(self.root, text = "x1")
        self.label1.place(relx = 0.01, rely = 0.01)
        self.enrty2 = Entry(self.root)
        self.enrty2.place(relx = 0.04, rely = 0.065, relwidth = 0.08, relheight = 0.045)
        self.label2 = Label(self.root, text = "y1")
        self.label2.place(relx = 0.01, rely = 0.065)
        self.enrty3 = Entry(self.root)
        self.enrty3.place(relx = 0.16, rely = 0.01, relwidth = 0.08, relheight = 0.045)
        self.label3 = Label(self.root, text = "x2")
        self.label3.place(relx = 0.13, rely = 0.01)
        self.enrty4 = Entry(self.root)
        self.enrty4.place(relx = 0.16, rely = 0.065, relwidth = 0.08, relheight = 0.045)
        self.label4 = Label(self.root, text = "y2")
        self.label4.place(relx = 0.13, rely = 0.065)
        self.enrty5 = Entry(self.root)
        self.enrty5.place(relx = 0.25, rely = 0.065, relwidth = 0.08, relheight = 0.045)
        self.label5 = Label(self.root, text = "длинна")
        self.label5.place(relx = 0.25, rely = 0.01)
        self.button1 = Button(self.root, text = "Создать", command = self.create_rhomb)
        self.button1.place(relx = 0.34, rely = 0.01, relwidth = 0.3, relheight = 0.1)
        self.button2 = Button(self.root, text = "Сохранить", command = self.saved_image)
        self.button2.place(relx = 0.65, rely = 0.01, relwidth = 0.3, relheight = 0.1)
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

    def create_rhomb(self):
        try:
            ax = int(self.enrty1.get())
            ay = int(self.enrty2.get())
            cx = int(self.enrty3.get())
            cy = int(self.enrty4.get())
            length_diag = int(self.enrty5.get())
        except ValueError:
            showerror("введите корректные числа")
            return
        ac = math.sqrt(((cx - ax) ** 2) + ((cy - ay) ** 2))
        if ac == 0:
            showerror("Ромб не определен")
            return
        ox = (ax + cx) // 2
        oy = (ay + cy) // 2
        perp_x = -(cy - ay) / ac
        perp_y = (cx - ax) / ac
        bx = ox + (length_diag / 2 * perp_x)
        by = oy + (length_diag / 2 * perp_y)
        dx = ox - (length_diag / 2 * perp_x)
        dy = oy - (length_diag / 2 * perp_y)
        canvas_width = self.canvas1.winfo_width()
        canvas_height = self.canvas1.winfo_height()
        canvas_width = canvas_width // 2
        canvas_height = canvas_height // 2
        ax += canvas_width
        bx += canvas_width
        cx += canvas_width
        dx += canvas_width
        ay += canvas_height
        by += canvas_height
        cy += canvas_height
        dy += canvas_height
        self.create_rhomb_CDA(ax, ay, bx, by, cx, cy, dx, dy)
        self.create_rhomb_Brezenhem(ax, ay, bx, by, cx, cy, dx, dy)
        self.create_rhomb_integer_Brezenhem(ax, ay, bx, by, cx, cy, dx, dy)
        self.draw_polygon(ax, ay, bx, by, cx, cy, dx, dy)

    def create_rhomb_CDA(self, ax, ay, bx, by, cx, cy, dx, dy):
        self.canvas1.delete("all")
        self.png_points1 = None
        canvas_width = self.canvas1.winfo_width()
        canvas_height = self.canvas1.winfo_height()
        self.png_points1 = []
        for y in range(canvas_height):
            row = []
            for x in range(canvas_width):
                row.append({1: "lightgray"})
            self.png_points1.append(row)
        self.draw_line_CDA(ax, bx, ay, by)
        self.draw_line_CDA(bx, cx, by, cy)
        self.draw_line_CDA(cx, dx, cy, dy)
        self.draw_line_CDA(ax, dx, ay, dy)

    def draw_line_CDA(self, x1, x2, y1, y2):
        if x1 == x2 and y1 == y2:
            self.canvas1.create_rectangle(x1, y1, x1 + 1, y1 + 1, outline = "black")
            return
        dx_abs = abs(x2 - x1)
        dy_abs = abs(y2 - y1)
        if dx_abs >= dy_abs:
            L = int(dx_abs)
        else:
            L = int(dy_abs)
        dx = (x2 - x1) / L
        dy = (y2 - y1) / L
        x = x1 + 0.5 * self.sign(dx)
        y = y1 + 0.5 * self.sign(dy)
        for i in range(L + 1):
            ix = math.floor(x)
            iy = math.floor(y)
            self.canvas1.create_rectangle(ix, iy, ix + 1, iy + 1, outline = "black")
            self.png_points1[int(y)][int(x)] = {1: "black"}
            x = x + dx
            y = y + dy

    def create_rhomb_Brezenhem(self, ax, ay, bx, by, cx, cy, dx, dy):
        self.png_points2 = None
        self.canvas2.delete("all")
        canvas_width = self.canvas2.winfo_width()
        canvas_height = self.canvas2.winfo_height()
        self.png_points2 = []
        for y in range(canvas_height):
            row = []
            for x in range(canvas_width):
                row.append({1: "lightgray"})
            self.png_points2.append(row)
        self.draw_line_Brezenhem(ax, bx, ay, by)
        self.draw_line_Brezenhem(bx, cx, by, cy)
        self.draw_line_Brezenhem(cx, dx, cy, dy)
        self.draw_line_Brezenhem(dx, ax, dy, ay)

    def draw_line_Brezenhem(self, x1, x2, y1, y2):
        if x1 == x2 and y1 == y2:
            self.canvas2.create_rectangle(x1, y1, x1 + 1, y1 + 1, outline = "black")
            return
        Dx, Dy = x2 - x1, y2 - y1
        sx, sy = self.sign(Dx), self.sign(Dy)
        Dx, Dy = abs(Dx), abs(Dy)
        flag = 0
        if Dy > Dx:
            temp = Dx
            Dx = Dy
            Dy = temp
            flag = 1
        if Dx != 0:
            f = Dy / Dx - 0.5
        else:
            f = 0
        X = x1
        Y = y1
        for i in range(int(Dx) + 1):
            self.canvas2.create_rectangle(X, Y, X + 1, Y + 1, outline = "black")
            self.png_points2[int(Y)][int(X)] = {1: "black"}
            if f >= 0:
                if flag == 1:
                    X = X + sx
                else:
                    Y = Y + sy
                f -= 1
            if flag == 1:
                Y = Y + sy
            else:
                X = X + sx
            if Dx != 0:
                f = f + Dy / Dx

    def create_rhomb_integer_Brezenhem(self, ax, ay, bx, by, cx, cy, dx, dy):
        self.png_points3 = None
        self.canvas3.delete("all")
        canvas_width = self.canvas3.winfo_width()
        canvas_height = self.canvas3.winfo_height()
        self.png_points3 = []
        for y in range(canvas_height):
            row = []
            for x in range(canvas_width):
                row.append({1: "lightgray"})
            self.png_points3.append(row)
        self.draw_line_integer_Brezenhem(ax, bx, ay, by)
        self.draw_line_integer_Brezenhem(bx, cx, by, cy)
        self.draw_line_integer_Brezenhem(cx, dx, cy, dy)
        self.draw_line_integer_Brezenhem(dx, ax, dy, ay)

    def draw_line_integer_Brezenhem(self, x1, x2, y1, y2):
        if x1 == x2 and y1 == y2:
            self.canvas3.create_rectangle(x1, y1, x1 + 1, y1 + 1, outline = "black")
            return
        Dx, Dy = x2 - x1, y2 - y1
        sx, sy = self.sign(Dx), self.sign(Dy)
        Dx, Dy = abs(Dx), abs(Dy)
        flag = 0
        if Dy > Dx:
            temp = Dx
            Dx = Dy
            Dy = temp
            flag = 1
        f = 2 * Dy - Dx
        X = x1
        Y = y1
        for i in range(int(Dx) + 1):
            self.canvas3.create_rectangle(X, Y, X + 1, Y + 1, outline = "black")
            self.png_points3[int(Y)][int(X)] = {1: "black"}
            if f >= 0:
                if flag == 1:
                    X = X + sx
                else:
                    Y = Y + sy
                f = f - 2 * Dx
            if flag == 1:
                Y = Y + sy
            else:
                X = X + sx
            f = f + 2 * Dy

    def draw_polygon(self, ax, ay, bx, by, cx, cy, dx, dy):
        self.png_points4 = None
        self.canvas4.delete("all")
        canvas_width = self.canvas4.winfo_width()
        canvas_height = self.canvas4.winfo_height()
        self.png_points4 = []
        for y in range(canvas_height):
            row = []
            for x in range(canvas_width):
                row.append({1: "lightgray"})
            self.png_points4.append(row)
        self.draw_line(ax, bx, ay, by)
        self.draw_line(bx, cx, by, cy)
        self.draw_line(cx, dx, cy, dy)
        self.draw_line(dx, ax, dy, ay)

    def draw_line(self, x1, x2, y1, y2):
        self.canvas4.create_line(x1, y1, x2, y2, fill = "black")

    def sign(self, value):
        return 1 if value > 0 else -1 if value < 0 else 0

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
        save_dir = os.path.join(script_dir, "saved_rhombs")
        os.makedirs(save_dir, exist_ok=True)
        arrays = [
            (self.png_points1, "CDA"),
            (self.png_points2, "Brezenhem"),
            (self.png_points3, "Integer_Brezenhem"),
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