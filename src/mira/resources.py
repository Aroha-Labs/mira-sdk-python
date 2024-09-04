import os
import requests
import openai

from src.mira.constants import PROMPT_API_URL


class Prompt:
    def __init__(self, content, content_source):
        self.content = content
        self.content_source = content_source

    def get_content(self):
        if self.content_source == "mira":
            return self._fetch_content_from_api()
        return self.content, None

    def _fetch_content_from_api(self):
        # Parse the content to extract organization, prompt name, and version
        parts = self.content.split('/')
        if len(parts) < 2:
            raise ValueError("Invalid content format for mira source")

        org, prompt_name = parts[0].lstrip('@'), parts[1]
        version = parts[2] if len(parts) > 2 else None

        # Construct the API URL
        base_url = f"{PROMPT_API_URL}/prompts/{org}/{prompt_name}"
        if version:
            base_url += f"?version={version}"

        # Make the API request
        response = requests.get(base_url, headers={'accept': 'application/json'})

        if response.status_code == 200:
            data = response.json()
            return data['content'], data['variables']
        elif response.status_code == 404:
            raise Exception(f"Prompt: {self.content}, not found")
        else:
            raise Exception(f"API request failed with status code {response.status_code}")


class Knowledge:
    def __init__(self, file_path):
        self.file_path = file_path
        self.content = self._load_content()

    def _load_content(self):
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Knowledge file not found: {self.file_path}")
        
        with open(self.file_path, 'r') as file:
            return file.read()

    def get_content(self):
        return self.content

class Model:
    def __init__(self, config):
        self.type = config['type']
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        openai.api_key = self.api_key

    def generate(self, prompt):
        print(f"Generating with model: {self.type}")
        print(f"Prompt: {prompt}")
        response = openai.chat.completions.create(
            model=self.type,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

class ResourceManager:
    def __init__(self, config):
        self.prompts = self._load_prompts(config.get('prompts', {}), config.get('prompt_source', 'local'))
        self.knowledge = self._load_knowledge(config.get('knowledge', {}))
        self.models = self._load_models(config.get('models', {}))

    def _load_prompts(self, prompt_config, prompt_source):
        return {k: Prompt(v, prompt_source) for k, v in prompt_config.items()}

    def _load_knowledge(self, knowledge_config):
        return {k: Knowledge(v['file']) for k, v in knowledge_config.items()}

    def _load_models(self, model_config):
        return {k: Model(v) for k, v in model_config.items()}

    def get_prompt(self, name):
        prompt = self.prompts.get(name)
        if prompt is None:
            print(f"Warning: Prompt '{name}' not found. Available prompts: {list(self.prompts.keys())}")
        return prompt

    def get_knowledge(self, name):
        knowledge = self.knowledge.get(name)
        if knowledge is None:
            print(f"Warning: Knowledge '{name}' not found. Available knowledge: {list(self.knowledge.keys())}")
        return knowledge

    def get_model(self, name):
        model = self.models.get(name)
        if model is None:
            print(f"Warning: Model '{name}' not found. Available models: {list(self.models.keys())}")
        return model
