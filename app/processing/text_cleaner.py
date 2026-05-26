import re
import logging

logger = logging.getLogger("ElephantTank.Processing.TextCleaner")

class TextCleaner:
    @staticmethod
    def clean(raw_text: str) -> str:
        """Cleans and normalizes extracted text."""
        # Remove multiple newlines
        cleaned = re.sub(r'\n+', '\n', raw_text)
        # Remove multiple spaces
        cleaned = re.sub(r'[ \t]+', ' ', cleaned)
        # Remove unprintable chars but keep basic punctuation
        cleaned = "".join(ch for ch in cleaned if ch.isprintable() or ch == '\n')
        return cleaned.strip()
