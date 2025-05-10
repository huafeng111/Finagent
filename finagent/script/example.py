#!/usr/bin/env python3
# example.py - Example usage of the FinAgent

import os
import json
from dotenv import load_dotenv
from finagent.agents.valuation_agent import ValuationAgent
from finagent.utils.document_processor import load_document

# Load environment variables (for API keys)
load_dotenv()

def main():
    # Example usage
    print("FinAgent - Financial Document Analysis Example")
    print("==============================================")
    
    # Check if OPENAI_API_KEY is set
    if not os.getenv("OPENAI_API_KEY"):
        print("Warning: OPENAI_API_KEY not found in environment variables or .env file")
        print("You will need to provide it when initializing the ValuationAgent")
    
    # Get input file from user
    file_path = input("Enter path to financial document (PDF or text file): ")
    
    try:
        # Load the document
        print(f"Loading document: {file_path}")
        documents = load_document(file_path)
        print("Document loaded successfully")
        # Initialize the valuation agent
        valuation_agent = ValuationAgent(model_name="deepseek-reasoner")
        
        # Process the documents
        print("Analyzing financial document...")
        results = valuation_agent.analyze(documents)
        
        
        # Save results to file
        output_dir = "../../data/result"
        os.makedirs(output_dir, exist_ok=True) # Ensure the directory exists
        base_name = os.path.basename(file_path)
        file_name_without_ext = os.path.splitext(base_name)[0]
        output_file = os.path.join(output_dir, f"{file_name_without_ext}.md")

        with open(output_file, 'w', encoding='utf-8') as f: # Added encoding='utf-8' for safety
            f.write(results)
        
        print(f"\nFull results saved to {output_file}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 