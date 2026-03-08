"""System and internet automation actions using PyAutoGUI and stdlib tools."""

from __future__ import annotations

import os
import time
import webbrowser
from pathlib import Path

import pyautogui


class Automation:
    """Executes desktop automation commands."""

    def __init__(self, base_dir: str = ".") -> None:
        self.base_dir = Path(base_dir)

    def run(self, command: str) -> str:
        cmd = command.lower().strip()

        if "open browser" in cmd:
            webbrowser.open("https://www.google.com")
            return "Opening browser."
        if "open youtube" in cmd:
            webbrowser.open("https://www.youtube.com")
            return "Opening YouTube."
        if "open github" in cmd:
            webbrowser.open("https://github.com")
            return "Opening GitHub."
        if "search google" in cmd or "search the internet" in cmd:
            query = command.split("about", maxsplit=1)[-1].strip()
            url = f"https://www.google.com/search?q={query}" if query else "https://www.google.com"
            webbrowser.open(url)
            return "Launching web search."
        if "type message" in cmd:
            message = command.split("type message", maxsplit=1)[-1].strip() or "Hello from AMAN"
            pyautogui.write(message, interval=0.03)
            return "Typed your message."
        if "scroll down" in cmd:
            pyautogui.scroll(-800)
            return "Scrolled down."
        if "close window" in cmd:
            pyautogui.hotkey("alt", "f4")
            return "Closing active window."
        if "create folder" in cmd:
            name = command.split("create folder", maxsplit=1)[-1].strip() or "aman_folder"
            path = self.base_dir / name
            path.mkdir(parents=True, exist_ok=True)
            return f"Folder created at {path}."
        if "create file" in cmd:
            name = command.split("create file", maxsplit=1)[-1].strip() or "aman_file.txt"
            path = self.base_dir / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.touch(exist_ok=True)
            return f"File created at {path}."
        if "delete file" in cmd:
            name = command.split("delete file", maxsplit=1)[-1].strip()
            if not name:
                return "Please specify a file to delete."
            path = self.base_dir / name
            if path.exists() and path.is_file():
                path.unlink()
                return f"Deleted file {path}."
            return f"File not found: {path}."
        if "open file" in cmd:
            name = command.split("open file", maxsplit=1)[-1].strip()
            if not name:
                return "Please provide a file path to open."
            path = self.base_dir / name
            if not path.exists():
                return f"File not found: {path}."
            os.system(f'xdg-open "{path}"')
            return f"Opening file {path}."
        if "set timer" in cmd:
            time.sleep(1)
            return "Timer command received. Add duration support in the next iteration."

        return "Automation command recognized, but action is not implemented yet."
