import random


class AIFacilitator:
    def __init__(self):
        self.prompts = [
            "Have you considered looking at this from a different perspective?",
            "What questions come to mind as you explore this topic?",
            "How might you test your understanding of this concept?",
            "Can you think of any real-world examples related to this?",
            "What connections do you see between this and other topics you've explored?",
        ]

    def generate_prompt(self, context):
        # In a more advanced implementation, you might use NLP to generate
        # context-aware prompts. For now, we'll just return a random prompt.
        return random.choice(self.prompts)
