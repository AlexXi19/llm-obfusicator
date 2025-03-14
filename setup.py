from setuptools import setup, find_packages
import os

# Read the contents of the README file
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="llm-obfuscator",
    version="0.1.0",
    author="Alex",
    author_email="your.email@example.com",  # Replace with your email
    description="A tool for obfuscating text by manipulating token IDs while preserving token count and structure",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/llm-obfusicator",  # Replace with your actual repository URL
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing",
    ],
    python_requires=">=3.8",
    install_requires=[
        "tiktoken>=0.5.0",
        "transformers>=4.30.0",
        "numpy>=1.20.0",
    ],
    entry_points={
        "console_scripts": [
            "llm-obfuscator=llm_obfuscator.cli:main",
        ],
    },
    keywords="llm, tokenization, obfuscation, nlp, ai",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/llm-obfusicator/issues",
        "Source": "https://github.com/yourusername/llm-obfusicator",
    },
) 