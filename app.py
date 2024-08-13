from transformers import GPTNeoForCausalLM, GPT2Tokenizer
from utils.data_utils import load_course_data
from utils.knowledge_graph import KnowledgeGraph
from utils.personalization import PersonalizedTutor
import config

def main():
    # Load model and tokenizer
    model = GPTNeoForCausalLM.from_pretrained('EleutherAI/gpt-neo-125M')    
    model.to(config.DEVICE)
    tokenizer = GPT2Tokenizer.from_pretrained('EleutherAI/gpt-neo-125M')

    # Load course data and knowledge graph
    course_content, course_qa = load_course_data('data/course_content.txt', 'data/course_qa.json')
    knowledge_graph = KnowledgeGraph('data/knowledge_graph.json')

    # Initialize personalized tutor
    tutor = PersonalizedTutor(model, tokenizer, knowledge_graph)

    # Main interaction loop
    while True:
        user_input = input("Student: ")
        if user_input.lower() == 'exit':
            break

        response, additional_info = tutor.respond(user_input, course_content, course_qa)
        print(f"Virtual Teacher: {response}")
        
        if additional_info:
            print("Additional Information:")
            print(additional_info)

        # Get user feedback
        user_feedback = input("Was this response helpful? (y/n): ")
        tutor.update_user_model(user_input, response, user_feedback)

if __name__ == "__main__":
    main()