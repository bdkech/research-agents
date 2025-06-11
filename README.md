# Academic Research Agent

A Python package for automated academic research and paper analysis. This agent helps researchers by:

- Refining research queries for better search results
- Retrieving relevant academic papers from arXiv
- Generating concise summaries and identifying key findings
- Creating well-formatted PDF reports

## Features

- **Query Refinement**: Enhances research queries for better search results
- **Paper Retrieval**: Fetches relevant papers from arXiv
- **Keyword Extraction**: Identifies important terms and concepts
- **Summarization**: Generates concise summaries and extracts key findings
- **CLI Interface**: Easy-to-use command-line interface
- **Asynchronous Processing**: Efficient handling of multiple papers
- **Customizable**: Configurable model selection and styling options

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/academic-researcher.git
cd academic-researcher

# Install the package
pip install -e .
```

## Usage

### Command Line Interface

The simplest way to use the research agent is through the CLI:

```bash
# Basic usage
academic-research "machine learning applications in healthcare"

# Advanced usage with options
academic-research "quantum computing algorithms" \
    --model "openai:gpt-4" \
    --max-papers 10 \
    --user-id 123 \
```

### Python API

You can also use the package programmatically:

```python
import asyncio
from academic_researcher.core.orchestrator import ResearchOrchestrator

async def main():
    # Create orchestrator
    orchestrator = ResearchOrchestrator(
        model_name="openai:gpt-4",
        max_results=5,
    )
    
    # Run research
    report = await orchestrator.research(
        topic="machine learning applications in healthcare",
        user_id=1,
        generate_pdf=True,
        output_filename="research_report.pdf",
    )
    
    # Access report data
    print(f"Analyzed {report.total_papers} papers")
    for paper, summary in zip(report.papers, report.summaries):
        print(f"\nTitle: {paper.title}")
        print(f"Summary: {summary.summary}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Configuration

The package can be configured through various options:

- **Model Selection**: Choose different models for processing
- **Paper Limit**: Set maximum number of papers to analyze
- **Usage Limits**: Configure API usage limits

## Project Structure

```
academic-researcher/
├── src/
│   └── academic_researcher/
│       ├── agents/
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── paper_retrieval.py
│       │   ├── prompt_processor.py
│       │   └── summarization.py
│       ├── core/
│       │   ├── __init__.py
│       │   └── orchestrator.py
│       ├── models/
│       │   ├── __init__.py
│       │   └── schemas.py
│       ├── utils/
│       │   ├── __init__.py
│       │   └── pdf_generator.py
│       ├── __init__.py
│       └── cli.py
├── pyproject.toml
└── README.md
```

## Dependencies

- Python 3.8+
- pydantic
- loguru
- click
- weasyprint
- markdown2pdf
- arxiv
- pydantic-ai

## Aknowledgements

Thanks to the Analytics Vidhya [blogpost on a research assistant agent](https://www.analyticsvidhya.com/blog/2025/03/multi-agent-research-assistant-system-using-pydantic/) to provide the initial inspiration and structure for this project.
