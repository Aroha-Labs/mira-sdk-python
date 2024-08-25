# mira-cli

A flexible CLI tool for running customizable AI-powered workflows.

## Installation

```bash
pip install pdm
```

```bash
pdm install
```

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
pdm run typer src/main.py run <flow-name>
```

Currently supported flows:

- `summarizer`: Summarize a text
- `youtube`: Transcript and summarize a YouTube video

Future flows:

- `translator`: Translate a text
- `chatbot`: Chat with a text
- `code_interpreter`: Generate images from a text
- `file_search`: Search for a file
- `youtube_video_summarizer`: Summarize a YouTube video
- `youtube_video_translator`: Translate a YouTube video


