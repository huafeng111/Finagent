#!/usr/bin/env python3
# example.py - Example usage of the FinAgent

import os
import json
from dotenv import load_dotenv
from agents.valuation_agent import ValuationAgent
from utils.document_processor import load_document

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
        
        # Initialize the valuation agent
        valuation_agent = ValuationAgent(openai_api_key=os.getenv("OPENAI_API_KEY"))
        
        # Process the documents
        print("Analyzing financial document...")
        results = valuation_agent.analyze(documents)
        
        # Parse and display results
        parsed_results = json.loads(results)
        
        print("\nAnalysis Results:")
        print("=================")
        print(f"Company: {parsed_results.get('company_name', 'N/A')}")
        print(f"Ticker: {parsed_results.get('ticker', 'N/A')}")
        print(f"Market Cap: {parsed_results.get('market_cap', 'N/A')}")
        print(f"P/E Ratio: {parsed_results.get('pe_ratio', 'N/A')}")
        
        # Revenue details
        revenue = parsed_results.get('revenue', {})
        print(f"Revenue: {revenue.get('current', 'N/A')}")
        print(f"Growth Rate: {revenue.get('growth_rate', 'N/A')}")
        
        print(f"EPS: {parsed_results.get('eps', 'N/A')}")
        print(f"Debt-to-Equity: {parsed_results.get('debt_to_equity', 'N/A')}")
        print(f"Free Cash Flow: {parsed_results.get('free_cash_flow', 'N/A')}")
        print(f"Dividend Yield: {parsed_results.get('dividend_yield', 'N/A')}")
        print(f"Estimated Fair Value: {parsed_results.get('estimated_fair_value', 'N/A')}")
        print(f"Valuation Method: {parsed_results.get('valuation_methodology', 'N/A')}")
        
        # Risk factors
        print("\nRisk Factors:")
        for risk in parsed_results.get('risk_factors', ['N/A']):
            print(f"- {risk}")
        
        # Save results to file
        output_file = "valuation_results.json"
        with open(output_file, 'w') as f:
            f.write(results)
        
        print(f"\nFull results saved to {output_file}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 