# mira-sdk / mira-cli

## Prerequisites

- Python >= 3.10
- pip
- pdm

## Setup

```
pdm sync
```

## Usage

### CLI Commands

The mira-cli provides several commands for managing flows, prompts, and executing operations. Here's a brief overview of the available commands:

1. Initialize a flow:
   ```
   pdm run python -m src.mira.cli.mira_cli init --flow <flow_name> --template <template_name>
   ```
   - List available templates:
     ```
     pdm run python -m src.mira.cli.mira_cli init --list
     ```

2. Execute a flow: - #TODO - lets call this as local testing or local run
   ```
   pdm run python -m src.mira.cli.mira_cli execute --config <path_to_config_file> --input key1=value1 key2=value2
   ```

3. Manage prompts: - we have to start with prompts
   - List all prompts:
     ```
     pdm run python -m src.mira.cli.mira_cli prompts --lists
     ```
   - Show details of a specific prompt:
     ```
     pdm run python -m src.mira.cli.mira_cli prompts --show --prompt-name <author/prompt_name>
     ```

4. Deploy a flow:
   ```
   pdm run python -m src.mira.cli.mira_cli deploy --flow <path_to_yaml_config> --name <flow_name>
   ```

5. Execute a deployed flow:
   ```
   pdm run python -m src.mira.cli.mira_cli execute-flow --flow-name <flow_name> --input-data '{"key": "value"}'
   ```

For more detailed information on each command and its options, use the `--help` flag:

### SDK Usage

The Mira SDK provides a simple way to execute flows and build custom flows programmatically. Here are examples of how to use the SDK:

#### Executing a Flow

To execute a flow using the MiraClient:

```python
from mira_sdk.mira.client.mira_client import MiraClient

client = MiraClient("flows/person.yaml")
result = client.execute({"coin": "Solana"})
print(result)
```

This script loads a flow from a YAML file and executes it with the given input.

#### Building a Custom Flow
#TODO - lets skip this piece for now

To create a custom flow using the FlowBuilder:

```python
from mira_sdk.mira.builder.flow_builder import FlowBuilder

builder = FlowBuilder()

# Set flow name and description
builder.set_name("SimpleTextGenerator")
builder.set_description("Persona Impersonator")

# Add resources
builder.add_prompt([{"second_prompt": "Generate a short story about {person} at {club}", "type": "local"},
                    {"main_prompt": "@aroha-labs/klok/1.0.0", "type": "mira"}])
builder.add_resource("knowledge", "writing_tips", {"file": "writing_tips.txt"})
builder.add_resource("models", "story_generator", {"type": "gpt-3.5-turbo"})

# Add component
builder.add_component(
    "story_generator",
    "Generator",
    {
        "prompt": "{resources.prompts.main_prompt}",
        "models": "{resources.models.story_generator}",
    },
)

# Add flow step
builder.add_flow_step(
    "story_generator",
    inputs=[{"person": "request", "club": "request"}],
    outputs=[{"target": "response"}]
)

# Save the flow
builder.save("flows/person.yaml")
```







