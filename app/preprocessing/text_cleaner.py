import re

class TextCleaner:
    def clean_text(self, raw_text: str) -> str:
        """
        Normalizes whitespace, removes encoding artifacts, and standardizes punctuation.
        Crucially preserves startup terminology and financial metrics.
        """
        # Purge null bytes or obscure encoding artifacts
        text = raw_text.replace('\x00', '')
        
        # Standardize hyphens and long dashes
        text = re.sub(r'[\u2010-\u2015]', '-', text)
        
        # De-hyphenate words forcefully split across visual document lines (e.g. "start-\nup" -> "startup")
        text = re.sub(r'([a-zA-Z]+)-\n([a-zA-Z]+)', r'\1\2', text)
        
        # Standardize smart quotes to programmatically safe strings
        text = re.sub(r'[\u2018\u2019]', "'", text)
        text = re.sub(r'[\u201C\u201D]', '"', text)
        
        # Normalize structural whitespace (replace excessive newlines with a neat delimiter)
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r'[ \t]+', ' ', text)
        
        return text.strip()
