import click
from ..client.mira_client import MiraClient


@click.group()
def cli():
    pass


@cli.command()
@click.option("--config", required=True, help="Path to the YAML config file")
@click.option("--input", required=True, multiple=True, help="Input data for the flow in key=value format")
def execute(config, input):
    client = MiraClient(config)
    input_dict = dict(item.split("=") for item in input)
    result = client.execute(input_dict)
    click.echo(f"Result: {result}")


if __name__ == "__main__":
    cli()
