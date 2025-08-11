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
    """
    Evaluate the safety of the given PROMPT.

    PROMPT: The text prompt to evaluate for safety.
    """
    import dataclasses
    import json

    from src.pipeline import SafetyPipeline

    pipeline = SafetyPipeline()
    report = pipeline.run(prompt)
    report_dict = dataclasses.asdict(report)
    click.echo(json.dumps(report_dict, indent=2))


@cli.command()
@click.option("--host", default="0.0.0.0", show_default=True, help="Hostname to bind the docs server to.", type=str)
@click.option("--port", default=8000, show_default=True, help="Port to serve the docs on.", type=int)
def docs(host, port):
    """
    Launch the documentation web server.
    """
    import subprocess

    cmd = ["gunicorn", "src.utils.docs_server:app", "--bind", f"{host}:{port}"]
    click.echo(f"Starting Gunicorn with command: {' '.join(cmd)}")
    subprocess.run(cmd)


if __name__ == "__main__":
    cli()
