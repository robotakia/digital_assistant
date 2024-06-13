import tkinter as tk
from openai import OpenAI
from PIL import Image, ImageTk
import requests
from io import BytesIO

# OpenAI API Key
api_key= "API KEY"

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

class TkinterBasicsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("DALL-E Image Generation")
        self.geometry("400x300")

        self.prompt_label = tk.Label(self, text="Enter prompt:")
        self.prompt_label.pack()

        self.prompt_entry = tk.Entry(self, width=50)
        self.prompt_entry.pack()

        self.generate_button = tk.Button(self, text="Generate Image", command=self.generate_and_display_image)
        self.generate_button.pack()

        self.image_label = tk.Label(self)
        self.image_label.pack()

    # Function to generate image and display in GUI
    def generate_and_display_image(self):
        prompt_text = self.prompt_entry.get()
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt_text,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url
        image_bytes = requests.get(image_url).content
        image = Image.open(BytesIO(image_bytes))
        image.thumbnail((300, 300))
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo

if __name__ == "__main__":
    app = TkinterBasicsApp()
    app.mainloop()
