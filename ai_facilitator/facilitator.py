import random
from collections import defaultdict


class AIFacilitator:
    def __init__(self):
        self.context_prompts = defaultdict(list)
        self.general_prompts = [
            "What connections do you see between this and other topics you've explored?",
            "How might you apply this concept in a real-world situation?",
            "What questions arise as you think about this topic?",
            "Can you think of any potential challenges or limitations to this idea?",
            "How would you explain this concept to someone unfamiliar with the subject?",
        ]
        self.initialize_context_prompts()

    def initialize_context_prompts(self):
        self.context_prompts['reading'] = [
            "What emotions or thoughts did this passage evoke for you?",
            "How does this text relate to your personal experiences?",
            "If you could ask the author one question, what would it be?",
            "Which character's perspective resonates with you the most, and why?",
            "How might this story be different if told from another character's point of view?",
        ]
        self.context_prompts['discussion'] = [
            "How do your peers' interpretations differ from your own?",
            "What new insights have you gained from this discussion?",
            "How has your understanding of the topic evolved through this conversation?",
            "What aspects of the discussion challenged your initial thoughts?",
            "How might you synthesize the different viewpoints presented here?",
        ]
        self.context_prompts['goal_setting'] = [
            "What inspired you to set this particular goal?",
            "How do you think achieving this goal will impact your learning journey?",
            "What potential obstacles do you foresee, and how might you overcome them?",
            "How does this goal relate to your broader interests or aspirations?",
            "What resources or support might you need to achieve this goal?",
        ]

    def generate_prompt(self, context, user_data=None):
        context_specific_prompts = self.context_prompts.get(context, [])
        all_prompts = context_specific_prompts + self.general_prompts

        if user_data:
            return self.personalize_prompt(all_prompts, user_data)
        else:
            return random.choice(all_prompts)

    def personalize_prompt(self, prompts, user_data):
        # This is a simple personalization method. In a more advanced system,
        # you could use NLP techniques or machine learning to generate more
        # tailored prompts based on the user's activity history, goals, etc.
        if 'recent_activities' in user_data:
            recent_activity = user_data['recent_activities'][0] if user_data['recent_activities'] else None
            if recent_activity:
                return f"Considering your recent {recent_activity['type']}, {random.choice(prompts)}"

        return random.choice(prompts)

    def generate_reflection_prompt(self, goal):
        reflection_prompts = [
            f"How has working towards '{goal}' changed your perspective?",
            f"What unexpected challenges or opportunities did you encounter while pursuing '{goal}'?",
            f"How might the skills or knowledge gained from '{goal}' apply to future learning?",
            f"What would you do differently if you were to approach '{goal}' again?",
            f"How has achieving (or working towards) '{goal}' influenced your next steps in learning?",
        ]
        return random.choice(reflection_prompts)

