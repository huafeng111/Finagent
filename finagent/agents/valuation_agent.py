#!/usr/bin/env python3
# valuation_agent.py - Agent for company stock valuation

import json
from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain.chains.summarize import load_summarize_chain

class ValuationAgent:
    def __init__(self, openai_api_key=None):
        """Initialize the valuation agent with the required tools and chains."""
        # Initialize LLM
        self.llm = ChatOpenAI(
            model_name="gpt-4", 
            temperature=0,
            openai_api_key=openai_api_key
        )
        
        # Initialize text splitter for large documents
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=4000,
            chunk_overlap=200
        )
        
        # Create the valuation prompt
        valuation_template = """
        You are a professional financial analyst specializing in company valuation.
        Analyze the following financial text and extract key information about the company's valuation.
        
        Extract the following information if available:
        1. Company name and ticker symbol
        2. Current market capitalization
        3. P/E ratio
        4. Revenue and growth rates
        5. Earnings per share (EPS)
        6. Debt-to-equity ratio
        7. Free cash flow
        8. Dividend yield (if applicable)
        9. Estimated fair value based on DCF (Discounted Cash Flow) or comparable companies
        10. Key risk factors affecting valuation
        
        Financial text:
        {text}
        
        Provide your analysis in JSON format with the following structure:
        {{
            "company_name": "Name of the company",
            "ticker": "Stock ticker",
            "market_cap": "Current market cap",
            "pe_ratio": "Current P/E ratio",
            "revenue": {{
                "current": "Current revenue",
                "growth_rate": "YoY growth rate"
            }},
            "eps": "Current EPS",
            "debt_to_equity": "Current debt-to-equity ratio",
            "free_cash_flow": "Current FCF",
            "dividend_yield": "Current dividend yield",
            "estimated_fair_value": "Your estimated fair value",
            "valuation_methodology": "Brief description of method used",
            "risk_factors": ["List of key risk factors"]
        }}
        
        If certain information is not available in the text, use "N/A" for that field.
        """
        
        self.valuation_prompt = PromptTemplate(
            input_variables=["text"],
            template=valuation_template
        )
        
        self.valuation_chain = LLMChain(
            llm=self.llm,
            prompt=self.valuation_prompt
        )
        
        # Create summarization chain for large documents
        self.summary_chain = load_summarize_chain(
            llm=self.llm,
            chain_type="map_reduce",
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
            summary = self.summary_chain.run(all_splits)
            text_to_analyze = summary
        else:
            text_to_analyze = documents[0].page_content
        
        # Run the valuation chain
        result = self.valuation_chain.run(text_to_analyze)
        
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