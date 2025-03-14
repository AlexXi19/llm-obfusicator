from llm_obfuscator.tokenizer.tokenizer import TokenizerRegistry
import random

def tokenize_text(model_name: str, text: str) -> list:
    """
    Tokenize input text using the appropriate tokenizer for the given model.
    
    Args:
        model_name: Name of the model to use for tokenization
        text: Input text to tokenize
        
    Returns:
        List of token ids
    """
    registry = TokenizerRegistry()
    registry.register_tokenizer(model_name)
    tokenizer = registry.tokenizers[model_name]
    return tokenizer.tokenize(text)

def get_vocab_size(tokenizer):
    """
    Get the vocabulary size for a tokenizer.
    
    Args:
        tokenizer: The tokenizer instance
        
    Returns:
        The vocabulary size
    """
    # Try to get vocabulary size based on tokenizer type
    if hasattr(tokenizer, 'encoder') and hasattr(tokenizer.encoder, 'n_vocab'):
        return tokenizer.encoder.n_vocab
    elif hasattr(tokenizer, 'tokenizer') and hasattr(tokenizer.tokenizer, 'vocab_size'):
        return tokenizer.tokenizer.vocab_size
    else:
        # Default to a safe value if we can't determine the actual size
        return 50000

def obfuscate_text(model_name: str, text: str, shift: int = None) -> str:
    """
    Tokenize text, obfuscate the tokens, and then detokenize back to text.
    
    Args:
        model_name: Name of the model to use for tokenization
        text: Input text to obfuscate
        shift: Optional fixed shift value for token mapping. If None, uses random shift.
        
    Returns:
        Obfuscated text after token manipulation
    """
    registry = TokenizerRegistry()
    registry.register_tokenizer(model_name)
    tokenizer = registry.tokenizers[model_name]
    
    # Tokenize the input text
    tokens = tokenizer.tokenize(text)
    
    # If no shift provided, generate a random shift between 1 and 100
    if shift is None:
        shift = random.randint(1, 100)
    
    # Get the vocabulary size for this tokenizer
    vocab_size = get_vocab_size(tokenizer)
    
    # Map tokens to new values using the shift
    obfuscated_tokens = [(token + shift) % vocab_size for token in tokens]
    
    # Detokenize back to text
    return tokenizer.detokenize(obfuscated_tokens)

# Example usage
if __name__ == "__main__":
    test_texts = [
        "Hello, world! My name is Alex.",
        "Hello, world! My name is Bob.",
        "Hello, world! My name is Charlie.",
        "Hello, world! My name is David.",
    ]
    
    for original_text in test_texts:
        obfuscated = obfuscate_text("gpt-4", original_text, shift=42)
        tokenized = tokenize_text("gpt-4", obfuscated)

        print(f"\nOriginal text: {original_text}")
        print(f"Obfuscated text: {obfuscated}")
        print(f'Token count: {len(tokenized)}')