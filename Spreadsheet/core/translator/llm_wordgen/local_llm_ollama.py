# llm_wordgen/local_llm_ollama.py

import subprocess
import json
from .interface import LexemeGenerator
from .prompts import new_lexem_prompt
import ollama

class OllamaLexemeGenerator(LexemeGenerator):
  def __init__(self, model="llama3"):
    self.model = model

  def generate(self, concept, language, grammar_info, examples, language_metadata=None, root_words=None, deviation=10.0):
    prompt = new_lexem_prompt(concept, language, grammar_info, examples, language_metadata, root_words=root_words, deviation=deviation)
    result = ollama.generate(model="llama3", prompt=prompt)

    # Extract only alphabetic characters for lexemes
    return result['response']