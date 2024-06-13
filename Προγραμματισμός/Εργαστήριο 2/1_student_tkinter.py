import tkinter as tk

class TkinterBasicsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("DALL-E Image Generation")
        self.geometry("400x300")

        self.prompt_label = tk.Label(self, text="Enter prompt:")
        self.prompt_label.pack()

        self.prompt_entry = tk.Entry(self, width=50)
        self.prompt_entry.pack()

        self.generate_button = tk.Button(self, text="Generate Image")
        self.generate_button.pack()

        self.image_label = tk.Label(self)
        self.image_label.pack()

if __name__ == "__main__":
    app = TkinterBasicsApp()
    app.mainloop()
