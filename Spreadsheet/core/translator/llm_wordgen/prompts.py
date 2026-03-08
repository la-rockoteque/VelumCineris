def new_lexem_prompt(concept, language, grammar_info, examples, language_metadata=None, root_words=None, deviation=10.0):
  """
  Create a natural-language prompt for LLM lexeme creation.
  """

  # Build language metadata section if available
  metadata_section = ""
  if language_metadata:
    metadata_section = f"""
Language metadata:
{language_metadata}

"""

  # Build root words section if provided
  root_section = ""
  if root_words:
    root_list = [f'  - "{word}" (from {lang})' for lang, word in root_words.items()]
    root_lines = "\n".join(root_list)
    root_section = f"""
Root words (use ALL as blended inspiration):
{root_lines}

IMPORTANT - Blended derivation approach:
- These roots provide INSPIRATION, not prescription
- Blend phonological and morphological elements from ALL provided roots
- Create a word that feels like it evolved from this mixed ancestry
- Apply the phonotactic rules of {language} to create a natural-sounding result
- The blend should honor the sound patterns and style of all root languages
- Think of this as creating a word in a creole or mixed language
- The word should feel related to the roots but adapted to {language}'s system

"""

  # Build deviation section
  deviation_section = f"""
IMPORTANT - Grammar deviation allowed ({deviation:.1f}%):
- You are ALLOWED to deviate from the strict grammar rules by up to {deviation:.1f}%
- This helps prevent duplicate words and adds natural variation
- Minor phonological variations are encouraged (different consonants, vowel qualities, stress patterns)
- You can slightly bend phonotactic rules, syllable structures, or morphological patterns
- The result should still sound like it belongs to {language}, but with creative flexibility
- This deviation is ESSENTIAL to avoid generating the same word repeatedly

"""

  return f"""
You are generating new vocabulary for the constructed language "{language}".

{metadata_section}{root_section}{deviation_section}Language guidelines:
{grammar_info}

Task:
Generate a new word in {language} meaning: "{concept}".

Requirements:
- Follow the phonotactics and style of the examples.
- Output ONLY the lexeme. No quotes, explanation, or extra text.
- Do NOT reuse the same base root for different concepts.
- Every new word must have a unique root.
- Avoid outputs that differ only by small vowel changes.
- Use the allowed {deviation:.1f}% deviation to ensure uniqueness.
"""

def script_symbol_prompt(language, unicode_range, symbol, category, place_or_height, manner_or_backness, voicing, allow_deduplication=False):
  """
  Create a prompt for generating a script glyph for a phoneme, designed for small LLMs.

  Args:
    allow_deduplication: If True, the LLM can generate multi-character symbols (e.g., ":;." as one symbol)
  """

  # Build deduplication section if enabled
  deduplication_section = ""
  if allow_deduplication:
    deduplication_section = """
IMPORTANT - Deduplication enabled:
- You can use MULTIPLE characters from the Unicode range to create a single symbol.
- For example: ":;." or "!?" could represent one phoneme.
- This allows for greater variety and distinction between phonemes.
- Multi-character symbols should still be visually coherent and distinct.

"""

  glyph_description = "ONE glyph (one Unicode character or a character + diacritic)" if not allow_deduplication else "ONE symbol (can be single or multiple characters from the range)"

  return f"""
You are generating a writing-system symbol for the constructed language "{language}".

The script must use ONLY characters inside this Unicode range:
{unicode_range}

{deduplication_section}Your task:
Produce {glyph_description} representing the phoneme "{symbol}".

Rules for construction:
- Stay strictly within the Unicode range.
- If a modification is needed, prefer adding combining marks rather than inventing shapes.
- Ensure each phoneme gets a distinct glyph.
- Derive the variation from these features:
  • Category: {category}
  • Place/Height: {place_or_height}
  • Manner/Backness: {manner_or_backness}
  • Voicing: {voicing}

Shaping guidelines for small models (apply simply):
- Base form comes from the Unicode range.
- Modify shape using these simple rules:
  • Voiced → add a dot.
  • Voiceless → plain.
  • Nasal → add a tail (use a combining diacritic).
  • Fricative → add a slash.
  • Approximant → use a rounder variant if available.
  • Vowel → pick a symbol from the middle of the range; consonant → from the start.

Output requirements:
- Output ONLY the constructed glyph. No explanation.
"""

def phonetics_prompt(word, language):
  """
  Create a prompt for generating IPA phonetic notation for a word in a constructed language.

  Args:
    word: The lexeme/word to generate phonetics for
    language: The name of the constructed language

  Returns:
    A prompt string for the LLM
  """

  return f"""
You are generating IPA (International Phonetic Alphabet) phonetic notation for words in the constructed language "{language}".

Your task:
Produce the IPA transcription for the word: "{word}"

Guidelines:
- Use standard IPA symbols
- Consider the phonotactics and sound patterns typical of the language
- The transcription should be pronounceable and follow natural language phonological rules
- Use standard IPA conventions for stress, length, and other suprasegmental features if needed
- Enclose the transcription in forward slashes: /transcription/

Output requirements:
- Output ONLY the IPA transcription in forward slashes (e.g., /ˈfɒnətɪks/)
- No explanation, no additional text
- Just the phonetic transcription

Example format: /ˈwɜːd/
"""
