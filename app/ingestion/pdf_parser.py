import fitz  # PyMuPDF
import logging

logger = logging.getLogger("ElephantTank.Ingestion.PDF")

class PDFExtractor:
    @staticmethod
    def extract_text(file_path: str) -> str:
        """Extracts text from a PDF document sequentially."""
        logger.info(f"Extracting PDF text from: {file_path}")
        text_content = []
        try:
            with fitz.open(file_path) as doc:
                for page_num in range(len(doc)):
                    page = doc.load_page(page_num)
                    text_content.append(page.get_text("text"))
            return "\n".join(text_content)
        except Exception as e:
            logger.error(f"Failed to parse PDF {file_path}: {e}")
            raise ValueError(f"Could not parse PDF: {e}")
