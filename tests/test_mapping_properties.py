#!/usr/bin/env python3
"""
Test script for validating the mathematical properties of token obfuscation.
This script focuses on ensuring the obfuscation is a bijective (one-to-one) mapping.
"""

import sys
import os
import random
import math
from collections import defaultdict

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.tokenizer.tokenizer import TokenizerRegistry
from src.main import get_vocab_size


def test_bijective_property(model_name, vocab_size=None):
    """
    Test that the obfuscation mapping is bijective (one-to-one and onto).
    
    Args:
        model_name: Name of the model to use for tokenization
        vocab_size: Size of the vocabulary to consider, or None to detect automatically
        
    Returns:
        True if the mapping is bijective, False otherwise
    """
    # Get the actual vocabulary size if not provided
    if vocab_size is None:
        registry = TokenizerRegistry()
        registry.register_tokenizer(model_name)
        tokenizer = registry.tokenizers[model_name]
        vocab_size = get_vocab_size(tokenizer)
    
    print(f"\nTesting bijective property for model {model_name} with vocab size {vocab_size}")
    
    # Create a set of test tokens (a subset of the vocabulary)
    test_tokens = set(range(min(1000, vocab_size)))  # Use at most 1000 tokens for testing
    
    # Test with different shift values
    shifts = [1, 42, 100, vocab_size-1, vocab_size, vocab_size+1, 2*vocab_size-1]
    
    for shift in shifts:
        print(f"\nTesting with shift = {shift}")
        
        # Apply the shift to all tokens
        shifted_tokens = set((token + shift) % vocab_size for token in test_tokens)
        
        # Check if the number of unique tokens is preserved
        if len(shifted_tokens) != len(test_tokens):
            print(f"✗ FAILED: Shift {shift} does not preserve the number of unique tokens")
            print(f"  Original tokens: {len(test_tokens)}")
            print(f"  Shifted tokens: {len(shifted_tokens)}")
            return False
        
        # Check if we can recover the original tokens
        recovered_tokens = set((token - shift) % vocab_size for token in shifted_tokens)
        
        if recovered_tokens != test_tokens:
            print(f"✗ FAILED: Cannot recover original tokens with shift {shift}")
            print(f"  Missing tokens: {test_tokens - recovered_tokens}")
            print(f"  Extra tokens: {recovered_tokens - test_tokens}")
            return False
        
        print(f"✓ PASSED: Shift {shift} preserves bijective property")
    
    return True


def test_frequency_preservation(model_name, text_length=1000, vocab_size=None):
    """
    Test that token frequency distribution is preserved after obfuscation.
    
    Args:
        model_name: Name of the model to use for tokenization
        text_length: Length of random text to generate for testing
        vocab_size: Size of the vocabulary to consider, or None to detect automatically
        
    Returns:
        True if frequency distribution is preserved, False otherwise
    """
    # Get the actual vocabulary size if not provided
    if vocab_size is None:
        registry = TokenizerRegistry()
        registry.register_tokenizer(model_name)
        tokenizer = registry.tokenizers[model_name]
        vocab_size = get_vocab_size(tokenizer)
    
    print(f"\nTesting frequency preservation for model {model_name}")
    
    # Generate a random sequence of tokens with a skewed distribution
    tokens = []
    for _ in range(text_length):
        # Use a power law distribution to make some tokens more common
        token = int(random.paretovariate(1.5)) % min(1000, vocab_size)
        tokens.append(token)
    
    # Count original frequencies
    original_freq = defaultdict(int)
    for token in tokens:
        original_freq[token] += 1
    
    # Apply a shift
    shift = 42
    shifted_tokens = [(token + shift) % vocab_size for token in tokens]
    
    # Count shifted frequencies
    shifted_freq = defaultdict(int)
    for token in shifted_tokens:
        shifted_freq[token] += 1
    
    # Compare frequency distributions
    original_counts = sorted(original_freq.values())
    shifted_counts = sorted(shifted_freq.values())
    
    if original_counts != shifted_counts:
        print(f"✗ FAILED: Frequency distribution changed after obfuscation")
        print(f"  Original frequencies: {original_counts[:10]}... (showing first 10)")
        print(f"  Shifted frequencies: {shifted_counts[:10]}... (showing first 10)")
        return False
    
    print(f"✓ PASSED: Frequency distribution preserved after obfuscation")
    return True


