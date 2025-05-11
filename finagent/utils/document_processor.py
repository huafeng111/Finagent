#!/usr/bin/env python3
# document_processor.py - Utilities for document processing

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_document(file_path):
    """Load document from PDF or text file
    
    Args:
        file_path (str): Path to the document file
        
    Returns:
        list: List of Document objects
    """
    import os
    
    _, ext = os.path.splitext(file_path)
    
    if ext.lower() == '.pdf':
        loader = PyPDFLoader(file_path)
    else:
        loader = TextLoader(file_path)
    
    return loader.load()

def split_documents(documents, chunk_size=4000, chunk_overlap=200):
    """Split documents into chunks for processing
    
    Args:
        documents (list): List of Document objects
        chunk_size (int): Size of each chunk
        chunk_overlap (int): Overlap between chunks
        
    Returns:
        list: List of Document chunks
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    
    return text_splitter.split_documents(documents) 