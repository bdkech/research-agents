"""Data models for the academic researcher package."""
from dataclasses import dataclass
from typing import List, Optional, TypedDict

from pydantic import BaseModel, Field


@dataclass
class ResearchContext():
    """Context for research operations."""
    user_id: Optional[str]
    query: str
    max_result_retries: int = 5

class RefinedQueryResult(BaseModel):
    """Refined query result."""
    query: str = Field(..., description="Refined arXiv search query")

class PaperMetadata(BaseModel):
    """Metadata for a research paper."""
    title: str = Field(..., description="Title of the paper")
    abstract: str = Field(..., description="Abstract of the paper")
    authors: List[str] = Field(..., description="List of authors")
    publication_date: str = Field(..., description="Publication date")

class GatherPapers(BaseModel):
    papers: list[PaperMetadata] = Field(..., description="Discovered papers")

class PaperSummary(BaseModel):
    """Summary of a research paper."""
    summary: str = Field(..., description="Concise summary of the paper")

class GatherSummaries(BaseModel):
    """Summary of a research paper."""
    summaries: list[PaperSummary] = Field(..., description="List of paper summaries")

class KeywordResult(BaseModel):
    """Extracted keywords from a paper."""
    keywords: List[str] = Field(..., description="List of extracted keywords")

class WorkflowState(TypedDict):
    """State type for the research workflow."""
    context: ResearchContext
    query: Optional[str]
    papers: Optional[List[PaperMetadata]]
    summaries: Optional[List[PaperSummary]]
    error: Optional[str]