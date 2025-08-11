import dataclasses
import json

import click


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """Welcome to the Prompt Safety Agent!

    This agent uses machine learning to automatically categorize LLM prompts as safe or unsafe.
    Additionally, it provides explanations and actionable recommendations.
    """
    if ctx.invoked_subcommand is None:
        click.echo("Welcome to the Prompt Safety Agent! Run with --help to learn more about available commands.")


@cli.command()
@click.argument("prompt")
def check(prompt):
    """Evaluate the safety of the given PROMPT."""
    from src.pipeline import SafetyPipeline

    pipeline = SafetyPipeline()
    report = pipeline.run(prompt)
    report_dict = dataclasses.asdict(report)
    click.echo(json.dumps(report_dict, indent=2))


if __name__ == "__main__":
    cli()
