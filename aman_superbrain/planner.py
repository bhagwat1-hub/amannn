"""Task and daily planning helpers built on top of memory storage."""

from memory import MemoryStore


class Planner:
    """Creates and retrieves productivity records."""

    def __init__(self, memory: MemoryStore) -> None:
        self.memory = memory

    def create_task(self, task: str) -> str:
        self.memory.add_memory("task", task)
        return f"Task added: {task}"

    def create_goal(self, goal: str) -> str:
        self.memory.add_memory("goal", goal)
        return f"Goal saved: {goal}"

    def save_note(self, note: str) -> str:
        self.memory.add_memory("note", note)
        return "Note saved to memory."

    def show_tasks(self) -> str:
        return self.memory.format_memories(category="task", limit=20)

    def show_notes(self) -> str:
        return self.memory.format_memories(category="note", limit=20)

    def plan_day(self) -> str:
        tasks = self.memory.list_memories(category="task", limit=5)
        if not tasks:
            return "No tasks found. Start by saying 'create task'."

        plan_lines = ["Suggested strategic plan for today:"]
        for idx, task in enumerate(reversed(tasks), start=1):
            plan_lines.append(f"{idx}. Focus block: {task.content}")
        plan_lines.append("Reserve one final review block before ending your day.")
        return "\n".join(plan_lines)
