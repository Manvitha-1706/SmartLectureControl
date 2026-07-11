import speech_recognition as sr
import pyautogui

recognizer = sr.Recognizer()
mic = sr.Microphone()

print("🎤 Voice control active. Say 'next', 'back', or 'stop'...")

with mic as source:
    recognizer.adjust_for_ambient_noise(source)

    while True:
        try:
            print("🎧 Listening...")
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")

            if "next" in command:
                pyautogui.press("right")
                print("➡️ Next slide")

            elif "back" in command or "previous" in command:
                pyautogui.press("left")
                print("⬅️ Previous slide")

            elif "stop" in command or "exit" in command:
                print("🛑 Exiting voice control")
                break

        except sr.UnknownValueError:
            print("🤔 Didn't catch that. Try again.")
        except sr.RequestError:
            print("⚠️ Speech recognition service error.")
            break
