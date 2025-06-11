"""Academic research assistant CLI."""
import asyncio
from typing import Optional

import click
from loguru import logger
from rich.console import Console
from academic_researcher.models.schemas import ResearchContext
from academic_researcher.workflow.research_workflow import create_research_workflow

console = Console()


@click.group()
@click.option(
    "--log-level",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
    default="INFO",
    help="Set the logging level",
)
@click.option(
    "--log-file",
    type=str,
    default=None,
    help="Path to log file (optional)",
)
def cli(log_level: str, log_file: Optional[str]) -> None:
    """Academic research assistant CLI."""
    logger.info(f"Starting academic researcher CLI with log level: {log_level}")


@cli.command()
@click.argument("topic", type=str)
@click.option("--model", default="qwen:14b", help="Model name to use")
@click.option("--host", default="http://localhost:11434/v1", help="Ollama host URL")
def research(topic: str, model: str, host: str):
    """Run research workflow on a given topic."""
    asyncio.run(_run_research(topic, model, host))


async def _run_research(topic: str, model: str, host: str):
    """Async implementation of research workflow."""
    try:
        logger.info(f"Starting research on topic: {topic}")
        
        # Create research context
        context = ResearchContext(user_id="1", query=topic)
        
        # Create and run workflow
        workflow = create_research_workflow(
            host=host,
            model_name=model,
            topic=topic
        )
        
        # Run the workflow
        results = await workflow.ainvoke(
            {"context": context}
        )
        print(results.keys())
        # Display results
        if results and results["papers"]:
            papers = results["papers"]
            console.print("\n[bold blue]Retrieved Papers:[/bold blue]")
            for idx, paper in enumerate(papers):
                console.print(f"\n[bold]{paper.title}[/bold]")
                console.print(f"Authors: {', '.join(paper.authors)}")
                console.print(f"Published: {paper.publication_date}")
                console.print(f"Summary: {results['summaries'][idx].summary}")
                console.print(f"Abstract: {paper.abstract[:200]}...")
        else:
            console.print("[yellow]No papers found[/yellow]")
            
    except Exception as e:
        logger.exception("Research workflow failed")
        console.print(f"[red]Error: {str(e)}[/red]")
        raise click.Abort()


if __name__ == "__main__":
    cli()