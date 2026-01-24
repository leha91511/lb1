from tkinter import *
from tkinter import PhotoImage
from tkinter.ttk import *
from tkinter.filedialog import *
from tkinter.messagebox import *
import os, struct, zlib

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
        self.png_points = None
        self.png_points2 = None
        self.widgets()
    
    def window_center(self, x, y):
        x = (x - 800) // 2
        y = (y - 500) // 2
        return x, y
    
    def widgets(self):
        self.button1 = Button(self.root, text = "Выбрать картинку", command = self.select_image)
        self.button1.place(relx = 0.01, rely = 0.01, relwidth = 0.18, relheight = 0.1)
        self.button2 = Button(self.root, text = "Обработать", command = self.processing_image)
        self.button2.place(relx = 0.2, rely = 0.01, relwidth = 0.18, relheight = 0.1)
        self.button3 = Button(self.root, text = "Выбрать картинку для наложения", command = self.select_image2)
        self.button3.place(relx = 0.39, rely = 0.01, relwidth = 0.18, relheight = 0.1)
        self.button4 = Button(self.root, text = "Обработать (только красный)", command = self.processing_image_red)
        self.button4.place(relx = 0.58, rely = 0.01, relwidth = 0.18, relheight = 0.1)
        self.button5 = Button(self.root, text = "Сохранить", command = self.saved_image)
        self.button5.place(relx = 0.77, rely = 0.01, relwidth = 0.18, relheight = 0.1)
        self.close_button = Button(self.root, text = "X", command = self.root.destroy)
        self.close_button.place(relx = 0.96, rely = 0.01, relwidth = 0.03, relheight = 0.05)
        self.frame = Frame(self.root)
        self.frame.place(relx = 0.01, rely = 0.13, relwidth = 0.98, relheight = 0.86)
        self.scrolly = Scrollbar(self.frame)
        self.scrolly.grid(row = 0, column = 1, sticky = "ns")
        self.scrollx = Scrollbar(self.frame, orient = HORIZONTAL)
        self.scrollx.grid(row = 1, column = 0, sticky = "ew")
        self.canvas1 = Canvas(self.frame, bg = "lightgray", yscrollcommand = self.scrolly.set, xscrollcommand = self.scrollx.set)
        self.canvas1.grid(row = 0, column = 0, sticky = "nsew")
        self.frame.grid_rowconfigure(0, weight = 1)
        self.frame.grid_columnconfigure(0, weight = 1)
        self.scrolly.config(command=self.canvas1.yview)
        self.scrollx.config(command=self.canvas1.xview)
    
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
    
    def processing_image(self, levels = 10):
        if not self.photo_image:
            showerror("Ошибка", "Сначала загрузите изображение")
            return
        if not self.png_points:
            return False
        self.canvas1.delete("all")
        canvas_width = self.canvas1.winfo_width()
        canvas_height = self.canvas1.winfo_height()
        img_height = len(self.png_points)
        img_width = len(self.png_points[0]) if img_height > 0 else 0
        x_offset = max(0, (canvas_width - img_width) // 2)
        y_offset = max(0, (canvas_height - img_height) // 2)
        self.png_points2 = []
        for y in range(len(self.png_points)):
            row = []
            for x in range(len(self.png_points[y])):
                png_color = self.png_points[y][x]
                png_color = png_color[1:]
                r = int(png_color[0:2], 16)
                g = int(png_color[2:4], 16)
                b = int(png_color[4:6], 16)
                rr = (r * (levels-1) // 255) * (255 // (levels-1))
                gg = (g * (levels-1) // 255) * (255 // (levels-1))
                bb = (b * (levels-1) // 255) * (255 // (levels-1))
                new_hex = f"#{rr:02x}{gg:02x}{bb:02x}"
                row.append(new_hex)
                self.canvas1.create_line(x + x_offset, y + y_offset, x + x_offset + 1, y + y_offset, fill = new_hex)
            self.png_points2.append(row)
    
    def processing_image_red(self, levels = 10):
        if not self.photo_image:
            showerror("Ошибка", "Сначала загрузите изображение")
            return
        if not self.png_points:
            return False
        self.canvas1.delete("all")
        canvas_width = self.canvas1.winfo_width()
        canvas_height = self.canvas1.winfo_height()
        img_height = len(self.png_points)
        img_width = len(self.png_points[0]) if img_height > 0 else 0
        x_offset = max(0, (canvas_width - img_width) // 2)
        y_offset = max(0, (canvas_height - img_height) // 2)
        self.png_points2 = []
        for y in range(len(self.png_points)):
            row = []
            for x in range(len(self.png_points[y])):
                png_color = self.png_points[y][x]
                png_color = png_color[1:]
                r = int(png_color[0:2], 16)
                g = int(png_color[2:4], 16)
                b = int(png_color[4:6], 16)
                rr = (r * (levels-1) // 255) * (255 // (levels-1))
                gg = g
                bb = b
                new_hex = f"#{rr:02x}{gg:02x}{bb:02x}"
                row.append(new_hex)
                self.canvas1.create_line(x + x_offset, y + y_offset, x + x_offset + 1, y + y_offset, fill = new_hex)
            self.png_points2.append(row)

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
                        row.append(pixel_dict)
                    except:
                        row.append("#FFFFFF")
                png_points.append(row)
            return png_points
        except Exception as e:
            print(f"Ошибка при создании массива: {e}")
            return None

    def select_image2(self):
        if not self.png_points:
            showerror("Ошибка", "сначала выберите основное изображение")
            return
        file_types = [
            ("Поддерживаемые форматы", "*.png *.ppm"),
            ("PNG файлы", "*.png"),
            ("PPM файлы", "*.ppm"),
            ("Все файлы", "*.*")]
        file_path = askopenfilename(title = "Выбрать изображение для наложения", filetypes = file_types)
        if file_path:
            self.image_path = file_path
            file_ext = os.path.splitext(file_path)[1].lower()
            supported_formats = ['.png', '.ppm']
            if file_ext in supported_formats:
                try:
                    self.display_image(file_path)
                    png_points = self.getPixelArray()
                except Exception as e:
                    showerror("Ошибка")
            else: showerror("формат не поддерживается")
        self.overlay_image(png_points)

    def overlay_image(self, png_points):
        self.canvas1.delete("all")
        canvas_width = self.canvas1.winfo_width()
        canvas_height = self.canvas1.winfo_height()
        img_height = len(self.png_points)
        img_width = len(self.png_points[0]) if img_height > 0 else 0
        second_height = len(png_points)
        second_width = len(png_points[0]) if second_height > 0 else 0
        height = min(img_height, second_height)
        width = min(img_width, second_width)
        x_offset = max(0, (canvas_width - width) // 2)
        y_offset = max(0, (canvas_height - height) // 2)
        self.png_points2 = []
        for y in range(height):
            row = []
            for x in range(width):
                png_color = self.png_points[y][x]
                png_color = png_color[1:]
                r = int(png_color[0:2], 16)
                g = int(png_color[2:4], 16)
                b = int(png_color[4:6], 16)
                png_color2 = png_points[y][x]
                png_color2 = png_color2[1:]
                rr = int(png_color2[0:2], 16)
                gg = int(png_color2[2:4], 16)
                bb = int(png_color2[4:6], 16)
                if rr == 255 and gg == 255 and bb == 255:
                    new_hex = f"#{r:02x}{g:02x}{b:02x}"
                else:
                    new_hex = f"#{(int((rr + r) / 2)):02x}{(int((gg + g) / 2)):02x}{(int((bb + b) / 2)):02x}"
                row.append(new_hex)
                self.canvas1.create_line(x + x_offset, y + y_offset, x + x_offset + 1, y + y_offset, fill = new_hex)
            self.png_points2.append(row)

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
                        hex_color =  png_points[i][j]
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
            self.write_png_from_points(self.png_points2, output_path)
            
        except Exception as e:
            showerror("Ошибка", f"Не удалось сохранить изображение: {str(e)}")

window = Window("Обработчик изображений")
window.run()