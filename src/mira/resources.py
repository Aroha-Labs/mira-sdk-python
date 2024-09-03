import os
import openai

class Prompt:
    def __init__(self, content):
        self.content = content

    def get_content(self):
        return self.content

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
        self.prompts = self._load_prompts(config.get('prompts', {}))
        self.knowledge = self._load_knowledge(config.get('knowledge', {}))
        self.models = self._load_models(config.get('models', {}))

    def _load_prompts(self, prompt_config):
        return {k: Prompt(v) for k, v in prompt_config.items()}

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
