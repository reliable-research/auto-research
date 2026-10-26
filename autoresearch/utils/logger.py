"""Console output and formatting utilities."""

import sys
from typing import Optional

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.markdown import Markdown
    RICH_AVAILABLE = True
    console = Console()
except ImportError:
    RICH_AVAILABLE = False
    console = None


def print_banner(text: str, subtitle: Optional[str] = None):
    """Print an attractive section banner."""
    if RICH_AVAILABLE and console:
        title_text = f"[bold cyan]{text}[/bold cyan]"
        if subtitle:
            title_text += f"\n[dim]{subtitle}[/dim]"
        console.print(Panel(title_text, expand=False, border_style="cyan"))
    else:
        print("\n" + "=" * 60)
        print(f"  {text}")
        if subtitle:
            print(f"  ({subtitle})")
        print("=" * 60 + "\n")


def print_info(message: str):
    if RICH_AVAILABLE and console:
        console.print(f"[blue]ℹ[/blue] {message}")
    else:
        print(f"[INFO] {message}")


def print_success(message: str):
    if RICH_AVAILABLE and console:
        console.print(f"[green]✔[/green] {message}")
    else:
        print(f"[SUCCESS] {message}")


def print_warning(message: str):
    if RICH_AVAILABLE and console:
        console.print(f"[yellow]⚠[/yellow] {message}")
    else:
        print(f"[WARNING] {message}")


def print_error(message: str):
    if RICH_AVAILABLE and console:
        console.print(f"[red]✖[/red] {message}")
    else:
        print(f"[ERROR] {message}")


def print_table(headers: list, rows: list, title: Optional[str] = None):
    """Print a tabular summary."""
    if RICH_AVAILABLE and console:
        table = Table(title=title, show_header=True, header_style="bold magenta")
        for header in headers:
            table.add_column(header)
        for row in rows:
            table.add_row(*[str(c) for c in row])
        console.print(table)
    else:
        if title:
            print(f"\n--- {title} ---")
        header_line = " | ".join(headers)
        print(header_line)
        print("-" * len(header_line))
        for row in rows:
            print(" | ".join(str(c) for c in row))
        print()
