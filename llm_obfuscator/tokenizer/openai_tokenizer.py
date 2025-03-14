import tiktoken
from .base_tokenizer import BaseTokenizer


class OpenAITokenizer(BaseTokenizer):
    def __init__(self, model_name: str):
        self.model_name = model_name
        try:
            self.encoder = tiktoken.encoding_for_model(model_name)
        except KeyError:
            try:
                self.encoder = tiktoken.get_encoding(model_name)
            except KeyError:
                raise ValueError(
                    f"Invalid model or tokenizer name: {model_name}")

    def tokenize(self, text: str) -> list:
        return self.encoder.encode(text)
        
    def detokenize(self, tokens: list) -> str:
        return self.encoder.decode(tokens)
