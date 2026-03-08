"""Text-to-speech support using pyttsx3."""

import pyttsx3


class Speaker:
    """Speech output abstraction for AMAN."""

    def __init__(self, rate: int = 180) -> None:
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", rate)

    def say(self, text: str) -> None:
        print(f"AMAN: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
