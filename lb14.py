from tkinter import *
from tkinter.ttk import *
import math

class Window:
    def __init__(self, title):
        self.root = Tk()
        self.root.title(title)
        self.root.attributes('-fullscreen', True)
        self.x = 0
        self.y = 0
        self.z = 0
        self.yaw = 0
        self.pitch = 0
        self.speed = 5
        self.angle_speed = 170
        self.keys_pressed = {'w': False, 's': False, 'a': False, 'd': False, 'space': False, 'ctrl': False, 'num4': False, 'num6': False, 'num2': False, 'num8': False}
        self.animation_id = None
        self.roberts_method = 1
        self.faces_tetrahedron = [
            (0, 1, 2), (0, 2, 3), (0, 1, 3), (1, 2, 3)
        ]
        self.faces_dodecahedron = [
            (3, 17, 11, 1, 16), (3, 12, 18, 7, 17), (3, 12, 2, 10, 16),
            (0, 8, 4, 15, 9), (0, 8, 14, 2, 10), (0, 10, 16, 1, 9),
            (13, 4, 8, 14, 6), (13, 4, 15, 5, 19), (13, 6, 18, 7, 19),
            (5, 11, 1, 9, 15), (5, 11, 17, 7, 19), (2, 12, 18, 6, 14)
        ]
        self.faces_dodecahedron2 = [
            (3, 17, 11), (3, 11, 1), (3, 1, 16),
            (3, 12, 18), (3, 18, 7), (3, 7, 17),
            (3, 12, 2), (3, 2, 10), (3, 10, 16),
            (0, 8, 4), (0, 4, 15), (0, 15, 9),
            (0, 8, 14), (0, 14, 2), (0, 2, 10),
            (0, 10, 16), (0, 16, 1), (0, 1, 9),
            (13, 4, 8), (13, 8, 14), (13, 14, 6),
            (13, 4, 15), (13, 15, 5), (13, 5, 19),
            (13, 6, 18), (13, 18, 7), (13, 7, 19),
            (5, 11, 1), (5, 1, 9), (5, 9, 15),
            (5, 11, 17), (5, 17, 7), (5, 7, 19),
            (2, 12, 18), (2, 18, 6), (2, 6, 14)
        ]
        self.figures = []
        self.widget()
        self.bind_keys()
        self.start_animation()
    
    def widget(self):
        self.canvas = Canvas(self.root, takefocus = 0)
        self.canvas.place(relx = 0, rely = 0.1, relwidth = 1, relheight = 0.9)
        self.button_exit = Button(self.root, text = "X", command = self.root.destroy)
        self.button_exit.place(relx = 0.97, rely = 0.005, relwidth = 0.025, relheight = 0.05)

        self.point1 = Label(self.root, text = "первая точка фигуры(x, y, z):")
        self.point1.place(relx = 0.005, rely = 0.005)
        self.x_1 = Spinbox(self.root, from_ = -20, to = 20, increment = 0.01, width = 5, font = "Calibri")
        self.x_1.place(relx = 0.12, rely = 0.005)
        self.y_1 = Spinbox(self.root, from_ = -20, to = 20, increment = 0.01, width = 5, font = "Calibri")
        self.y_1.place(relx = 0.165, rely = 0.005)
        self.z_1 = Spinbox(self.root, from_ = -20, to = 20, increment = 0.01, width = 5, font = "Calibri")
        self.z_1.place(relx = 0.21, rely = 0.005)
        self.point2 = Label(self.root, text = "вторая точка фигуры(x, y, z):")
        self.point2.place(relx = 0.005, rely = 0.03)
        self.x_2 = Spinbox(self.root, from_ = -20, to = 20, increment = 0.01, width = 5, font = "Calibri")
        self.x_2.place(relx = 0.12, rely = 0.03)
        self.y_2 = Spinbox(self.root, from_ = -20, to = 20, increment = 0.01, width = 5, font = "Calibri")
        self.y_2.place(relx = 0.165, rely = 0.03)
        self.z_2 = Spinbox(self.root, from_ = -20, to = 20, increment = 0.01, width = 5, font = "Calibri")
        self.z_2.place(relx = 0.21, rely = 0.03)
        
        self.piram_points1 = Label(self.root, text = "Задайте количество точек в основании пирамиды")
        self.piram_points1.place(relx = 0.26, rely = 0.005)
        self.piram_points2 = Spinbox(self.root, from_ = 3, to = 15, increment = 1, width = 5, font = "Calibri")
        self.piram_points2.place(relx = 0.45, rely = 0.005)
        self.clipping_height = Label(self.root, text = "Задайте высоту среза пирамиды в %")
        self.clipping_height.place(relx = 0.26, rely = 0.03)
        self.clip = Spinbox(self.root, from_ = 0, to = 100, increment = 1, width = 5, font = "Calibri")
        self.clip.place(relx = 0.45, rely = 0.03)
        self.piramid = Button(self.root, text = "Добавить пирамиду", command = self.calculate_piramid_vertices)
        self.piramid.place(relx = 0.26, rely = 0.055, relwidth = 0.1, relheight = 0.05)
        self.culinder = Button(self.root, text = "Добавить цилиндр", command = self.calculate_culinder_vertices)
        self.culinder.place(relx = 0.36, rely = 0.055, relwidth = 0.1, relheight = 0.05)
        self.tetrahedron = Button(self.root, text = "Добавить тетраэдр", command = self.calculate_tetrahedron_vertices)
        self.tetrahedron.place(relx = 0.46, rely = 0.055, relwidth = 0.1, relheight = 0.05)
        self.dodecahedron = Button(self.root, text = "Добавить додекаэдр", command = self.calculate_dodecahedron_vertices)
        self.dodecahedron.place(relx = 0.56, rely = 0.055, relwidth = 0.1, relheight = 0.05)
        self.rad_culinder = Label(self.root, text = "Задайте радиус для фигуры:")
        self.rad_culinder.place(relx = 0.5, rely = 0.005)
        self.radius = Spinbox(self.root, from_ = 0, to = 10, increment = 0.01, width = 5, font = "Calibri")
        self.radius.place(relx = 0.62, rely = 0.005)
        self.pos_and_angle = Label(self.root, text = self.get_display_text())
        self.pos_and_angle.place(relx = 0.005, rely = 0.105)

        self.btn_method1 = Button(self.root, text="Метод 1", command = lambda: self.set_roberts_method(1))
        self.btn_method1.place(relx = 0.7, rely = 0.005, relwidth = 0.07, relheight = 0.04)
        self.btn_method2 = Button(self.root, text="Метод 2", command = lambda: self.set_roberts_method(2))
        self.btn_method2.place(relx = 0.78, rely = 0.005, relwidth = 0.07, relheight = 0.04)
        self.btn_method3 = Button(self.root, text="Метод 3", command = lambda: self.set_roberts_method(3))
        self.btn_method3.place(relx = 0.86, rely = 0.005, relwidth = 0.07, relheight = 0.04)

        self.x_1.set(0)
        self.y_1.set(0)
        self.z_1.set(0)
        self.x_2.set(0)
        self.y_2.set(1)
        self.z_2.set(0)
        self.piram_points2.set(3)
        self.clip.set(50)
        self.radius.set(0)

        self.canvas.bind('<Button-1>', lambda e: self.root.focus_set())

    def set_roberts_method(self, method):
        self.roberts_method = method

    def get_display_text(self):
        return f"Позиция камеры: x={self.x:.1f}, y={self.y:.1f}, z={self.z:.1f}, направление взора: горизонтальное={self.yaw}°, вертикальное={self.pitch}°"

    def update_display(self):
        self.pos_and_angle.config(text = f"Позиция камеры: x={self.x:.1f}, y={self.y:.1f}, z={self.z:.1f}, направление взора: горизонтальное={self.yaw}°, вертикальное={self.pitch}°")

    def bind_keys(self):
        self.root.bind_all('<w>', lambda e: self.set_key('w', True))
        self.root.bind_all('<s>', lambda e: self.set_key('s', True))
        self.root.bind_all('<a>', lambda e: self.set_key('a', True))
        self.root.bind_all('<d>', lambda e: self.set_key('d', True))
        self.root.bind_all('<space>', lambda e: self.set_key('space', True))
        self.root.bind_all('<Control_L>', lambda e: self.set_key('ctrl', True))
        self.root.bind_all('<KeyRelease-w>', lambda e: self.set_key('w', False))
        self.root.bind_all('<KeyRelease-s>', lambda e: self.set_key('s', False))
        self.root.bind_all('<KeyRelease-a>', lambda e: self.set_key('a', False))
        self.root.bind_all('<KeyRelease-d>', lambda e: self.set_key('d', False))
        self.root.bind_all('<KeyRelease-space>', lambda e: self.set_key('space', False))
        self.root.bind_all('<KeyRelease-Control_L>', lambda e: self.set_key('ctrl', False))
        self.root.bind_all('<Left>', lambda e: self.set_key('num6', True))
        self.root.bind_all('<Right>', lambda e: self.set_key('num4', True))
        self.root.bind_all('<Down>', lambda e: self.set_key('num2', True))
        self.root.bind_all('<Up>', lambda e: self.set_key('num8', True))
        self.root.bind_all('<KeyRelease-Left>', lambda e: self.set_key('num6', False))
        self.root.bind_all('<KeyRelease-Right>', lambda e: self.set_key('num4', False))
        self.root.bind_all('<KeyRelease-Down>', lambda e: self.set_key('num2', False))
        self.root.bind_all('<KeyRelease-Up>', lambda e: self.set_key('num8', False))
        self.root.focus_set()
        self.root.focus_force()

    def set_key(self, key, state):
        old_state = self.keys_pressed.get(key, False)
        self.keys_pressed[key] = state

    def update_position(self, delta_time):
        yaw_rad = math.radians(-self.yaw)
        forward_x = math.sin(yaw_rad)
        forward_z = math.cos(yaw_rad)
        right_x = math.cos(yaw_rad)
        right_z = -math.sin(yaw_rad)
        move_distance = self.speed * delta_time
        if self.keys_pressed['w']:
            self.x += forward_x * move_distance
            self.z += forward_z * move_distance
        if self.keys_pressed['s']:
            self.x -= forward_x * move_distance
            self.z -= forward_z * move_distance
        if self.keys_pressed['a']:
            self.x -= right_x * move_distance
            self.z -= right_z * move_distance
        if self.keys_pressed['d']:
            self.x += right_x * move_distance
            self.z += right_z * move_distance
        if self.keys_pressed['space']:
            self.y += move_distance
        if self.keys_pressed['ctrl']:
            self.y -= move_distance
        angle_change = self.angle_speed * delta_time
        if self.keys_pressed['num4']:
            self.yaw -= angle_change
        if self.keys_pressed['num6']:
            self.yaw += angle_change
        self.yaw = self.yaw % 360
        if self.keys_pressed['num2']:
            self.pitch -= angle_change
        if self.keys_pressed['num8']:
            self.pitch += angle_change
        self.pitch = max(-89, min(89, self.pitch))
        self.update_display()

    def animate(self):
        delta_time = 1.0 / 30.0
        self.update_position(delta_time)
        self.canvas.delete("all")
        self.draw_all()
        self.Roberts_algorithm()
        self.draw_axes()
        self.animation_id = self.root.after(int(1000 / 60), self.animate)

    def start_animation(self):
        if self.animation_id is None:
            self.animate()

    def stop_animation(self):
        if self.animation_id:
            self.root.after_cancel(self.animation_id)
            self.animation_id = None

    def run(self):
        try:
            self.root.mainloop()
        finally:
            self.stop_animation()

    def calculate_tetrahedron_vertices(self):
        try:
            x = float(self.x_1.get())
            y = float(self.y_1.get())
            z = float(self.z_1.get())
            radius = float(self.radius.get())
        except ValueError:
            x = y = z = 0
            radius = 1
        height = math.sqrt(2/3) * radius
        circumradius = math.sqrt(3/8) * radius
        angle = 2 * math.pi / 3
        horizontal_distance = circumradius * math.sqrt(2/3)
        vertices_relative = [
            (0, circumradius, 0),
            (horizontal_distance * math.cos(0), -height/2, horizontal_distance * math.sin(0)),
            (horizontal_distance * math.cos(angle), -height/2, horizontal_distance * math.sin(angle)),
            (horizontal_distance * math.cos(2 * angle), -height/2, horizontal_distance * math.sin(2 * angle))
        ]
        vertices = [(vx + x, vy + y, vz + z) for vx, vy, vz in vertices_relative]
        self.figures.append(("tetra", tuple(vertices), self.faces_tetrahedron, self.faces_tetrahedron, (x, y, z)))
    
    def calculate_dodecahedron_vertices(self):
        try:
            x = float(self.x_1.get())
            y = float(self.y_1.get())
            z = float(self.z_1.get())
            radius = float(self.radius.get())
        except ValueError:
            x = y = z = 0
            radius = 1
        phi = (1 + math.sqrt(5)) / 2
        scale = radius / (2 / phi)
        base_vertices = []
        for i in (-1, 1):
            for j in (-1, 1):
                for k in (-1, 1):
                    base_vertices.append((i, j, k))
        for s1 in (-1, 1):
            for s2 in (-1, 1):
                base_vertices.append((0, s1 / phi, s2 * phi))
                base_vertices.append((s1 / phi, s2 * phi, 0))
                base_vertices.append((s2 * phi, 0, s1 / phi))
        vertices = [(vx * scale + x, vy * scale + y, vz * scale + z) for vx, vy, vz in base_vertices]
        self.figures.append(("dodeca", tuple(vertices), self.faces_dodecahedron, self.faces_dodecahedron2, (x, y, z)))

    def calculate_piramid_vertices(self):
        try:
            x1 = float(self.x_1.get())
            y1 = float(self.y_1.get())
            z1 = float(self.z_1.get())
            x2 = float(self.x_2.get())
            y2 = float(self.y_2.get())
            z2 = float(self.z_2.get())
            radius = float(self.radius.get())
            piramid_points = int(self.piram_points2.get())
            cut = float(self.clip.get()) / 100
        except ValueError:
            x1 = x2 = y1 = y2 = z1 = z2 = 0
            radius = 1
            piramid_points = 3
            cut = 0.5
        axis_vector = (x2 - x1, y2 - y1, z2 - z1)
        axis_length = math.sqrt(axis_vector[0] ** 2 + axis_vector[1] ** 2 + axis_vector[2] ** 2)
        if axis_length < 0.001:
            axis_vector = (0, 1, 0)
            axis_length = 1
        axis_direction = (axis_vector[0] / axis_length, axis_vector[1] / axis_length, axis_vector[2] / axis_length)
        if abs(axis_direction[0]) < 0.9:
            temp_vector = (1, 0, 0)
        else:
            temp_vector = (0, 1, 0)
        basis_u = (
            axis_direction[1] * temp_vector[2] - axis_direction[2] * temp_vector[1],
            axis_direction[2] * temp_vector[0] - axis_direction[0] * temp_vector[2],
            axis_direction[0] * temp_vector[1] - axis_direction[1] * temp_vector[0]
        )
        basis_u_length = math.sqrt(basis_u[0]**2 + basis_u[1]**2 + basis_u[2]**2)
        if basis_u_length > 0:
            basis_u = (basis_u[0] / basis_u_length, 
                    basis_u[1] / basis_u_length, 
                    basis_u[2] / basis_u_length)
        basis_v = (
            axis_direction[1] * basis_u[2] - axis_direction[2] * basis_u[1],
            axis_direction[2] * basis_u[0] - axis_direction[0] * basis_u[2],
            axis_direction[0] * basis_u[1] - axis_direction[1] * basis_u[0]
        )
        basis_v_length = math.sqrt(basis_v[0]**2 + basis_v[1]**2 + basis_v[2]**2)
        if basis_v_length > 0:
            basis_v = (basis_v[0] / basis_v_length, 
                    basis_v[1] / basis_v_length, 
                    basis_v[2] / basis_v_length)
        bottom_vertices = []
        angle_step = 2 * math.pi / piramid_points
        for i in range(piramid_points):
            angle = i * angle_step
            local_x = radius * math.cos(angle)
            local_z = radius * math.sin(angle)
            world_x = x1 + local_x * basis_u[0] + local_z * basis_v[0]
            world_y = y1 + local_x * basis_u[1] + local_z * basis_v[1]
            world_z = z1 + local_x * basis_u[2] + local_z * basis_v[2]
            bottom_vertices.append((world_x, world_y, world_z))
        top_vertices = []
        top_radius = radius * (1 - cut)
        top_center = (
            x1 + axis_direction[0] * axis_length * cut,
            y1 + axis_direction[1] * axis_length * cut,
            z1 + axis_direction[2] * axis_length * cut
        )
        for i in range(piramid_points):
            angle = i * angle_step
            local_x = top_radius * math.cos(angle)
            local_z = top_radius * math.sin(angle)
            world_x = top_center[0] + local_x * basis_u[0] + local_z * basis_v[0]
            world_y = top_center[1] + local_x * basis_u[1] + local_z * basis_v[1]
            world_z = top_center[2] + local_x * basis_u[2] + local_z * basis_v[2]
            top_vertices.append((world_x, world_y, world_z))
        all_vertices = bottom_vertices + top_vertices
        faces = []
        faces.append(tuple(range(piramid_points)))
        faces.append(tuple(range(piramid_points, 2 * piramid_points)))
        for i in range(piramid_points):
            next_i = (i + 1) % piramid_points
            faces.append((i, next_i, piramid_points + next_i, piramid_points + i))
        faces2 = []
        for i in range(1, piramid_points - 1):
            faces2.append((0, i, i + 1))
        for i in range(1, piramid_points - 1):
            faces2.append((piramid_points, piramid_points + i, piramid_points + i + 1))
        for i in range(piramid_points):
            next_i = (i + 1) % piramid_points
            faces2.append((i, next_i, piramid_points + next_i))
            faces2.append((i, piramid_points + next_i, piramid_points + i))
        center_x = (x1 + top_center[0]) / 2
        center_y = (y1 + top_center[1]) / 2
        center_z = (z1 + top_center[2]) / 2
        self.figures.append(("piramid", tuple(all_vertices), tuple(faces), tuple(faces2), (center_x, center_y, center_z)))

    def calculate_culinder_vertices(self):
        try:
            x1 = float(self.x_1.get())
            y1 = float(self.y_1.get())
            z1 = float(self.z_1.get())
            x2 = float(self.x_2.get())
            y2 = float(self.y_2.get())
            z2 = float(self.z_2.get())
            radius = float(self.radius.get())
        except ValueError:
            x1 = x2 = y1 = y2 = z1 = z2 = 0
            radius = 1
        cylinder_points = 20
        axis_vector = (x2 - x1, y2 - y1, z2 - z1)
        axis_length = math.sqrt(axis_vector[0] ** 2 + axis_vector[1] ** 2 + axis_vector[2] ** 2)
        if axis_length < 0.001:
            axis_vector = (0, 1, 0)
            axis_length = 1
        axis_direction = (axis_vector[0] / axis_length, 
                        axis_vector[1] / axis_length, 
                        axis_vector[2] / axis_length)
        if abs(axis_direction[0]) < 0.9:
            temp_vector = (1, 0, 0)
        else:
            temp_vector = (0, 1, 0)
        basis_u = (
            axis_direction[1] * temp_vector[2] - axis_direction[2] * temp_vector[1],
            axis_direction[2] * temp_vector[0] - axis_direction[0] * temp_vector[2],
            axis_direction[0] * temp_vector[1] - axis_direction[1] * temp_vector[0]
        )
        basis_u_length = math.sqrt(basis_u[0] ** 2 + basis_u[1] ** 2 + basis_u[2] ** 2)
        if basis_u_length > 0:
            basis_u = (basis_u[0] / basis_u_length, 
                    basis_u[1] / basis_u_length, 
                    basis_u[2] / basis_u_length)
        basis_v = (
            axis_direction[1] * basis_u[2] - axis_direction[2] * basis_u[1],
            axis_direction[2] * basis_u[0] - axis_direction[0] * basis_u[2],
            axis_direction[0] * basis_u[1] - axis_direction[1] * basis_u[0]
        )
        basis_v_length = math.sqrt(basis_v[0] ** 2 + basis_v[1] ** 2 + basis_v[2] ** 2)
        if basis_v_length > 0:
            basis_v = (basis_v[0] / basis_v_length, 
                    basis_v[1] / basis_v_length, 
                    basis_v[2] / basis_v_length)
        bottom_vertices = []
        angle_step = 2 * math.pi / cylinder_points
        for i in range(cylinder_points):
            angle = i * angle_step
            local_x = radius * math.cos(angle)
            local_z = radius * math.sin(angle)
            world_x = x1 + local_x * basis_u[0] + local_z * basis_v[0]
            world_y = y1 + local_x * basis_u[1] + local_z * basis_v[1]
            world_z = z1 + local_x * basis_u[2] + local_z * basis_v[2]
            bottom_vertices.append((world_x, world_y, world_z))
        top_vertices = []
        for i in range(cylinder_points):
            angle = i * angle_step
            local_x = radius * math.cos(angle)
            local_z = radius * math.sin(angle)
            world_x = x2 + local_x * basis_u[0] + local_z * basis_v[0]
            world_y = y2 + local_x * basis_u[1] + local_z * basis_v[1]
            world_z = z2 + local_x * basis_u[2] + local_z * basis_v[2]
            top_vertices.append((world_x, world_y, world_z))
        all_vertices = bottom_vertices + top_vertices
        n = cylinder_points
        faces = []
        faces.append(tuple(range(n)))
        faces.append(tuple(range(n, 2*n)))
        for i in range(n):
            next_i = (i + 1) % n
            faces.append((i, next_i, n + next_i, n + i))
        faces2 = []
        for i in range(1, n-1):
            faces2.append((0, i, i+1))
        for i in range(1, n-1):
            faces2.append((n, n+i, n+i+1))
        for i in range(n):
            next_i = (i + 1) % n
            faces2.append((i, next_i, n + next_i))
            faces2.append((i, n + next_i, n + i))
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2
        center_z = (z1 + z2) / 2
        self.figures.append(("cylinder", tuple(all_vertices), tuple(faces), tuple(faces2), (center_x, center_y, center_z)))

    def world_to_screen(self, x, y, z):
        dx = x - self.x
        dy = y - self.y
        dz = z - self.z
        yaw_rad = math.radians(self.yaw)
        cos_yaw = math.cos(yaw_rad)
        sin_yaw = math.sin(yaw_rad)
        x1 = dx * cos_yaw + dz * sin_yaw
        y1 = dy
        z1 = -dx * sin_yaw + dz * cos_yaw
        pitch_rad = math.radians(self.pitch)
        cos_pitch = math.cos(pitch_rad)
        sin_pitch = math.sin(pitch_rad)
        x2 = x1
        y2 = y1 * cos_pitch - z1 * sin_pitch
        z2 = y1 * sin_pitch + z1 * cos_pitch
        if z2 > 0.1:
            fov = 90
            scale = 400 / (z2 * math.tan(math.radians(fov / 2)))
            screen_x = self.canvas.winfo_width() / 2 + x2 * scale
            screen_y = self.canvas.winfo_height() / 2 - y2 * scale
            return (screen_x, screen_y, z2)
        return None

    def draw_axes(self):
        center_x = self.canvas.winfo_width() / 2
        center_y = self.canvas.winfo_height() / 2
        axes_points = {
            'X': [(x, 0, 0) for x in range(-10, 11)],
            'Y': [(0, y, 0) for y in range(-10, 11)],
            'Z': [(0, 0, z) for z in range(-10, 11)]
        }
        colors = {'X': 'red', 'Y': 'green', 'Z': 'blue'}
        for axis, points in axes_points.items():
            screen_points = []
            for world_point in points:
                screen_pos = self.world_to_screen(*world_point)
                if screen_pos:
                    screen_points.append((screen_pos[0], screen_pos[1], world_point))
            for i in range(len(screen_points) - 1):
                x1, y1, _ = screen_points[i]
                x2, y2, _ = screen_points[i + 1]
                self.canvas.create_line(x1, y1, x2, y2, fill=colors[axis], width=2)
            for sx, sy, (world_x, world_y, world_z) in screen_points:
                if (axis == 'X' and world_x == 0 and world_y == 0 and world_z == 0) or (axis == 'Y' and world_x == 0 and world_y == 0 and world_z == 0) or (axis == 'Z' and world_x == 0 and world_y == 0 and world_z == 0):
                    continue
                self.canvas.create_oval(sx - 3, sy - 3, sx + 3, sy + 3, fill = colors[axis], outline='', width=1)
                value = world_x if axis == 'X' else (world_y if axis == 'Y' else world_z)
                if value != 0:
                    label = f"{value}"
                    offset_x = 5 if sx < center_x else -25
                    offset_y = 5 if sy < center_y else -15
                    self.canvas.create_text(sx + offset_x, sy + offset_y, text = label, fill = colors[axis], font = ('Arial', 8, 'bold'))
        origin = self.world_to_screen(0, 0, 0)
        if origin:
            ox, oy, _ = origin
            self.canvas.create_oval(ox - 5, oy - 5, ox + 5, oy + 5, fill = 'yellow', outline = 'black', width=2)
        x_end = self.world_to_screen(11, 0, 0)
        if x_end:
            xe, ye, _ = x_end
            self.canvas.create_text(xe + 10, ye, text = "X", fill = 'red', font = ('Arial', 12, 'bold'))
        y_end = self.world_to_screen(0, 11, 0)
        if y_end:
            ye, ye_y, _ = y_end
            self.canvas.create_text(ye, ye_y - 10, text = "Y", fill = 'green', font = ('Arial', 12, 'bold'))
        z_end = self.world_to_screen(0, 0, 11)
        if z_end:
            ze, ze_y, _ = z_end
            self.canvas.create_text(ze + 10, ze_y + 5, text = "Z", fill = 'blue', font = ('Arial', 12, 'bold'))

    def draw_all(self):
        for figure in self.figures:
            if figure[0] == "tetra":
                self.draw_tetrahedron(figure[1])
            elif figure[0] == "dodeca":
                self.draw_dodecahedron(figure[1])
            elif figure[0] == "piramid":
                self.draw_piramid_points(figure[1], figure[2])
            elif figure[0] == "cylinder":
                self.draw_cylinder(figure[1], figure[2])

    def draw_tetrahedron(self, vertices):
        screen_vertices = []
        for vx, vy, vz in vertices:
            screen_pos = self.world_to_screen(vx, vy, vz)
            if screen_pos is None:
                return
            screen_vertices.append(screen_pos)
        if len(screen_vertices) != 4:
            return
        faces = self.faces_tetrahedron
        for i, j, k in faces:
            if i < len(screen_vertices) and j < len(screen_vertices) and k < len(screen_vertices):
                x1, y1, _ = screen_vertices[i]
                x2, y2, _ = screen_vertices[j]
                x3, y3, _ = screen_vertices[k]
                self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, fill = '', outline = 'lime')

    def draw_dodecahedron(self, vertices):
        screen_vertices = []
        for vx, vy, vz in vertices:
            screen_pos = self.world_to_screen(vx, vy, vz)
            if screen_pos is None:
                return
            screen_vertices.append(screen_pos)
        if len(screen_vertices) != 20:
            return
        faces = self.faces_dodecahedron
        for i, j, k, l, m in faces:
            if i < len(screen_vertices) and j < len(screen_vertices) and k < len(screen_vertices) and l < len(screen_vertices) and m < len(screen_vertices):
                x1, y1, _ = screen_vertices[i]
                x2, y2, _ = screen_vertices[j]
                x3, y3, _ = screen_vertices[k]
                x4, y4, _ = screen_vertices[l]
                x5, y5, _ = screen_vertices[m]
                self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, fill = '', outline = 'lime')

    def draw_piramid_points(self, vertices, faces):
        screen_vertices = []
        for vx, vy, vz in vertices:
            screen_pos = self.world_to_screen(vx, vy, vz)
            if screen_pos is None:
                return
            screen_vertices.append(screen_pos)
        for face in faces:
            points = []
            for idx in face:
                if idx < len(screen_vertices):
                    x, y, _ = screen_vertices[idx]
                    points.extend([x, y])
            if len(points) >= 6:
                self.canvas.create_polygon(points, fill = '', outline = 'lime', width = 2)

    def draw_cylinder(self, vertices, faces):
        screen_vertices = []
        for vx, vy, vz in vertices:
            screen_pos = self.world_to_screen(vx, vy, vz)
            if screen_pos is None:
                return
            screen_vertices.append(screen_pos)
        for face in faces:
            points = []
            for idx in face:
                if idx < len(screen_vertices):
                    x, y, _ = screen_vertices[idx]
                    points.extend([x, y])
            if len(points) >= 6:
                self.canvas.create_polygon(points, fill = '', outline = 'lime', width = 2)

    def Roberts_algorithm(self):
        if self.figures:
            visible_faces = []
            for figur in self.figures:
                name, vertices, faces, faces2, center = figur
                camera_pos = (self.x, self.y, self.z)
                faces3 = []
                for face_idx, face_indices in enumerate(faces):
                    first_three = [vertices[idx] for idx in face_indices[:3]]
                    raw_normal = self.compute_normal(first_three)
                    all_face_vertices = [vertices[idx] for idx in face_indices]
                    face_center = self.compute_face_center(all_face_vertices)
                    normal = self.correct_normal_orientation(raw_normal, face_center, center)
                    to_camera = self.vector_subtract(camera_pos, face_center)
                    to_camera_normalized = self.normalize(to_camera)
                    dot = self.dot_product(normal, to_camera_normalized)
                    if dot > 0:
                        faces3.append(face_idx)
                new_figur = name, vertices, faces, faces2, center, faces3
                visible_faces.append(new_figur)
            if self.roberts_method == 1:
                self.draw_visible_faces(visible_faces)
                return
            triangles_list = []
            for figur in self.figures:
                name, vertices, faces, faces2, center = figur
                for face_tri in faces2:
                    triangle_points = (
                        vertices[face_tri[0]],
                        vertices[face_tri[1]],
                        vertices[face_tri[2]]
                    )
                    triangles_list.append((triangle_points, center))
            all_edges = []
            for figur in visible_faces:
                name, vertices, faces, faces2, center, face_idx = figur
                edges = self.conventionally_visible_edges(vertices, faces, face_idx)
                all_edges.extend(edges)
            all_segments = self.overlaps_edges(all_edges, triangles_list)
            all_visible_edges = self.all_visible(all_segments, triangles_list)
            self.draw_visible_edges(all_visible_edges)
            if self.roberts_method == 2:
                return
            intersection_edges = self.find_all_intersection_edges()
            if intersection_edges:
                self.draw_visible_edges(intersection_edges)

    def compute_normal(self, vertices):
        if len(vertices) < 3:
            return (0, 0, 0)
        x1, y1, z1 = vertices[0]
        x2, y2, z2 = vertices[1]
        x3, y3, z3 = vertices[2]
        ux = x2 - x1
        uy = y2 - y1
        uz = z2 - z1
        
        vx = x3 - x1
        vy = y3 - y1
        vz = z3 - z1
        
        nx = uy * vz - uz * vy
        ny = uz * vx - ux * vz
        nz = ux * vy - uy * vx
        length = math.sqrt(nx*nx + ny*ny + nz*nz)
        if length > 0:
            nx /= length
            ny /= length
            nz /= length
        else:
            nx = ny = nz = 0
        return (nx, ny, nz)

    def compute_face_center(self, vertices):
        if not vertices:
            return (0, 0, 0)
        sum_x = 0.0
        sum_y = 0.0
        sum_z = 0.0
        for v in vertices:
            sum_x += v[0]
            sum_y += v[1]
            sum_z += v[2]
        n = len(vertices)
        center_x = sum_x / n
        center_y = sum_y / n
        center_z = sum_z / n
        return (center_x, center_y, center_z)

    def correct_normal_orientation(self, raw_normal, face_center, figure_center):
        to_face = (
            face_center[0] - figure_center[0],
            face_center[1] - figure_center[1],
            face_center[2] - figure_center[2]
        )
        length = math.sqrt(to_face[0]**2 + to_face[1]**2 + to_face[2]**2)
        if length > 0:
            to_face_normalized = (
                to_face[0] / length,
                to_face[1] / length,
                to_face[2] / length
            )
        else:
            return raw_normal
        dot = (raw_normal[0] * to_face_normalized[0] + 
            raw_normal[1] * to_face_normalized[1] + 
            raw_normal[2] * to_face_normalized[2])
        if dot < 0:
            return (-raw_normal[0], -raw_normal[1], -raw_normal[2])
        return raw_normal

    def vector_subtract(self, v1, v2):
        return (v1[0] - v2[0], v1[1] - v2[1], v1[2] - v2[2])

    def normalize(self, v):
        x, y, z = v
        length = math.sqrt(x*x + y*y + z*z)
        if length > 0:
            return (x / length, y / length, z / length)
        return (0, 0, 0)

    def dot_product(self, v1, v2):
        return v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2]

    def draw_visible_faces(self, visible_figures):
        for figur in visible_figures:
            name, vertices, faces, faces2, center, visible_indices = figur
            screen_vertices = []
            for vx, vy, vz in vertices:
                screen_pos = self.world_to_screen(vx, vy, vz)
                if screen_pos is None:
                    return
                screen_vertices.append(screen_pos)
            for face_idx in visible_indices:
                face = faces[face_idx]
                points = []
                for idx in face:
                    if idx < len(screen_vertices):
                        x, y, _ = screen_vertices[idx]
                        points.extend([x, y])
                if len(points) >= 6:
                    self.canvas.create_polygon(points, fill = '', outline = 'black', width = 2)

    def conventionally_visible_edges(self, vertices, faces, face_idx):
        edges_set = set()
        result = []
        for idx in face_idx:
            face = faces[idx]
            num_verts = len(face)
            for i in range(num_verts):
                v1_idx = face[i]
                v2_idx = face[(i + 1) % num_verts]
                key = (min(v1_idx, v2_idx), max(v1_idx, v2_idx))
                if key not in edges_set:
                    edges_set.add(key)
                    v1 = vertices[v1_idx]
                    v2 = vertices[v2_idx]
                    result.append((v1[0], v1[1], v1[2], v2[0], v2[1], v2[2]))
        return result

    def overlaps_edges(self, all_edges, triangles_list):
        result_segments = []
        for edge in all_edges:
            x1, y1, z1, x2, y2, z2 = edge
            p1_3d = (x1, y1, z1)
            p2_3d = (x2, y2, z2)
            screen_p1 = self.world_to_screen(x1, y1, z1)
            screen_p2 = self.world_to_screen(x2, y2, z2)
            if not screen_p1 or not screen_p2:
                continue
            sx1, sy1, sz1 = screen_p1
            sx2, sy2, sz2 = screen_p2
            intersection_params = []
            for triangle, center in triangles_list:
                screen_triangle = []
                all_visible = True
                for v in triangle:
                    screen_v = self.world_to_screen(v[0], v[1], v[2])
                    if not screen_v:
                        all_visible = False
                        break
                    screen_triangle.append((screen_v[0], screen_v[1]))
                if not all_visible or len(screen_triangle) < 3:
                    continue
                intersections = self.segment_triangle_intersection_2d(
                    (sx1, sy1), (sx2, sy2), screen_triangle
                )
                for ix, iy in intersections:
                    t = self.point_to_segment_param((sx1, sy1), (sx2, sy2), (ix, iy))
                    if 0 < t < 1:
                        intersect_3d = (
                            p1_3d[0] + t * (p2_3d[0] - p1_3d[0]),
                            p1_3d[1] + t * (p2_3d[1] - p1_3d[1]),
                            p1_3d[2] + t * (p2_3d[2] - p1_3d[2])
                        )
                        intersection_params.append((t, intersect_3d))
            points_on_edge = [(0, p1_3d)] + [(t, p) for t, p in intersection_params] + [(1, p2_3d)]
            points_on_edge.sort(key=lambda x: x[0])
            unique_points = []
            for t, point in points_on_edge:
                is_duplicate = False
                for existing_t, existing_point in unique_points:
                    if abs(t - existing_t) < 0.0001 or self.distance_between_points(point, existing_point) < 0.001:
                        is_duplicate = True
                        break
                if not is_duplicate:
                    unique_points.append((t, point))
            for i in range(len(unique_points) - 1):
                segment = (unique_points[i][1], unique_points[i + 1][1])
                result_segments.append(segment)
        return result_segments

    def segment_triangle_intersection_2d(self, p1, p2, triangle):
        intersections = []
        for i in range(3):
            a = triangle[i]
            b = triangle[(i + 1) % 3]
            intersection = self.segment_segment_intersection_2d(p1, p2, a, b)
            if intersection:
                intersections.append(intersection)
        mid_point = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
        if self.point_in_triangle_2d(mid_point, triangle):
            pass
        return intersections

    def segment_segment_intersection_2d(self, a, b, c, d):
        x1, y1 = a
        x2, y2 = b
        x3, y3 = c
        x4, y4 = d
        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if abs(denom) < 0.0001:
            return None
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denom
        if 0 <= t <= 1 and 0 <= u <= 1:
            x = x1 + t * (x2 - x1)
            y = y1 + t * (y2 - y1)
            return (x, y)
        return None

    def point_in_triangle_2d(self, p, triangle):
        def sign(p1, p2, p3):
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])
        d1 = sign(p, triangle[0], triangle[1])
        d2 = sign(p, triangle[1], triangle[2])
        d3 = sign(p, triangle[2], triangle[0])
        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
        return not (has_neg and has_pos)

    def point_to_segment_param(self, p1, p2, point):
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        if abs(dx) > abs(dy):
            if abs(dx) < 0.0001:
                return 0
            return (point[0] - p1[0]) / dx
        else:
            if abs(dy) < 0.0001:
                return 0
            return (point[1] - p1[1]) / dy

    def point_in_triangle(self, p, triangle):
        a, b, c = triangle
        v0 = self.vector_subtract(c, a)
        v1 = self.vector_subtract(b, a)
        v2 = self.vector_subtract(p, a)
        dot00 = self.dot_product(v0, v0)
        dot01 = self.dot_product(v0, v1)
        dot02 = self.dot_product(v0, v2)
        dot11 = self.dot_product(v1, v1)
        dot12 = self.dot_product(v1, v2)
        inv_denom = 1.0 / (dot00 * dot11 - dot01 * dot01)
        u = (dot11 * dot02 - dot01 * dot12) * inv_denom
        v = (dot00 * dot12 - dot01 * dot02) * inv_denom
        epsilon = 0.0001
        return (u >= -epsilon) and (v >= -epsilon) and (u + v <= 1 + epsilon)

    def all_visible(self, all_segments, triangles_list):
        visible_segments = []
        for segment in all_segments:
            p1, p2 = segment
            points_to_check = [
                ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2, (p1[2] + p2[2]) / 2),
                ((p1[0] * 0.75 + p2[0] * 0.25), (p1[1] * 0.75 + p2[1] * 0.25), (p1[2] * 0.75 + p2[2] * 0.25)),
                ((p1[0] * 0.25 + p2[0] * 0.75), (p1[1] * 0.25 + p2[1] * 0.75), (p1[2] * 0.25 + p2[2] * 0.75)),
            ]
            is_visible = True
            for point in points_to_check:
                if not self.is_point_visible_simple(point, triangles_list):
                    is_visible = False
                    break
            if is_visible:
                visible_segments.append(segment)
        return visible_segments

    def is_point_visible_simple(self, point, triangles_list):
        screen_point = self.world_to_screen(point[0], point[1], point[2])
        if not screen_point:
            return False
        _, _, point_depth = screen_point
        for triangle, center in triangles_list:
            triangle_depth = self.get_triangle_depth_at_point(triangle, point)
            if triangle_depth is not None:
                if triangle_depth < point_depth - 0.01:
                    return False
        return True

    def get_triangle_depth_at_point(self, triangle, point_3d):
        screen_point = self.world_to_screen(point_3d[0], point_3d[1], point_3d[2])
        if not screen_point:
            return None
        px, py, _ = screen_point
        screen_vertices = []
        for v in triangle:
            screen_v = self.world_to_screen(v[0], v[1], v[2])
            if not screen_v:
                return None
            screen_vertices.append(screen_v)
        if not self.point_in_triangle_2d((px, py), [(v[0], v[1]) for v in screen_vertices]):
            return None
        x1, y1, z1 = screen_vertices[0]
        x2, y2, z2 = screen_vertices[1]
        x3, y3, z3 = screen_vertices[2]
        denom = (y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3)
        if abs(denom) < 0.0001:
            return None
        a = ((y2 - y3) * (px - x3) + (x3 - x2) * (py - y3)) / denom
        b = ((y3 - y1) * (px - x3) + (x1 - x3) * (py - y3)) / denom
        c = 1 - a - b
        if a < -0.0001 or b < -0.0001 or c < -0.0001:
            return None
        depth = a * z1 + b * z2 + c * z3
        return depth

    def distance_between_points(self, p1, p2):
        dx = p1[0] - p2[0]
        dy = p1[1] - p2[1]
        dz = p1[2] - p2[2]
        return math.sqrt(dx*dx + dy*dy + dz*dz)

    def draw_visible_edges(self, visible_segments):
        for segment in visible_segments:
            p1, p2 = segment
            screen_p1 = self.world_to_screen(p1[0], p1[1], p1[2])
            screen_p2 = self.world_to_screen(p2[0], p2[1], p2[2])
            if screen_p1 and screen_p2:
                x1, y1, _ = screen_p1
                x2, y2, _ = screen_p2
                self.canvas.create_line(x1, y1, x2, y2, fill='black', width=2)

    def cross_product(self, v1, v2):
        """Векторное произведение"""
        return (
            v1[1] * v2[2] - v1[2] * v2[1],
            v1[2] * v2[0] - v1[0] * v2[2],
            v1[0] * v2[1] - v1[1] * v2[0]
        )

    def vector_length(self, v):
        """Длина вектора"""
        return math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)

    def vector_add(self, v1, v2):
        """Сложение векторов"""
        return (v1[0] + v2[0], v1[1] + v2[1], v1[2] + v2[2])

    def vector_multiply(self, v, scalar):
        """Умножение вектора на скаляр"""
        return (v[0] * scalar, v[1] * scalar, v[2] * scalar)

    def vector_subtract(self, v1, v2):
        """Вычитание векторов"""
        return (v1[0] - v2[0], v1[1] - v2[1], v1[2] - v2[2])

    def are_coplanar(self, tri1, tri2, epsilon=0.001):
        """Проверяет, лежат ли два треугольника в одной плоскости"""
        normal1 = self.compute_normal(tri1)
        normal2 = self.compute_normal(tri2)
        
        # Проверка параллельности нормалей
        dot = self.dot_product(normal1, normal2)
        if abs(abs(dot) - 1.0) > epsilon:
            return False
        
        # Проверка, лежит ли точка первого треугольника в плоскости второго
        p = tri1[0]
        # Уравнение плоскости второго треугольника: n·(x - p0) = 0
        # Вычисляем D для плоскости второго треугольника
        d2 = -(normal2[0] * tri2[0][0] + normal2[1] * tri2[0][1] + normal2[2] * tri2[0][2])
        distance = abs(normal2[0] * p[0] + normal2[1] * p[1] + normal2[2] * p[2] + d2)
        
        return distance < epsilon

    def line_segment_intersection_3d(self, line_point, line_dir, seg_p1, seg_p2, epsilon=0.0001):
        """
        Находит пересечение прямой (line_point + t * line_dir) с отрезком [seg_p1, seg_p2]
        Возвращает (точка_пересечения, параметр_t) или None
        """
        # Вектор отрезка
        seg_dir = (seg_p2[0] - seg_p1[0], seg_p2[1] - seg_p1[1], seg_p2[2] - seg_p1[2])
        
        # Решаем систему: line_point + t * line_dir = seg_p1 + u * seg_dir
        # (line_dir, -seg_dir) * (t, u) = seg_p1 - line_point
        
        # Используем метод Крамера для двух уравнений (берем две координаты с наибольшими компонентами)
        # Выбираем координаты для решения
        coords = [(0, 1), (0, 2), (1, 2)]  # пары координат для проверки
        best_det = 0
        best_solution = None
        
        for i, j in coords:
            a11 = line_dir[i]
            a12 = -seg_dir[i]
            a21 = line_dir[j]
            a22 = -seg_dir[j]
            
            det = a11 * a22 - a12 * a21
            
            if abs(det) > epsilon and abs(det) > abs(best_det):
                b1 = seg_p1[i] - line_point[i]
                b2 = seg_p1[j] - line_point[j]
                
                t = (b1 * a22 - a12 * b2) / det
                u = (a11 * b2 - b1 * a21) / det
                
                if -epsilon <= u <= 1 + epsilon:
                    point = (
                        seg_p1[0] + u * seg_dir[0],
                        seg_p1[1] + u * seg_dir[1],
                        seg_p1[2] + u * seg_dir[2]
                    )
                    # Проверяем, что точка лежит на прямой
                    check_point = (
                        line_point[0] + t * line_dir[0],
                        line_point[1] + t * line_dir[1],
                        line_point[2] + t * line_dir[2]
                    )
                    if self.distance_between_points(point, check_point) < epsilon:
                        return (point, t)
        
        return None

    def line_triangle_intersection_points(self, triangle, line_point, line_dir, epsilon=0.0001):
        """
        Находит точки пересечения прямой с треугольником
        Возвращает список точек пересечения (0, 1 или 2 точки)
        """
        intersection_points = []
        
        # Проверяем пересечение прямой с каждым ребром треугольника
        for i in range(3):
            p1 = triangle[i]
            p2 = triangle[(i + 1) % 3]
            
            result = self.line_segment_intersection_3d(line_point, line_dir, p1, p2, epsilon)
            if result:
                point, t = result
                # Проверяем, что точка не дублируется
                is_duplicate = False
                for existing in intersection_points:
                    if self.distance_between_points(point, existing) < epsilon:
                        is_duplicate = True
                        break
                if not is_duplicate:
                    intersection_points.append(point)
        
        return intersection_points

    def get_line_parameter(self, point, line_point, line_dir, epsilon=0.0001):
        """Возвращает параметр t для точки на прямой: point = line_point + t * line_dir"""
        # Используем координату с максимальной проекцией для стабильности
        max_abs = max(abs(line_dir[0]), abs(line_dir[1]), abs(line_dir[2]))
        
        if abs(line_dir[0]) > epsilon and abs(line_dir[0]) == max_abs:
            return (point[0] - line_point[0]) / line_dir[0]
        elif abs(line_dir[1]) > epsilon:
            return (point[1] - line_point[1]) / line_dir[1]
        else:
            return (point[2] - line_point[2]) / line_dir[2]
        
    def find_triangles_intersection_edge(self, tri1, tri2, epsilon=0.0001):
        """
        Находит ребро пересечения двух треугольников
        Возвращает (p1, p2) или None
        """
        normal1 = self.compute_normal(tri1)
        normal2 = self.compute_normal(tri2)
        
        # Проверка на компланарность
        if self.are_coplanar(tri1, tri2, epsilon):
            # Для компланарных треугольников используем 2D метод
            return self.find_coplanar_triangles_intersection(tri1, tri2, epsilon)
        
        # Линия пересечения плоскостей
        line_dir = self.cross_product(normal1, normal2)
        if self.vector_length(line_dir) < epsilon:
            return None
        
        line_dir = self.normalize(line_dir)
        
        # Находим точку на линии пересечения плоскостей
        # Решаем систему уравнений двух плоскостей
        line_point = self.find_line_intersection_point(tri1, tri2, normal1, normal2, epsilon)
        if not line_point:
            return None
        
        # Находим пересечение прямой с каждым треугольником
        points1 = self.line_triangle_intersection_points(tri1, line_point, line_dir, epsilon)
        points2 = self.line_triangle_intersection_points(tri2, line_point, line_dir, epsilon)
        
        if len(points1) < 2 or len(points2) < 2:
            return None
        
        # Сортируем точки по параметру вдоль прямой
        params1 = [self.get_line_parameter(p, line_point, line_dir, epsilon) for p in points1]
        params2 = [self.get_line_parameter(p, line_point, line_dir, epsilon) for p in points2]
        
        t1_min, t1_max = min(params1), max(params1)
        t2_min, t2_max = min(params2), max(params2)
        
        # Находим пересечение интервалов
        t_start = max(t1_min, t2_min)
        t_end = min(t1_max, t2_max)
        
        if t_start <= t_end + epsilon:
            p_start = (
                line_point[0] + t_start * line_dir[0],
                line_point[1] + t_start * line_dir[1],
                line_point[2] + t_start * line_dir[2]
            )
            p_end = (
                line_point[0] + t_end * line_dir[0],
                line_point[1] + t_end * line_dir[1],
                line_point[2] + t_end * line_dir[2]
            )
            return (p_start, p_end)
        
        return None

    def find_line_intersection_point(self, tri1, tri2, normal1, normal2, epsilon=0.0001):
        """
        Находит точку на линии пересечения плоскостей двух треугольников
        """
        # Уравнения плоскостей: n1·(x - p1) = 0, n2·(x - p2) = 0
        p1 = tri1[0]
        p2 = tri2[0]
        
        # Находим точку пересечения с плоскостью, где одна из координат = 0
        # Используем метод решения системы из двух уравнений
        line_dir = self.cross_product(normal1, normal2)
        
        # Выбираем координату для зануления
        for coord in range(3):
            if abs(line_dir[coord]) > epsilon:
                # Создаем систему для нахождения точки, где coord = 0
                # n1·x = d1, n2·x = d2, x[coord] = 0
                d1 = normal1[0] * p1[0] + normal1[1] * p1[1] + normal1[2] * p1[2]
                d2 = normal2[0] * p2[0] + normal2[1] * p2[1] + normal2[2] * p2[2]
                
                # Исключаем координату coord
                if coord == 0:
                    # x = 0, решаем для y, z
                    # n1_y * y + n1_z * z = d1
                    # n2_y * y + n2_z * z = d2
                    det = normal1[1] * normal2[2] - normal1[2] * normal2[1]
                    if abs(det) > epsilon:
                        y = (d1 * normal2[2] - normal1[2] * d2) / det
                        z = (normal1[1] * d2 - d1 * normal2[1]) / det
                        return (0, y, z)
                elif coord == 1:
                    # y = 0, решаем для x, z
                    det = normal1[0] * normal2[2] - normal1[2] * normal2[0]
                    if abs(det) > epsilon:
                        x = (d1 * normal2[2] - normal1[2] * d2) / det
                        z = (normal1[0] * d2 - d1 * normal2[0]) / det
                        return (x, 0, z)
                else:
                    # z = 0, решаем для x, y
                    det = normal1[0] * normal2[1] - normal1[1] * normal2[0]
                    if abs(det) > epsilon:
                        x = (d1 * normal2[1] - normal1[1] * d2) / det
                        y = (normal1[0] * d2 - d1 * normal2[0]) / det
                        return (x, y, 0)
        
        return None

    def find_coplanar_triangles_intersection(self, tri1, tri2, epsilon=0.0001):
        """
        Находит пересечение двух компланарных треугольников
        Возвращает отрезок (p1, p2) или None
        """
        # Находим проекцию на плоскость с максимальной площадью
        # Выбираем две координаты с наибольшим разбросом
        all_points = tri1 + tri2
        
        # Находим bounding box для определения проекции
        min_x = min(p[0] for p in all_points)
        max_x = max(p[0] for p in all_points)
        min_y = min(p[1] for p in all_points)
        max_y = max(p[1] for p in all_points)
        min_z = min(p[2] for p in all_points)
        max_z = max(p[2] for p in all_points)
        
        dx = max_x - min_x
        dy = max_y - min_y
        dz = max_z - min_z
        
        # Выбираем две координаты с наибольшим разбросом для проекции
        if dx >= dy and dx >= dz:
            # Проецируем на XY (игнорируем Z)
            proj_func = lambda p: (p[0], p[1])
        elif dy >= dx and dy >= dz:
            # Проецируем на XZ (игнорируем Y)
            proj_func = lambda p: (p[0], p[2])
        else:
            # Проецируем на YZ (игнорируем X)
            proj_func = lambda p: (p[1], p[2])
        
        # Проецируем треугольники в 2D
        tri1_2d = [proj_func(p) for p in tri1]
        tri2_2d = [proj_func(p) for p in tri2]
        
        # Находим пересечение двух треугольников в 2D
        intersection_points = []
        
        # Проверяем пересечения ребер
        for i in range(3):
            p1 = tri1_2d[i]
            p2 = tri1_2d[(i + 1) % 3]
            for j in range(3):
                p3 = tri2_2d[j]
                p4 = tri2_2d[(j + 1) % 3]
                
                intersection = self.segment_segment_intersection_2d(p1, p2, p3, p4)
                if intersection:
                    # Находим 3D координаты точки пересечения
                    # Находим параметры на ребре первого треугольника
                    seg_dir = (p2[0] - p1[0], p2[1] - p1[1])
                    if abs(seg_dir[0]) > epsilon:
                        t = (intersection[0] - p1[0]) / seg_dir[0]
                    elif abs(seg_dir[1]) > epsilon:
                        t = (intersection[1] - p1[1]) / seg_dir[1]
                    else:
                        t = 0
                    
                    # Интерполируем 3D координаты
                    point_3d = (
                        tri1[i][0] + t * (tri1[(i + 1) % 3][0] - tri1[i][0]),
                        tri1[i][1] + t * (tri1[(i + 1) % 3][1] - tri1[i][1]),
                        tri1[i][2] + t * (tri1[(i + 1) % 3][2] - tri1[i][2])
                    )
                    intersection_points.append(point_3d)
        
        # Добавляем вершины, лежащие внутри другого треугольника
        for point in tri1:
            if self.point_in_triangle_2d(proj_func(point), tri2_2d):
                intersection_points.append(point)
        
        for point in tri2:
            if self.point_in_triangle_2d(proj_func(point), tri1_2d):
                intersection_points.append(point)
        
        # Убираем дубликаты
        unique_points = []
        for p in intersection_points:
            is_dup = False
            for q in unique_points:
                if self.distance_between_points(p, q) < epsilon:
                    is_dup = True
                    break
            if not is_dup:
                unique_points.append(p)
        
        if len(unique_points) >= 2:
            # Находим две крайние точки
            # Для этого находим направление с максимальным разбросом
            if len(unique_points) == 2:
                return (unique_points[0], unique_points[1])
            else:
                # Находим две самые удаленные точки
                max_dist = 0
                best_pair = None
                for i in range(len(unique_points)):
                    for j in range(i + 1, len(unique_points)):
                        dist = self.distance_between_points(unique_points[i], unique_points[j])
                        if dist > max_dist:
                            max_dist = dist
                            best_pair = (unique_points[i], unique_points[j])
                return best_pair
        
        return None

    def find_all_intersection_edges(self):
        """
        Находит все ребра пересечения между всеми парами фигур
        Возвращает список отрезков (p1, p2)
        """
        intersection_edges = []
        
        # Получаем все треугольники из всех фигур
        all_triangles = []
        for figur in self.figures:
            name, vertices, faces, faces2, center = figur
            for face_tri in faces2:
                triangle_points = (
                    vertices[face_tri[0]],
                    vertices[face_tri[1]],
                    vertices[face_tri[2]]
                )
                all_triangles.append((triangle_points, name, center))
        
        # Проверяем каждую пару треугольников из разных фигур
        for i in range(len(all_triangles)):
            tri1, name1, center1 = all_triangles[i]
            for j in range(i + 1, len(all_triangles)):
                tri2, name2, center2 = all_triangles[j]
                
                # Пропускаем треугольники из одной фигуры
                if name1 == name2 and center1 == center2:
                    continue
                
                # Находим ребро пересечения
                edge = self.find_triangles_intersection_edge(tri1, tri2)
                if edge:
                    intersection_edges.append(edge)
        
        return intersection_edges

window = Window("Обработчик изображений")
window.run()