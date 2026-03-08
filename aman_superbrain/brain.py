"""Reasoning engine powered by OpenAI GPT models."""

from openai import OpenAI

from personality import system_prompt


class Brain:
    """Handles conversational reasoning and coding help."""

    def __init__(self, model: str = "gpt-4o-mini") -> None:
        self.client = OpenAI()
        self.model = model

    def reply(self, user_message: str, context: str = "") -> str:
        messages = [{"role": "system", "content": system_prompt()}]

        if context:
            messages.append({"role": "system", "content": f"Context:\n{context}"})

        messages.append({"role": "user", "content": user_message})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.4,
        )
        return response.choices[0].message.content or "I need a moment to think."
