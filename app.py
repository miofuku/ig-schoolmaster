# app.py
import torch
from transformers import GPTNeoForCausalLM, GPT2Tokenizer
from utils.data_utils import load_course_data
from utils.dialog_utils import DialogManager
from utils.model_utils import fine_tune_model
import config

def main():
    # Load model and tokenizer
    model = GPTNeoForCausalLM.from_pretrained('EleutherAI/gpt-neo-1.3B')
    model.to(config.DEVICE)
    tokenizer = GPT2Tokenizer.from_pretrained('EleutherAI/gpt-neo-1.3B')

    # Load course data
    course_content, course_qa = load_course_data('data/course_content.txt', 'data/course_qa.json')

    # Initialize dialog manager
    dialog_manager = DialogManager('models/dialog_manager.pt')

    # Main interaction loop
    while True:
        user_input = input("Student: ")
        if user_input.lower() == 'exit':
            break

        response, feedback = dialog_manager.respond(user_input, course_content, course_qa, model, tokenizer)
        print(f"Virtual Teacher: {response}")

        # Get user feedback
        user_feedback = input("Was this response helpful? (y/n): ")

        # If the response wasn't helpful, fine-tune the model
        if user_feedback.lower() == 'n':
            print("I'm sorry the response wasn't helpful. I'll learn from this interaction.")
            fine_tune_model(model, tokenizer, user_input, response, course_content)
            print("I've updated my knowledge. Let me try to answer your question again.")
            
            # Generate a new response after fine-tuning
            response, _ = dialog_manager.respond(user_input, course_content, course_qa, model, tokenizer)
            print(f"Virtual Teacher: {response}")

if __name__ == "__main__":
    main()
