"""Main CLI interface for the Python Agent System

This module provides the command-line interface for interacting with AI agents,
running data pipelines, and managing the system.
"""

from pathlib import Path
from typing import Optional, List

import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.syntax import Syntax
import pandas as pd

from src.agents.base import AgentRole
from src.agents.data_analyst import DataAnalystAgent, DataAnalysisRequest
from src.orchestration import Orchestrator, TaskAnalyzer, OrchestrationStrategy

# Initialize Typer app and Rich console
app = typer.Typer(
    help="AI Agent CLI - Interact with Pydantic-based AI agents",
    add_completion=True,
    rich_markup_mode="rich"
)
console = Console()

# Sub-command groups
agent_app = typer.Typer(help="Agent management commands")
data_app = typer.Typer(help="Data analysis commands")
pipeline_app = typer.Typer(help="Pipeline management commands")
orchestration_app = typer.Typer(help="Multi-agent orchestration commands")

app.add_typer(agent_app, name="agent")
app.add_typer(data_app, name="data")
app.add_typer(pipeline_app, name="pipeline")
app.add_typer(orchestration_app, name="orchestrate")


@app.command()
def version():
    """Show version information"""
    console.print(Panel.fit(
        "[bold blue]Python Agent System[/bold blue]\n"
        "Version: 0.1.0\n"
        "Built with: Pydantic, FastAPI, Typer",
        title="About"
    ))


@orchestration_app.command("analyze")
def analyze_orchestration(
    task_file: Path = typer.Argument(
        ...,
        help="Path to markdown file containing tasks"
    ),
    strategy: Optional[str] = typer.Option(
        None,
        "--strategy", "-s",
        help="Orchestration strategy (auto-detect if not provided)"
    )
):
    """Analyze tasks and create orchestration plan"""
    if not task_file.exists():
        console.print(f"[red]Task file not found: {task_file}[/red]")
        raise typer.Exit(1)
    
    # Read task file
    content = task_file.read_text()
    
    # Extract feature name
    feature_name = task_file.stem.replace('-tasks', '')
    
    # Analyze tasks
    with console.status("[bold green]Analyzing tasks...[/bold green]"):
        analyzer = TaskAnalyzer()
        tasks = analyzer.extract_tasks_from_markdown(content)
        
        if not tasks:
            console.print("[red]No tasks found in file[/red]")
            raise typer.Exit(1)
        
        # Create orchestration plan
        orchestrator = Orchestrator()
        
        # Parse strategy if provided
        orch_strategy = None
        if strategy:
            try:
                orch_strategy = OrchestrationStrategy(strategy)
            except ValueError:
                console.print(f"[red]Invalid strategy: {strategy}[/red]")
                console.print(f"Valid options: {', '.join([s.value for s in OrchestrationStrategy])}")
                raise typer.Exit(1)
        
        plan = orchestrator.create_orchestration_plan(
            feature_name,
            tasks,
            orch_strategy
        )
    
    # Display orchestration plan
    console.print(Panel.fit(
        f"[bold]Orchestration Plan for: {feature_name}[/bold]\n"
        f"Strategy: {plan.strategy.value}\n"
        f"Total Tasks: {plan.total_tasks}\n"
        f"Agents Required: {len(plan.agent_assignments)}",
        title="🤖 Orchestration Analysis"
    ))
    
    # Show time savings
    console.print("\n[bold]Time Analysis:[/bold]")
    console.print(f"Sequential Execution: {plan.estimated_sequential_time} minutes")
    console.print(f"Parallel Execution: {plan.estimated_parallel_time} minutes")
    console.print(f"[bold green]Time Savings: {plan.time_savings_percent}%[/bold green]\n")
    
    # Show agent assignments
    table = Table(title="Agent Assignments")
    table.add_column("Agent", style="cyan")
    table.add_column("Role", style="magenta")
    table.add_column("Tasks", style="green")
    table.add_column("Focus", style="yellow")
    
    for agent_id, assignment in plan.agent_assignments.items():
        table.add_row(
            agent_id,
            assignment.agent_role.value,
            f"{len(assignment.tasks)} tasks",
            assignment.focus
        )
    
    console.print(table)
    
    # Show execution phases
    console.print("\n[bold]Execution Phases:[/bold]")
    for i, phase in enumerate(plan.phases, 1):
        console.print(f"\nPhase {i}:")
        for agent_id, task_ids in phase.items():
            console.print(f"  • {agent_id}: {', '.join(task_ids)}")
    
    # Show critical path
    console.print(f"\n[bold]Critical Path:[/bold] {' → '.join(plan.critical_path)}")
    
    # Suggest command
    console.print(Panel(
        f"[bold green]Recommended Command:[/bold green]\n\n"
        f"agent orchestrate start {feature_name} --strategy={plan.strategy.value}\n\n"
        f"This will spawn {len(plan.agent_assignments)} specialized agents "
        f"to work in parallel, saving approximately {plan.time_savings_percent}% of time.",
        title="💡 Next Step"
    ))


