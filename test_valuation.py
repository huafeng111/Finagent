#!/usr/bin/env python3
# test_valuation.py - 测试ValuationAgent功能

import os
from dotenv import load_dotenv
from finagent.agents.valuation_agent import ValuationAgent
from finagent.utils.document_processor import load_document

# 加载环境变量（用于API密钥）
load_dotenv()

def main():
    # 测试用例
    print("测试FinAgent估值功能")
    print("=================")
    
    # 检查OpenAI API密钥是否设置
    if not os.getenv("OPENAI_API_KEY"):
        print("警告: 环境变量中未找到OPENAI_API_KEY")
        print("请设置API密钥后重试")
        return
    
    # 使用测试文档
    file_path = "test_document.txt"
    
    try:
        # 加载文档
        print(f"加载文档: {file_path}")
        documents = load_document(file_path)
        print("文档加载成功")
        
        # 初始化估值agent
        print("初始化估值agent...")
        valuation_agent = ValuationAgent(model_name="gpt-4o")
        
        # 处理文档
        print("分析文档内容...")
        results = valuation_agent.analyze(documents)
        
        # 保存结果到文件
        output_file = "test_result.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(results)
        
        print(f"分析结果已保存到 {output_file}")
        
    except Exception as e:
        print(f"错误: {str(e)}")

if __name__ == "__main__":
    main() 