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
        self.root.geometry(f"1300x500+{x}+{y}")
        self.root.resizable(False, False)
        self.root.overrideredirect(True)
        self.image_path = None
        self.photo_image = None
        self.png_points = None
        self.png_points2 = None
        self.widgets()
    
    def window_center(self, x, y):
        x = (x-1300)//2
        y = (y-500)//2
        return x, y
    
    def widgets(self):
        self.button1 = Button(self.root, text = "Выбрать картинку", command = self.select_image)
        self.button1.place(relx = 0.005, rely = 0.005, relwidth = 0.3, relheight = 0.1)
        self.button2 = Button(self.root, text = "Обработать", command = self.processing_image)
        self.button2.place(relx = 0.325, rely = 0.005, relwidth = 0.3, relheight = 0.1)
        self.button3 = Button(self.root, text = "Сохранить", command = self.saved_image)
        self.button3.place(relx = 0.645, rely = 0.005, relwidth = 0.3, relheight = 0.1)
        self.close_button = Button(self.root, text = "X", command = self.root.destroy)
        self.close_button.place(relx = 0.96, rely = 0.01, relwidth = 0.03, relheight = 0.05)
        self.frame1 = Frame(self.root)
        self.frame1.place(relx = 0.005, rely = 0.13, relwidth = 0.49, relheight = 0.86)
        self.frame2 = Frame(self.root)
        self.frame2.place(relx = 0.5, rely = 0.13, relwidth = 0.495, relheight = 0.86)
        self.scrolly1 = Scrollbar(self.frame1)
        self.scrolly1.grid(row = 0, column = 1, sticky = "ns")
        self.scrollx1 = Scrollbar(self.frame1, orient = HORIZONTAL)
        self.scrollx1.grid(row = 1, column = 0, sticky = "ew")
        self.scrolly2 = Scrollbar(self.frame2)
        self.scrolly2.grid(row = 0, column = 1, sticky = "ns")
        self.scrollx2 = Scrollbar(self.frame2, orient = HORIZONTAL)
        self.scrollx2.grid(row = 1, column = 0, sticky = "ew")
        self.canvas1 = Canvas(self.frame1, bg = "lightgray", yscrollcommand=self.scrolly1.set, xscrollcommand=self.scrollx1.set)
        self.canvas1.grid(row = 0, column = 0, sticky = "nsew")
        self.canvas2 = Canvas(self.frame2, bg = "gray", yscrollcommand=self.scrolly2.set, xscrollcommand=self.scrollx2.set)
        self.canvas2.grid(row = 0, column = 0, sticky = "nsew")
        self.frame1.grid_rowconfigure(0, weight = 1)
        self.frame1.grid_columnconfigure(0, weight = 1)
        self.scrolly1.config(command=self.canvas1.yview)
        self.scrollx1.config(command=self.canvas1.xview)
        self.frame2.grid_rowconfigure(0, weight = 1)
        self.frame2.grid_columnconfigure(0, weight = 1)
        self.scrolly2.config(command=self.canvas2.yview)
        self.scrollx2.config(command=self.canvas2.xview)
    
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
                    self.display_image(file_path)
                    self.png_points = self.getPixelArray()
                    self.canvas2.delete("all")
                    self.png_points2 = None
                except Exception as e:
                    showerror("Ошибка")
            else: showerror("формат не поддерживается")
    
    def display_image(self, file_path):
        self.canvas1.delete("all")
        try:
            self.photo_image = PhotoImage(file = file_path)
            img_width = self.photo_image.width()
            img_height = self.photo_image.height()
            self.orig_img_width = img_width
            self.orig_img_height = img_height
            canvas_width = self.canvas1.winfo_width()
            canvas_height = self.canvas1.winfo_height()
            x_offset = max(0, (canvas_width - img_width) // 2)
            y_offset = max(0, (canvas_height - img_height) // 2)
            scrollregion_width = max(img_width + 2*x_offset, canvas_width)
            scrollregion_height = max(img_height + 2*y_offset, canvas_height)
            self.canvas1.config(scrollregion=(0, 0, scrollregion_width, scrollregion_height))
            self.canvas_image_id = self.canvas1.create_image(x_offset, y_offset, image=self.photo_image, anchor="nw")
            if img_width > canvas_width or img_height > canvas_height:
                self.canvas1.xview_moveto(0.5 - (canvas_width / (2 * scrollregion_width)))
                self.canvas1.yview_moveto(0.5 - (canvas_height / (2 * scrollregion_height)))
            self.canvas1.update_idletasks()
        except Exception as e:
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
                        pixel_dict = {1: hex_color}
                        row.append(pixel_dict)
                    except:
                        row.append({1: "#FFFFFF"})
                png_points.append(row)
            return png_points
        except Exception as e:
            print(f"Ошибка при создании массива: {e}")
            return None

    def processing_image(self):
        if not self.photo_image:
            showerror("Ошибка", "Сначала загрузите изображение")
            return
        height = len(self.png_points)
        width = len(self.png_points[0]) if height > 0 else 0
        y1 = int(0.55 * height)
        y2 = int(0.95 * height)
        x1 = int(0.05 * width)
        x2 = int(0.45 * width)
        cent_width = int(0.5 * width)
        self.png_points2 = []
        for i in range(height):
            row = []
            for j in range(width):
                row.append({1: "#FFFFFF"})
            self.png_points2.append(row)
        for i in range(y1, y2):
            for j in range(x1, x2):
                if 0 <= i < height and 0 <= j + cent_width < width:
                    self.png_points2[i][j + cent_width] = self.png_points[i][j]
        for i in range(height):
            self.png_points2[i][cent_width] = {1: "#000000"}
            if i == int(0.1 * height) or i == int(0.2 * height) or i == int(0.3 * height) or i == int(0.4 * height) or i == int(0.6 * height) or i == int(0.7 * height) or i == int(0.8 * height) or i == int(0.9 * height):
                self.png_points2[i][cent_width - 2] = {1: "#000000"}
                self.png_points2[i][cent_width - 1] = {1: "#000000"}
                self.png_points2[i][cent_width + 1] = {1: "#000000"}
                self.png_points2[i][cent_width + 2] = {1: "#000000"}
            if i == int(0.4 * height):
                self.png_points2[i + 2][cent_width + 4] = {1: "#000000"}
                self.png_points2[i + 2][cent_width + 5] = {1: "#000000"}
                self.png_points2[i + 2][cent_width + 6] = {1: "#000000"}
                self.png_points2[i + 2][cent_width + 7] = {1: "#000000"}
                self.png_points2[i + 2][cent_width + 8] = {1: "#000000"}
                self.png_points2[i + 1][cent_width + 6] = {1: "#000000"}
                self.png_points2[i][cent_width + 6] = {1: "#000000"}
                self.png_points2[i - 1][cent_width + 6] = {1: "#000000"}
                self.png_points2[i - 2][cent_width + 6] = {1: "#000000"}
                self.png_points2[i - 3][cent_width + 6] = {1: "#000000"}
                self.png_points2[i - 4][cent_width + 6] = {1: "#000000"}
                self.png_points2[i - 5][cent_width + 6] = {1: "#000000"}
                self.png_points2[i - 4][cent_width + 5] = {1: "#000000"}
                self.png_points2[i - 3][cent_width + 4] = {1: "#000000"}
            if i == int(0.5 * height):
                self.png_points2[i - 2][cent_width + 4] = {1: "#000000"}
                self.png_points2[i - 2][cent_width + 5] = {1: "#000000"}
                self.png_points2[i - 2][cent_width + 6] = {1: "#000000"}
                self.png_points2[i - 2][cent_width + 7] = {1: "#000000"}
                self.png_points2[i - 2][cent_width + 8] = {1: "#000000"}
                self.png_points2[i - 3][cent_width + 4] = {1: "#000000"}
                self.png_points2[i - 4][cent_width + 4] = {1: "#000000"}
                self.png_points2[i - 5][cent_width + 4] = {1: "#000000"}
                self.png_points2[i - 6][cent_width + 4] = {1: "#000000"}
                self.png_points2[i - 7][cent_width + 4] = {1: "#000000"}
                self.png_points2[i - 8][cent_width + 4] = {1: "#000000"}
                self.png_points2[i - 9][cent_width + 4] = {1: "#000000"}
                self.png_points2[i - 3][cent_width + 8] = {1: "#000000"}
                self.png_points2[i - 4][cent_width + 8] = {1: "#000000"}
                self.png_points2[i - 5][cent_width + 8] = {1: "#000000"}
                self.png_points2[i - 6][cent_width + 8] = {1: "#000000"}
                self.png_points2[i - 7][cent_width + 8] = {1: "#000000"}
                self.png_points2[i - 8][cent_width + 8] = {1: "#000000"}
                self.png_points2[i - 9][cent_width + 8] = {1: "#000000"}
                self.png_points2[i - 9][cent_width + 5] = {1: "#000000"}
                self.png_points2[i - 9][cent_width + 6] = {1: "#000000"}
                self.png_points2[i - 9][cent_width + 7] = {1: "#000000"}
        for j in range(width):
            self.png_points2[int(0.5 * height)][j] = {1: "#000000"}
            x = (j - cent_width) * 10 / width
            y = 10 - (x * math.sin(x) + 5)
            y = int(y * height / 10)
            self.png_points2[y][j] = {1: "#000000"}
            if j == int(0.1 * width) or j == int(0.2 * width) or j == int(0.3 * width) or j == int(0.4 * width) or j == int(0.6 * width) or j == int(0.7 * width) or j == int(0.8 * width) or j == int(0.9 * width):
                self.png_points2[int(0.5 * height) - 2][j] = {1: "#000000"}
                self.png_points2[int(0.5 * height) - 1][j] = {1: "#000000"}
                self.png_points2[int(0.5 * height) + 1][j] = {1: "#000000"}
                self.png_points2[int(0.5 * height) + 2][j] = {1: "#000000"}
            if j == int(0.6 * width):
                self.png_points2[int(0.5 * height) - 2][j - 2] = {1: "#000000"}
                self.png_points2[int(0.5 * height) - 2][j - 1] = {1: "#000000"}
                self.png_points2[int(0.5 * height) - 2][j] = {1: "#000000"}
                self.png_points2[int(0.5 * height) - 2][j + 1] = {1: "#000000"}
                self.png_points2[int(0.5 * height) - 2][j + 2] = {1: "#000000"}
                self.png_points2[int(0.5 * height) - 3][j] = {1: "#000000"}
                self.png_points2[int(0.5 * height) - 4][j] = {1: "#000000"}
                self.png_points2[int(0.5 * height) - 5][j] = {1: "#000000"}
                self.png_points2[int(0.5 * height) - 6][j] = {1: "#000000"}
                self.png_points2[int(0.5 * height) - 7][j] = {1: "#000000"}
                self.png_points2[int(0.5 * height) - 8][j] = {1: "#000000"}
                self.png_points2[int(0.5 * height) - 7][j - 1] = {1: "#000000"}
                self.png_points2[int(0.5 * height) - 6][j - 2] = {1: "#000000"}
        self.canvas2.delete("all")
        processed_image = PhotoImage(width=width, height=height)
        for y in range(height):
            for x in range(width):
                pixel_dict = self.png_points2[y][x]
                hex_color = pixel_dict.get(1, "#FFFFFF")
                processed_image.put(hex_color, (x, y))
        self.processed_photo = processed_image
        canvas_width = self.canvas2.winfo_width()
        canvas_height = self.canvas2.winfo_height()
        x_offset = max(0, (canvas_width - width) // 2)
        y_offset = max(0, (canvas_height - height) // 2)
        scrollregion_width = max(width + 2*x_offset, canvas_width)
        scrollregion_height = max(height + 2*y_offset, canvas_height)
        self.canvas2.config(scrollregion=(0, 0, scrollregion_width, scrollregion_height))
        self.canvas_image_id = self.canvas2.create_image(x_offset, y_offset, image=self.processed_photo, anchor="nw")
        if width > canvas_width or height > canvas_height:
            self.canvas2.xview_moveto(0.5 - (canvas_width / (2 * scrollregion_width)))
            self.canvas2.yview_moveto(0.5 - (canvas_height / (2 * scrollregion_height)))
        self.canvas2.update_idletasks()

    def saved_image(self):
        if not self.image_path:
            showerror("Ошибка", "Сначала загрузите изображение")
            return
        try:
            directory = os.path.dirname(self.image_path)
            filename = os.path.basename(self.image_path)
            name, ext = os.path.splitext(filename)
            output_filename = f"{name}_processed.png"
            output_path = os.path.join(directory, output_filename)
            counter = 1
            while os.path.exists(output_path):
                output_filename = f"{name}_processed_{counter}.png"
                output_path = os.path.join(directory, output_filename)
                counter += 1
            success = self.write_png_from_points(self.png_points2, output_path)
            
        except Exception as e:
            showerror("Ошибка", f"Не удалось сохранить изображение: {str(e)}")

    def write_png_from_points(self, png_points, filename):
        try:
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
                        if i < len(png_points) and j < len(png_points[i]):
                            pixel_dict = png_points[i][j]
                            hex_color = pixel_dict.get(1, "#FFFFFF")
                            if hex_color.startswith('#') and len(hex_color) == 7:
                                r = int(hex_color[1:3], 16)
                                g = int(hex_color[3:5], 16)
                                b = int(hex_color[5:7], 16)
                            else:
                                r = g = b = 0
                        else:
                            r = g = b = 0
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