import torch
import torch.nn as nn
import torch.nn.functional as F

class Transformer(nn.Module):
    def __init__(self, input_dim, embed_dim, num_heads, ff_dim, num_layers, max_seq_len, dropout=0.1):
        """
        Initialize the Transformer model with embedding, positional encoding, and encoder layers.
        """
        super(Transformer, self).__init__()
        self.embedding = nn.Embedding(input_dim, embed_dim)
        self.positional_encoding = self._generate_positional_encoding(max_seq_len, embed_dim)
        self.encoder_layers = nn.ModuleList([
            nn.TransformerEncoderLayer(
                d_model=embed_dim,
                nhead=num_heads,
                dim_feedforward=ff_dim,
                dropout=dropout,
            ) for _ in range(num_layers)
        ])
        self.dropout = nn.Dropout(dropout)
        self.fc_out = nn.Linear(embed_dim, input_dim)
        
    def _generate_positional_encoding(self, max_seq_len, embed_dim):
        """
        Generate a positional encoding tensor to add positional information to embeddings.
        """
        pe = torch.zeros(max_seq_len, embed_dim)  # Create a tensor of zeros
        position = torch.arange(0, max_seq_len, dtype=torch.float).unsqueeze(1)  # [max_seq_len, 1]
        div_term = torch.exp(torch.arange(0, embed_dim, 2).float() * (-torch.log(torch.tensor(10000.0)) / embed_dim))
        
        pe[:, 0::2] = torch.sin(position * div_term)  # Apply sin to even indices
        if embed_dim % 2 == 1:  # Handle case when embed_dim is odd
            pe[:, 1::2] = torch.cos(position * div_term[:-1])  # Apply cos to odd indices
        else:
            pe[:, 1::2] = torch.cos(position * div_term)  # Apply cos to odd indices
        
        return pe.unsqueeze(0)  # Add batch dimension

    def forward(self, x):
        """
        Perform a forward pass through the Transformer model.
        """
        seq_len = x.size(1)
        x = self.embedding(x)
        x = x + self.positional_encoding[:, :seq_len, :].to(x.device)
        x = self.dropout(x)
        for layer in self.encoder_layers:
            x = layer(x)
        return self.fc_out(x)


# Hyperparameters
INPUT_DIM = 1000  # Vocabulary size
EMBED_DIM = 128   # Embedding size
NUM_HEADS = 4     # Number of attention heads
FF_DIM = 512      # Feedforward network dimension
NUM_LAYERS = 2    # Number of transformer layers
MAX_SEQ_LEN = 50  # Maximum sequence length
DROPOUT = 0.1

# Initialize the model
model = Transformer(
    input_dim=INPUT_DIM,
    embed_dim=EMBED_DIM,
    num_heads=NUM_HEADS,
    ff_dim=FF_DIM,
    num_layers=NUM_LAYERS,
    max_seq_len=MAX_SEQ_LEN,
    dropout=DROPOUT
)

# Function to simulate a simple tokenizer
def tokenize_input(user_input, vocab_size=INPUT_DIM):
    """
    Convert a string input into a sequence of token IDs.
    """
    tokens = [ord(char) % vocab_size for char in user_input]
    return tokens

# Get user input
user_input = input("Enter a sequence of text: ")

# Tokenize the user input
tokenized_input = tokenize_input(user_input)

# Convert to PyTorch tensor and pad to MAX_SEQ_LEN
input_tensor = torch.tensor(tokenized_input[:MAX_SEQ_LEN]).unsqueeze(0)  # Shape: [1, seq_len]
if input_tensor.size(1) < MAX_SEQ_LEN:
    padding = torch.zeros(MAX_SEQ_LEN - input_tensor.size(1), dtype=torch.long)
    input_tensor = torch.cat((input_tensor, padding.unsqueeze(0)), dim=1)

# Run the model on user input
output = model(input_tensor)

# Print the shape of the output and optionally inspect it
print("Output shape:", output.shape)  # Should be [1, MAX_SEQ_LEN, INPUT_DIM]
print("Model output (first token):", output[0, 0, :5])  # Show a small part of the output
