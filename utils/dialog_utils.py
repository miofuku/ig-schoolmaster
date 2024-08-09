import torch
import numpy as np
from collections import defaultdict

class DialogManager:
    def __init__(self, model_path):
        self.model = torch.load(model_path)
        self.user_state = defaultdict(lambda: {'context': '', 'score': 0})

    def respond(self, user_input, course_content, course_qa, model, tokenizer):
        user_id = 'user_123' # 假设用户唯一标识
        user_state = self.user_state[user_id]
        
        # 根据用户输入和上下文生成回应
        input_text = user_state['context'] + ' ' + user_input
        input_ids = tokenizer.encode(input_text, return_tensors='pt')
        output = model.generate(input_ids, max_length=100, num_return_sequences=1, do_sample=True, top_k=50, top_p=0.95, num_iterations=1)
        response = tokenizer.decode(output[0], skip_special_tokens=True)
        
        # 更新用户状态
        user_state['context'] += ' ' + user_input + ' ' + response
        user_state['score'] += self.score_response(response, course_qa)
        self.user_state[user_id] = user_state

        return response, user_state['score']

    def score_response(self, response, course_qa):
        # 根据回应内容和课程 QA 数据计算得分
        score = 0
        for qa in course_qa:
            if qa['question'] in response or qa['answer'] in response:
                score += 1
        return score