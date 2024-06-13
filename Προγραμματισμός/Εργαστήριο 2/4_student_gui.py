import tkinter as tk
import threading
import queue
import speech_recognition as sr
from gtts import gTTS
import requests
import json
import pygame
from io import BytesIO
from openai import OpenAI
from PIL import Image, ImageTk
import re

API_KEY = "API KEY"

class ChatWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Robotaki Classroom Assistant")
        self.geometry("1024x600")

        # Robot State Indicator
        self.robot_state_label = tk.Label(self, text="Robotaki State:\n Sleeping", font=("Arial", 15, "bold"), fg="red")
        self.robot_state_label.grid(row=2, column=2, padx=10, pady=(0, 10),sticky="sew")

        # Camera Feed Panel
        self.camera_feed_label = tk.Label(self, text="Camera Feed", font=("Arial", 12, "bold"), bg="grey")
        self.camera_feed_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Image Preview Panel
        self.image_label = tk.Label(self, text="Image Preview", font=("Arial", 12, "bold"), bg="grey")
        self.image_label.grid(row=0, column=2, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.chat_history = tk.Text(self, wrap="word", font = ("Arial", 13, "bold"))
        self.chat_history.grid(row=2, column=0,  rowspan = 2, columnspan=1, padx=10, pady=10, sticky="nsew")

        # Configure tags for different message types
        self.tags = {"system": "black", "user": "blue", "AI": "green"}
        for tag, color in self.tags.items():
            self.chat_history.tag_configure(tag, foreground=color)

        # Set column and row weights to allow resizing
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        pygame.mixer.init()

        self.queue = queue.Queue()
        self.speech_to_text_thread = threading.Thread(target=self.detect_wake_word)
        self.speech_to_text_thread.daemon = True
        self.speech_to_text_thread.start()

        self.robot_awake = False  # Initialize the robot state
        self.update_gui()

    def detect_wake_word(self):
        while True:
            self.queue.put(("Πες 'ρομποτάκι' για να ξυπνήσω...", "system"))
            user_input = self.speech_to_text()
            if "ρομποτάκι" in user_input:
                    if not self.robot_awake:
                        self.robot_state_label.config(text="Robot State: Awake", fg="green")
                        self.queue.put(("Το ρομποτάκι είναι ξύπνιο!", "system"))
                        self.robot_awake = True
                        self.conversation_loop()
                        self.robot_awake = False

    def text_to_speech(self, text):
        language = 'el'
        tts = gTTS(text=text, lang=language)
        mp3_fp = BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        return mp3_fp

    def play_sound(self, sound):
        pygame.mixer.music.load(sound)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pass

# Tokenizes input string into sentences for OpenAI interaction    
    @staticmethod
    def tokenize_string(input_string):
        # Splitting the string based on the specified delimiters
        tokens = re.split(r'([.!?;,] )', input_string)

        # Combining each token with its corresponding delimiter
        tokenized_string = [tokens[i] + (tokens[i+1] if i < len(tokens)-1 else '') for i in range(0, len(tokens), 2)]

        # Return both the tokenized string and the number of tokens
        return tokenized_string, len(tokenized_string)
    
    def chat_with_openai(self, question):
        url = "https://api.openai.com/v1/chat/completions"
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": f"Είσαι ένας βοηθός για την τάξη {question} Μέγιστο 300 χαρακτήρες"}],
            "temperature": 1, "top_p": 1, "n": 1, "stream": False, "max_tokens": 300, "presence_penalty": 0, "frequency_penalty": 0
        }
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'Bearer {API_KEY}'}
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        try:
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print("Error processing response:", e)
            print("Response content:", response.content)
            return "Sorry, I couldn't understand that."

    # Function to generate image and display in GUI
    def generate_and_display_image(self):
        client = OpenAI(api_key=API_KEY)
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

    def update_gui(self):
        while True:
            if not self.queue.empty():
                message, role = self.queue.get()
                self.chat_history.insert("end", message + "\n", role)
                self.chat_history.see("end")
            else:
                break
        self.after(100, self.update_gui)

    def conversation_loop(self):
        while True:
            user_input = self.speech_to_text()
            if user_input:
                if user_input.lower() == "αντίο":
                    self.queue.put(("AI: Αντίο! Θα κοιμηθώ τώρα.", "AI"))
                    sound = self.text_to_speech("Αντίο! Θα κοιμηθώ τώρα.")
                    self.play_sound(sound)
                    self.robot_awake = False
                    self.robot_state_label.config(text="Robot State: Sleeping", fg="red")
                    break  # Exit the loop if user says "αντίο" while the robot is awake
                #call dall-e function
                elif "εμφάνισε μου" in user_input.lower():
                    prompt_text = user_input.split("εμφάνισε μου",1)[1].strip()
                    self.generate_and_display_image(prompt_text)
                else: 
                    response = self.chat_with_openai(user_input)
                    self.queue.put((f"AI: {response}", "AI"))
                    sound = self.text_to_speech(response)
                    self.play_sound(sound)
        self.queue.put(("AI: Το ρομποτάκι είναι τώρα απενεργοποιημένο.", "system"))

    def speech_to_text(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.queue.put(("Ακούω...", "system"))
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, phrase_time_limit = 5)
        try:
            self.queue.put(("Αναγνώριση...", "system"))
            text = recognizer.recognize_google(audio, language="el-GR")
            self.queue.put((f"Ο χρήστης είπε: {text}", "user"))
            return text
        except sr.UnknownValueError:
            self.queue.put(("Δεν κατάλαβα. Παρακαλώ, επανέλαβε", "system"))
            return ""
        except sr.RequestError:
            self.queue.put(("Sorry, I couldn't process your request at the moment.", "system"))
            return ""

if __name__ == "__main__":
    app = ChatWindow()
    app.mainloop()
