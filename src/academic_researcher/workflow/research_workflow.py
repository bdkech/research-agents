from typing import Any
from langgraph.graph import StateGraph, Graph

from academic_researcher.agents.prompt_processor import PromptProcessorAgent
from academic_researcher.agents.paper_retreiver import PaperRetreiverAgent
from academic_researcher.agents.summarizer import SummarizerAgent 
from academic_researcher.models.schemas import WorkflowState 


def create_research_workflow(
    host: str,
    model_name: str,
    topic: str,
    usage_limits: Any = None
) -> Graph:
    """Create a research workflow using LangGraph."""
    
    # Initialize agents
    prompt_processor = PromptProcessorAgent(
        host=host,
        model_name=model_name,
        usage_limits=usage_limits,
        topic=topic
    )
    
    paper_retriever = PaperRetreiverAgent(
        host=host,
        model_name=model_name,
        usage_limits=usage_limits
    )
    
    summarizer = SummarizerAgent(
        host=host,
        model_name=model_name,
        usage_limits=usage_limits
    )
    
    # Define node functions
    async def process_query_node(state: WorkflowState) -> WorkflowState:
        # Use the topic from state["context"]
        result = await prompt_processor.run(state["context"].query)
        # result.output.query is the refined query string
        return {**state, "query": result.output.query}

    async def fetch_papers_node(state: WorkflowState) -> WorkflowState:
        result = await paper_retriever.run(state["query"])
        # result.output.papers is the list of PaperMetadata
        return {**state, "papers": result.output.papers}

    async def summarize_node(state: WorkflowState) -> WorkflowState:
        papers = state['papers']
        if not papers:
            return {**state, "summaries": []}
        summaries = []
        for paper in papers:
            result = await summarizer.run(paper.abstract)
            if result and result.output:
                summaries.append(result.output)
        return {**state, "summaries": summaries}
    
    # Create workflow graph with proper state type
    workflow = StateGraph(WorkflowState)
    
    # Add nodes
    workflow.add_node("process_query", process_query_node)
    workflow.add_node("fetch_papers", fetch_papers_node)
    workflow.add_node("summarize", summarize_node) 
    
    # Define edges
    workflow.add_edge("process_query", "fetch_papers")
    workflow.add_edge("fetch_papers", "summarize")
    
    # Set entry point
    workflow.set_entry_point("process_query")
    
    # Compile the graph
    return workflow.compile()