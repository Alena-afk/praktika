import tkinter as tk
from tkinter import filedialog, simpledialog
from PIL import Image, ImageTk, ImageDraw, ImageOps
import cv2
import numpy as np

class ImageProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Устройство для обработки изображений")

        self.img_label = tk.Label(self.root)
        self.img_label.pack()

        upload_btn = tk.Button(self.root, text="Загрузить изображение", command=self.upload_image)
        upload_btn.pack()

        channel_btn = tk.Button(self.root, text="Показать канал", command=self.show_channel_dialog)
        channel_btn.pack()

        negative_btn = tk.Button(self.root, text="Показать негативное изображение", command=self.show_negative)
        negative_btn.pack()

        rotate_btn = tk.Button(self.root, text="Поворот изображения", command=self.rotate_image_dialog)
        rotate_btn.pack()

        circle_btn = tk.Button(self.root, text="Нарисовать круг", command=self.draw_circle_dialog)
        circle_btn.pack()

        camera_btn = tk.Button(self.root, text="Съемка с камеры", command=self.capture_from_camera)
        camera_btn.pack()

        self.file_path = None
        self.img = None
        self.cap = None

    def upload_image(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg")])

        if self.file_path:
            self.img = Image.open(self.file_path).convert("RGB")
            img_resized = self.img.resize((400, 400))
            img_tk = ImageTk.PhotoImage(img_resized)
            self.img_label.configure(image=img_tk)
            self.img_label.image = img_tk

    def show_channel_dialog(self):
        if self.img:
            channel = simpledialog.askstring("Ввод", "Ввод канала (R, G, B): ").upper()
            if channel and channel in ['R', 'G', 'B']:
                self.show_channel(channel)

    def show_channel(self, channel):
        r, g, b = self.img.split()
        if channel == "R":
            img_channel = Image.merge('RGB', (r, Image.new('L', r.size, 0), Image.new('L', r.size, 0)))
        elif channel == "G":
            img_channel = Image.merge('RGB', (Image.new('L', r.size, 0), g, Image.new('L', r.size, 0)))
        elif channel == "B":
            img_channel = Image.merge('RGB', (Image.new('L', r.size, 0), Image.new('L', r.size, 0), b))
        img_tk = ImageTk.PhotoImage(img_channel)
        self.img_label.configure(image=img_tk)
        self.img_label.image = img_tk

    def show_negative(self):
        if self.img:
            img_gray = self.img.convert('L')
            img_negative = ImageOps.invert(img_gray)
            img_tk = ImageTk.PhotoImage(img_negative)
            self.img_label.configure(image=img_tk)
            self.img_label.image = img_tk

    def rotate_image_dialog(self):
        if self.img:
            angle = simpledialog.askinteger("Ввод", "Ввод угла поворота:", initialvalue=0)
            if angle is not None:
                self.rotate_image(angle)

    def rotate_image(self, angle):
        img_rotated = self.img.rotate(angle, expand=True)
        img_tk = ImageTk.PhotoImage(img_rotated)
        self.img_label.configure(image=img_tk)
        self.img_label.image = img_tk

    def draw_circle_dialog(self):
        if self.img:
            x = simpledialog.askinteger("Ввод", "Введите координату x:", initialvalue=0)
            y = simpledialog.askinteger("Ввод", "Введите координату y:", initialvalue=0)
            radius = simpledialog.askinteger("Введите", "Введите радиус окружности: ", initialvalue=50)
            self.draw_circle(x, y, radius)

    def draw_circle(self, x, y, radius):
        draw = ImageDraw.Draw(self.img)
        draw.ellipse((x-radius, y-radius, x+radius, y+radius), outline="red")
        img_tk = ImageTk.PhotoImage(self.img)
        self.img_label.configure(image=img_tk)
        self.img_label.image = img_tk

    def capture_from_camera(self):
        self.cap = cv2.VideoCapture(0)

        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                img_resized = img.resize((400, 400))
                img_tk = ImageTk.PhotoImage(img_resized)
                self.img_label.configure(image=img_tk)
                self.img_label.image = img_tk
        else:
            print("Не удается подключиться к камере. Возможные решения: проверьте подключение камеры, перезагрузите компьютер, обновите драйверы камеры.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessingApp(root)
    root.mainloop()











