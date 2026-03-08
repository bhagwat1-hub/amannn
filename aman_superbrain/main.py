"""Main runtime loop for AMAN Superbrain."""

from __future__ import annotations

from datetime import datetime

from automation import Automation
from brain import Brain
from memory import MemoryStore
from personality import STARTUP_MESSAGE
from planner import Planner
from speak import Speaker
from vision import VisionSystem
from voice import VoiceListener


class AmanSuperbrain:
    """Coordinates voice input, reasoning, memory, automation, and vision."""

    def __init__(self) -> None:
        self.speaker = Speaker()
        self.listener = VoiceListener()
        self.memory = MemoryStore()
        self.planner = Planner(self.memory)
        self.brain = Brain()
        self.automation = Automation()
        self.vision = VisionSystem()
        self.is_awake = True

    def handle_command(self, command: str) -> str:
        text = command.strip()
        lower = text.lower()

        if "aman wake up" in lower:
            self.is_awake = True
            return "I am awake and ready."
        if "aman sleep" in lower:
            self.is_awake = False
            return "Entering standby mode. Say AMAN wake up to resume."
        if "aman stop" in lower or "aman cancel" in lower:
            return "stop"

        if not self.is_awake:
            return "Standing by."

        if "what can you do" in lower:
            return (
                "I can assist with conversation, coding, memory notes, task planning, "
                "automation, web actions, and vision object detection."
            )

        if lower.startswith("remember "):
            content = text[9:]
            self.memory.add_memory("knowledge", content)
            return "Saved to memory."
        if "save note" in lower:
            content = text.split("save note", maxsplit=1)[-1].strip() or "Empty note"
            return self.planner.save_note(content)
        if "what do you remember" in lower or "show my notes" in lower:
            return self.memory.format_memories(limit=25)

        if "create task" in lower:
            task = text.split("create task", maxsplit=1)[-1].strip() or "Unnamed task"
            return self.planner.create_task(task)
        if "show my tasks" in lower:
            return self.planner.show_tasks()
        if "plan my day" in lower:
            return self.planner.plan_day()
        if "set reminder" in lower or "remind me later" in lower:
            reminder = text.split("later", maxsplit=1)[-1].strip() or text
            self.memory.add_memory("reminder", reminder)
            return "Reminder saved."

        if "what time is it" in lower:
            return f"Current time is {datetime.now().strftime('%H:%M:%S')}."

        if "activate vision" in lower or "detect objects" in lower or "what do you see" in lower:
            labels = self.vision.detect_from_webcam()
            if not labels:
                return "Vision could not detect objects or camera is unavailable."
            return f"I detected: {', '.join(labels)}"

        automation_triggers = [
            "open browser",
            "open file",
            "search google",
            "search the internet",
            "open youtube",
            "open github",
            "type message",
            "scroll down",
            "close window",
            "create folder",
            "create file",
            "delete file",
            "set timer",
        ]
        if any(trigger in lower for trigger in automation_triggers):
            return self.automation.run(text)

        context = self.memory.format_memories(limit=10)
        return self.brain.reply(user_message=text, context=context)

    def run(self) -> None:
        self.speaker.say(STARTUP_MESSAGE)

        while True:
            try:
                heard = self.listener.listen_once()
                if not heard:
                    continue

                response = self.handle_command(heard)
                if response == "stop":
                    self.speaker.say("AMAN shutting down. Stay strategic.")
                    break

                self.speaker.say(response)
            except KeyboardInterrupt:
                self.speaker.say("Session ended.")
                break
            except Exception as exc:
                self.speaker.say(f"I hit an error: {exc}")


if __name__ == "__main__":
    AmanSuperbrain().run()