@orchestration_app.command("start")
def start_orchestration(
    feature_name: str = typer.Argument(..., help="Feature name to orchestrate"),
    strategy: str = typer.Option(
        "auto",
        "--strategy", "-s",
        help="Orchestration strategy"
    ),
    agents: Optional[int] = typer.Option(
        None,
        "--agents", "-a",
        help="Number of agents (auto-detect if not specified)"
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Show plan without executing"
    )
):
    """Start multi-agent orchestration for a feature"""
    console.print(Panel.fit(
        f"[bold blue]Multi-Agent Orchestration[/bold blue]\n"
        f"Feature: {feature_name}\n"
        f"Strategy: {strategy}",
        title="🚀 Starting Orchestration"
    ))
    
    if dry_run:
        console.print("[yellow]Dry run mode - no agents will be spawned[/yellow]")
    
    # This would integrate with the actual agent spawning system
    console.print("\n[yellow]Orchestration execution coming soon![/yellow]")
    console.print("This will:")
    console.print("• Spawn multiple specialized agents")
    console.print("• Distribute tasks based on expertise")
    console.print("• Coordinate parallel execution")
    console.print("• Handle inter-agent communication")
    console.print("• Merge results when complete")


@orchestration_app.command("status")
def orchestration_status(
    feature_name: Optional[str] = typer.Argument(
        None,
        help="Feature name to check (show all if not specified)"
    )
):
    """Check status of orchestrated work"""
    if feature_name:
        console.print(f"[bold]Orchestration Status: {feature_name}[/bold]")
    else:
        console.print("[bold]All Active Orchestrations[/bold]")
    
    # Mock status display
    console.print("""
╔══════════════════════════════════════════════════════════╗
║ ORCHESTRATION STATUS: user-authentication               ║
╠══════════════════════════════════════════════════════════╣
║ Strategy: feature_development | Agents: 4 | Progress: 45% ║
╠══════════════════════════════════════════════════════════╣
║ BACKEND_AGENT     [████████░░] 80%  Current: Task 2.3   ║
║ DATA_AGENT        [██████░░░░] 60%  Current: Task 1.3   ║
║ FRONTEND_AGENT    [████░░░░░░] 40%  Current: Task 3.1   ║
║ QA_AGENT          [██░░░░░░░░] 20%  Status: Waiting     ║
╚══════════════════════════════════════════════════════════╝
    """)


# Keep existing commands below...
@agent_app.command("list")
def list_agents():
    """List all available agents"""
    table = Table(title="Available AI Agents")
    table.add_column("Role", style="cyan", no_wrap=True)
    table.add_column("Name", style="magenta")
    table.add_column("Description", style="green")
    
    for role in AgentRole:
        # This would be replaced with actual agent registry
        table.add_row(
            role.value,
            role.value.replace("_", " ").title(),
            f"Specialized in {role.value.replace('_', ' ')}"
        )
    
    console.print(table)


