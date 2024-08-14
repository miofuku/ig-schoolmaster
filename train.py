import torch
from transformers import GPTNeoForCausalLM, GPT2Tokenizer
from utils.data_utils import load_course_data
from utils.model_utils import train_model

def main():
    # Load pre-trained model and tokenizer
    model = GPTNeoForCausalLM.from_pretrained('EleutherAI/gpt-neo-125M')
    tokenizer = GPT2Tokenizer.from_pretrained('EleutherAI/gpt-neo-125M')

    # Load course data
    course_content, course_qa = load_course_data('data/course_content.txt', 'data/course_qa.json')

    # Train the model
    trained_model = train_model(model, tokenizer, course_content, course_qa)

    # Save the trained model
    torch.save(trained_model.state_dict(), 'models/trained_model/model.pt')
    tokenizer.save_pretrained('models/trained_model/')

if __name__ == "__main__":
    main()