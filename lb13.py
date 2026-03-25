from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import *
from tkinter.messagebox import *
import random
from tkinter import colorchooser

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
        self.fill_color = "#000000"
        self.clip_mode = "inside"
        self.polyhedron_points = None
        self.mark = 0
        self.point1 = None
        self.point2 = (0, 0)
        self.widgets()
    
    def window_center(self, x, y, window_x, window_y):
        x = (x - window_x) // 2
        y = (y - window_y) // 2
        return x, y
    
    def create_canvas(self, frame):
        canvas = Canvas(frame, bg = "white")
        canvas.grid(row = 0, column = 0, sticky="nsew")
        frame.grid_rowconfigure(0, weight = 1)
        frame.grid_columnconfigure(0, weight = 1)
        return canvas

    def run(self):
        self.root.mainloop()

    def widgets(self):
        self.frame_image = Frame(self.root)
        self.frame_image.place(relx = 0.005, rely = 0.06, relwidth = 0.99, relheight = 0.92)
        self.canvas_image = self.create_canvas(self.frame_image)
        self.button_exit = Button(self.root, text = "X", command = self.root.destroy)
        self.button_exit.place(relx = 0.97, rely = 0.005, relwidth = 0.025, relheight = 0.05)
        self.color = Button(self.root, text = "Выберите цвет заливки", command = self.Color)
        self.color.place(relx = 0.005, rely = 0.005, relwidth = 0.11, relheight = 0.05)
        self.clipping_mode = Button(self.root, text = "Отсеч внутри окна", command = self.toggle_mode)
        self.clipping_mode.place(relx = 0.115, rely = 0.005, relwidth = 0.1, relheight = 0.05)
        self.create_rand_figure = Button(self.root, text = "Создать многоугольник", command = self.Create_rand_figure)
        self.create_rand_figure.place(relx = 0.225, rely = 0.005, relwidth = 0.11, relheight = 0.05)
        self.create_window = Button(self.root, text = "Выбрать область\n    отсечнения", command = self.Mark)
        self.create_window.place(relx = 0.335, rely = 0.005, relwidth = 0.11, relheight = 0.05)
        self.clipp = Button(self.root, text = "Отсечь", command = self.cut)
        self.clipp.place(relx = 0.445, rely = 0.005, relwidth = 0.11, relheight = 0.05)
        self.canvas_image.bind("<Button-1>", self.minting_area)

    def Mark(self):
        self.mark = 2

    def minting_area(self, event):
        if self.mark > 0:
            self.canvas_image.delete("all")
            x, y = event.x, event.y
            self.point1 = self.point2
            self.point2 = (x, y)
            self.canvas_image.create_polygon(self.point1[0], self.point1[1], self.point2[0], self.point1[1], self.point2[0], self.point2[1], self.point1[0], self.point2[1], fill = "", outline = "red")
            if self.polyhedron_points:
                points_tuple = tuple(self.polyhedron_points)
                self.canvas_image.create_polygon(points_tuple, fill = "", outline = "gray", width = 2)
            self.mark -= 1

    def Create_rand_figure(self):
        self.canvas_image.delete("all")
        x = random.randint(3, 20)
        width = self.canvas_image.winfo_width()
        height = self.canvas_image.winfo_height()
        self.polyhedron_points = []
        for i in range(x):
            self.polyhedron_points.append(random.randint(0, width))
            self.polyhedron_points.append(random.randint(0, height))
        points_tuple = tuple(self.polyhedron_points)
        self.canvas_image.create_polygon(points_tuple, fill = "", outline = "gray", width = 2)
        if self.point1 and self.point2:
            self.canvas_image.create_polygon(self.point1[0], self.point1[1], self.point2[0], self.point1[1], self.point2[0], self.point2[1], self.point1[0], self.point2[1], fill = "", outline = "red")

    def toggle_mode(self):
        if self.clip_mode == "inside":
            self.clip_mode = "outside"
            self.clipping_mode.config(text = "Отсеч снаружи окна")
        else:
            self.clip_mode = "inside"
            self.clipping_mode.config(text = "Отсеч внутри окна")

    def Color(self):
        color = colorchooser.askcolor(title = "", initialcolor = self.fill_color)
        if color:
            self.fill_color = color[1]
    
    def cut(self):
        if not self.polyhedron_points or not self.point1 or not self.point2:
            showerror("Ошибка" "Выберите область отсечения и многоугольник")
            return
        self.canvas_image.delete("all")
        x_left = min(self.point1[0], self.point2[0])
        y_top = min(self.point1[1], self.point2[1])
        x_right = max(self.point1[0], self.point2[0])
        y_bottom = max(self.point1[1], self.point2[1])
        polygon = []
        for i in range(0, len(self.polyhedron_points), 2):
            polygon.append((self.polyhedron_points[i], self.polyhedron_points[i+1]))
        if self.clip_mode == "inside":
            clip_window = (x_left, y_top, x_right, y_bottom)
            clipped_polygon = self.sutherland_hodgman_clip(polygon, clip_window)
            if clipped_polygon and len(clipped_polygon) >= 3:
                self.fill_polygons(clipped_polygon)
            self.canvas_image.create_polygon(x_left, y_top, x_right, y_top, x_right, y_bottom, x_left, y_bottom, fill = "", outline = "red", dash = (6, 3))
        else:
            clip_window = (x_left, y_top, x_right, y_bottom)
            clipped_polygon = self.sutherland_hodgman_clip(polygon, clip_window)
            outside_polygons = self.polygon_difference(polygon, clipped_polygon, clip_window)
            if outside_polygons:
                for ext_polygon in outside_polygons:
                    if ext_polygon and len(ext_polygon) > 2:
                        self.fill_polygons(ext_polygon)
            self.canvas_image.create_polygon(x_left, y_top, x_right, y_top, x_right, y_bottom, x_left, y_bottom, fill = "", outline = "red", dash = (6, 3))

    def sutherland_hodgman_clip(self, polygon, clip_window):
        x_left, y_top, x_right, y_bottom = clip_window
        edges = [
            ('left', x_left),
            ('top', y_top),
            ('right', x_right),
            ('bottom', y_bottom)
        ]
        result_polygon = polygon
        for edge_type, edge_value in edges:
            result_polygon = self.clip_polygon_against_edge(result_polygon, edge_type, edge_value)
            if not result_polygon or len(result_polygon) < 3:
                return []
        return result_polygon

    def clip_polygon_against_edge(self, polygon, edge_type, edge_value):
        if not polygon:
            return []
        output_list = []
        points_count = len(polygon)
        for i in range(points_count):
            curr_point = polygon[i]
            prev_point = polygon[(i - 1) % points_count]
            curr_inside = self.is_point_inside_edge(curr_point, edge_type, edge_value)
            prev_inside = self.is_point_inside_edge(prev_point, edge_type, edge_value)
            if prev_inside and curr_inside:
                output_list.append(curr_point)
            elif prev_inside and not curr_inside:
                intersection = self.compute_intersection(prev_point, curr_point, edge_type, edge_value)
                if intersection:
                    output_list.append(intersection)
            elif not prev_inside and curr_inside:
                intersection = self.compute_intersection(prev_point, curr_point, edge_type, edge_value)
                if intersection:
                    output_list.append(intersection)
                output_list.append(curr_point)
        return output_list

    def is_point_inside_edge(self, point, edge_type, edge_value):
        x, y = point
        if edge_type == 'left':
            return x >= edge_value
        elif edge_type == 'right':
            return x <= edge_value
        elif edge_type == 'top':
            return y >= edge_value
        elif edge_type == 'bottom':
            return y <= edge_value
        return False

    def compute_intersection(self, p1, p2, edge_type, edge_value):
        x1, y1 = p1
        x2, y2 = p2
        if x1 == x2 and y1 == y2:
            return None
        
        if edge_type == 'left':
            x = edge_value
            if x2 - x1 != 0:
                t = (x - x1) / (x2 - x1)
                y = y1 + t * (y2 - y1)
                return (x, y)
            else:
                return None
        
        elif edge_type == 'right':
            x = edge_value
            if x2 - x1 != 0:
                t = (x - x1) / (x2 - x1)
                y = y1 + t * (y2 - y1)
                return (x, y)
            else:
                return None
        
        elif edge_type == 'top':
            y = edge_value
            if y2 - y1 != 0:
                t = (y - y1) / (y2 - y1)
                x = x1 + t * (x2 - x1)
                return (x, y)
            else:
                return None
        
        elif edge_type == 'bottom':
            y = edge_value
            if y2 - y1 != 0:
                t = (y - y1) / (y2 - y1)
                x = x1 + t * (x2 - x1)
                return (x, y)
            else:
                return None
        return None

    def polygon_difference(self, polygon_a, polygon_b, clip_window):
        x_left, y_top, x_right, y_bottom = clip_window
        if not polygon_b: return [polygon_a]
        elif set(polygon_a) == set(polygon_b): return []
        all_x = [p[0] for p in polygon_a]
        all_y = [p[1] for p in polygon_a]
        min_x, max_x = min(all_x), max(all_x)
        min_y, max_y = min(all_y), max(all_y)
        outside_regions = []
        if min_y < y_top:
            clipped = self.sutherland_hodgman_clip(polygon_a, (min_x, min_y, max_x, y_top))
            if clipped and len(clipped) >= 3:
                outside_regions.append(clipped)
        if max_y > y_bottom:
            clipped = self.sutherland_hodgman_clip(polygon_a, (min_x, y_bottom, max_x, max_y))
            if clipped and len(clipped) >= 3:
                outside_regions.append(clipped)
        if min_x < x_left:
            clipped = self.sutherland_hodgman_clip(polygon_a, (min_x, y_top, x_left, y_bottom))
            if clipped and len(clipped) >= 3:
                outside_regions.append(clipped)
        if max_x > x_right:
            clipped = self.sutherland_hodgman_clip(polygon_a, (x_right, y_top, max_x, y_bottom))
            if clipped and len(clipped) >= 3:
                outside_regions.append(clipped)
        unique_regions = []
        for region in outside_regions:
            region_set = set(region)
            is_duplicate = False
            for existing in unique_regions:
                if set(existing) == region_set:
                    is_duplicate = True
                    break
            if not is_duplicate:
                unique_regions.append(region)
        return unique_regions

    def fill_polygons(self, polygon):
        if not polygon:
            return
        edges = []
        for i in range(len(polygon)):
            x1, y1 = polygon[i]
            x2, y2 = polygon[(i + 1) % len(polygon)]
            if y1 == y2:
                continue
            if y1 < y2:
                y_min, y_max = y1, y2
                x_min, x_max = x1, x2
            else:
                y_min, y_max = y2, y1
                x_min, x_max = x2, x1
            dx = (x_max - x_min) / (y_max - y_min)
            edges.append({
                'y_min': y_min,
                'y_max': y_max,
                'x': x_min,
                'dx': dx
            })
        if not edges:
            return
        edges.sort(key=lambda e: e['y_min'])
        y_min_all = int(min(e['y_min'] for e in edges))
        y_max_all = int(max(e['y_max'] for e in edges))
        active_edges = []
        edge_index = 0
        for y in range(y_min_all, y_max_all + 1):
            while edge_index < len(edges) and edges[edge_index]['y_min'] <= y:
                active_edges.append(edges[edge_index].copy())
                edge_index += 1
            active_edges = [e for e in active_edges if e['y_max'] > y]
            if len(active_edges) < 2:
                continue
            active_edges.sort(key=lambda e: e['x'])
            for i in range(0, len(active_edges) - 1, 2):
                x_start = int(active_edges[i]['x'])
                x_end = int(active_edges[i + 1]['x'])
                for x in range(x_start, x_end + 1):
                    self.canvas_image.create_rectangle(x, y, x + 1, y + 1, fill = self.fill_color, outline = "")
            for edge in active_edges:
                edge['x'] += edge['dx']

window = Window("Обработчик изображений")
window.run()