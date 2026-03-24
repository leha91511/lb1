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
        self.surface_bezier_iteration = 0
        self.surface_bezier_built = False
        self.doo_sabin_iteration = 0
        self.doo_sabin_built = False
        self.current_mode = None
        self.widgets()
    
    def window_center(self, x, y, window_x, window_y):
        x = (x - window_x) // 2
        y = (y - window_y) // 2
        return x, y

    def widgets(self):
        self.button_exit = Button(self.root, text = "X", command = self.root.destroy)
        self.button_exit.place(relx = 0.97, rely = 0.005, relwidth = 0.025, relheight = 0.05)
        self.surface_bezier = Button(self.root, text = "Поверхность Безье", command = self.Surface_bezier)
        self.surface_bezier.place(relx = 0.005, rely = 0.005, relwidth = 0.1, relheight = 0.05)
        self.surface_doo_sabin = Button(self.root, text = "Поверхность\nДу-Сабина", command = self.Surface_doo_sabin)
        self.surface_doo_sabin.place(relx = 0.205, rely = 0.005, relwidth = 0.09, relheight = 0.05)

        self.label_x1 = Label(self.root, text = "x1")
        self.label_x1.place(relx = 0.305, rely = 0.005)
        self.label_x2 = Label(self.root, text = "x2")
        self.label_x2.place(relx = 0.405, rely = 0.005)
        self.label_x3 = Label(self.root, text = "x3")
        self.label_x3.place(relx = 0.505, rely = 0.005)
        self.label_x4 = Label(self.root, text = "x4")
        self.label_x4.place(relx = 0.605, rely = 0.005)
        self.label_y1 = Label(self.root, text = "y1")
        self.label_y1.place(relx = 0.305, rely = 0.03)
        self.label_y2 = Label(self.root, text = "y2")
        self.label_y2.place(relx = 0.405, rely = 0.03)
        self.label_y3 = Label(self.root, text = "y3")
        self.label_y3.place(relx = 0.505, rely = 0.03)
        self.label_y4 = Label(self.root, text = "y4")
        self.label_y4.place(relx = 0.605, rely = 0.03)
        self.splitting_param = Label(self.root, text = "параметр разбиения")
        self.splitting_param.place(relx = 0.705, rely = 0.005)

        self.x1 = Spinbox(self.root, from_ = 0, to = 1500, increment = 1, width = 5, font = "Calibri")
        self.x1.place(relx = 0.32, rely = 0.005, relwidth = 0.08, relheight = 0.025)
        self.x2 = Spinbox(self.root, from_ = 0, to = 1500, increment = 1, width = 5, font = "Calibri")
        self.x2.place(relx = 0.42, rely = 0.005, relwidth = 0.08, relheight = 0.025)
        self.x3 = Spinbox(self.root, from_ = 0, to = 1500, increment = 1, width = 5, font = "Calibri")
        self.x3.place(relx = 0.52, rely = 0.005, relwidth = 0.08, relheight = 0.025)
        self.x4 = Spinbox(self.root, from_ = 0, to = 1500, increment = 1, width = 5, font = "Calibri")
        self.x4.place(relx = 0.62, rely = 0.005, relwidth = 0.08, relheight = 0.025)
        self.y1 = Spinbox(self.root, from_ = 0, to = 1500, increment = 1, width = 5, font = "Calibri")
        self.y1.place(relx = 0.32, rely = 0.03, relwidth = 0.08, relheight = 0.025)
        self.y2 = Spinbox(self.root, from_ = 0, to = 1500, increment = 1, width = 5, font = "Calibri")
        self.y2.place(relx = 0.42, rely = 0.03, relwidth = 0.08, relheight = 0.025)
        self.y3 = Spinbox(self.root, from_ = 0, to = 1500, increment = 1, width = 5, font = "Calibri")
        self.y3.place(relx = 0.52, rely = 0.03, relwidth = 0.08, relheight = 0.025)
        self.y4 = Spinbox(self.root, from_ = 0, to = 1500, increment = 1, width = 5, font = "Calibri")
        self.y4.place(relx = 0.62, rely = 0.03, relwidth = 0.08, relheight = 0.025)
        self.splitting_param_spinbox = Spinbox(self.root, from_ = 1, to = 10, increment = 1, width = 5, font = "Calibri")
        self.splitting_param_spinbox.place(relx = 0.705, rely = 0.03, relwidth = 0.08, relheight = 0.025)

        self.x1.set(100)
        self.x2.set(100)
        self.x3.set(400)
        self.x4.set(400)
        self.y1.set(100)
        self.y2.set(400)
        self.y3.set(400)
        self.y4.set(300)
        self.splitting_param_spinbox.set(8)

        self.frame_image = Frame(self.root)
        self.frame_image.place(relx = 0.005, rely = 0.06, relwidth = 0.99, relheight = 0.92)
        self.canvas_image = self.create_canvas(self.frame_image)
    
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

    def Surface_bezier(self):
        try:
            x1 = int(self.x1.get())
            y1 = int(self.y1.get())
            x2 = int(self.x2.get())
            y2 = int(self.y2.get())
            x3 = int(self.x3.get())
            y3 = int(self.y3.get())
            x4 = int(self.x4.get())
            y4 = int(self.y4.get())
            P1 = (x1, y1)
            P2 = (x2, y2)
            P3 = (x3, y3)
            P4 = (x4, y4)
            if not self.is_convex_quadrilateral(P1, P2, P3, P4):
                showerror("Ошибка", "Четырёхугольник не является выпуклым!\n"
                        "Диагонали должны пересекаться внутри фигуры.")
                return
            grid = [[None for _ in range(4)] for _ in range(4)]
            grid[0][0] = P1
            grid[0][3] = P2
            grid[3][3] = P3
            grid[3][0] = P4
            P1P2 = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            P1P4 = math.sqrt((x4 - x1) ** 2 + (y4 - y1) ** 2)
            P2P3 = math.sqrt((x3 - x2) ** 2 + (y3 - y2) ** 2)
            P3P4 = math.sqrt((x4 - x3) ** 2 + (y4 - y3) ** 2)
            r1 = P1P2 / 4
            r4 = P1P4 / 4
            r2 = P2P3 / 4
            r3 = P3P4 / 4
            grid[0][1] = (x1 + (x2 - x1) / 3 + random.uniform(-r1, r1), y1 + (y2 - y1) / 3 + random.uniform(-r1, r1))
            grid[0][2] = (x1 + (x2 - x1) * 2 / 3 + random.uniform(-r1, r1), y1 + (y2 - y1) * 2 / 3 + random.uniform(-r1, r1))
            grid[1][3] = (x2 + (x3 - x2) / 3 + random.uniform(-r2, r2), y2 + (y3 - y2) / 3 + random.uniform(-r2, r2))
            grid[2][3] = (x2 + (x3 - x2) * 2 / 3 + random.uniform(-r2, r2), y2 + (y3 - y2) * 2 / 3 + random.uniform(-r2, r2))
            grid[3][2] = (x3 + (x4 - x3) / 3 + random.uniform(-r3, r3), y3 + (y4 - y3) / 3 + random.uniform(-r3, r3))
            grid[3][1] = (x3 + (x4 - x3) * 2 / 3 + random.uniform(-r3, r3), y3 + (y4 - y3) * 2 / 3 + random.uniform(-r3, r3))
            grid[2][0] = (x4 + (x1 - x4) / 3 + random.uniform(-r4, r4), y4 + (y1 - y4) / 3 + random.uniform(-r4, r4))
            grid[1][0] = (x4 + (x1 - x4) * 2 / 3 + random.uniform(-r4, r4), y4 + (y1 - y4) * 2 / 3 + random.uniform(-r4, r4))
            
            def points(i, j):
                if i == 1 and j == 1:
                    point1 = (x1 + (x2 - x1) / 3, y1 + (y2 - y1) / 3)
                    point2 = (x3 + (x4 - x3) * 2 / 3, y3 + (y4 - y3) * 2 / 3)
                    point3 = (x4 + (x1 - x4) * 2 / 3, y4 + (y1 - y4) * 2 / 3)
                    point4 = (x2 + (x3 - x2) / 3, y2 + (y3 - y2) / 3)
                elif i == 2 and j == 1:
                    point1 = (x1 + (x2 - x1) * 2 / 3, y1 + (y2 - y1) * 2 / 3)
                    point2 = (x3 + (x4 - x3)/ 3, y3 + (y4 - y3) / 3)
                    point3 = (x4 + (x1 - x4) * 2 / 3, y4 + (y1 - y4) * 2 / 3)
                    point4 = (x2 + (x3 - x2) / 3, y2 + (y3 - y2) / 3)
                elif i == 1 and j == 2:
                    point1 = (x1 + (x2 - x1) / 3, y1 + (y2 - y1) / 3)
                    point2 = (x3 + (x4 - x3) * 2 / 3, y3 + (y4 - y3) * 2 / 3)
                    point3 = (x4 + (x1 - x4) / 3, y4 + (y1 - y4) / 3)
                    point4 = (x2 + (x3 - x2) * 2 / 3, y2 + (y3 - y2) * 2 / 3)
                else:
                    point1 = (x1 + (x2 - x1) * 2 / 3, y1 + (y2 - y1) * 2 / 3)
                    point2 = (x3 + (x4 - x3)/ 3, y3 + (y4 - y3) / 3)
                    point3 = (x4 + (x1 - x4) / 3, y4 + (y1 - y4) / 3)
                    point4 = (x2 + (x3 - x2) * 2 / 3, y2 + (y3 - y2) * 2 / 3)
                x, y = find_intersection(point1, point2, point3, point4)
                len1 = math.hypot(point2[0] - point1[0], point2[1] - point1[1])
                len2 = math.hypot(point4[0] - point3[0], point4[1] - point3[1])
                rx = len1 / 4
                ry = len2 / 4
                while True:
                    u = random.uniform(-1, 1)
                    v = random.uniform(-1, 1)
                    if u * u + v * v <= 1:
                        dx = u * rx
                        dy = v * ry
                        break
                return (x + dx, y + dy)
                
            def find_intersection(point1, point2, point3, point4):
                x1, y1 = point1
                x2, y2 = point2
                x3, y3 = point3
                x4, y4 = point4
                denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
                
                if abs(denom) < 1e-10:
                    return ((x1 + x3) / 2, (y1 + y3) / 2)
                
                t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
                intersect_x = x1 + t * (x2 - x1)
                intersect_y = y1 + t * (y2 - y1)
                return (intersect_x, intersect_y)
            
            x, y = points(1, 1)
            grid[1][1] = (x, y)
            x, y = points(2, 1)
            grid[1][2] = (x, y)
            x, y = points(1, 2)
            grid[2][1] = (x, y)
            x, y = points(2, 2)
            grid[2][2] = (x, y)

            if not hasattr(self, 'surface_bezier_iteration'):
                self.surface_bezier_iteration = 0
                self.surface_bezier_built = False
            
            if not self.surface_bezier_built:
                self.surface_bezier_built = True
                self.surface_bezier_iteration = 0
                self.current_mode = "surface_bezier"
                self.original_grid = grid
                self.current_grid = grid
                self.canvas_image.delete("all")
                self.draw_bezier_grid(self.current_grid, "blue", "red")
            else:
                self.surface_bezier_iteration += 1
                if self.surface_bezier_iteration <= 5:
                    self.draw_bezier_surface_iteration(self.surface_bezier_iteration)
                else:
                    self.surface_bezier_built = False
                    self.surface_bezier_iteration = 0
                    self.current_mode = None
                    self.draw_final_bezier_surface()
                    showerror("Построение", "Построение поверхности Безье завершено")
                    
        except Exception as e:
            showerror("Ошибка", f"Ошибка при построении поверхности: {str(e)}")

    def draw_bezier_grid(self, grid, line_color, point_color):
        if not grid:
            return
        for i in range(4):
            for j in range(4):
                if grid[i][j]:
                    if (i == 0 or i == 3) and (j == 0 or j == 3):
                        self.draw_point(grid[i][j][0], grid[i][j][1], "orange", radius=4)
                    else:
                        self.draw_point(grid[i][j][0], grid[i][j][1], point_color, radius=3)
        for i in range(4):
            for j in range(3):
                if grid[i][j] and grid[i][j+1]:
                    self.draw_line(grid[i][j][0], grid[i][j][1],
                                grid[i][j+1][0], grid[i][j+1][1],
                                line_color, width=1)
        for j in range(4):
            for i in range(3):
                if grid[i][j] and grid[i+1][j]:
                    self.draw_line(grid[i][j][0], grid[i][j][1],
                                grid[i+1][j][0], grid[i+1][j][1],
                                line_color, width=1)

    def bezier_curve(self, p0, p1, p2, p3, t):
        t2 = t * t
        t3 = t2 * t
        mt = 1 - t
        mt2 = mt * mt
        mt3 = mt2 * mt
        x = mt3 * p0[0] + 3 * mt2 * t * p1[0] + 3 * mt * t2 * p2[0] + t3 * p3[0]
        y = mt3 * p0[1] + 3 * mt2 * t * p1[1] + 3 * mt * t2 * p2[1] + t3 * p3[1]
        return (x, y)

    def bezier_surface_point(self, grid, u, v):
        points = []
        for i in range(4):
            point = self.bezier_curve(grid[i][0], grid[i][1], grid[i][2], grid[i][3], u)
            points.append(point)
        return self.bezier_curve(points[0], points[1], points[2], points[3], v)

    def build_bezier_surface(self, grid, subdivisions):
        size = subdivisions + 1
        surface = [[None for _ in range(size)] for _ in range(size)]
        for i in range(size):
            u = i / subdivisions
            for j in range(size):
                v = j / subdivisions
                surface[i][j] = self.bezier_surface_point(grid, u, v)
        return surface

    def draw_bezier_surface(self, surface, line_color, point_color):
        size = len(surface)
        for i in range(size):
            for j in range(size - 1):
                if surface[i][j] and surface[i][j+1]:
                    self.draw_line(surface[i][j][0], surface[i][j][1],
                                surface[i][j+1][0], surface[i][j+1][1],
                                line_color, width=1)
        for j in range(size):
            for i in range(size - 1):
                if surface[i][j] and surface[i+1][j]:
                    self.draw_line(surface[i][j][0], surface[i][j][1],
                                surface[i+1][j][0], surface[i+1][j][1],
                                line_color, width=1)
        if size <= 20:
            for i in range(size):
                for j in range(size):
                    if surface[i][j]:
                        self.draw_point(surface[i][j][0], surface[i][j][1], point_color, radius=1)

    def draw_bezier_surface_iteration(self, iteration):
        subdivisions = 2 ** iteration
        self.canvas_image.delete("all")
        self.draw_bezier_grid(self.original_grid, "gray", "lightgray")
        colors = ["red", "blue", "green", "orange", "purple", "brown", "pink", "cyan"]
        for i in range(4):
            p0 = self.original_grid[i][0]
            p1 = self.original_grid[i][1]
            p2 = self.original_grid[i][2]
            p3 = self.original_grid[i][3]
            self.draw_bezier_curve(p0, p1, p2, p3, colors[i], subdivisions)
        for j in range(4):
            p0 = self.original_grid[0][j]
            p1 = self.original_grid[1][j]
            p2 = self.original_grid[2][j]
            p3 = self.original_grid[3][j]
            self.draw_bezier_curve(p0, p1, p2, p3, colors[4 + j], subdivisions)

    def draw_final_bezier_surface(self):
        t = int(self.splitting_param_spinbox.get())
        subdivisions = 2 ** t
        self.canvas_image.delete("all")
        self.draw_bezier_grid(self.original_grid, "gray", "lightgray")
        colors = ["red", "blue", "green", "orange", "purple", "brown", "pink", "cyan"]
        for i in range(4):
            p0 = self.original_grid[i][0]
            p1 = self.original_grid[i][1]
            p2 = self.original_grid[i][2]
            p3 = self.original_grid[i][3]
            self.draw_bezier_curve(p0, p1, p2, p3, colors[i], subdivisions)
        for j in range(4):
            p0 = self.original_grid[0][j]
            p1 = self.original_grid[1][j]
            p2 = self.original_grid[2][j]
            p3 = self.original_grid[3][j]
            self.draw_bezier_curve(p0, p1, p2, p3, colors[4 + j], subdivisions)
        
    def draw_bezier_curve(self, p0, p1, p2, p3, color, segments):
        points = []
        for k in range(segments + 1):
            t = k / segments
            point = self.bezier_curve(p0, p1, p2, p3, t)
            points.append(point)
        for k in range(len(points) - 1):
            self.draw_line(points[k][0], points[k][1],
                        points[k+1][0], points[k+1][1],
                        color, width=2)

    def draw_point(self, x, y, color, radius = 2):
        self.canvas_image.create_oval(x - radius, y - radius, x + radius, y + radius, fill = color, outline = color)

    def draw_line(self, x1, y1, x2, y2, color, width = 2, dash = None):
        self.canvas_image.create_line(x1, y1, x2, y2, fill = color, width = width, dash = dash)

    def is_convex_quadrilateral(self, P0, P1, P2, P3):
        def cross_product(o, a, b):
            return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
        cp1 = cross_product(P0, P1, P2)
        cp2 = cross_product(P1, P2, P3)
        cp3 = cross_product(P2, P3, P0)
        cp4 = cross_product(P3, P0, P1)
        signs = []
        for cp in [cp1, cp2, cp3, cp4]:
            if cp > 0:
                signs.append(1)
            elif cp < 0:
                signs.append(-1)
            else:
                signs.append(0)
        signs = [s for s in signs if s != 0]
        if len(signs) == 0:
            return True
        return all(s == signs[0] for s in signs)

    def Surface_doo_sabin(self):
        try:
            x1 = int(self.x1.get())
            y1 = int(self.y1.get())
            x2 = int(self.x2.get())
            y2 = int(self.y2.get())
            x3 = int(self.x3.get())
            y3 = int(self.y3.get())
            x4 = int(self.x4.get())
            y4 = int(self.y4.get())
            P0 = (x1, y1)
            P1 = (x2, y2)
            P2 = (x3, y3)
            P3 = (x4, y4)
            if not self.is_convex_quadrilateral(P0, P1, P2, P3):
                showerror("Ошибка", "Четырёхугольник не является выпуклым!\n" "Диагонали должны пересекаться внутри фигуры.")
                return
            self.t = int(self.splitting_param_spinbox.get()) / 10
            P0_mirror = (2*P3[0] - P0[0], 2*P3[1] - P0[1])
            P1_mirror = (2*P3[0] - P1[0], 2*P3[1] - P1[1])
            P2_mirror = (2*P3[0] - P2[0], 2*P3[1] - P2[1])
            P0_mirror2 = (2*P1[0] - P0[0], 2*P1[1] - P0[1])
            P2_mirror2 = (2*P1[0] - P2[0], 2*P1[1] - P2[1])
            P3_mirror2 = (2*P1[0] - P3[0], 2*P1[1] - P3[1])

            def midlle_point(p1, p2):
                return ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)

            surface = [P0, midlle_point(P0, P1), P1, midlle_point(P1, P2_mirror2), P2_mirror2, midlle_point(P2_mirror2, P3_mirror2),
                       P3_mirror2, midlle_point(P3_mirror2, P0_mirror2), P0_mirror2, midlle_point(P0_mirror2, P1), P1,
                        midlle_point(P1, P2), P2, midlle_point(P2, P3), P3, midlle_point(P3, P0_mirror),  P0_mirror,
                        midlle_point(P0_mirror, P1_mirror), P1_mirror, midlle_point(P1_mirror, P2_mirror), P2_mirror,
                        midlle_point(P2_mirror, P3), P3, midlle_point(P3, P0), P0]

            if not hasattr(self, 'doo_sabin_iteration'):
                self.doo_sabin_iteration = 0
                self.doo_sabin_built = False
            
            if not self.doo_sabin_built:
                self.doo_sabin_built = True
                self.doo_sabin_iteration = 0
                self.current_mode = "doo_sabin"
                self.original_vertices = surface.copy()
                self.current_vertices = surface.copy()
                self.canvas_image.delete("all")
                self.draw_polygon(self.current_vertices, "blue", point_color="red")
            else:
                self.doo_sabin_iteration += 1
                if self.doo_sabin_iteration <= 4:
                    self.apply_smoothing()
                else:
                    self.doo_sabin_built = False
                    self.doo_sabin_iteration = 0
                    self.current_mode = None
                    self.draw_final_polygon()
        except Exception as e:
            showerror("Ошибка", f"Ошибка при построении: {str(e)}")

    def draw_polygon(self, vertices, line_color, point_color="red"):
        for v in vertices:
            self.draw_point(v[0], v[1], point_color, radius=2)
        for i in range(len(vertices)):
            v1 = vertices[i]
            v2 = vertices[(i + 1) % len(vertices)]
            self.draw_line(v1[0], v1[1], v2[0], v2[1], line_color, width=2)

    def apply_smoothing(self):
        vertices = self.current_vertices
        n = len(vertices)
        t = self.t
        def transform_points(points, t):
            if not points:
                return []
            result = []
            m = len(points)
            for i in range(0, m, 2):
                if i > 0:
                    left_x = t * points[i-1][0] + (1 - t) * points[i][0]
                    left_y = t * points[i-1][1] + (1 - t) * points[i][1]
                    result.append((left_x, left_y))
                result.append(points[i])
                if i < m - 1:
                    right_x = (1 - t) * points[i][0] + t * points[i+1][0]
                    right_y = (1 - t) * points[i][1] + t * points[i+1][1]
                    result.append((right_x, right_y))
            return result
        expanded_vertices = transform_points(vertices, t)
        m = len(expanded_vertices)
        new_vertices = []
        for i in range(m):
            if i % 2 == 0:
                prev = expanded_vertices[(i - 1) % m]
                curr = expanded_vertices[i]
                next_v = expanded_vertices[(i + 1) % m]
                center_x = (prev[0] + next_v[0]) / 2
                center_y = (prev[1] + next_v[1]) / 2
                new_x = curr[0] + t * (center_x - curr[0])
                new_y = curr[1] + t * (center_y - curr[1])
                new_vertices.append((new_x, new_y))
            else:
                new_vertices.append(expanded_vertices[i])
        self.current_vertices = new_vertices
        self.canvas_image.delete("all")
        self.draw_polygon(self.original_vertices, "gray", point_color="red")
        self.draw_polygon(self.current_vertices, "green", point_color="lightgreen")

    def draw_final_polygon(self):
        self.canvas_image.delete("all")
        self.draw_polygon(self.original_vertices, "gray", point_color="red")
        self.draw_polygon(self.current_vertices, "purple", point_color="orchid")

window = Window("Обработчик изображений")
window.run()