import torch

DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
BATCH_SIZE = 1
LEARNING_RATE = 5e-5
MAX_LENGTH = 512
FINE_TUNE_EPOCHS = 3