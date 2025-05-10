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
    def __init__(self, model_name="gpt-4o"):
        """Initialize the valuation agent with the required tools and chains.

        Args:
            model_name (str): The name of the LLM model to use (e.g., "gpt-4o", "deepseek-coder").
        """
        api_key = None
        base_url = None
        api_key_env_var = None

        if model_name.startswith("gpt"):
            api_key_env_var = "OPENAI_API_KEY"
            api_key = os.getenv(api_key_env_var)
            # base_url can remain None for default OpenAI endpoint
        elif model_name.startswith("deepseek"):
            api_key_env_var = "DEEPSEEK_API_KEY"
            api_key = os.getenv(api_key_env_var)
            base_url = "https://api.deepseek.com/v1" # DeepSeek's OpenAI-compatible endpoint
        else:
            # Try OPENAI_API_KEY by default for unknown models
            api_key_env_var = "OPENAI_API_KEY"
            api_key = os.getenv(api_key_env_var)
            print(f"Warning: Unknown model prefix for '{model_name}'. Attempting to use OPENAI_API_KEY and default endpoint.")

        if not api_key:
            raise ValueError(f"Error: API key environment variable '{api_key_env_var}' not found for model '{model_name}'.")

        # Initialize LLM
        print("Initializing LLM...")
        print("model name", model_name)
        self.llm = ChatOpenAI(
            model_name=model_name,
            temperature=0,
            openai_api_key=api_key,
            openai_api_base=base_url # Pass base_url if it's set (for DeepSeek)
        )
        
        
        # --- Load the valuation prompt from file ---
        # Construct the path to the prompt file relative to this script's location
        current_dir = os.path.dirname(os.path.abspath(__file__))
        prompt_path = os.path.join(current_dir, '..', 'prompts', 'price_eval')

        try:
            with open(prompt_path, 'r', encoding='utf-8') as f:
                valuation_template = f.read()
                
            # 修改模板，添加{text}占位符
            # 在原始模板后附加要分析的文本
            valuation_template = valuation_template + "\n\n<document_to_analyze>\n{text}\n</document_to_analyze>"
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
        """Analyze the provided documents and return valuation results as a raw string.
        
        Args:
            documents: A list of Document objects containing financial text
            
        Returns:
            A raw string containing the valuation analysis from the LLM.
        """
        # Combine the content of all documents
        full_text = "\n".join([doc.page_content for doc in documents])
        
        # 调试: 打印模板中的占位符
        print("Template has {text} placeholder:", "{text}" in self.valuation_prompt.template)
        
        # 调试: 生成最终提示，查看文本是否被注入
        formatted_prompt = self.valuation_prompt.format(text=full_text)
        print("\n--- 前50个字符的提示 ---")
        print(formatted_prompt[:50])
        print("--- 提示字符总长度 ---")
        print(len(formatted_prompt))
        
        # Run the valuation chain directly on the full text
        result_object = self.valuation_chain.invoke({"text": full_text})
        result = result_object.content
        print("Result:")
        print(result)
        return result # Return the raw string output 