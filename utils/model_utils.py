import os
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import AdamW

class CustomDataset(Dataset):
    def __init__(self, input_ids, attention_mask, labels):
        self.input_ids = input_ids
        self.attention_mask = attention_mask
        self.labels = labels

    def __len__(self):
        return len(self.input_ids)

    def __getitem__(self, idx):
        return {
            'input_ids': self.input_ids[idx],
            'attention_mask': self.attention_mask[idx],
            'labels': self.labels[idx]
        }

def fine_tune_model(model, tokenizer, user_input, response, course_content):    # Prepare input for fine-tuning
    context = f"{course_content}\n\nStudent: {user_input}\nVirtual Teacher: {response}"
    inputs = tokenizer(context, return_tensors='pt', truncation=True, padding=True, max_length=512)
    labels = inputs['input_ids'].clone()

    # Create dataset and dataloader
    dataset = CustomDataset(inputs['input_ids'], inputs['attention_mask'], labels)
    dataloader = DataLoader(dataset, batch_size=1, shuffle=True)

    # Set up optimizer
    optimizer = AdamW(model.parameters(), lr=5e-5)

    # Fine-tuning loop
    model.train()
    for epoch in range(3):  # Adjust number of epochs as needed
        for batch in dataloader:
            optimizer.zero_grad()
            outputs = model(
                input_ids=batch['input_ids'].to(model.device),
                attention_mask=batch['attention_mask'].to(model.device),
                labels=batch['labels'].to(model.device)
            )
            loss = outputs.loss
            loss.backward()
            optimizer.step()

    model.eval()
    save_model(model, 'models/gpt_neo_finetuned.pt')


def save_model(model, path):
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    torch.save(model.state_dict(), path)
    print(f"Model saved to {path}")


def load_model(model, path):
    if os.path.exists(path):
        model.load_state_dict(torch.load(path))
        print(f"Model loaded from {path}")
    return model