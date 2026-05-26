import os
import logging
from typing import Dict, Any

from app.parsers.pdf_parser import PDFParser
from app.parsers.pptx_parser import PPTXParser
from app.preprocessing.text_cleaner import TextCleaner
from app.chunking.segmenter import DocumentSegmenter
from app.extraction.missing_data import MissingDataDetector

logger = logging.getLogger("ElephantTank.DocumentIngestion")

class IngestionWorkflow:
    def __init__(self):
        self.pdf_parser = PDFParser()
        self.pptx_parser = PPTXParser()
        self.cleaner = TextCleaner()
        self.segmenter = DocumentSegmenter()
        self.detector = MissingDataDetector()
        
    def process_document(self, file_path: str) -> Dict[str, Any]:
        """
        Orchestrates the deterministic Document Understanding pipeline:
        File -> Parser -> Cleaner -> Chunking -> Missing Data Annotation.
        """
        logger.info(f"Initiating ingestion pipeline for: {file_path}")
        ext = os.path.splitext(file_path)[1].lower()
        
        # 1. Deterministic Parsing Layer
        if ext == ".pdf":
            raw_pages = self.pdf_parser.extract_text(file_path)
        elif ext in [".ppt", ".pptx"]:
            raw_pages = self.pptx_parser.extract_text(file_path)
        else:
            raise ValueError(f"Unsupported startup artifact format: {ext}")
            
        # 2. Text Cleaning & Normalization Layer
        cleaned_pages = []
        for page in raw_pages:
            cleaned_text = self.cleaner.clean_text(page["content"])
            cleaned_pages.append({"page_number": page.get("page_number", page.get("slide_number")), "content": cleaned_text})
            
        # 3. Intelligent Chunking Layer
        chunks = self.segmenter.segment_by_slide(cleaned_pages)
        logger.info(f"Ingestion generated {len(chunks)} robust semantic chunks.")
        
        # 4. Extraction & Schema Mapping Simulation
        # (This stage maps chunk regex/LLM outputs into the StartupIntelligenceOutput schema)
        extracted_data = {
            "status": "INGESTED_AND_CHUNKED",
            "total_semantic_chunks": len(chunks),
            "chunks_sample": chunks[:2] if chunks else []
        }
        
        return extracted_data
