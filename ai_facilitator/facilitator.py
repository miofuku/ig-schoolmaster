import random
from collections import defaultdict
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


class AIFacilitator:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
        self.model = AutoModelForCausalLM.from_pretrained("distilgpt2")

        if self.tokenizer.pad_token_id is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
            self.model.config.pad_token_id = self.model.config.eos_token_id

        self.context_prompts = defaultdict(list)
        self.initialize_context_prompts()

    def initialize_context_prompts(self):
        self.context_prompts['reading'] = [
            "How does the text challenge or reinforce your existing beliefs?",
            "What connections can you draw between this reading and your personal experiences?",
            "If you could ask the author one question, what would it be and why?",
            "How might this text be interpreted differently in various cultural contexts?",
            "What aspects of the reading did you find most thought-provoking or surprising?"
        ]
        self.context_prompts['discussion'] = [
            "How have your peers' perspectives influenced your understanding of the topic?",
            "What new questions have emerged for you during this discussion?",
            "How might you apply the insights from this discussion to real-world situations?",
            "What aspects of the discussion challenged your initial thoughts on the subject?",
            "How would you synthesize the different viewpoints presented in this conversation?"
        ]
        self.context_prompts['goal_setting'] = [
            "How does this goal align with your broader learning objectives?",
            "What potential obstacles do you foresee in achieving this goal, and how might you overcome them?",
            "How might achieving this goal impact your approach to future learning?",
            "What resources or support might you need to successfully reach this goal?",
            "How will you measure your progress towards this goal?"
        ]

    def generate_prompt(self, context, user_data=None):
        context_specific_prompts = self.context_prompts.get(context, [])

        if not context_specific_prompts:
            context_specific_prompts = [
                f"What aspects of {context} do you find most intriguing?",
                f"How might {context} relate to your broader learning journey?",
                f"What questions arise as you think about {context}?",
                f"How would you explain {context} to someone unfamiliar with the subject?",
                f"What potential implications or consequences do you see arising from {context}?"
            ]

        selected_prompt = random.choice(context_specific_prompts)

        if user_data:
            return self.personalize_prompt(selected_prompt, user_data)
        else:
            return selected_prompt

    def generate_rule_based_prompt(self, context):
        # Implement rule-based prompt generation here
        templates = {
            "reading": "How does {topic} relate to your personal experiences?",
            "discussion": "What new perspectives on {topic} have you gained from this conversation?",
            "goal_setting": "How might achieving {goal} impact your broader learning journey?",
        }
        return templates.get(context, "What insights have you gained about {topic}?")

    def generate_lm_prompt(self, context):
        input_text = f"Generate a thought-provoking reflection question about {context}:"
        inputs = self.tokenizer(input_text, return_tensors="pt", padding=True, truncation=True)

        try:
            with torch.no_grad():
                output = self.model.generate(
                    input_ids=inputs.input_ids,
                    attention_mask=inputs.attention_mask,
                    max_length=100,  # Increased max_length for more detailed prompts
                    num_return_sequences=1,
                    temperature=0.7,
                    pad_token_id=self.tokenizer.pad_token_id,
                    do_sample=True
                )
            generated_prompt = self.tokenizer.decode(output[0], skip_special_tokens=True)

            # Ensure the generated prompt ends with a question mark
            if not generated_prompt.endswith('?'):
                generated_prompt += '?'

            return generated_prompt
        except Exception as e:
            print(f"Error generating prompt: {str(e)}")
            return f"How has your understanding of {context} evolved through your recent experiences?"

    def combine_and_filter_prompts(self, rule_based_prompt, lm_prompt):
        # Implement logic to combine and filter prompts
        # This could involve checking for alignment with philosophy, removing direct statements, etc.
        combined = f"{rule_based_prompt} Additionally, {lm_prompt}"
        # Add filtering logic here
        return combined

    def personalize_prompt(self, prompt, user_data):
        if 'recent_activities' in user_data and user_data['recent_activities']:
            recent_activity = user_data['recent_activities'][0]
            return f"Considering your recent {recent_activity['type']}, {prompt}"
        return prompt

    def generate_reflection_prompt(self, goal):
        reflection_templates = [
            "How has working towards '{goal}' changed your perspective on learning?",
            "What unexpected challenges or insights did you encounter while pursuing '{goal}'?",
            "In what ways has your approach to '{goal}' evolved since you started?",
            "How might the skills or knowledge gained from '{goal}' apply to future learning objectives?",
            "What aspects of working on '{goal}' have you found most rewarding or interesting?",
            "If you were to approach '{goal}' again, what would you do differently and why?",
            "How has achieving (or working towards) '{goal}' influenced your next steps in learning?",
            "What connections have you discovered between '{goal}' and other areas of your studies or life?"
        ]

        return random.choice(reflection_templates).format(goal=goal)

