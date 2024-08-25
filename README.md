# mira-cli

A flexible CLI tool for running customizable AI-powered workflows.

## Creating a Flow

1. Create a YAML file in the `flow/` directory with the following structure:

```yaml
model: <OpenAI model name>
system_prompt:
  - content: <System prompt for the AI>
user_prompt:
  - content: <User prompt for the AI>
parameter:
  - <param_name>:
      type: <param_type>
      description: <param_description>
```

Example: `flow/summarizer.yml`

## Using the CLI

Run a flow:

```bash
typer src/main.py run <flow_name>
```
