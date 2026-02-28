import requests
import speech_recognition as sr
import pyttsx3
import os
import webbrowser

# ===================== CONFIG =====================

OPENROUTER_API_KEY = "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"

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

VOICE_RATE = 180
VOICE_VOLUME = 1.0

# ==================================================

# Initialize voice engine
engine = pyttsx3.init()
engine.setProperty('rate', VOICE_RATE)
engine.setProperty('volume', VOICE_VOLUME)

# ===================== SPEAK =====================

def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

# ===================== LISTEN =====================

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        query = recognizer.recognize_google(audio)
        print("You:", query)
        return query
    except:
        speak("Sorry, I did not understand.")
        return None

# ===================== AI RESPONSE =====================

def ask_ai(prompt):

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "Jarvis"
    }

    data = {
        "model": "deepseek/deepseek-r1",  # DeepSeek R1 via OpenRouter
        "messages": [
            {"role": "system", "content": "You are Jarvis, a smart AI assistant."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(
            OPENROUTER_URL,
            headers=headers,
            json=data
        )

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"API Error: {response.status_code} - {response.text}"

    except Exception as e:
        return f"Connection Error: {str(e)}"

# ===================== AUTOMATION =====================

def open_application(app_name):

    app_name = app_name.lower()

    # Websites
    if "youtube" in app_name:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube")
        return

    if "google" in app_name:
        webbrowser.open("https://www.google.com")
        speak("Opening Google")
        return

    if "github" in app_name:
        webbrowser.open("https://www.github.com")
        speak("Opening GitHub")
        return

    # Apps
    if "chrome" in app_name:
        os.system("start chrome")
        speak("Opening Chrome")
        return

    if "notepad" in app_name:
        os.system("start notepad")
        speak("Opening Notepad")
        return

    if "calculator" in app_name:
        os.system("start calc")
        speak("Opening Calculator")
        return

    if "vs code" in app_name:
        os.system("start code")
        speak("Opening VS Code")
        return

    speak("I don't know how to open that yet.")

def search_google(query):
    webbrowser.open(f"https://www.google.com/search?q={query}")
    speak("Searching on Google")

def shutdown():
    speak("Shutting down system")
    os.system("shutdown /s /t 1")

def restart():
    speak("Restarting system")
    os.system("shutdown /r /t 1")

# ===================== COMMAND HANDLER =====================

def handle_command(command):

    command = command.lower()

    if "open" in command:
        app = command.replace("open", "").strip()
        open_application(app)
        return

    if "search" in command:
        query = command.replace("search", "").strip()
        search_google(query)
        return

    if "shutdown" in command:
        shutdown()
        return

    if "restart" in command:
        restart()
        return

    # AI Response
    response = ask_ai(command)
    speak(response)

# ===================== MAIN =====================

def main():
    speak("Hello, I am Jarvis. How can I assist you?")

    while True:
        command = listen()

        if command:
            if "exit" in command.lower():
                speak("Goodbye")
                break

            handle_command(command)

if __name__ == "__main__":
    main()

