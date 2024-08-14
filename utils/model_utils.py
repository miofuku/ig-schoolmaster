from torch.utils.data import Dataset, DataLoader
from transformers import AdamW
import config

class CourseDataset(Dataset):
    def __init__(self, tokenizer, content, qa_pairs, max_length):
        self.tokenizer = tokenizer
        self.content = content
        self.qa_pairs = qa_pairs
        self.max_length = max_length

    def __len__(self):
        return len(self.qa_pairs) + 1  # content + QA pairs

    def __getitem__(self, idx):
        if idx == 0:
            text = self.content
        else:
            qa = self.qa_pairs[idx - 1]
            text = f"Question: {qa['question']}\nAnswer: {qa['answer']}"

        encodings = self.tokenizer(text, truncation=True, padding='max_length', max_length=self.max_length, return_tensors='pt')
        return {
            'input_ids': encodings['input_ids'].squeeze(),
            'attention_mask': encodings['attention_mask'].squeeze(),
            'labels': encodings['input_ids'].squeeze()
        }


def fine_tune_model(model, tokenizer, context, response):
    inputs = tokenizer(context + response, return_tensors='pt', truncation=True, padding=True, max_length=config.MAX_LENGTH)
    labels = inputs['input_ids'].clone()

    dataset = CourseDataset(inputs['input_ids'], inputs['attention_mask'], labels)
    dataloader = DataLoader(dataset, batch_size=config.BATCH_SIZE, shuffle=True)

    optimizer = AdamW(model.parameters(), lr=config.LEARNING_RATE)

    model.train()
    for epoch in range(config.FINE_TUNE_EPOCHS):
        for batch in dataloader:
            optimizer.zero_grad()
            outputs = model(
                input_ids=batch['input_ids'].to(config.DEVICE),
                attention_mask=batch['attention_mask'].to(config.DEVICE),
                labels=batch['labels'].to(config.DEVICE)
            )
            loss = outputs.loss
            loss.backward()
            optimizer.step()

    model.eval()

def train_model(model, tokenizer, content, qa_pairs):
    dataset = CourseDataset(tokenizer, content, qa_pairs, config.MAX_LENGTH)
    dataloader = DataLoader(dataset, batch_size=config.BATCH_SIZE, shuffle=True)

    optimizer = AdamW(model.parameters(), lr=config.LEARNING_RATE)

    model.train()
    for epoch in range(config.TRAIN_EPOCHS):
        total_loss = 0
        for batch in dataloader:
            optimizer.zero_grad()
            outputs = model(
                input_ids=batch['input_ids'].to(config.DEVICE),
                attention_mask=batch['attention_mask'].to(config.DEVICE),
                labels=batch['labels'].to(config.DEVICE)
            )
            loss = outputs.loss
            total_loss += loss.item()
            loss.backward()
            optimizer.step()
        
        print(f"Epoch {epoch+1}/{config.TRAIN_EPOCHS}, Loss: {total_loss/len(dataloader)}")

    return model
    
