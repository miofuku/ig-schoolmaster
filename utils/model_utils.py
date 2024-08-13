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

def fine_tune_model(model, tokenizer, context, response):
    inputs = tokenizer(context + response, return_tensors='pt', truncation=True, padding=True, max_length=config.MAX_LENGTH)
    labels = inputs['input_ids'].clone()

    dataset = CustomDataset(inputs['input_ids'], inputs['attention_mask'], labels)
    dataloader = DataLoader(dataset, batch_size=config.BATCH_SIZE, shuffle=True)

    optimizer = AdamW(model.parameters(), lr=config.LEARNING_RATE)

    model.train()
    for epoch in range(config.FINE_TUNE_EPOCHS):
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
