from collections import defaultdict

class PersonalizedTutor:
    def __init__(self, model, tokenizer, knowledge_graph):
        self.model = model
        self.tokenizer = tokenizer
        self.knowledge_graph = knowledge_graph
        self.student_profiles = defaultdict(lambda: {'context': '', 'knowledge_level': defaultdict(int), 'interests': defaultdict(int)})

    def respond(self, user_input, course_content, course_qa):
        user_id = 'user_123'  # Assume a unique user identifier
        student_profile = self.student_profiles[user_id]
        
        # Query knowledge graph for relevant information
        relevant_info = self.knowledge_graph.query(user_input)

        # Prepare context for the model
        context = f"{student_profile['context']}\n{course_content}\n{relevant_info}\nStudent: {user_input}\nVirtual Teacher:"

        # Generate response
        input_ids = self.tokenizer.encode(context, return_tensors='pt')
        output = self.model.generate(input_ids, max_length=200, num_return_sequences=1, do_sample=True, top_k=50, top_p=0.95)
        response = self.tokenizer.decode(output[0], skip_special_tokens=True)

        # Update context
        student_profile['context'] += f"\nStudent: {user_input}\nVirtual Teacher: {response}"

        return response

    def update_student_profile(self, user_input, response, feedback):
        user_id = 'user_123'  # Assume a unique user identifier
        profile = self.student_profiles[user_id]

        # Update knowledge level based on interaction
        topics = self.knowledge_graph.extract_topics(user_input + ' ' + response)
        for topic in topics:
            if feedback.lower() == 'y':
                profile['knowledge_level'][topic] += 1
            else:
                profile['knowledge_level'][topic] = max(0, profile['knowledge_level'][topic] - 1)

        # Update interests based on user input
        interests = self.knowledge_graph.extract_interests(user_input)
        for interest in interests:
            profile['interests'][interest] += 1