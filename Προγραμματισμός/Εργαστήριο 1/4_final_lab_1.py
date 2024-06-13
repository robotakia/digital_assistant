from gtts import gTTS
import os
from openai import OpenAI
import requests
import json
import speech_recognition as sr

def text_to_speech(text):
    tts = gTTS(text=text, lang='el')
    tts.save('output.mp3')
    os.system("start output.mp3")

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
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print("Error processing response:", e)
        print("Response content:", response.content)
        return "Sorry, I couldn't understand that."

user_input = speech_to_text()
response = chat_with_openai(user_input)
text_to_speech(response)