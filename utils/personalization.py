from collections import defaultdict
import torch
from utils.model_utils import fine_tune_model

class PersonalizedTutor:
    def __init__(self, model, tokenizer, knowledge_graph):
        self.model = model
        self.tokenizer = tokenizer
        self.knowledge_graph = knowledge_graph
        self.user_model = defaultdict(lambda: {'mastered_concepts': set(), 'learning_pace': 'medium', 'preferred_style': 'neutral'})

    def respond(self, user_input, course_content, course_qa):
        user_id = 'user_123'  # Assume a unique user identifier
        user_state = self.user_model[user_id]

        # Identify relevant concepts from the knowledge graph
        relevant_concepts = self.knowledge_graph.get_related_concepts(user_input)
        
        # Prepare context based on user's mastery and learning pace
        context = self._prepare_personalized_context(user_state, relevant_concepts, course_content)
        
        # Generate response
        input_text = f"{context}\nStudent: {user_input}\nVirtual Teacher:"
        input_ids = self.tokenizer.encode(input_text, return_tensors='pt').to(self.model.device)
        output = self.model.generate(input_ids, max_length=200, num_return_sequences=1, do_sample=True, top_k=50, top_p=0.95)
        response = self.tokenizer.decode(output[0], skip_special_tokens=True)

        # Prepare additional information
        additional_info = self._prepare_additional_info(user_state, relevant_concepts)

        return response, additional_info

    def _prepare_personalized_context(self, user_state, relevant_concepts, course_content):
        context = course_content
        for concept in relevant_concepts:
            if concept not in user_state['mastered_concepts']:
                context += f"\nFocus on explaining {concept}."
        
        if user_state['learning_pace'] == 'slow':
            context += "\nProvide a detailed and step-by-step explanation."
        elif user_state['learning_pace'] == 'fast':
            context += "\nGive a concise overview of the key points."

        if user_state['preferred_style'] == 'visual':
            context += "\nUse analogies and visual descriptions when possible."
        elif user_state['preferred_style'] == 'practical':
            context += "\nInclude practical examples and applications."

        return context

    def _prepare_additional_info(self, user_state, relevant_concepts):
        info = "Related concepts you might want to explore:\n"
        for concept in relevant_concepts:
            if concept not in user_state['mastered_concepts']:
                info += f"- {concept}\n"
                prerequisites = self.knowledge_graph.get_prerequisites(concept)
                if prerequisites:
                    info += f"  Prerequisites: {', '.join(prerequisites)}\n"
        return info

    def update_user_model(self, user_input, response, feedback):
        user_id = 'user_123'  # Assume a unique user identifier
        user_state = self.user_model[user_id]

        # Update mastered concepts
        relevant_concepts = self.knowledge_graph.get_related_concepts(user_input)
        if feedback.lower() == 'y':
            user_state['mastered_concepts'].update(relevant_concepts)

        # Update learning pace
        if len(response) > 200 and feedback.lower() == 'y':
            user_state['learning_pace'] = 'fast'
        elif len(response) < 100 and feedback.lower() == 'n':
            user_state['learning_pace'] = 'slow'

        # Update preferred style (simplified)
        if "visual" in user_input.lower() or "diagram" in user_input.lower():
            user_state['preferred_style'] = 'visual'
        elif "example" in user_input.lower() or "application" in user_input.lower():
            user_state['preferred_style'] = 'practical'

        # Fine-tune the model based on the interaction
        context = self._prepare_personalized_context(user_state, relevant_concepts, "")
        fine_tune_model(self.model, self.tokenizer, context, response)

        self.user_model[user_id] = user_state