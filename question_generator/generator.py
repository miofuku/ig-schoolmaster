import random


class QuestionGenerator:
    def __init__(self):
        self.question_templates = [
            "How might {topic} relate to your personal experiences?",
            "What contradictions do you see in {topic}?",
            "How would you explain {topic} to someone who's never heard of it?",
            "What's a real-world application of {topic}?",
            "How has your understanding of {topic} changed over time?",
        ]

    def generate_question(self, topic):
        template = random.choice(self.question_templates)
        return template.format(topic=topic)
