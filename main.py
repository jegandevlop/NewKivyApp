from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
import time
import os
import base64

class CameraApp(App):
    def build(self):
        Window.clearcolor = get_color_from_hex('#f0f0f0')
        self.last_image_path = None

        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.camera = Camera(play=True)
        self.camera.resolution = (640, 480)
        self.camera.size_hint_y = 0.5

        # Horizontal layout for buttons
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=60, spacing=10)

        self.capture_button = Button(
            text="📸 Capture",
            background_normal='',
            background_color=get_color_from_hex('#4CAF50'),
            color=(1, 1, 1, 1),
            font_size=16
        )
        self.capture_button.bind(on_press=self.capture)

        self.b64_button = Button(
            text="🔄 To Base64",
            background_normal='',
            background_color=get_color_from_hex('#2196F3'),
            color=(1, 1, 1, 1),
            font_size=16
        )
        self.b64_button.bind(on_press=self.convert_to_b64)

        self.upload_button = Button(
            text="☁️ Upload",
            background_normal='',
            background_color=get_color_from_hex('#673AB7'),
            color=(1, 1, 1, 1),
            font_size=16
        )
        self.upload_button.bind(on_press=self.upload_to_onedrive)

        button_layout.add_widget(self.capture_button)
        button_layout.add_widget(self.b64_button)
        button_layout.add_widget(self.upload_button)

        self.img = Image(size_hint_y=0.4)

        main_layout.add_widget(self.camera)
        main_layout.add_widget(button_layout)
        main_layout.add_widget(self.img)

        return main_layout

    def capture(self, *args):
        timestr = time.strftime("%Y%m%d_%H%M%S")
        filename = f"IMG_{timestr}.png"
        self.camera.export_to_png(filename)
        self.last_image_path = filename
        print(f"Captured {filename} at {os.getcwd()}")

        self.img.source = filename
        self.img.reload()

    def convert_to_b64(self, *args):
        if self.last_image_path and os.path.exists(self.last_image_path):
            with open(self.last_image_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                print("Base64 Encoded Image:\n", encoded_string[:200], "...")
        else:
            print("No image captured yet!")

    def upload_to_onedrive(self, *args):
        if not self.last_image_path or not os.path.exists(self.last_image_path):
            print("No image to upload.")
            return

        print("Uploading to OneDrive... (placeholder)")
        # TODO: Add your Microsoft Graph API access token and upload logic here

if __name__ == '__main__':
    CameraApp().run()
