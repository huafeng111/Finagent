#!/usr/bin/env python3
# valuation_agent.py - Agent for company stock valuation

import json
import os # Import os module
from langchain.tools import Tool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain.chains import load_summarize_chain

class ValuationAgent:
    def __init__(self, openai_api_key=None):
        """Initialize the valuation agent with the required tools and chains."""
        # Initialize LLM
        self.llm = ChatOpenAI(
            model_name="gpt-4o", 
            temperature=0,
            openai_api_key=openai_api_key
        )
        
        # Initialize text splitter for large documents
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=4000,
            chunk_overlap=200
        )
        
        # --- Load the valuation prompt from file ---
        # Construct the path to the prompt file relative to this script's location
        current_dir = os.path.dirname(os.path.abspath(__file__))
        prompt_path = os.path.join(current_dir, '..', 'prompts', 'price_eval.prompt')

        try:
            with open(prompt_path, 'r', encoding='utf-8') as f:
                valuation_template = f.read()
        except FileNotFoundError:
             # Fallback or error handling if the prompt file is missing
             print(f"Error: Prompt file not found at {prompt_path}")
             # You might want to raise an exception or use a default prompt here
             raise 
        except Exception as e:
            print(f"Error reading prompt file {prompt_path}: {e}")
            raise
        # --- End loading prompt --- 
        
        self.valuation_prompt = PromptTemplate(
            input_variables=["text"],
            template=valuation_template
        )
        
        self.valuation_chain = self.valuation_prompt | self.llm
        
        # Create summarization chain for large documents
        self.summary_chain = load_summarize_chain(
            llm=self.llm,
            chain_type="stuff",
            verbose=False
        )
    
    def analyze(self, documents):
        """Analyze the provided documents and return valuation results.
        
        Args:
            documents: A list of Document objects containing financial text
            
        Returns:
            A JSON string containing the valuation analysis
        """
        # If we have multiple documents or a large document, we need to summarize first
        if len(documents) > 1 or len(documents[0].page_content) > 8000:
            # Split into chunks if needed
            all_splits = []
            for doc in documents:
                splits = self.text_splitter.split_text(doc.page_content)
                all_splits.extend([Document(page_content=s) for s in splits])
            
            # Summarize the content
            summary_result = self.summary_chain.invoke({"input_documents": all_splits})
            text_to_analyze = summary_result.get("output_text", "")
        else:
            text_to_analyze = documents[0].page_content
        
        # Run the valuation chain
        result_object = self.valuation_chain.invoke({"text": text_to_analyze})
        result = result_object.content
        
        # Ensure the result is valid JSON
        try:
            # Parse and then re-encode to ensure valid JSON
            parsed_result = json.loads(result)
            return json.dumps(parsed_result, indent=2)
        except json.JSONDecodeError:
            # If the model didn't return proper JSON, format it
            return json.dumps({
                "error": "Failed to parse valuation",
                "raw_output": result
            }, indent=2) 