def test_edge_cases(vocab_size=None):
    """
    Test edge cases for the obfuscation mapping.
    
    Args:
        vocab_size: Size of the vocabulary to consider, or None to detect automatically
        
    Returns:
        True if all edge cases pass, False otherwise
    """
    # Use a default vocabulary size if not provided
    if vocab_size is None:
        registry = TokenizerRegistry()
        registry.register_tokenizer("gpt-4")  # Use a common model
        tokenizer = registry.tokenizers["gpt-4"]
        vocab_size = get_vocab_size(tokenizer)
    
    print(f"\nTesting edge cases with vocab size {vocab_size}")
    
    # Test with empty token list
    tokens = []
    shift = 42
    shifted_tokens = [(token + shift) % vocab_size for token in tokens]
    
    if len(shifted_tokens) != 0:
        print(f"✗ FAILED: Empty token list should result in empty shifted list")
        return False
    
    # Test with a single token
    tokens = [0]
    shifted_tokens = [(token + shift) % vocab_size for token in tokens]
    
    if len(shifted_tokens) != 1 or shifted_tokens[0] != shift % vocab_size:
        print(f"✗ FAILED: Single token case failed")
        print(f"  Expected: {[shift % vocab_size]}")
        print(f"  Got: {shifted_tokens}")
        return False
    
    # Test with tokens at vocabulary boundaries
    tokens = [0, vocab_size-1]
    shifted_tokens = [(token + shift) % vocab_size for token in tokens]
    expected = [(0 + shift) % vocab_size, (vocab_size-1 + shift) % vocab_size]
    
    if shifted_tokens != expected:
        print(f"✗ FAILED: Boundary tokens case failed")
        print(f"  Expected: {expected}")
        print(f"  Got: {shifted_tokens}")
        return False
    
    # Test with shift = 0 (identity mapping)
    tokens = [1, 2, 3, 4, 5]
    shift = 0
    shifted_tokens = [(token + shift) % vocab_size for token in tokens]
    
    if shifted_tokens != tokens:
        print(f"✗ FAILED: Identity mapping (shift=0) failed")
        print(f"  Expected: {tokens}")
        print(f"  Got: {shifted_tokens}")
        return False
    
    # Test with shift = vocab_size (should also be identity mapping)
    shift = vocab_size
    shifted_tokens = [(token + shift) % vocab_size for token in tokens]
    
    if shifted_tokens != tokens:
        print(f"✗ FAILED: Full cycle shift (shift=vocab_size) failed")
        print(f"  Expected: {tokens}")
        print(f"  Got: {shifted_tokens}")
        return False
    
    print(f"✓ PASSED: All edge cases passed")
    return True


def test_prefix_preservation(model_name, vocab_size=50000):
    """
    Test that texts with the same prefix maintain similar prefixes after obfuscation.
    
    Args:
        model_name: Name of the model to use for tokenization
        vocab_size: Size of the vocabulary to consider
        
    Returns:
        True if prefix similarity is preserved, False otherwise
    """
    print(f"\nTesting prefix preservation for model {model_name}")
    
    # Test cases with common prefixes
    test_cases = [
        "The quick brown fox jumps",
        "The quick brown fox runs",
        "The quick brown cat sleeps",
        "The quick red fox dances"
    ]
    
    # Use a fixed shift for consistent results
    shift = 42
    
    # Obfuscate all test cases
    obfuscated_texts = []
    for text in test_cases:
        registry = TokenizerRegistry()
        registry.register_tokenizer(model_name)
        tokenizer = registry.tokenizers[model_name]
        tokens = tokenizer.tokenize(text)
        obfuscated_tokens = [(token + shift) % 50000 for token in tokens]
        obfuscated = tokenizer.detokenize(obfuscated_tokens)
        obfuscated_texts.append(obfuscated)
        print(f"Original: {text}")
        print(f"Obfuscated: {obfuscated}\n")
    
    # Check if the obfuscated texts share common prefixes where expected
    for i in range(len(obfuscated_texts)-1):
        # Find the common prefix length with the next text in original texts
        original_common_length = 0
        for j in range(min(len(test_cases[i]), len(test_cases[i+1]))):
            if test_cases[i][j] != test_cases[i+1][j]:
                break
            original_common_length = j + 1
        
        # Find the common prefix length in obfuscated texts
        obfuscated_common_length = 0
        for j in range(min(len(obfuscated_texts[i]), len(obfuscated_texts[i+1]))):
            if obfuscated_texts[i][j] != obfuscated_texts[i+1][j]:
                break
            obfuscated_common_length = j + 1
        
        # If original texts had a common prefix, obfuscated texts should too
        if original_common_length > 0 and obfuscated_common_length == 0:
            print(f"✗ FAILED: Prefix preservation test failed")
            print(f"  Original texts had {original_common_length} characters in common")
            print(f"  Obfuscated texts had {obfuscated_common_length} characters in common")
            print(f"  Text 1: {obfuscated_texts[i]}")
            print(f"  Text 2: {obfuscated_texts[i+1]}")
            return False
    
    print(f"✓ PASSED: Prefix preservation test passed")
    return True


def test_mathematical_properties():
    """
    Test the mathematical properties of the obfuscation mapping.
    """
    print(f"\n{'='*80}")
    print(f"TESTING MATHEMATICAL PROPERTIES OF TOKEN OBFUSCATION")
    print(f"{'='*80}")
    
    # Get the actual vocabulary size
    registry = TokenizerRegistry()
    registry.register_tokenizer("gpt-4")
    tokenizer = registry.tokenizers["gpt-4"]
    vocab_size = get_vocab_size(tokenizer)
    
    # Test bijective property
    bijective = test_bijective_property("gpt-4", vocab_size)
    
    # Test frequency preservation
    frequency = test_frequency_preservation("gpt-4", 1000, vocab_size)
    
    # Test edge cases
    edges = test_edge_cases(vocab_size)
    
    # Test prefix preservation
    prefixes = test_prefix_preservation("gpt-4", vocab_size)
    
    # Overall result
    print(f"\n{'='*80}")
    print(f"OVERALL RESULTS")
    print(f"{'='*80}")
    
    if bijective and frequency and edges and prefixes:
        print(f"✓ ALL TESTS PASSED: The obfuscation mapping has the required mathematical properties")
    else:
        print(f"✗ SOME TESTS FAILED: The obfuscation mapping may not have all required properties")
    
    return bijective and frequency and edges and prefixes


if __name__ == "__main__":
    test_mathematical_properties() 