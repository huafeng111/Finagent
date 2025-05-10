#!/usr/bin/env python3
# document_processor.py - Utility for loading and processing documents

from langchain_core.documents import Document
from typing import List, Union, Optional
import os
from langchain_community.document_loaders import PyPDFLoader

def load_document(file_path: str) -> List[Document]:
    """
    Load a document from a file path and return as a list of Document objects.
    
    Args:
        file_path: Path to the document file (supports .txt, .pdf)
        
    Returns:
        List of Document objects
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    file_extension = os.path.splitext(file_path)[1].lower()
    
    if file_extension == '.txt':
        return load_text_file(file_path)
    elif file_extension == '.pdf':
        return load_pdf_file(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")

def load_text_file(file_path: str) -> List[Document]:
    """Load a text file and convert to Document."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        return [Document(page_content=text, metadata={"source": file_path})]
    except UnicodeDecodeError:
        # Try with another encoding if utf-8 fails
        with open(file_path, 'r', encoding='latin-1') as f:
            text = f.read()
        return [Document(page_content=text, metadata={"source": file_path})]

def load_pdf_file(file_path: str) -> List[Document]:
    """Load a PDF file and convert to Document."""
    try:
        loader = PyPDFLoader(file_path)
        return loader.load()
    except ImportError:
        raise ImportError("PyPDFLoader requires extra dependencies. Install with: pip install langchain-community[pdf]") 