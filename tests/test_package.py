"""
Test the package functionality.
"""

import pytest
from llm_obfuscator import tokenize_text, obfuscate_text

def test_tokenize_text():
    """Test tokenizing text."""
    text = "Hello, world!"
    tokens = tokenize_text("gpt-4", text)
    assert isinstance(tokens, list)
    assert len(tokens) > 0

def test_obfuscate_text():
    """Test obfuscating text."""
    text = "Hello, world!"
    obfuscated = obfuscate_text("gpt-4", text, shift=42)
    assert isinstance(obfuscated, str)
    assert obfuscated != text  # Obfuscated text should be different

def test_token_count_preservation():
    """Test that token count is preserved after obfuscation."""
    text = "Hello, world! This is a test of the token count preservation."
    tokens_original = tokenize_text("gpt-4", text)
    obfuscated = obfuscate_text("gpt-4", text, shift=42)
    tokens_obfuscated = tokenize_text("gpt-4", obfuscated)
    
    # Token count should be the same or very close (within 8% as mentioned in README)
    assert abs(len(tokens_original) - len(tokens_obfuscated)) / len(tokens_original) <= 0.08 