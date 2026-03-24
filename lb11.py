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
        self.tetra_x = -3
        self.tetra_y = 0
        self.tetra_z = 3
        self.tetra_size = 3
        self.dodeca_x = 3
        self.dodeca_y = 0
        self.dodeca_z = 3
        self.dodeca_size = 1
        self.edges_tetrahedron = [
            (0, 1), (0, 2), (0, 3),
            (1, 2), (2, 3), (3, 1)
        ]
        self.faces_tetrahedron = [
            (0, 1, 2), (0, 2, 3), (0, 1, 3), (1, 2, 3)
        ]
        self.edges_dodecahedron = [
            (1, 11), (1, 16), (11, 17), (17, 3),
            (16, 3), (10, 2), (16, 10), (2, 12),
            (12, 3), (5, 11), (7, 17), (7, 18),
            (18, 12), (7, 19), (19, 5), (18, 6),
            (13, 6), (14, 6), (14, 2), (13, 19),
            (4, 13), (15, 4), (15, 5), (14, 8),
            (4, 8), (1, 9), (9, 15), (8, 0),
            (9, 0), (0, 10)
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
        self.widget()
        self.bind_keys()
        self.start_animation()
    
    def widget(self):
        self.canvas = Canvas(self.root, takefocus = 0)
        self.canvas.place(relx = 0, rely = 0, relwidth = 1, relheight = 1)
        self.button_exit = Button(self.root, text = "X", command = self.root.destroy)
        self.button_exit.place(relx = 0.97, rely = 0.005, relwidth = 0.025, relheight = 0.05)
        self.pos_and_angle = Label(self.root, text = self.get_display_text())
        self.pos_and_angle.place(relx = 0.005, rely = 0.005)
        self.canvas.bind('<Button-1>', lambda e: self.root.focus_set())

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
        self.draw_tetrahedron()
        self.draw_dodecahedron()
        self.is_visible()
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

    def calculate_tetrahedron_vertices(self, x, y, z, length):
        height = math.sqrt(2/3) * length
        circumradius = math.sqrt(3/8) * length
        angle = 2 * math.pi / 3
        horizontal_distance = circumradius * math.sqrt(2/3)
        vertices_relative = [
            (0, circumradius, 0),
            (horizontal_distance * math.cos(0), -height/2, horizontal_distance * math.sin(0)),
            (horizontal_distance * math.cos(angle), -height/2, horizontal_distance * math.sin(angle)),
            (horizontal_distance * math.cos(2 * angle), -height/2, horizontal_distance * math.sin(2 * angle))
        ]
        vertices = [(vx + x, vy + y, vz + z) for vx, vy, vz in vertices_relative]
        return vertices
    
    def calculate_dodecahedron_vertices(self, x, y, z, length):
        phi = (1 + math.sqrt(5)) / 2
        scale = length / (2 / phi)
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
        return vertices

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

    def draw_tetrahedron(self):
        vertices = self.calculate_tetrahedron_vertices(
            self.tetra_x, self.tetra_y, self.tetra_z, self.tetra_size
        )
        screen_vertices = []
        for vx, vy, vz in vertices:
            screen_pos = self.world_to_screen(vx, vy, vz)
            if screen_pos is None:
                return
            screen_vertices.append(screen_pos)
        if len(screen_vertices) != 4:
            return
        edges = self.edges_tetrahedron
        for i, j in edges:
            if i < len(screen_vertices) and j < len(screen_vertices):
                x1, y1, _ = screen_vertices[i]
                x2, y2, _ = screen_vertices[j]
                self.canvas.create_line(x1, y1, x2, y2, fill='black', width=2)
        faces = self.faces_tetrahedron
        for i, j, k in faces:
            if i < len(screen_vertices) and j < len(screen_vertices) and k < len(screen_vertices):
                x1, y1, _ = screen_vertices[i]
                x2, y2, _ = screen_vertices[j]
                x3, y3, _ = screen_vertices[k]
                self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, fill = '', outline = 'lime')
        for x, y, _ in screen_vertices:
            self.canvas.create_oval(x - 4, y - 4, x + 4, y + 4, fill = 'red', outline = 'white', width = 1)
    
    def draw_dodecahedron(self):
        vertices = self.calculate_dodecahedron_vertices(self.dodeca_x, self.dodeca_y, self.dodeca_z, self.dodeca_size)
        screen_vertices = []
        for vx, vy, vz in vertices:
            screen_pos = self.world_to_screen(vx, vy, vz)
            if screen_pos is None:
                return
            screen_vertices.append(screen_pos)
        if len(screen_vertices) != 20:
            return
        edges = self.edges_dodecahedron
        for i, j in edges:
            if i < len(screen_vertices) and j < len(screen_vertices):
                x1, y1, _ = screen_vertices[i]
                x2, y2, _ = screen_vertices[j]
                self.canvas.create_line(x1, y1, x2, y2, fill='black', width=2)
        faces = self.faces_dodecahedron
        for i, j, k, l, m in faces:
            if i < len(screen_vertices) and j < len(screen_vertices) and k < len(screen_vertices) and l < len(screen_vertices) and m < len(screen_vertices):
                x1, y1, _ = screen_vertices[i]
                x2, y2, _ = screen_vertices[j]
                x3, y3, _ = screen_vertices[k]
                x4, y4, _ = screen_vertices[l]
                x5, y5, _ = screen_vertices[m]
                self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, fill = '', outline = 'lime')
        for x, y, _ in screen_vertices:
            self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill = 'red', outline ='', width = 1)

    def is_visible(self):
        all_faces = self.get_all_faces()
        self.draw_visible_edges(
            self.calculate_tetrahedron_vertices(self.tetra_x, self.tetra_y, self.tetra_z, self.tetra_size),
            self.edges_tetrahedron,
            self.faces_tetrahedron,
            all_faces
        )
        self.draw_visible_edges(
            self.calculate_dodecahedron_vertices(self.dodeca_x, self.dodeca_y, self.dodeca_z, self.dodeca_size),
            self.edges_dodecahedron,
            self.faces_dodecahedron,
            all_faces
        )

    def get_all_faces(self):
        all_faces = []
        tetra_vertices = self.calculate_tetrahedron_vertices(
            self.tetra_x, self.tetra_y, self.tetra_z, self.tetra_size
        )
        for face_indices in self.faces_tetrahedron:
            face_points = []
            for idx in face_indices:
                if idx < len(tetra_vertices):
                    face_points.append(tetra_vertices[idx])
            if len(face_points) >= 3:
                all_faces.append(face_points)
        dodeca_vertices = self.calculate_dodecahedron_vertices(
            self.dodeca_x, self.dodeca_y, self.dodeca_z, self.dodeca_size
        )
        for face_indices in self.faces_dodecahedron:
            face_points = []
            for idx in face_indices:
                if idx < len(dodeca_vertices):
                    face_points.append(dodeca_vertices[idx])
            if len(face_points) >= 3:
                all_faces.append(face_points)
        return all_faces

    def draw_visible_edges(self, vertices, edges, faces, all_faces):
        object_faces = []
        for face_indices in faces:
            face_points = []
            for idx in face_indices:
                if idx < len(vertices):
                    face_points.append(vertices[idx])
            if len(face_points) >= 3:
                object_faces.append(face_points)
        for i, j in edges:
            if i < len(vertices) and j < len(vertices):
                self.draw_visible_edge_segments(
                    vertices[i], vertices[j],
                    all_faces, object_faces
                )

    def draw_visible_edge_segments(self, start, end, all_faces, object_faces):
        num_segments = 10
        segment_length = 1.0 / num_segments
        for seg in range(num_segments):
            t1 = seg * segment_length
            t2 = (seg + 1) * segment_length
            mid_t = (t1 + t2) / 2
            mid_point = (
                start[0] + mid_t * (end[0] - start[0]),
                start[1] + mid_t * (end[1] - start[1]),
                start[2] + mid_t * (end[2] - start[2])
            )
            if self.is_point_visible(mid_point, all_faces, object_faces):
                p1 = (
                    start[0] + t1 * (end[0] - start[0]),
                    start[1] + t1 * (end[1] - start[1]),
                    start[2] + t1 * (end[2] - start[2])
                )
                p2 = (
                    start[0] + t2 * (end[0] - start[0]),
                    start[1] + t2 * (end[1] - start[1]),
                    start[2] + t2 * (end[2] - start[2])
                )
                screen_p1 = self.world_to_screen(p1[0], p1[1], p1[2])
                screen_p2 = self.world_to_screen(p2[0], p2[1], p2[2])
                if screen_p1 and screen_p2:
                    x1, y1, _ = screen_p1
                    x2, y2, _ = screen_p2
                    self.canvas.create_line(x1, y1, x2, y2, fill='black', width=2)

    def is_point_visible(self, point, all_faces, object_faces):
        camera = (self.x, self.y, self.z)
        ray_dir = (
            point[0] - camera[0],
            point[1] - camera[1],
            point[2] - camera[2]
        )
        length = math.sqrt(ray_dir[0]**2 + ray_dir[1]**2 + ray_dir[2]**2)
        if length < 0.001:
            return True
        ray_dir = (ray_dir[0]/length, ray_dir[1]/length, ray_dir[2]/length)
        point_distance = length
        for face in all_faces:
            if self.is_point_on_face(point, face):
                continue
            intersection = self.ray_face_intersection(camera, ray_dir, face)
            if intersection:
                intersect_point, t = intersection
                if t < point_distance - 0.001:
                    return False
        return True

    def is_point_on_face(self, point, face_vertices):
        normal = self.calculate_face_normal(face_vertices)
        v = (
            point[0] - face_vertices[0][0],
            point[1] - face_vertices[0][1],
            point[2] - face_vertices[0][2]
        )
        distance = abs(v[0]*normal[0] + v[1]*normal[1] + v[2]*normal[2])
        if distance > 0.01:
            return False
        return self.is_point_in_face_3d(point, face_vertices)

    def is_point_in_face_3d(self, point, face_vertices):
        if len(face_vertices) == 3:
            return self.point_in_triangle_3d(point, face_vertices[0], face_vertices[1], face_vertices[2])
        normal = self.calculate_face_normal(face_vertices)
        abs_normal = (abs(normal[0]), abs(normal[1]), abs(normal[2]))
        if abs_normal[0] > abs_normal[1] and abs_normal[0] > abs_normal[2]:
            proj_point = (point[1], point[2])
            proj_vertices = [(v[1], v[2]) for v in face_vertices]
        elif abs_normal[1] > abs_normal[2]:
            proj_point = (point[0], point[2])
            proj_vertices = [(v[0], v[2]) for v in face_vertices]
        else:
            proj_point = (point[0], point[1])
            proj_vertices = [(v[0], v[1]) for v in face_vertices]
        return self.point_in_polygon_2d(proj_point, proj_vertices)

    def point_in_triangle_3d(self, p, a, b, c):
        v0 = (c[0] - a[0], c[1] - a[1], c[2] - a[2])
        v1 = (b[0] - a[0], b[1] - a[1], b[2] - a[2])
        v2 = (p[0] - a[0], p[1] - a[1], p[2] - a[2])
        dot00 = v0[0]*v0[0] + v0[1]*v0[1] + v0[2]*v0[2]
        dot01 = v0[0]*v1[0] + v0[1]*v1[1] + v0[2]*v1[2]
        dot02 = v0[0]*v2[0] + v0[1]*v2[1] + v0[2]*v2[2]
        dot11 = v1[0]*v1[0] + v1[1]*v1[1] + v1[2]*v1[2]
        dot12 = v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2]
        inv_denom = 1 / (dot00 * dot11 - dot01 * dot01)
        u = (dot11 * dot02 - dot01 * dot12) * inv_denom
        v = (dot00 * dot12 - dot01 * dot02) * inv_denom
        return (u >= 0) and (v >= 0) and (u + v <= 1)

    def point_in_polygon_2d(self, point, polygon):
        x, y = point
        inside = False
        n = len(polygon)
        for i in range(n):
            x1, y1 = polygon[i]
            x2, y2 = polygon[(i + 1) % n]
            if ((y1 > y) != (y2 > y)):
                x_intersect = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
                if x < x_intersect:
                    inside = not inside
        return inside

    def calculate_face_normal(self, face_vertices):
        if len(face_vertices) < 3:
            return (0, 0, 1)
        v1 = face_vertices[0]
        v2 = face_vertices[1]
        v3 = face_vertices[2]
        u = (v2[0] - v1[0], v2[1] - v1[1], v2[2] - v1[2])
        v = (v3[0] - v1[0], v3[1] - v1[1], v3[2] - v1[2])
        normal = (
            u[1]*v[2] - u[2]*v[1],
            u[2]*v[0] - u[0]*v[2],
            u[0]*v[1] - u[1]*v[0]
        )
        length = math.sqrt(normal[0]**2 + normal[1]**2 + normal[2]**2)
        if length > 0:
            normal = (normal[0]/length, normal[1]/length, normal[2]/length)
        return normal

    def ray_face_intersection(self, ray_origin, ray_dir, face_vertices):
        if len(face_vertices) == 3:
            return self.ray_triangle_intersection(ray_origin, ray_dir, face_vertices)
        v0 = face_vertices[0]
        closest_intersection = None
        closest_t = float('inf')
        for i in range(1, len(face_vertices) - 1):
            v1 = face_vertices[i]
            v2 = face_vertices[i + 1]
            triangle = [v0, v1, v2]
            intersection = self.ray_triangle_intersection(ray_origin, ray_dir, triangle)
            if intersection:
                point, t = intersection
                if t < closest_t:
                    closest_t = t
                    closest_intersection = (point, t)
        return closest_intersection

    def ray_triangle_intersection(self, ray_origin, ray_dir, triangle):
        v0, v1, v2 = triangle
        edge1 = (v1[0] - v0[0], v1[1] - v0[1], v1[2] - v0[2])
        edge2 = (v2[0] - v0[0], v2[1] - v0[1], v2[2] - v0[2])
        h = (
            ray_dir[1]*edge2[2] - ray_dir[2]*edge2[1],
            ray_dir[2]*edge2[0] - ray_dir[0]*edge2[2],
            ray_dir[0]*edge2[1] - ray_dir[1]*edge2[0]
        )
        a = edge1[0]*h[0] + edge1[1]*h[1] + edge1[2]*h[2]
        if abs(a) < 1e-6:
            return None
        f = 1.0 / a
        s = (
            ray_origin[0] - v0[0],
            ray_origin[1] - v0[1],
            ray_origin[2] - v0[2]
        )
        u = f * (s[0]*h[0] + s[1]*h[1] + s[2]*h[2])
        if u < 0 or u > 1:
            return None
        q = (
            s[1]*edge1[2] - s[2]*edge1[1],
            s[2]*edge1[0] - s[0]*edge1[2],
            s[0]*edge1[1] - s[1]*edge1[0]
        )
        v = f * (ray_dir[0]*q[0] + ray_dir[1]*q[1] + ray_dir[2]*q[2])
        if v < 0 or u + v > 1:
            return None
        t = f * (edge2[0]*q[0] + edge2[1]*q[1] + edge2[2]*q[2])
        if t < 0:
            return None
        point = (
            ray_origin[0] + t * ray_dir[0],
            ray_origin[1] + t * ray_dir[1],
            ray_origin[2] + t * ray_dir[2]
        )
        return (point, t)

window = Window("Обработчик изображений")
window.run()