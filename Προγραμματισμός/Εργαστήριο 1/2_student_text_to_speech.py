from gtts import gTTS
import os

def text_to_speech(text):
    tts = gTTS(text=text, lang='el')
    tts.save('output.mp3')
    os.system("start output.mp3")

# Example usage:
text = "Καλημέρα, πως είσαι;"
text_to_speech(text)
