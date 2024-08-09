import torch
from torch.utils.data import Dataset, DataLoader
from transformers import GPTJForCausalLM, GPTJTokenizer, AdamW, get_linear_schedule_with_warmup
from tqdm import tqdm
import pandas as pd

# 设置设备
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 加载预训练的GPT-J模型和分词器
model = GPTJForCausalLM.from_pretrained("EleutherAI/gpt-j-6B")
tokenizer = GPTJTokenizer.from_pretrained("EleutherAI/gpt-j-6B")

# 将模型移动到GPU（如果可用）
model.to(device)

# 定义自定义数据集
class CustomDataset(Dataset):
    def __init__(self, data_file, tokenizer, max_length):
        self.data = pd.read_csv(data_file)
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        text = self.data.iloc[idx]['text']
        encoding = self.tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=self.max_length,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten()
        }

# 创建数据加载器
train_dataset = CustomDataset('path/to/your/train_data.csv', tokenizer, max_length=512)
train_loader = DataLoader(train_dataset, batch_size=4, shuffle=True)

# 设置优化器和学习率调度器
optimizer = AdamW(model.parameters(), lr=5e-5)
scheduler = get_linear_schedule_with_warmup(
    optimizer, num_warmup_steps=0, num_training_steps=len(train_loader) * 3
)

# 训练循环
num_epochs = 3
for epoch in range(num_epochs):
    model.train()
    total_loss = 0
    for batch in tqdm(train_loader, desc=f"Epoch {epoch + 1}"):
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        
        outputs = model(input_ids, attention_mask=attention_mask, labels=input_ids)
        loss = outputs.loss
        
        loss.backward()
        optimizer.step()
        scheduler.step()
        optimizer.zero_grad()
        
        total_loss += loss.item()
    
    avg_loss = total_loss / len(train_loader)
    print(f"Epoch {epoch + 1}, Average Loss: {avg_loss:.4f}")

# 保存微调后的模型
model.save_pretrained("path/to/save/finetuned_model")
tokenizer.save_pretrained("path/to/save/finetuned_model")

# 加载微调后的模型（用于推理）
finetuned_model = GPTJForCausalLM.from_pretrained("path/to/save/finetuned_model")
finetuned_tokenizer = GPTJTokenizer.from_pretrained("path/to/save/finetuned_model")

# 示例推理
input_text = "What is the capital of France?"
input_ids = finetuned_tokenizer.encode(input_text, return_tensors="pt").to(device)
output = finetuned_model.generate(input_ids, max_length=100, num_return_sequences=1, do_sample=True)
generated_text = finetuned_tokenizer.decode(output[0], skip_special_tokens=True)
print(f"Generated text: {generated_text}")