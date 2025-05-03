#!/usr/bin/env python3
# document_processor.py - Utilities for document processing

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

def load_document(file_path):
    """Load document from PDF or text file
    
    Args:
        file_path (str): Path to the document file
        
    Returns:
        list: List of Document objects
    """
    import os
    
    # Check if the file exists first
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Error: File not found at path: {file_path}")

    _, ext = os.path.splitext(file_path)
    
    if ext.lower() == '.pdf':
        loader = PyPDFLoader(file_path)
        return loader.load()
    elif ext.lower() == '.txt':
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text_content = f.read()
            # Return as a list containing one Document object, similar to TextLoader
            return [Document(page_content=text_content, metadata={'source': file_path})]
        except Exception as e:
            raise ValueError(f"Error reading text file {file_path}: {e}") from e
    else:
        # Keep handling for other text-based formats if needed, 
        # or raise an error for unsupported types.
        # For now, let's assume only .txt and .pdf are primary targets
        # and other types might need specific loaders or raise error.
        # Using a generic approach for other potential text types, 
        # falling back to TextLoader but without complex encoding checks.
        try:
            # Using default TextLoader for other potential text files
            from langchain_community.document_loaders import TextLoader 
            loader = TextLoader(file_path, encoding='utf-8') 
            return loader.load()
        except Exception as e:
             raise ValueError(f"Unsupported file type or error loading file {file_path}: {e}")
