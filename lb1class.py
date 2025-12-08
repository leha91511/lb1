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
        self.widgets()
    
    def window_center(self, x, y):
        x = (x-800)//2
        y = (y-500)//2
        return x, y
    
    def widgets(self):
        self.button1 = Button(self.root, text = "Выбрать картинку", command = self.select_image)
        self.button1.place(relx = 0.01, rely = 0.01, relwidth = 0.3, relheight = 0.1)
        self.button2 = Button(self.root, text = "Обработать", command = self.processing_image)
        self.button2.place(relx = 0.33, rely = 0.01, relwidth = 0.3, relheight = 0.1)
        self.button3 = Button(self.root, text = "Сохранить", command = self.saved_image)
        self.button3.place(relx = 0.65, rely = 0.01, relwidth = 0.3, relheight = 0.1)
        self.close_button = Button(self.root, text = "X", command = self.root.destroy)
        self.close_button.place(relx = 0.96, rely = 0.01, relwidth = 0.03, relheight = 0.05)
        self.frame = Frame(self.root)
        self.frame.place(relx = 0.01, rely = 0.13, relwidth = 0.98, relheight = 0.86)
        self.scrolly = Scrollbar(self.frame)
        self.scrolly.grid(row = 0, column = 1, sticky = "ns")
        self.scrollx = Scrollbar(self.frame, orient = HORIZONTAL)
        self.scrollx.grid(row = 1, column = 0, sticky = "ew")
        self.canvas1 = Canvas(self.frame, bg = "lightgray", yscrollcommand=self.scrolly.set, xscrollcommand=self.scrollx.set)
        self.canvas1.grid(row = 0, column = 0, sticky = "nsew")
        self.frame.grid_rowconfigure(0, weight = 1)
        self.frame.grid_columnconfigure(0, weight = 1)
        self.scrolly.config(command=self.canvas1.yview)
        self.scrollx.config(command=self.canvas1.xview)
    
    def run(self):
        self.root.mainloop()
    
    def select_image(self):
        file_types = [
            ("Поддерживаемые форматы", "*.png *.gif *.ppm"),
            ("PNG файлы", "*.png"),
            ("GIF файлы", "*.gif"), 
            ("PPM файлы", "*.ppm"),
            ("Все файлы", "*.*")]
        file_path = askopenfilename(title = "Выбрать изображение", filetypes = file_types)
        if file_path:
            self.image_path = file_path
            file_ext = os.path.splitext(file_path)[1].lower()
            supported_formats = ['.png', '.gif', '.ppm']
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
    
    def processing_image(self):
        if not self.photo_image:
            showerror("Ошибка", "Сначала загрузите изображение")
            return
        canvas_width = self.canvas1.winfo_width()
        canvas_height = self.canvas1.winfo_height()
        x_offset = max(0, (canvas_width - self.orig_img_width) // 2)
        y_offset = max(0, (canvas_height - self.orig_img_height) // 2)
        left_edge_x = x_offset
        right_edge_x = x_offset + (self.orig_img_width - 1)
        center_x = (left_edge_x + right_edge_x) // 2
        top_edge_y = y_offset
        bottom_edge_y = y_offset + (self.orig_img_height - 1)
        img_width = self.orig_img_width
        img_height = self.orig_img_height
        img_left_x = 0
        img_top_y = 0
        img_center_x = img_width // 2
        img_bottom_y = img_height - 1
        self.canvas1.create_line(left_edge_x, top_edge_y, left_edge_x + 1, top_edge_y, fill = f"#{255:02x}{127:02x}{127:02x}")
        self.png_points[img_top_y][img_left_x] = {1: f"#{255:02x}{127:02x}{127:02x}"}
        self.canvas1.create_line(center_x, top_edge_y, center_x + 1, top_edge_y, fill = f"#{127:02x}{255:02x}{127:02x}")
        self.png_points[img_top_y][img_center_x] = {1: f"#{127:02x}{255:02x}{127:02x}"}
        self.canvas1.create_line(left_edge_x, bottom_edge_y, left_edge_x + 1, bottom_edge_y, fill = f"#{127:02x}{127:02x}{255:02x}")
        self.png_points[img_bottom_y][img_left_x] = {1: f"#{127:02x}{127:02x}{255:02x}"}

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
            success = self.write_png_from_points(self.png_points, output_path)
            
        except Exception as e:
            showerror("Ошибка", f"Не удалось сохранить изображение: {str(e)}")


window = Window("Обработчик изображений")
window.run()