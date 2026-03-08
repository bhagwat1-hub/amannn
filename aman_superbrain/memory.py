"""Persistent SQLite memory store for AMAN notes and tasks."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable


@dataclass
class MemoryItem:
    id: int
    category: str
    content: str
    created_at: str


class MemoryStore:
    """Simple long-term memory backed by SQLite."""

    def __init__(self, db_path: str = "aman_memory.db") -> None:
        self.db_path = Path(db_path)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _initialize(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )
            conn.commit()

    def add_memory(self, category: str, content: str) -> int:
        timestamp = datetime.utcnow().isoformat(timespec="seconds")
        with self._connect() as conn:
            cursor = conn.execute(
                "INSERT INTO memories (category, content, created_at) VALUES (?, ?, ?)",
                (category, content.strip(), timestamp),
            )
            conn.commit()
            return int(cursor.lastrowid)

    def list_memories(self, category: str | None = None, limit: int = 20) -> list[MemoryItem]:
        query = "SELECT id, category, content, created_at FROM memories"
        params: Iterable[object]

        if category:
            query += " WHERE category = ?"
            params = (category,)
        else:
            params = ()

        query += " ORDER BY id DESC LIMIT ?"
        params = (*params, limit)

        with self._connect() as conn:
            rows = conn.execute(query, params).fetchall()

        return [MemoryItem(*row) for row in rows]

    def format_memories(self, category: str | None = None, limit: int = 20) -> str:
        items = self.list_memories(category=category, limit=limit)
        if not items:
            return "I do not have anything stored yet."

        lines = ["Here is what I remember:"]
        for item in items:
            lines.append(f"- [{item.category}] {item.content} ({item.created_at})")
        return "\n".join(lines)
