#!/usr/bin/env python3
# valuation_agent.py - Agent for company stock valuation

import json
from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import Document
from langchain_core.runnables import RunnableSequence
from finagent.templates.prompt import VALUATION_TEMPLATE

class ValuationAgent:
    def __init__(self, openai_api_key=None, deepseek_api_key=None, model_name="gpt-4"):
        """Initialize the valuation agent with the required tools and chains."""
        # Initialize LLM based on model provider
        if model_name.startswith("deepseek"):
            self.llm = ChatOpenAI(
                model_name=model_name,
                temperature=0,
                openai_api_key=deepseek_api_key,
                base_url="https://api.deepseek.com"
            )
        else:
            self.llm = ChatOpenAI(
                model_name=model_name, 
                temperature=0,
                openai_api_key=openai_api_key
            )
        
        # Create the valuation prompt from imported template
        self.valuation_prompt = PromptTemplate(
            input_variables=["text"],
            template=VALUATION_TEMPLATE
        )
        
        # Replace LLMChain with RunnableSequence
        self.valuation_chain = self.valuation_prompt | self.llm
    
    def analyze(self, documents):
        """Analyze the provided documents and return valuation results.
        
        Args:
            documents: A list of Document objects containing financial text
            
        Returns:
            Raw output from the LLM
        """
        # Simply use the document content directly without text splitting or summarization
        if isinstance(documents, list) and len(documents) > 0:
            text_to_analyze = documents[0].page_content
        else:
            text_to_analyze = documents
        
        # Replace run with invoke
        result = self.valuation_chain.invoke({"text": text_to_analyze})
        
        # Extract content from the message
        if hasattr(result, 'content'):
            return result.content
        return str(result) 