import random
import nltk
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize


class QuestionGenerator:
    def __init__(self):
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        self.stop_words = set(stopwords.words('english'))

        self.question_templates = [
            "How might {topic} relate to {theme}?",
            "What contradictions do you see between {topic} and {theme}?",
            "How would you explain the relationship between {topic} and {theme} to someone unfamiliar with both?",
            "Can you think of a real-world situation where {topic} and {theme} intersect?",
            "How has your understanding of {topic} changed after considering its connection to {theme}?",
            "What questions arise when you consider {topic} in the context of {theme}?",
            "How might {author}'s perspective on {topic} differ from your own?",
            "In what ways does {topic} challenge or reinforce your existing beliefs?",
            "How might {topic} be viewed differently in various cultural contexts?",
            "What potential consequences or implications do you see arising from {topic}?"
        ]

    def generate_question(self, book):
        topic = book['title']
        author = book['author']
        summary = book['summary']
        tags = book['tags']

        # Extract key themes from the summary
        words = word_tokenize(summary.lower())
        words = [word for word in words if word.isalnum() and word not in self.stop_words]
        freq_dist = FreqDist(words)
        themes = [word for word, _ in freq_dist.most_common(3) if word not in topic.lower().split()]

        # Choose a theme, preferring tags if available
        theme = random.choice(tags) if tags else random.choice(themes) if themes else "the book's central theme"

        # Select a question template
        template = random.choice(self.question_templates)

        # Generate the question
        question = template.format(topic=topic, theme=theme, author=author)

        return question

    def generate_multiple_questions(self, book, n=3):
        return [self.generate_question(book) for _ in range(n)]
