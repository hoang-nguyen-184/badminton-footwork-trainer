import threading


def speak_number(number):
    """Speak a number aloud in a background thread using pyttsx3."""
    def _speak():
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.say(str(number))
            engine.runAndWait()
        except Exception:
            pass

    t = threading.Thread(target=_speak, daemon=True)
    t.start()
