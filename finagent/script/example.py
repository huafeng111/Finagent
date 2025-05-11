#!/usr/bin/env python3
# example.py - Example usage of the FinAgent

import os
import json
import concurrent.futures
from dotenv import load_dotenv
from finagent.agents.valuation_agent import ValuationAgent
from finagent.utils.document_processor import load_document

# Load environment variables (for API keys)
load_dotenv()

def analyze_document(agent, documents, index):
    """Run a single analysis and return the result with its index"""
    print(f"Running analysis {index+1}...")
    result = agent.analyze(documents)
    print(f"Analysis {index+1} complete")
    return result

def main():
    # Example usage
    print("FinAgent - Financial Document Analysis Example")
    print("==============================================")
    
    # Check if API keys are set
    if not os.getenv("OPENAI_API_KEY"):
        print("Warning: OPENAI_API_KEY not found in environment variables or .env file")
    
    if not os.getenv("DEEPSEEK_API_KEY"):
        print("Warning: DEEPSEEK_API_KEY not found in environment variables or .env file")
    
    # Get input file from user
    file_path = input("Enter path to financial document (PDF or text file): ")
    
    try:
        # Load the document
        print(f"Loading document: {file_path}")
        documents = load_document(file_path)
        print("Document loaded successfully")
        
        # Ask user which model to use
        model_choice = input("Choose model (1 for OpenAI GPT-4, 2 for DeepSeek): ")
        
        if model_choice == "2":
            model_name = "deepseek-chat"  # Use the correct DeepSeek model name
            api_key = os.getenv("DEEPSEEK_API_KEY")
            # Initialize the valuation agent with DeepSeek
            valuation_agent = ValuationAgent(deepseek_api_key=api_key, model_name=model_name)
        else:
            # Default to OpenAI
            model_name = "gpt-4o-mini"
            api_key = os.getenv("OPENAI_API_KEY")
            valuation_agent = ValuationAgent(openai_api_key=api_key, model_name=model_name)
        
        print(f"Using model: {model_name}")
        
        # Ask for parallel processing count (1-5)
        parallel_count = input("Enter number of parallel analyses to run (1-5): ")
        try:
            parallel_count = int(parallel_count)
            parallel_count = min(max(1, parallel_count), 5)  # Ensure it's between 1 and 5
        except ValueError:
            print("Invalid input, defaulting to 1 analysis")
            parallel_count = 1
        
        print(f"Running {parallel_count} analyses in parallel using ThreadPoolExecutor...")
        
        # Process the documents in parallel
        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=parallel_count) as executor:
            # Submit tasks
            future_to_index = {
                executor.submit(analyze_document, valuation_agent, documents, i): i 
                for i in range(parallel_count)
            }
            
            # Collect results as they complete
            for future in concurrent.futures.as_completed(future_to_index):
                results.append(future.result())
        
        print("All analyses completed")
        
        # Save results to file
        output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "result")
        os.makedirs(output_dir, exist_ok=True) # Ensure the directory exists
        base_name = os.path.basename(file_path)
        file_name_without_ext = os.path.splitext(base_name)[0]
        output_file = os.path.join(output_dir, f"{file_name_without_ext}.md")

        with open(output_file, 'w', encoding='utf-8') as f:
            for i, result in enumerate(results):
                if i > 0:
                    f.write("\n\n##########\n\n")
                f.write(result)
        
        print(f"\nFull results saved to {output_file}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 