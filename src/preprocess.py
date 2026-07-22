import re
import emoji
from hazm import stopwords_list, Normalizer

normalizer = Normalizer()

HAZM_STOPWORDS = set(stopwords_list())
SENTIMENT_WORDS = {"خوب", "بد", "خیلی", "کم", "زیاد", "عالی", "نه", "نمی", "هیچ", "بهتر", "ترین", "بسیار", "افتضاح", "ضعیف", "ارزش"}
CUSTOM_NEUTRAL_WORDS = {"سلام", "ممنون", "مرسی", "تشکر", "ممنونم", "ممنونیم", "دستتون", "درد", "نکنه", "دیجی", "کالا", "دیجی‌کالا", "ارسال", "پیک", "بسته", "بسته‌بندی", "پست"}
STOP_WORDS = (HAZM_STOPWORDS | CUSTOM_NEUTRAL_WORDS) - SENTIMENT_WORDS

NUMBERS_PATTERN = re.compile(r"[0-9\u06f0-\u06f9\u0660-\u0669]")
ENGLISH_PATTERN = re.compile(r"[a-zA-Z]")
PUNCT_PATTERN = re.compile(r"[^\w\s\u200c]")
REPEATED_CHARS_PATTERN = re.compile(r"(.)\1{2,}")
SPACES_PATTERN = re.compile(r"\s+")

def clean_structure(text):
    """
    Cleans structural noise from the text including emojis, numbers, 
    English letters, punctuations, and redundant character repeats.
    """
    text = str(text)
    text = emoji.replace_emoji(text, replace="")      # Remove emojis
    text = NUMBERS_PATTERN.sub("", text)              # Remove English, Persian, and Arabic digits
    text = ENGLISH_PATTERN.sub("", text)              # Remove English characters/words
    text = PUNCT_PATTERN.sub("", text)                # Remove special characters and punctuation (keeps ZWNJ)
    text = REPEATED_CHARS_PATTERN.sub(r"\1", text)    # Reduce character elongation (e.g., "عاااالی" -> "عالی")
    text = SPACES_PATTERN.sub(" ", text).strip()      # Normalize multiple spaces and strip margins
    return text

def remove_stopwords(text):
    """Removes predefined custom and general stop words from the text."""
    words = text.split()
    filtered_words = [word for word in words if word not in STOP_WORDS] 

    return " ".join(filtered_words)

def preprocess_text(text, min_words: int = 3):
    """
    Main preprocessing pipeline that normalization, cleans text
    structure, removes stop words, and filters out short texts.
    """
    
    normalized_text = normalizer.normalize(text)
    cleaned = clean_structure(normalized_text)
    final_result = remove_stopwords(cleaned)
    words = final_result.split()
    
    if len(words) < min_words:
        return None
        
    return " ".join(words)
