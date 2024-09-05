import os
import click
from ..client.mira_client import MiraClient
import yaml
import requests



TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "..", "templates")

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


@cli.command()
@click.option("--list", is_flag=True, help="List all templates")
@click.option("--flow", required=False, help="Name of the flow to initialize")
@click.option("--template", required=False, help="Template to use for the flow")
def init(list, flow, template):
    if list:
        templates = [f for f in os.listdir(TEMPLATE_DIR) if f.endswith('.yaml')]
        click.echo("Available templates:")
        for template in templates:
            template_name = template[:-5]  # Remove '.yaml' extension
            template_path = os.path.join(TEMPLATE_DIR, template)
            with open(template_path, "r") as file:
                template_data = yaml.safe_load(file)
            
            click.echo(f"\n  - {template_name}")
            click.echo(f"    Name: {template_data.get('name', 'N/A')}")
            click.echo(f"    Description: {template_data.get('description', 'N/A')}")
        
        if not templates:
            click.echo("No templates found.")
        return

    if not flow or not template:
        click.echo("Both --flow and --template options are required when not using --list.")
        return

    template_path = os.path.join(TEMPLATE_DIR, f"{template}.yaml")

    if not os.path.exists(template_path):
        click.echo(f"Template '{template}' not found.")
        return

    client = MiraClient(config_path=template_path)
    client.init_flow(flow, template_path)
    click.echo(f"Initialized flow '{flow}' with template '{template}'")


@cli.command()
@click.option("--lists", is_flag=True, help="List all prompts")
@click.option("--skip", default=0, help="Number of items to skip")
@click.option("--limit", default=100, help="Maximum number of items to return")
@click.option("--show", is_flag=True, help="Show prompt details")
@click.option("--prompt-name", required=False, help="Give in the format author/prompt_name")
def prompts(skip, limit, show, lists, prompt_name):

    if not show and not lists:
        click.echo("Either --show or --lists option must be provided.")
        return

    if show:      
        url = f"https://prompt-mgmt-api.stg.arohalabs.dev/prompts/{prompt_name}"
        headers = {'accept': 'application/json'}
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            prompt_details = response.json()
            
            click.echo("\nPrompt details:")
            click.echo(f"  ID: {prompt_details.get('id', 'N/A')}")
            click.echo(f"  Content: {prompt_details.get('content', 'N/A')}")
            click.echo(f"  Version: {prompt_details.get('version', 'N/A')}")
            click.echo(f"  Created At: {prompt_details.get('created_at', 'N/A')}")
        except requests.RequestException as e:
            click.echo(f"Error fetching prompt details: {str(e)}")
        
        return

    url = f"https://prompt-mgmt-api.stg.arohalabs.dev/prompts/?skip={skip}&limit={limit}"
    headers = {'accept': 'application/json'}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        prompts = response.json()
        
        if prompts:
            click.echo("Available prompts:")
            for prompt in prompts:
                click.echo(f"\n  - ID: {prompt.get('id', 'N/A')}")
                click.echo(f"    Name: {prompt.get('name', 'N/A')}")
                click.echo(f"    Author: {prompt.get('author_name', 'N/A')}")
                # click.echo(f"    Description: {prompt.get('description', 'N/A')}")
        else:
            click.echo("No prompts found.")
    except requests.RequestException as e:
        click.echo(f"Error fetching prompts: {str(e)}")




if __name__ == "__main__":
    cli()
