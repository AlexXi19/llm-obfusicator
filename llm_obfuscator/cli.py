#!/usr/bin/env python3
"""
Command-line interface for the LLM Token Obfuscator.
"""

import argparse
import sys
from llm_obfuscator import tokenize_text, obfuscate_text, __version__

def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="LLM Token Obfuscator - A tool for obfuscating text by manipulating token IDs"
    )
    parser.add_argument(
        "--version", action="version", version=f"llm-obfuscator {__version__}"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Tokenize command
    tokenize_parser = subparsers.add_parser("tokenize", help="Tokenize text using a model's tokenizer")
    tokenize_parser.add_argument("model", help="Model name to use for tokenization (e.g., gpt-4, gpt2)")
    tokenize_parser.add_argument("text", help="Text to tokenize")
    
    # Obfuscate command
    obfuscate_parser = subparsers.add_parser("obfuscate", help="Obfuscate text by shifting token IDs")
    obfuscate_parser.add_argument("model", help="Model name to use for tokenization (e.g., gpt-4, gpt2)")
    obfuscate_parser.add_argument("text", help="Text to obfuscate")
    obfuscate_parser.add_argument("--shift", type=int, help="Fixed shift value for token mapping (optional)")
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        sys.exit(1)
    
    if args.command == "tokenize":
        tokens = tokenize_text(args.model, args.text)
        print(f"Tokens: {tokens}")
        print(f"Token count: {len(tokens)}")
    
    elif args.command == "obfuscate":
        shift = args.shift if hasattr(args, "shift") and args.shift is not None else None
        obfuscated = obfuscate_text(args.model, args.text, shift=shift)
        print(f"Original text: {args.text}")
        print(f"Obfuscated text: {obfuscated}")
        tokens = tokenize_text(args.model, obfuscated)
        print(f"Token count: {len(tokens)}")

if __name__ == "__main__":
    main() 