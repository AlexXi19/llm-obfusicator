#!/usr/bin/env python3
"""
Test script for demonstrating and validating token obfuscation.
This script can be run directly to see the obfuscation in action.
"""

import sys
import os
from collections import defaultdict

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.main import tokenize_text, obfuscate_text, get_vocab_size
from src.tokenizer.tokenizer import TokenizerRegistry


def validate_one_to_one_mapping(model, text, shift):
    """
    Validate that the obfuscation is a one-to-one mapping.
    
    Args:
        model: Model name to use for tokenization
        text: Text to tokenize and obfuscate
        shift: Shift value for obfuscation
        
    Returns:
        True if validation passes, False otherwise
    """
    registry = TokenizerRegistry()
    registry.register_tokenizer(model)
    tokenizer = registry.tokenizers[model]
    
    # Get original tokens
    original_tokens = tokenizer.tokenize(text)
    
    # Get vocabulary size
    vocab_size = get_vocab_size(tokenizer)
    
    # Create mapping from original to obfuscated
    token_mapping = {}
    reverse_mapping = {}
    
    for token in original_tokens:
        obfuscated = (token + shift) % vocab_size
        
        # Check if this mapping is consistent
        if token in token_mapping and token_mapping[token] != obfuscated:
            print(f"ERROR: Token {token} maps to multiple values: {token_mapping[token]} and {obfuscated}")
            return False
            
        # Check if this creates a collision in the reverse mapping
        if obfuscated in reverse_mapping and reverse_mapping[obfuscated] != token:
            print(f"ERROR: Multiple tokens map to {obfuscated}: {reverse_mapping[obfuscated]} and {token}")
            return False
            
        token_mapping[token] = obfuscated
        reverse_mapping[obfuscated] = token
    
    print(f"✓ Validation passed: Obfuscation is a one-to-one mapping")
    print(f"  - {len(token_mapping)} unique tokens mapped")
    return True


def compare_token_counts(model, text, shift):
    """
    Compare token counts before and after obfuscation.
    
    Args:
        model: Model name to use for tokenization
        text: Text to tokenize and obfuscate
        shift: Shift value for obfuscation
        
    Returns:
        True if token counts match, False otherwise
    """
    # Get original token count
    original_tokens = tokenize_text(model, text)
    original_count = len(original_tokens)
    
    # Obfuscate the text
    obfuscated = obfuscate_text(model, text, shift=shift)
    
    # Get obfuscated token count
    obfuscated_tokens = tokenize_text(model, obfuscated)
    obfuscated_count = len(obfuscated_tokens)
    
    print(f"Original token count: {original_count}")
    print(f"Obfuscated token count: {obfuscated_count}")
    
    if original_count == obfuscated_count:
        print(f"✓ Validation passed: Token counts match")
        return True
    else:
        print(f"✗ Validation failed: Token counts don't match")
        return False


def analyze_token_frequency(model, text, shift):
    """
    Analyze and compare token frequency distributions before and after obfuscation.
    
    Args:
        model: Model name to use for tokenization
        text: Text to tokenize and obfuscate
        shift: Shift value for obfuscation
    """
    registry = TokenizerRegistry()
    registry.register_tokenizer(model)
    tokenizer = registry.tokenizers[model]
    
    # Get vocabulary size
    vocab_size = get_vocab_size(tokenizer)
    
    # Get original tokens and their frequency
    original_tokens = tokenizer.tokenize(text)
    original_freq = defaultdict(int)
    for token in original_tokens:
        original_freq[token] += 1
    
    # Get obfuscated tokens and their frequency
    obfuscated_tokens = [(token + shift) % vocab_size for token in original_tokens]
    obfuscated_freq = defaultdict(int)
    for token in obfuscated_tokens:
        obfuscated_freq[token] += 1
    
    # Compare frequency distributions
    original_counts = sorted(original_freq.values())
    obfuscated_counts = sorted(obfuscated_freq.values())
    
    print(f"Original unique tokens: {len(original_freq)}")
    print(f"Obfuscated unique tokens: {len(obfuscated_freq)}")
    
    if original_counts == obfuscated_counts:
        print(f"✓ Validation passed: Frequency distributions match")
    else:
        print(f"✗ Validation failed: Frequency distributions don't match")
        print(f"  Original frequencies: {original_counts}")
        print(f"  Obfuscated frequencies: {obfuscated_counts}")


def demonstrate_obfuscation(model, text, shift):
    """
    Demonstrate the obfuscation process with detailed output.
    
    Args:
        model: Model name to use for tokenization
        text: Text to tokenize and obfuscate
        shift: Shift value for obfuscation
    """
    print(f"\n{'='*80}")
    print(f"OBFUSCATION DEMONSTRATION")
    print(f"{'='*80}")
    print(f"Model: {model}")
    print(f"Shift: {shift}")
    print(f"Original text: {text}")
    
    # Get original tokens
    registry = TokenizerRegistry()
    registry.register_tokenizer(model)
    tokenizer = registry.tokenizers[model]
    original_tokens = tokenizer.tokenize(text)
    
    # Get vocabulary size
    vocab_size = get_vocab_size(tokenizer)
    
    # Apply obfuscation
    obfuscated_tokens = [(token + shift) % vocab_size for token in original_tokens]
    
    # Detokenize
    obfuscated_text = tokenizer.detokenize(obfuscated_tokens)
    
    print(f"\nOriginal tokens: {original_tokens}")
    print(f"Obfuscated tokens: {obfuscated_tokens}")
    print(f"Obfuscated text: {obfuscated_text}")
    
    # Verify reversibility
    reversed_tokens = [(token - shift) % vocab_size for token in obfuscated_tokens]
    reversed_text = tokenizer.detokenize(reversed_tokens)
    
    print(f"\nReversed tokens: {reversed_tokens}")
    print(f"Reversed text: {reversed_text}")
    
    if original_tokens == reversed_tokens:
        print(f"\n✓ Reversibility check passed")
    else:
        print(f"\n✗ Reversibility check failed")
    
    print(f"\n{'='*80}")
    print(f"VALIDATION RESULTS")
    print(f"{'='*80}")
    
    # Run validations
    validate_one_to_one_mapping(model, text, shift)
    compare_token_counts(model, text, shift)
    analyze_token_frequency(model, text, shift)


def main():
    # Default values instead of using argparse
    model = 'gpt-4'
    text = 'Hello, world! This is a test of the token obfuscation system.'
    shift = 42
    
    demonstrate_obfuscation(model, text, shift)


if __name__ == "__main__":
    main() 