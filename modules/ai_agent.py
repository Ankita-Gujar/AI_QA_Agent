import ollama


class AIAgent:

    def __init__(self):
        self.model = "llama3.2:3b"

    def analyze(self, prompt):

        response = ollama.chat(

            model=self.model,

            messages=[
                {
                    "role": "system",
                    "content": """
You are a Senior DTP QA Engineer.

Never output JSON.

Never output Python dictionaries.

Never output Markdown.

Return ONLY a professional QA report in plain text.

Use headings and bullet points.

The report should be readable by DTP Designers.
"""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]

        )

        return response["message"]["content"]