import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from utils.data_utils import load_course_data
from utils.dialog_utils import DialogManager

# 加载模型和数据
model_name = "distilgpt2"
model = GPT2LMHeadModel.from_pretrained(model_name)
model.load_state_dict(torch.load('models/distilgpt2_finetuned.pt'))
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
course_content, course_qa = load_course_data('data/course_content.txt', 'data/course_qa.json')
dialog_manager = DialogManager('models/dialog_manager.pt')

# 对话循环
while True:
    user_input = input("Student: ")
    response, score = dialog_manager.respond(user_input, course_content, course_qa, model, tokenizer)
    print(f"Virtual Teacher: {response}")