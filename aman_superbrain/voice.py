"""Voice input support using speech_recognition and Whisper."""

import speech_recognition as sr


class VoiceListener:
    """Continuously listens and converts speech to text."""

    def __init__(self, energy_threshold: int = 300) -> None:
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = energy_threshold
        self.microphone = sr.Microphone()

    def listen_once(self, timeout: float = 5, phrase_time_limit: float = 10) -> str:
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = self.recognizer.listen(
                source, timeout=timeout, phrase_time_limit=phrase_time_limit
            )
        text = self.recognizer.recognize_whisper(audio)
        return text.strip()
