import tkinter as tk
import cv2
import numpy as np
import PIL.Image, PIL.ImageTk

class ChatWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Camera Feedback")
        self.geometry("700x500")

        self.camera_feed_label = tk.Label(self)
        self.camera_feed_label.pack()

        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        self.capture_frames()

    def capture_frames(self):
        cap = cv2.VideoCapture(0)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Perform face detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            # Draw bounding boxes around detected faces
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.camera_feed_label.configure(image=image)
            self.camera_feed_label.image = image
            
            self.update_idletasks()
            self.update()

        cap.release()

if __name__ == "__main__":
    app = ChatWindow()
    app.mainloop()
