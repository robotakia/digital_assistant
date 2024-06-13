import speech_recognition as sr

def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Ακούω...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        print("Αναγνώριση...")
        text = recognizer.recognize_google(audio, language="el-GR")
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Δεν κατάλαβα. Παρακαλώ, επανέλαβε")
        return ""
    except sr.RequestError:
        print("Συγγνώμη το αίτημα σας δεν μπορεί να εξυπηρετηθεί αυτή τη στιγμή.")
        return ""

# Example usage:
text = speech_to_text()
