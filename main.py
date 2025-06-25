import pandas as pd
from rich import box
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table

from agents.query_agent import IPLAgentInputSchema, IPLAgentOutputSchema, ipl_query_agent
from config import ChatConfig, get_logger
from context_provider import IPLContextProvider

logger = get_logger(__name__)
console = Console()

WELCOME_MESSAGE = (
    "Welcome to IPL Sage, The IPL Data Analysis Assistant!"
    "I'm here to help you analyze IPL cricket data effortlessly."
    "Just ask me anything related to IPL statistics,"
    " and I'll generate the necessary DuckDB queries for you!"
)
STARTER_QUESTIONS = [
    "Who has taken the most wickets in the 2025 season?",
    "Which team has the best bowling economy rate for the 2025 season",
    "Which player has the highest number of sixes in the tournament?",
]


def display_welcome():
    welcome_panel = Panel(WELCOME_MESSAGE, title="[bold cyan]IPL Sage[/bold cyan]", border_style="cyan", padding=(1, 2))
    console.print("\n")
    console.print(welcome_panel)

    # Create a table for starter questions
    table = Table(
        show_header=True,
        header_style="bold cyan",
        box=box.ROUNDED,
        title="[bold]Example Questions to Get Started[/bold]",
    )
    table.add_column("№", style="dim", width=4)
    table.add_column("Question", style="green")

    for i, question in enumerate(STARTER_QUESTIONS, 1):
        table.add_row(str(i), question)

    console.print("\n")
    console.print(table)
    console.print("\n" + "─" * 80 + "\n")


def display_duckdb_query(agent_output: IPLAgentOutputSchema) -> None:
    """Display the reasoning and answer from the QA agent."""
    # Display reasoning
    if hasattr(agent_output, "reasoning"):
        reasoning_panel = Panel(
            Markdown(agent_output.reasoning),
            title="[bold]🤔 Analysis & Reasoning[/bold]",
            border_style="green",
            padding=(1, 2),
        )
        console.print("\n")
        console.print(reasoning_panel)
    else:
        console.print("\n")
        console.print("No Reasoning Provided")

    # Display answer
    print(agent_output)
    answer_panel = Panel(
        Markdown(agent_output.duckdb_query),
        title="[bold]💡 DuckDB Query[/bold]",
        border_style="blue",
        padding=(1, 2),
    )
    console.print("\n")
    console.print(answer_panel)


def display_duckdb_query_output(
    df: pd.DataFrame, title: str = "📊 DataFrame Output", border_style: str = "magenta"
) -> None:
    """Display a pandas DataFrame in a styled panel in the console."""
    table = Table(show_header=True, header_style="bold cyan")
    for col in df.columns:
        table.add_column(str(col))
    for _, row in df.iterrows():
        table.add_row(*(str(val) for val in row))

    df_panel = Panel(
        table,
        title=f"[bold]{title}[/bold]",
        border_style=border_style,
        padding=(1, 2),
    )
    console.print("\n")
    console.print(df_panel)


def chatloop() -> None:
    """
    Initialize the IPL data processing and DuckDB connection.
    """
    console.print("\n[bold magenta]🚀 Initializing IPL Sage...[/bold magenta]")

    # Initialize and Register context providers
    console.print("[dim]Creating context providers...[/dim]")
    iplcontext = IPLContextProvider(title="CSV Schema Context")
    ipl_query_agent.register_context_provider("CSV Schema Context", iplcontext)

    # console.print("[dim]• Initializing conversation memory...[/dim]")
    # initialize_conversation()

    # Display Welcome Message
    console.print("[bold green]✨ System initialized successfully![/bold green]\n")
    display_welcome()

    # Chat Loop
    while True:
        # Capture User Question
        user_message = console.input("\n[bold green]Your question:[/bold green] ").strip()

        if user_message.lower() in ChatConfig.exit_commands:
            console.print("\n[bold]👋 Goodbye! Thanks for using IPL Sage.[/bold]")
            break

        ipl_agent_output = ipl_query_agent.run(IPLAgentInputSchema(user_query=user_message))
        display_duckdb_query(ipl_agent_output)

        query_output = iplcontext.connection.execute(ipl_agent_output.duckdb_query).fetchdf()
        display_duckdb_query_output(query_output)

        console.print("\n" + "─" * 80)


if __name__ == "__main__":
    chatloop()
