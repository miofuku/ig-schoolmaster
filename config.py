import torch

DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
BATCH_SIZE = 4
LEARNING_RATE = 5e-5
MAX_LENGTH = 512