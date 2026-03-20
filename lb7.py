from tkinter import *
from tkinter import PhotoImage
from tkinter.ttk import *
from tkinter.filedialog import *
from tkinter.messagebox import *
import os, struct, zlib
import math
import colorsys

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
        self.fnch_png_points = None
        self.fvch_png_points = None
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
        #ФНЧ преобразование: левая часть - насыщенность, правая - цветовой тон
        self.button_fnch_image = Button(self.root, text = "ФНЧ преобразование", command = self.apply_fnch)
        self.button_fnch_image.place(relx = 0.5, rely = 0.005, relwidth = 0.2, relheight = 0.05)
        self.frame_fnch_image = Frame(self.root)
        self.frame_fnch_image.place(relx = 0.5, rely = 0.06, relwidth = 0.49, relheight = 0.44)
        self.canvas_fnch_image = self.create_canvas(self.frame_fnch_image)
        self.button_saved_fnch_image = Button(self.root, text = "Сохранить", command = lambda: self.saved_image('fnch'))
        self.button_saved_fnch_image.place(relx = 0.705, rely = 0.005, relwidth = 0.15, relheight = 0.05)
        #ФВЧ преобразование: левая часть - лапласиан гауссиана только для яркости, правая - лапласиан гауссиана только для насыщенности
        self.button_fvch_image = Button(self.root, text = "ФВЧ преобразование", command = self.apply_fvch)
        self.button_fvch_image.place(relx = 0.005, rely = 0.5, relwidth = 0.2, relheight = 0.05)
        self.frame_fvch_image = Frame(self.root)
        self.frame_fvch_image.place(relx = 0.005, rely = 0.55, relwidth = 0.49, relheight = 0.44)
        self.canvas_fvch_image = self.create_canvas(self.frame_fvch_image)
        self.button_saved_fvch_image = Button(self.root, text = "Сохранить", command = lambda: self.saved_image('fvch'))
        self.button_saved_fvch_image.place(relx = 0.21, rely = 0.5, relwidth = 0.15, relheight = 0.05)

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

    def rgb_to_hsl(self, r, g, b):
        R = r / 255.0
        G = g / 255.0
        B = b / 255.0
        h, l, s = colorsys.rgb_to_hls(R, G, B)
        return h * 360, s, l
    
    def hsl_to_rgb(self, h, s, l):
        H = h / 360.0
        r, g, b = colorsys.hls_to_rgb(H, l, s)
        return int(r * 255), int(g * 255), int(b * 255)

    def apply_low_pass_filter(self, channel_data, width, height):
        if width < 3 or height < 3:
            return channel_data
        result = [[0 for _ in range(width)] for _ in range(height)]
        extended = [[0 for _ in range(width + 2)] for _ in range(height + 2)]
        for y in range(height):
            for x in range(width):
                extended[y + 1][x + 1] = channel_data[y][x]
        for y in range(height + 2):
            extended[y][0] = extended[y][1]
            extended[y][width + 1] = extended[y][width]
        for x in range(width + 2):
            extended[0][x] = extended[1][x]
            extended[height + 1][x] = extended[height][x]
        kernel_size = 3
        kernel = [[1, 1, 1],
                  [1, 1, 1],
                  [1, 1, 1]]
        kernel_sum = 9
        for y in range(height):
            for x in range(width):
                total = 0
                for ky in range(kernel_size):
                    for kx in range(kernel_size):
                        total += extended[y + ky][x + kx] * kernel[ky][kx]
                result[y][x] = total / kernel_sum
        return result
    
    def apply_fnch(self):
        if not self.orig_png_points:
            showerror("Ошибка", "Сначала загрузите изображение")
            return
        try:
            height = len(self.orig_png_points)
            width = len(self.orig_png_points[0]) if height > 0 else 0
            h_channel = [[0 for _ in range(width)] for _ in range(height)]
            s_channel = [[0 for _ in range(width)] for _ in range(height)]
            l_channel = [[0 for _ in range(width)] for _ in range(height)]
            for y in range(height):
                for x in range(width):
                    hex_color = self.orig_png_points[y][x][0]
                    hex_color = hex_color[1:]
                    r = int(hex_color[0:2], 16)
                    g = int(hex_color[2:4], 16)
                    b = int(hex_color[4:6], 16)
                    h, s, l = self.rgb_to_hsl(r, g, b)
                    h_channel[y][x] = h
                    s_channel[y][x] = s
                    l_channel[y][x] = l
            mid_x = width // 2
            if mid_x >= 3:
                left_s_channel = [[s_channel[y][x] for x in range(mid_x)] for y in range(height)]
                filtered_left_s = self.apply_low_pass_filter(left_s_channel, mid_x, height)
            else:
                filtered_left_s = [[s_channel[y][x] for x in range(mid_x)] for y in range(height)]
            right_width = width - mid_x
            if right_width >= 3:
                right_h_channel = [[h_channel[y][mid_x + x] for x in range(right_width)] for y in range(height)]
                filtered_right_h = self.apply_low_pass_filter(right_h_channel, right_width, height)
            else:
                filtered_right_h = [[h_channel[y][mid_x + x] for x in range(right_width)] for y in range(height)]
            result_points = []
            for y in range(height):
                row = []
                for x in range(width):
                    if x < mid_x:
                        new_s = filtered_left_s[y][x]
                        new_h = h_channel[y][x]
                        new_l = l_channel[y][x]
                    else:
                        right_x = x - mid_x
                        new_h = filtered_right_h[y][right_x]
                        new_s = s_channel[y][x]
                        new_l = l_channel[y][x]
                    new_h = max(0, min(359, new_h))
                    new_s = max(0, min(1, new_s))
                    new_l = max(0, min(1, new_l))
                    r, g, b = self.hsl_to_rgb(new_h, new_s, new_l)
                    hex_color = f"#{r:02x}{g:02x}{b:02x}"
                    row.append((hex_color, (x, y)))
                result_points.append(row)
            self.fnch_png_points = result_points
            self.display_image(self.canvas_fnch_image, self.fnch_png_points)
        except Exception as e:
            print(f"Ошибка в apply_fnch: {str(e)}")
            showerror("Ошибка", f"Не удалось применить ФНЧ: {str(e)}")

    def apply_fvch(self):
        if not self.orig_png_points:
            showerror("Ошибка", "Сначала загрузите изображение")
            return
        try:
            height = len(self.orig_png_points)
            width = len(self.orig_png_points[0]) if height > 0 else 0
            h_channel = [[0 for _ in range(width)] for _ in range(height)]
            s_channel = [[0 for _ in range(width)] for _ in range(height)]
            l_channel = [[0 for _ in range(width)] for _ in range(height)]
            for y in range(height):
                for x in range(width):
                    hex_color = self.orig_png_points[y][x][0]
                    hex_color = hex_color[1:]
                    r = int(hex_color[0:2], 16)
                    g = int(hex_color[2:4], 16)
                    b = int(hex_color[4:6], 16)
                    h, s, l = self.rgb_to_hsl(r, g, b)
                    h_channel[y][x] = h
                    s_channel[y][x] = s
                    l_channel[y][x] = l
            mid_x = width // 2
            if mid_x >= 5:
                left_l_channel = [[l_channel[y][x] for x in range(mid_x)] for y in range(height)]
                filtered_left_l = self.apply_log_filter(left_l_channel, mid_x, height)
            else:
                filtered_left_l = [[0 for _ in range(mid_x)] for _ in range(height)]
            right_width = width - mid_x
            if right_width >= 5:
                right_s_channel = [[s_channel[y][mid_x + x] for x in range(right_width)] for y in range(height)]
                filtered_right_s = self.apply_log_filter(right_s_channel, right_width, height)
            else:
                filtered_right_s = [[0 for _ in range(right_width)] for _ in range(height)]
            result_points = []
            for y in range(height):
                row = []
                for x in range(width):
                    if x < mid_x:
                        new_l = l_channel[y][x] + filtered_left_l[y][x] * 0.5
                        new_h = h_channel[y][x]
                        new_s = s_channel[y][x]
                    else:
                        right_x = x - mid_x
                        new_s = s_channel[y][x] + filtered_right_s[y][right_x] * 0.5
                        new_h = h_channel[y][x]
                        new_l = l_channel[y][x]
                    new_h = max(0, min(359, new_h))
                    new_s = max(0, min(1, new_s))
                    new_l = max(0, min(1, new_l))
                    r, g, b = self.hsl_to_rgb(new_h, new_s, new_l)
                    hex_color = f"#{r:02x}{g:02x}{b:02x}"
                    row.append((hex_color, (x, y)))
                result_points.append(row)
            self.fvch_png_points = result_points
            self.display_image(self.canvas_fvch_image, self.fvch_png_points)
        except Exception as e:
            print(f"Ошибка в apply_fvch: {str(e)}")
            showerror("Ошибка", f"Не удалось применить ФВЧ: {str(e)}")
    
    def apply_log_filter(self, channel_data, width, height):
        if width < 5 or height < 5:
            return [[0 for _ in range(width)] for _ in range(height)]
        blurred = self.apply_gaussian_filter(channel_data, width, height)
        result = self.apply_laplacian_filter(blurred, width, height)
        return result
    
    def apply_gaussian_filter(self, channel_data, width, height):
        gaussian_kernel = [
            [1, 4, 6, 4, 1],
            [4, 16, 24, 16, 4],
            [6, 24, 36, 24, 6],
            [4, 16, 24, 16, 4],
            [1, 4, 6, 4, 1]
        ]
        kernel_sum = 256
        result = [[0 for _ in range(width)] for _ in range(height)]
        kernel_size = 5
        offset = kernel_size // 2
        extended = [[0 for _ in range(width + kernel_size)] for _ in range(height + kernel_size)]
        for y in range(height):
            for x in range(width):
                extended[y + offset][x + offset] = channel_data[y][x]
        
        for y in range(offset):
            for x in range(width + kernel_size):
                extended[y][x] = extended[offset + (offset - y)][x]

        for y in range(offset):
            for x in range(width + kernel_size):
                extended[height + offset + y][x] = extended[height + offset - 1 - y][x]

        for y in range(height + kernel_size):
            for x in range(offset):
                extended[y][x] = extended[y][offset + (offset - x)]

        for y in range(height + kernel_size):
            for x in range(offset):
                extended[y][width + offset + x] = extended[y][width + offset - 1 - x]
        
        for y in range(height):
            for x in range(width):
                total = 0
                for ky in range(kernel_size):
                    for kx in range(kernel_size):
                        total += extended[y + ky][x + kx] * gaussian_kernel[ky][kx]
                result[y][x] = total / kernel_sum
        return result
    
    def apply_laplacian_filter(self, channel_data, width, height):
        laplacian_kernel = [
            [0, -1, 0],
            [-1, 4, -1],
            [0, -1, 0]
        ]
        result = [[0 for _ in range(width)] for _ in range(height)]
        kernel_size = 3
        offset = kernel_size // 2
        extended = [[0 for _ in range(width + kernel_size)] for _ in range(height + kernel_size)]
        for y in range(height):
            for x in range(width):
                extended[y + offset][x + offset] = channel_data[y][x]
        
        for y in range(offset):
            for x in range(width + kernel_size):
                extended[y][x] = extended[offset + (offset - y)][x]
    
        for y in range(offset):
            for x in range(width + kernel_size):
                extended[height + offset + y][x] = extended[height + offset - 1 - y][x]
    
        for y in range(height + kernel_size):
            for x in range(offset):
                extended[y][x] = extended[y][offset + (offset - x)]
    
        for y in range(height + kernel_size):
            for x in range(offset):
                extended[y][width + offset + x] = extended[y][width + offset - 1 - x]
        
        for y in range(height):
            for x in range(width):
                total = 0
                for ky in range(kernel_size):
                    for kx in range(kernel_size):
                        total += extended[y + ky][x + kx] * laplacian_kernel[ky][kx]
                result[y][x] = total
        max_abs = max(max(abs(val) for val in row) for row in result) if result else 1
        if max_abs > 0:
            for y in range(height):
                for x in range(width):
                    result[y][x] = result[y][x] / max_abs
        return result

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

    def run(self):
        self.root.mainloop()

window = Window("Обработчик изображений")
window.run()