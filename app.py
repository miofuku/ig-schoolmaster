from transformers import GPTNeoForCausalLM, GPT2Tokenizer
from utils.data_utils import load_course_data
from utils.knowledge_graph import KnowledgeGraph
from utils.personalization import PersonalizedTutor
from utils.model_utils import pretrain_model, fine_tune_model
import config

def main():
    # Load pre-trained model and tokenizer
    model = GPTNeoForCausalLM.from_pretrained('EleutherAI/gpt-neo-125M')
    model.to(config.DEVICE)
    tokenizer = GPT2Tokenizer.from_pretrained('EleutherAI/gpt-neo-125M')

    # Load course data and knowledge graph
    course_content, course_qa = load_course_data('data/course_content.txt', 'data/course_qa.json')
    knowledge_graph = KnowledgeGraph('data/knowledge_graph.json')

    # Pre-train the model with supplementary data
    pretrain_model(model, tokenizer, 'data/supplementary_data.txt')

    # Initialize personalized tutor
    tutor = PersonalizedTutor(model, tokenizer, knowledge_graph)

    # Main interaction loop
    while True:
        user_input = input("Student: ")
        if user_input.lower() == 'exit':
            break

        response = tutor.respond(user_input, course_content, course_qa)
        print(f"Virtual Teacher: {response}")

        # Get user feedback
        user_feedback = input("Was this response helpful? (y/n): ")

        # If the response wasn't helpful, fine-tune the model
        if user_feedback.lower() == 'n':
            print("I'm sorry the response wasn't helpful. I'll learn from this interaction.")
            fine_tune_model(model, tokenizer, user_input, response, course_content, knowledge_graph)
            print("I've updated my knowledge. Let me try to answer your question again.")
            
            # Generate a new response after fine-tuning
            response = tutor.respond(user_input, course_content, course_qa)
            print(f"Virtual Teacher: {response}")

        # Update student profile based on interaction
        tutor.update_student_profile(user_input, response, user_feedback)

if __name__ == "__main__":
    main()
