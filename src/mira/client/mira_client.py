import os
from .console import Console
from ..utils import split_name

class FlowConfig:
    def __init__(self, data:dict):
        self.flow = data.get('flow')
        self.name = data.get('name')
        self.resources = data.get('resources')
        self.components = data.get('components')
        self.description = data.get('description')

    def dict(self):
        return {
            'flow': self.flow,
            'name': self.name,
            'resources': self.resources,
            'components': self.components,
            'description': self.description
        }

class Flow:
    def __init__(self, flow_name:str, config:FlowConfig):
        self.org, self.name = split_name(flow_name)
        self.config = config  # FlowConfig

    def __str__(self):
        return f"{self.org}/{self.name}"


class Prompt:
    def __init__(self, org, name, version, content, variables=None):
        self.org = org
        self.name = name
        self.version = version
        self.content = content
        self.variables = variables or {}
        self.prompt_id = None  # This will be set when retrieved from or created in the console

    def __str__(self):
        return f"{self.org}/{self.name}/{self.version}"


class MiraClient:
    def __init__(self, config=None):
        self.config = config or {}
        self.console = Console(self.config.get("API_KEY"))

    def execute_flow(self, flow: Flow, input_dict: dict):
        return self.console.execute_flow(flow.org, flow.name, input_dict)

    def get_flow(self, flow_name: str) -> Flow:
        org, name = split_name(flow_name)
        flow_dict = self.console.get_flow(org, name)
        return Flow(flow_name, flow_dict.get('config'))

    def get_flows_by_author(self, author_name: str) -> list[Flow]:
        if len(author_name) > 1 and author_name[0] == "@":
            author_name = author_name[1:]
        flows_list = self.console.get_flows_by_author(author_name)
        return [Flow(f"{flow['org']}/{flow['name']}", FlowConfig(flow.get('config', {}))) for flow in flows_list]

    def deploy_flow(self, flow: Flow):
        return self.console.deploy_flow(flow.org, flow.name, flow.config.dict())

    def get_prompt(self, prompt_name: str) -> Prompt:
        version = None
        if len(prompt_name.split("/")) > 2:
            version = prompt_name.split("/")[-1]
        org, name = split_name(prompt_name)
        prompt_dict = self.console.get_prompt_version(org, name, version)
        prompt = Prompt(org, name, prompt_dict['version'], prompt_dict['content'], prompt_dict.get('variables'))
        prompt.prompt_id = prompt_dict['prompt_id']
        return prompt

    def create_prompt(self, prompt: Prompt) -> Prompt:
        result = self.console.create_prompt(prompt.org, prompt.name, prompt.version, prompt.content, prompt.variables)
        prompt.prompt_id = result['prompt_id']
        return prompt

    def update_prompt(self, prompt: Prompt) -> Prompt:
        current_prompt = self.console.get_prompt_version(prompt.org, prompt.name, None)
        result = self.console.add_prompt_version(current_prompt['prompt_id'], prompt.version, prompt.content, prompt.variables)
        prompt.prompt_id = result['prompt_id']
        return prompt

    def get_prompts_by_author(self, author_name: str) -> list[Prompt]:
        if len(author_name) > 1 and author_name[0] == "@":
            author_name = author_name[1:]
        prompts_list = self.console.get_prompts_by_author(author_name)
        return [Prompt(p['org'], p['name'], p['version'], p['content'], p.get('variables')) for p in prompts_list]

    def get_all_versions_by_prompt(self, prompt: Prompt) -> list[Prompt]:
        versions = self.console.get_all_versions_by_prompt(prompt.prompt_id)
        return [Prompt(prompt.org, prompt.name, v['version'], v['content'], v.get('variables')) for v in versions]

    def add_knowledge(self, knowledge_name: str, absolute_file_path: str):
        org, knowledge_name = split_name(knowledge_name)

        if not os.path.exists(absolute_file_path):
            raise FileNotFoundError(f"The file {absolute_file_path} does not exist.")

        if not os.access(absolute_file_path, os.R_OK):
            raise PermissionError(f"The file {absolute_file_path} is not readable.")

        max_size = 200 * 1024 * 1024  # 200MB in bytes
        if os.path.getsize(absolute_file_path) > max_size:
            raise ValueError(f"The file {absolute_file_path} exceeds the maximum allowed size of 200MB.")

        allowed_types = ['.csv', '.txt', '.pdf', '.zip', '.md']
        file_extension = os.path.splitext(absolute_file_path)[1].lower()
        if file_extension not in allowed_types:
            raise ValueError(f"Unsupported file type. Allowed types are: {', '.join(allowed_types)}")

        return self.console.add_knowledge(absolute_file_path, org, knowledge_name)

    def get_knowledge_context_for_prompt(self, knowledge_name: str, prompt_text: str):
        org, knowledge_name = split_name(knowledge_name)
        return self.console.get_knowledge_context_for_prompt(org, knowledge_name, prompt_text)