@agent_app.command("chat")
def agent_chat(
    agent_role: AgentRole = typer.Option(
        AgentRole.DATA_ANALYST,
        "--role", "-r",
        help="Agent role to chat with"
    ),
    session_name: Optional[str] = typer.Option(
        None,
        "--session", "-s",
        help="Session name for memory persistence"
    )
):
    """Start an interactive chat with an agent"""
    console.print(f"[bold green]Starting chat with {agent_role.value}...[/bold green]")
    
    # Initialize agent based on role
    if agent_role == AgentRole.DATA_ANALYST:
        agent = DataAnalystAgent()
    else:
        console.print(f"[red]Agent role {agent_role} not yet implemented[/red]")
        return
    
    # Load session if specified
    if session_name:
        memory_path = f".claude/sessions/{session_name}.json"
        if Path(memory_path).exists():
            agent.load_memory(memory_path)
            console.print(f"[green]Loaded session: {session_name}[/green]")
    
    console.print(
        Panel(
            f"Chat with [bold]{agent.name}[/bold]\n"
            f"{agent.description}\n\n"
            "Commands:\n"
            "  /help - Show help\n"
            "  /clear - Clear chat history\n"
            "  /save - Save session\n"
            "  /exit - Exit chat",
            title="Agent Chat"
        )
    )
    
    while True:
        try:
            # Get user input
            user_input = console.input("\n[bold blue]You:[/bold blue] ")
            
            # Handle commands
            if user_input.lower() == "/exit":
                break
            elif user_input.lower() == "/clear":
                agent.reset_memory()
                console.print("[yellow]Memory cleared[/yellow]")
                continue
            elif user_input.lower() == "/save" and session_name:
                Path(".claude/sessions").mkdir(parents=True, exist_ok=True)
                agent.save_memory(f".claude/sessions/{session_name}.json")
                console.print(f"[green]Session saved: {session_name}[/green]")
                continue
            elif user_input.lower() == "/help":
                console.print(agent_chat.__doc__)
                continue
            
            # Process with agent
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
                transient=True
            ) as progress:
                progress.add_task("Thinking...", total=None)
                
                from src.agents.base import AgentResponse
                response = agent.think(
                    prompt=user_input,
                    response_model=AgentResponse
                )
            
            # Display response
            console.print(f"\n[bold green]{agent.name}:[/bold green]")
            console.print(response.content)
            
            if response.next_steps:
                console.print("\n[bold yellow]Suggested next steps:[/bold yellow]")
                for step in response.next_steps:
                    console.print(f"  • {step}")
            
            if response.confidence < 0.7:
                console.print(
                    f"\n[dim]Confidence: {response.confidence:.0%}[/dim]"
                )
        
        except KeyboardInterrupt:
            console.print("\n[yellow]Chat interrupted[/yellow]")
            break
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
    
    # Save session on exit if specified
    if session_name:
        Path(".claude/sessions").mkdir(parents=True, exist_ok=True)
        agent.save_memory(f".claude/sessions/{session_name}.json")
        console.print(f"[green]Session saved: {session_name}[/green]")
    
    console.print("[bold]Chat ended[/bold]")


