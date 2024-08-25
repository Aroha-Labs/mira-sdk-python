import typer
import yaml
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
import requests
from youtube_transcript_api import YouTubeTranscriptApi
import re

load_dotenv()

client = OpenAI()
app = typer.Typer()

def get_content(params):
    if 'url' in params:
        url = params['url']
        if 'youtube.com' in url or 'youtu.be' in url:
            return get_youtube_transcript(url)
        else:
            return get_url_content(url)
    elif 'path' in params:
        return read_file_content(params['path'])
    else:
        raise ValueError("Unsupported content type in parameters")
    
def read_file_content(file_path):
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    with path.open('r', encoding='utf-8') as file:
        return file.read()

def get_youtube_transcript(url):
    video_id = extract_video_id(url)
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    return ' '.join([entry['text'] for entry in transcript])

def get_url_content(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def extract_video_id(url):
    # Extract video ID from YouTube URL
    youtube_regex = r'(youtu\.be\/|youtube\.com\/(watch\?(.*&)?v=|(embed|v)\/))([^?&"\'>]+)'
    match = re.search(youtube_regex, url)
    if match:
        return match.group(5)
    else:
        raise ValueError("Invalid YouTube URL")

@app.command()
def flowRunner(
    flow: str = typer.Argument(..., help="The name of the flow to run"),
    path: str = typer.Option(None, help="The file path to summarize"),
    url: str = typer.Option(None, help="The URL of the YouTube video")
):
    # Load the flow data
    with open(f"flow/{flow}.yml", "r") as file:
        flow_data = yaml.safe_load(file)

    # Validate required fields
    required_fields = ["model", "system_prompt", "user_prompt", "parameter"]
    for field in required_fields:
        if field not in flow_data:
            raise ValueError(f"Missing required field '{field}' in the YAML file.")

    # Prepare parameters
    params = {}
    for param in flow_data["parameter"]:
        param_name = list(param.keys())[0]
        if param_name == "path" and path:
            params["path"] = path
        elif param_name == "url" and url:
            params["url"] = url
        else:
            param_value = typer.prompt(f"Enter {param_name}")
            params[param_name] = param_value

    # Get content based on parameters
    content = get_content(params)

    # Call the OpenAI API
    response = client.chat.completions.create(
        model=flow_data["model"],
        messages=[
            {
                "role": "system",
                "content": flow_data["system_prompt"][0]["content"]
            },
            {
                "role": "user",
                "content": f"{flow_data['user_prompt'][0]['content']}: {content}"
            }
        ]
    )

    # Print the summary
    summary = response.choices[0].message.content
    typer.echo("Summary:")
    typer.echo(summary)

if __name__ == "__main__":
    app()
