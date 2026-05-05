from rich.console import Console
from rich.table import Table
from rich.progress import Progress

console = Console()

class Dashboard:

    def banner(self, text):
        console.rule(f"[bold cyan]{text}")

    def log(self, text, color="green"):
        console.print(f"[{color}]✔ {text}[/]")

    def error(self, text):
        console.print(f"[red]✖ {text}[/]")

    def progress(self, total):
        return Progress()

    def summary(self, results):
        table = Table(title="Test Summary")

        table.add_column("Collection")
        table.add_column("Test")
        table.add_column("Status")
        table.add_column("Details")

        for r in results:
            color = "green" if "PASS" in r["status"] else "red"
            table.add_row(
                r["collection"],
                r["test"],
                f"[{color}]{r['status']}[/]",
                str(r.get("details", "-"))
            )

        console.print(table)