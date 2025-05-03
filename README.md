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