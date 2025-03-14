#!/usr/bin/env python3
"""
Debug script to investigate token count mismatch issues.
"""

import sys
import os

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.main import tokenize_text, obfuscate_text
from src.tokenizer.tokenizer import TokenizerRegistry


def debug_token_count(model_name, text, shift=42):
    """
    Debug token count mismatch for a specific text.
    
    Args:
        model_name: Name of the model to use for tokenization
        text: Text to tokenize and obfuscate
        shift: Shift value for obfuscation
    """
    print(f"\n{'='*80}")
    print(f"DEBUGGING TOKEN COUNT MISMATCH")
    print(f"{'='*80}")
    print(f"Model: {model_name}")
    print(f"Shift: {shift}")
    print(f"Original text: {text}")
    
    # Get original tokens
    registry = TokenizerRegistry()
    registry.register_tokenizer(model_name)
    tokenizer = registry.tokenizers[model_name]
    original_tokens = tokenizer.tokenize(text)
    
    # Apply obfuscation
    obfuscated_tokens = [(token + shift) % 50000 for token in original_tokens]
    
    # Detokenize
    obfuscated_text = tokenizer.detokenize(obfuscated_tokens)
    
    # Re-tokenize the obfuscated text
    retokenized = tokenizer.tokenize(obfuscated_text)
    
    print(f"\nOriginal token count: {len(original_tokens)}")
    print(f"Obfuscated token count: {len(retokenized)}")
    
    print(f"\nOriginal tokens: {original_tokens}")
    print(f"Obfuscated tokens (after shift): {obfuscated_tokens}")
    print(f"Re-tokenized obfuscated text: {retokenized}")
    
    # Check for differences
    if len(original_tokens) != len(retokenized):
        print(f"\n✗ TOKEN COUNT MISMATCH DETECTED")
        print(f"  Original count: {len(original_tokens)}")
        print(f"  Obfuscated count: {len(retokenized)}")
        
        # Find where the tokenization differs
        print(f"\nObfuscated text: {obfuscated_text}")
        
        # Check if any tokens in the obfuscated text are special tokens or outside the normal range
        unusual_tokens = [t for t in obfuscated_tokens if t > 40000]  # Most common tokens are below this range
        if unusual_tokens:
            print(f"\nUnusual tokens in obfuscated sequence: {unusual_tokens}")
            
        # Check if any tokens in the retokenized sequence are different from the obfuscated tokens
        if len(obfuscated_tokens) == len(retokenized):
            differences = [(i, obfuscated_tokens[i], retokenized[i]) 
                          for i in range(len(obfuscated_tokens)) 
                          if obfuscated_tokens[i] != retokenized[i]]
            if differences:
                print(f"\nToken differences (index, obfuscated, retokenized):")
                for diff in differences:
                    print(f"  {diff}")
        
        # Check if the detokenized text has any unusual characters
        try:
            unusual_chars = [c for c in obfuscated_text if ord(c) > 127]
            if unusual_chars:
                print(f"\nUnusual characters in obfuscated text: {unusual_chars}")
        except:
            print(f"\nCould not analyze characters in obfuscated text")
    else:
        print(f"\n✓ Token counts match")


if __name__ == "__main__":
    # Test with the text that's failing in the unit tests
    model = "gpt-4"
    text = "This is a longer text with multiple sentences. It should test the obfuscation more thoroughly."
    debug_token_count(model, text)
    
    # Also test with other examples from the test suite
    texts = [
        "Hello, world!",
        "Special characters: !@#$%^&*()_+-=[]{}|;':\",./<>?",
        "Numbers: 0123456789",
        "Emojis: 😀 🚀 🌍 🎉"
    ]
    
    for test_text in texts:
        debug_token_count(model, test_text) 