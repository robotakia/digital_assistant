from gtts import gTTS
from openai import OpenAI
import requests
import json
import speech_recognition as sr
import pygame
from io import BytesIO

pygame.mixer.init()

def text_to_speech(text):
    tts = gTTS(text=text, lang='el')
    #change where to output
    mp3_fp = BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    return mp3_fp

# Plays sound using pygame mixer
def play_sound(sound):
    pygame.mixer.music.load(sound)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pass

def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Ακούω...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        print("Αναγνώριση...")
        text = recognizer.recognize_google(audio, language="el-GR")
        return text
    except sr.UnknownValueError:
        print("Δεν κατάλαβα. Παρακαλώ, επανέλαβε")
        return ""
    except sr.RequestError:
        print("Συγγνώμη το αίτημα σας δεν μπορεί να εξυπηρετηθεί αυτή τη στιγμή.")
        return ""
    
def chat_with_openai(user_input):
    url = "https://api.openai.com/v1/chat/completions"
    api_key = "API KEY"
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": f"Είσαι ένας βοηθός για την τάξη {user_input} Μέγιστο 300 χαρακτήρες"}],
        "temperature": 1, "top_p": 1, "n": 1, "stream": False, "max_tokens": 300, "presence_penalty": 0, "frequency_penalty": 0
    }
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'Bearer {api_key}'}
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    try:
        print("ChatGPT: ",response.json()["choices"][0]["message"]["content"])
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print("Error processing response:", e)
        print("Response content:", response.content)
        return "Sorry, I couldn't understand that."


def conversation_loop():
    while True:
        user_input = speech_to_text()
        if user_input != "":
            print("Xρήστης: ", user_input)
            if user_input == "αντίο":
                print("Αντίο! Θα κοιμηθώ τώρα.")
                break
            else:    
                response = chat_with_openai(user_input)
                sound = text_to_speech(response)
                play_sound(sound)

while True:
    print("Πες 'Ρομποτάκι' για να ξυπνήσω...")
    user_input = speech_to_text()
    if user_input == "ρομποτάκι":
        print("Το ρομποτάκι είναι ξύπνιο!")
        conversation_loop()