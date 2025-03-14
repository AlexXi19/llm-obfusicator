"""
LLM Token Obfuscator

A tool for obfuscating text by manipulating token IDs while preserving token count and structure.
"""

__version__ = "0.1.0"

from llm_obfuscator.main import tokenize_text, obfuscate_text, get_vocab_size
