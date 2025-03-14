# LLM Token Obfuscator

A tool for obfuscating text by manipulating token IDs while preserving token count and structure. Originally developed for benchmarking LLM inference performance and prefix caching behavior by generating test data that maintains token patterns but with obscured text.

## Overview

This project provides a system for obfuscating text by applying a shift to token IDs. The obfuscation is reversible and preserves the token count, making it useful for:

- Testing LLM systems with obfuscated content
- Benchmarking tokenization performance
- Creating privacy-preserving datasets
- Generating synthetic text with realistic token distributions

Example of obfuscated text patterns:

```
Original: The quick brown fox jumps
Obfuscated: eng($_ ét rl manga

Original: The quick brown fox runs
Obfuscated: eng($_ ét rl Android
```

Note how the common prefix "The quick brown" is obfuscated to "eng($\_ ét" in both cases, preserving the pattern.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/llm-obfusicator.git
cd llm-obfusicator
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```python
from src.main import obfuscate_text

# Obfuscate text using a specific model's tokenizer
obfuscated = obfuscate_text("gpt-4", "Hello, world!")
print(obfuscated)

# Use a fixed shift value for deterministic results
obfuscated = obfuscate_text("gpt-4", "Hello, world!", shift=42)
print(obfuscated)
```

### Supported Models

The system supports both OpenAI and HuggingFace tokenizers:

- OpenAI models: `gpt-4`, `gpt-3.5-turbo`, `cl100k_base`, etc.
- HuggingFace models: `gpt2`, `bert-base-uncased`, etc.

## Testing

The project includes several test suites to validate the obfuscation system:

### Running All Tests

The easiest way to run all tests is to use the provided shell script:

```bash
# Make the script executable (if needed)
chmod +x run_all_tests.sh

# Run all tests
./run_all_tests.sh
```

This will run all test files in sequence, including unit tests and specialized test scripts.

### Running Basic Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test.py
```

### Specialized Test Scripts

The project includes specialized test scripts for different aspects of the obfuscation system:

```bash
# Test with real-world examples
python tests/test_real_world.py

# Test obfuscation demonstration
python tests/test_obfuscation.py

# Test mathematical properties
python tests/test_mapping_properties.py
```

## Validation

The obfuscation system has been validated to ensure:

1. **Token Count Preservation**: The number of tokens remains the same after obfuscation
2. **One-to-One Mapping**: The obfuscation is a bijective (one-to-one) mapping
3. **Frequency Preservation**: Token frequency distributions are preserved
4. **Reversibility**: The original text can be recovered by applying the reverse shift

## How It Works

The obfuscation process works as follows:

1. Text is tokenized using the specified model's tokenizer
2. Each token ID is shifted by a fixed amount (either specified or randomly generated)
3. The shifted tokens are detokenized back to text

The shift operation is performed modulo the vocabulary size (typically 50,000) to ensure all tokens remain within the valid vocabulary range.

> **Note**: The token count preservation has a known margin of error of up to 8% for obscured texts. We are working on improving this.

## License

[MIT License](LICENSE)
