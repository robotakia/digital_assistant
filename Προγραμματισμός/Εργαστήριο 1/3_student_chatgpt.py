from openai import OpenAI
import requests
import json

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

# Example usage:
user_input = "Ποιό είναι το νόημα της ζωής;"
response = chat_with_openai(user_input)
print(response)
