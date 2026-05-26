import fitz  # PyMuPDF
from typing import List, Dict

class PDFParser:
    def extract_text(self, file_path: str) -> List[Dict[str, str]]:
        """
        Extracts text from a PDF, preserving page structure and reading order.
        Returns a list of dictionaries containing page_number and raw_text.
        """
        extracted_pages = []
        try:
            doc = fitz.open(file_path)
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                # 'blocks' preserves rough spatial layout reading order
                blocks = page.get_text("blocks")
                # Sort blocks by y-coordinate then x-coordinate to maintain top-to-bottom reading order
                blocks.sort(key=lambda b: (b[1], b[0]))
                
                page_text = "\n".join([b[4].strip() for b in blocks if b[4].strip()])
                extracted_pages.append({
                    "page_number": page_num + 1,
                    "content": page_text
                })
        except Exception as e:
            raise RuntimeError(f"Failed to deterministicly parse PDF {file_path}: {e}")
            
        return extracted_pages
