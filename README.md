# FinAgent - Financial Document Analysis Tool

FinAgent is a LangChain-based tool for analyzing financial documents and extracting valuable information, such as company valuations. It uses AI to process financial texts and generate structured analyses.

## Features

- Load and process financial documents (PDF, text files)
- Extract key valuation metrics from financial texts
- Generate structured JSON output with financial analysis
- Support for large documents through chunking and summarization

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/finagent.git
   cd finagent
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key:
   - Create a `.env` file in the root directory
   - Add your API key: `OPENAI_API_KEY=your_api_key_here`

## Usage

### Basic Usage

You can use the script in two ways:

1. Use the example script:
   ```
   python finagent/example.py
   ```
   Follow the prompts to input a PDF or text file for analysis.

2. Use the main script with command-line arguments:
   ```
   python finagent/main.py --input financial_document.pdf --output results.json
   ```

### Example Output

The tool outputs a JSON file containing structured financial information, including:

- Company name and ticker symbol
- Market capitalization
- P/E ratio
- Revenue and growth rates
- Earnings per share (EPS)
- Debt-to-equity ratio
- Free cash flow
- Dividend yield
- Estimated fair value
- Risk factors

## Project Structure

- `finagent/main.py`: Main entry point for the application
- `finagent/agents/`: Contains agent implementations
  - `valuation_agent.py`: Agent for company stock valuation
- `finagent/utils/`: Utility functions
  - `document_processor.py`: Tools for loading and processing documents
- `finagent/example.py`: Example script demonstrating usage

## Extending the Project

You can extend this project by:

1. Adding more specialized agents in the `agents` directory
2. Implementing additional document formats in `utils/document_processor.py`
3. Creating more complex chains in a new `chains` directory

## License

[MIT License](LICENSE)

## 自动激活 Poetry 环境

### 方法一：使用Poetry的自动激活功能

在项目目录中运行以下命令，将在`.env`文件中添加`POETRY_VIRTUALENVS_IN_PROJECT=true`设置，使得Poetry在进入项目目录时自动激活环境：

```bash
# 在当前项目中设置
poetry config virtualenvs.in-project true --local

# 全局设置（所有项目）
poetry config virtualenvs.in-project true
```

### 方法二：使用Direnv（推荐）

1. 安装 direnv:
```bash
# Mac
brew install direnv

# Linux
sudo apt install direnv
```

2. 添加到shell配置：
```bash
# 对于zsh（在~/.zshrc中添加）
eval "$(direnv hook zsh)"

# 对于bash（在~/.bashrc中添加）
eval "$(direnv hook bash)"
```

3. 在项目根目录创建`.envrc`文件：
```bash
echo 'source $(poetry env info -p)/bin/activate' > .envrc
direnv allow
```

### 方法三：使用脚本

在项目根目录有一个`activate_env.sh`脚本，可以直接运行激活环境：

```bash
./activate_env.sh
```