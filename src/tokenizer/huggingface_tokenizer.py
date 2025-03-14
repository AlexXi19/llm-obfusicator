from transformers import AutoTokenizer
from .base_tokenizer import BaseTokenizer


class HuggingFaceTokenizer(BaseTokenizer):
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def tokenize(self, text: str) -> list:
        return self.tokenizer.encode(text, add_special_tokens=True)
        
    def detokenize(self, tokens: list) -> str:
        return self.tokenizer.decode(tokens)
