import os
import torch
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from transformers import AdamW
from knowledge_graph import KnowledgeGraph

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


class KnowledgeGuidedLoss(torch.nn.Module):
    def __init__(self, knowledge_graph, tokenizer, lambda_kg=0.1):
        super().__init__()
        self.knowledge_graph = knowledge_graph
        self.tokenizer = tokenizer
        self.lambda_kg = lambda_kg

    def forward(self, logits, labels, input_ids):
        # Standard language modeling loss
        lm_loss = F.cross_entropy(logits.view(-1, logits.size(-1)), labels.view(-1), ignore_index=-100)

        # Knowledge consistency loss
        kg_loss = self.knowledge_consistency_loss(logits, input_ids)

        # Combine losses
        total_loss = lm_loss + self.lambda_kg * kg_loss

        return total_loss

    def knowledge_consistency_loss(self, logits, input_ids):
        # Convert logits to probabilities
        probs = F.softmax(logits, dim=-1)

        # Extract the most likely next tokens
        next_token_probs, next_tokens = torch.max(probs, dim=-1)

        # Convert tokens to text
        generated_text = self.tokenizer.decode(next_tokens[0])

        # Extract statements from generated text
        statements = self.extract_statements(generated_text)

        # Calculate consistency with knowledge graph
        consistency_scores = [
            self.knowledge_graph.verify_statement(s, p, o) 
            for s, p, o in statements
        ]

        # Convert consistency scores to tensor and calculate loss
        consistency_tensor = torch.tensor(consistency_scores, device=logits.device)
        kg_loss = F.binary_cross_entropy(next_token_probs[0], consistency_tensor)

        return kg_loss

    def extract_statements(self, text):
        # Placeholder: In a real system, use NLP to extract subject-predicate-object triples
        # For simplicity, we'll just split the text into words and create dummy triples
        words = text.split()
        statements = [
            (words[i], "relates_to", words[i+1]) 
            for i in range(len(words)-1)
        ]
        return statements


def fine_tune_model(model, tokenizer, user_input, response, course_content, knowledge_graph):
    # Prepare input for fine-tuning
    context = f"{course_content}\n\nStudent: {user_input}\nVirtual Teacher: {response}"
    inputs = tokenizer(context, return_tensors='pt', truncation=True, padding=True, max_length=512)
    inputs = inputs.to(model.device)
    labels = inputs['input_ids'].clone()

    # Create dataset and dataloader
    dataset = CustomDataset(inputs['input_ids'], inputs['attention_mask'], labels)
    dataloader = DataLoader(dataset, batch_size=1, shuffle=True)

    # Set up optimizer and loss function
    optimizer = AdamW(model.parameters(), lr=5e-5)
    kg_loss_fn = KnowledgeGuidedLoss(knowledge_graph, tokenizer)

    # Fine-tuning loop
    model.train()
    for epoch in range(3):  # Adjust number of epochs as needed
        for batch in dataloader:
            optimizer.zero_grad()
            outputs = model(
                input_ids=batch['input_ids'],
                attention_mask=batch['attention_mask'],
                labels=batch['labels']
            )
            
            # Calculate knowledge-guided loss
            loss = kg_loss_fn(outputs.logits, batch['labels'], batch['input_ids'])
            
            loss.backward()
            optimizer.step()

    model.eval()
    save_model(model, 'models/gpt_neo_kg_finetuned.pt')



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