@data_app.command("analyze")
def analyze_data(
    file_path: Path = typer.Argument(
        ...,
        help="Path to data file (CSV, Excel, JSON)"
    ),
    question: str = typer.Option(
        ...,
        "--question", "-q",
        help="Question to answer about the data"
    ),
    output: Optional[Path] = typer.Option(
        None,
        "--output", "-o",
        help="Output file for results"
    ),
    sql: Optional[str] = typer.Option(
        None,
        "--sql",
        help="SQL query to run on the data"
    ),
    profile: bool = typer.Option(
        False,
        "--profile", "-p",
        help="Generate data quality profile"
    )
):
    """Analyze data using AI agents"""
    # Validate file exists
    if not file_path.exists():
        console.print(f"[red]File not found: {file_path}[/red]")
        raise typer.Exit(1)
    
    # Load data
    with console.status("[bold green]Loading data...[/bold green]"):
        try:
            if file_path.suffix.lower() == ".csv":
                df = pd.read_csv(file_path)
            elif file_path.suffix.lower() in [".xlsx", ".xls"]:
                df = pd.read_excel(file_path)
            elif file_path.suffix.lower() == ".json":
                df = pd.read_json(file_path)
            else:
                console.print(f"[red]Unsupported file type: {file_path.suffix}[/red]")
                raise typer.Exit(1)
        except Exception as e:
            console.print(f"[red]Error loading file: {e}[/red]")
            raise typer.Exit(1)
    
    console.print(f"[green]Loaded data:[/green] {df.shape[0]:,} rows × {df.shape[1]} columns")
    
    # Initialize agent
    agent = DataAnalystAgent()
    
    # Profile data if requested
    if profile:
        with console.status("[bold green]Profiling data...[/bold green]"):
            quality_report = agent.profile_data(df)
        
        # Display quality report
        console.print("\n[bold]Data Quality Report[/bold]")
        console.print(f"Total rows: {quality_report.total_rows:,}")
        console.print(f"Total columns: {quality_report.total_columns}")
        console.print(f"Quality score: {quality_report.quality_score:.1%}")
        
        if quality_report.issues:
            console.print("\n[yellow]Issues found:[/yellow]")
            for issue in quality_report.issues:
                console.print(f"  • {issue}")
        
        if quality_report.recommendations:
            console.print("\n[green]Recommendations:[/green]")
            for rec in quality_report.recommendations:
                console.print(f"  • {rec}")
    
    # Analyze data
    with console.status("[bold green]Analyzing data...[/bold green]"):
        request = DataAnalysisRequest(
            question=question,
            sql_query=sql
        )
        response = agent.analyze_dataframe(df, request)
    
    # Display results
    console.print(f"\n[bold]Analysis Results[/bold]")
    console.print(Panel(response.summary, title="Summary"))
    
    if response.insights:
        console.print("\n[bold]Key Insights:[/bold]")
        for insight in response.insights:
            importance_color = "green" if insight.importance > 0.7 else "yellow"
            console.print(
                f"  [{importance_color}]•[/{importance_color}] "
                f"{insight.insight} (importance: {insight.importance:.0%})"
            )
            console.print(f"    Evidence: [dim]{insight.evidence}[/dim]")
    
    if response.recommendations:
        console.print("\n[bold]Recommendations:[/bold]")
        for rec in response.recommendations:
            console.print(f"  • {rec}")
    
    if response.sql_used:
        console.print("\n[bold]SQL Query Used:[/bold]")
        console.print(Syntax(response.sql_used, "sql"))
    
    # Save output if requested
    if output:
        output_data = {
            "summary": response.summary,
            "insights": [i.model_dump() for i in response.insights],
            "statistics": response.statistics,
            "recommendations": response.recommendations,
            "confidence": response.confidence
        }
        
        if output.suffix.lower() == ".json":
            import json
            with open(output, "w") as f:
                json.dump(output_data, f, indent=2)
        else:
            # Default to markdown
            with open(output, "w") as f:
                f.write(f"# Data Analysis Results\n\n")
                f.write(f"## Summary\n{response.summary}\n\n")
                f.write(f"## Insights\n")
                for insight in response.insights:
                    f.write(f"- {insight.insight} (importance: {insight.importance:.0%})\n")
                f.write(f"\n## Recommendations\n")
                for rec in response.recommendations:
                    f.write(f"- {rec}\n")
        
        console.print(f"\n[green]Results saved to: {output}[/green]")


@data_app.command("suggest")
def suggest_analysis(
    file_path: Path = typer.Argument(
        ...,
        help="Path to data file"
    )
):
    """Get AI suggestions for interesting analyses"""
    # Load data
    if not file_path.exists():
        console.print(f"[red]File not found: {file_path}[/red]")
        raise typer.Exit(1)
    
    with console.status("[bold green]Loading data...[/bold green]"):
        if file_path.suffix.lower() == ".csv":
            df = pd.read_csv(file_path)
        else:
            console.print(f"[red]Currently only CSV files are supported[/red]")
            raise typer.Exit(1)
    
    # Get suggestions
    agent = DataAnalystAgent()
    with console.status("[bold green]Generating analysis suggestions...[/bold green]"):
        suggestions = agent.suggest_analysis(df)
    
    # Display suggestions
    console.print(Panel.fit(
        "[bold]Suggested Analyses[/bold]\n"
        "Based on your data, here are some interesting questions to explore:",
        title="Analysis Ideas"
    ))
    
    for i, suggestion in enumerate(suggestions, 1):
        console.print(f"\n[bold cyan]{i}.[/bold cyan] {suggestion}")
    
    console.print("\n[dim]Use: agent data analyze <file> --question \"<your question>\"[/dim]")


@pipeline_app.command("list")
def list_pipelines():
    """List available data pipelines"""
    console.print("[yellow]Pipeline management coming soon![/yellow]")


@pipeline_app.command("run")
def run_pipeline(
    config: Path = typer.Argument(
        ...,
        help="Pipeline configuration file"
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Show what would be run without executing"
    )
):
    """Run a data pipeline"""
    console.print("[yellow]Pipeline execution coming soon![/yellow]")


if __name__ == "__main__":
    app()