#!/usr/bin/env python3
"""
Test script for real-world examples and practical use cases of token obfuscation.
This script tests the obfuscation system with various types of content.
"""

import sys
import os
import time

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.main import tokenize_text, obfuscate_text
from src.tokenizer.tokenizer import TokenizerRegistry


# Sample texts for different domains
SAMPLE_TEXTS = {
    "code": """
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

# Calculate the 10th Fibonacci number
result = fibonacci(10)
print(f"The 10th Fibonacci number is {result}")
""",
    
    "prose": """
The quick brown fox jumps over the lazy dog. This pangram contains every letter of the English alphabet at least once. Pangrams are often used to test fonts, keyboards, and other text-related tools. The most famous pangram is probably "The quick brown fox jumps over the lazy dog."
""",
    
    "technical": """
The Transformer architecture, introduced in the paper "Attention is All You Need," has revolutionized natural language processing. It relies on a self-attention mechanism that allows the model to weigh the importance of different words in a sentence when making predictions. This has led to models like BERT, GPT, and T5, which have achieved state-of-the-art results on various NLP tasks.
""",
    
    "multilingual": """
English: Hello, world!
Spanish: ¡Hola, mundo!
French: Bonjour, monde!
German: Hallo, Welt!
Chinese: 你好，世界！
Japanese: こんにちは、世界！
Arabic: مرحبا بالعالم!
""",
    
    "special_chars": """
!@#$%^&*()_+-=[]{}|;':",./<>?`~
€£¥©®™§±×÷≠≈∞≤≥∑∏√∫∂∆π
😀😃😄😁😆😅🤣😂🙂🙃😉😊😇
""",
}


def test_real_world_examples(model_name, shift=42):
    """
    Test the obfuscation system with real-world examples.
    
    Args:
        model_name: Name of the model to use for tokenization
        shift: Shift value for obfuscation
    """
    print(f"\n{'='*80}")
    print(f"TESTING REAL-WORLD EXAMPLES WITH MODEL: {model_name}")
    print(f"{'='*80}")
    
    results = {}
    
    for domain, text in SAMPLE_TEXTS.items():
        print(f"\nTesting domain: {domain}")
        print(f"{'='*40}")
        
        try:
            # Get original token count
            start_time = time.time()
            original_tokens = tokenize_text(model_name, text)
            tokenize_time = time.time() - start_time
            
            # Obfuscate the text
            start_time = time.time()
            obfuscated = obfuscate_text(model_name, text, shift=shift)
            obfuscate_time = time.time() - start_time
            
            # Get obfuscated token count
            obfuscated_tokens = tokenize_text(model_name, obfuscated)
            
            # Print results
            print(f"Original text (first 50 chars): {text[:50]}...")
            print(f"Obfuscated text (first 50 chars): {obfuscated[:50]}...")
            print(f"Original token count: {len(original_tokens)}")
            print(f"Obfuscated token count: {len(obfuscated_tokens)}")
            print(f"Tokenization time: {tokenize_time:.4f} seconds")
            print(f"Obfuscation time: {obfuscate_time:.4f} seconds")
            
            # Check if token counts match
            if len(original_tokens) == len(obfuscated_tokens):
                print(f"✓ PASSED: Token counts match")
                result = "PASS"
            else:
                print(f"✗ FAILED: Token counts don't match")
                result = "FAIL"
            
            results[domain] = {
                "original_count": len(original_tokens),
                "obfuscated_count": len(obfuscated_tokens),
                "tokenize_time": tokenize_time,
                "obfuscate_time": obfuscate_time,
                "result": result
            }
            
        except Exception as e:
            print(f"✗ ERROR: {str(e)}")
            results[domain] = {"result": "ERROR", "error": str(e)}
    
    # Print summary
    print(f"\n{'='*80}")
    print(f"SUMMARY")
    print(f"{'='*80}")
    
    all_passed = True
    for domain, result in results.items():
        status = result["result"]
        if status == "PASS":
            print(f"✓ {domain}: PASSED")
        else:
            all_passed = False
            print(f"✗ {domain}: FAILED - {result.get('error', '')}")
    
    if all_passed:
        print(f"\n✓ ALL TESTS PASSED: The obfuscation system works well with all tested content types")
    else:
        print(f"\n✗ SOME TESTS FAILED: The obfuscation system may have issues with certain content types")


def test_practical_use_case(model_name, shift=42):
    """
    Test a practical use case: obfuscating sensitive information.
    
    Args:
        model_name: Name of the model to use for tokenization
        shift: Shift value for obfuscation
    """
    print(f"\n{'='*80}")
    print(f"TESTING PRACTICAL USE CASE: OBFUSCATING SENSITIVE INFORMATION")
    print(f"{'='*80}")
    
    # Sample sensitive information
    sensitive_text = """
Personal Information:
Name: John Doe
Email: john.doe@example.com
Phone: (555) 123-4567
SSN: 123-45-6789
Credit Card: 4111-1111-1111-1111
Password: p@ssw0rd123!
"""
    
    try:
        # Obfuscate the sensitive information
        obfuscated = obfuscate_text(model_name, sensitive_text, shift=shift)
        
        print(f"Original sensitive text:\n{sensitive_text}\n")
        print(f"Obfuscated text:\n{obfuscated}\n")
        
        # Check if sensitive patterns are still recognizable
        sensitive_patterns = [
            "John Doe",
            "john.doe@example.com",
            "(555) 123-4567",
            "123-45-6789",
            "4111-1111-1111-1111",
            "p@ssw0rd123!"
        ]
        
        found_patterns = 0
        for pattern in sensitive_patterns:
            if pattern in obfuscated:
                found_patterns += 1
                print(f"✗ WARNING: Sensitive pattern '{pattern}' is still recognizable in the obfuscated text")
        
        if found_patterns == 0:
            print(f"✓ PASSED: No sensitive patterns are directly recognizable in the obfuscated text")
        else:
            print(f"✗ WARNING: {found_patterns} sensitive patterns are still recognizable")
        
        # Verify we can recover the original text
        registry = TokenizerRegistry()
        registry.register_tokenizer(model_name)
        tokenizer = registry.tokenizers[model_name]
        
        # Tokenize obfuscated text
        obfuscated_tokens = tokenizer.tokenize(obfuscated)
        
        # Apply reverse shift
        recovered_tokens = [(token - shift) % 50000 for token in obfuscated_tokens]
        
        # Detokenize
        recovered_text = tokenizer.detokenize(recovered_tokens)
        
        if recovered_text == sensitive_text:
            print(f"✓ PASSED: Successfully recovered the original text from obfuscated text")
        else:
            print(f"✗ FAILED: Could not recover the original text")
            print(f"Original: {sensitive_text[:50]}...")
            print(f"Recovered: {recovered_text[:50]}...")
        
    except Exception as e:
        print(f"✗ ERROR: {str(e)}")


def main():
    # Default values instead of using argparse
    model = 'gpt-4'
    shift = 42
    
    test_real_world_examples(model, shift)
    test_practical_use_case(model, shift)


if __name__ == "__main__":
    main() 