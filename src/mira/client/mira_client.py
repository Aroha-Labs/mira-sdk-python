import os


from .console import Console
from ..utils import split_name


class MiraClient:
    def __init__(self, config=None):
        if config is None:
            config = {}
        self.config = config
        self.console = Console(self.config.get("API_KEY"))

    def execute_flow(self, flow_name: str, input_dict: dict):
        org, flow_name = split_name(flow_name)
        return self.console.execute_flow(org, flow_name, input_dict)

    def get_flow(self, flow_name: str):
        org, flow_name = split_name(flow_name)
        return self.console.get_flow(org, flow_name)

    def get_flows_by_author(self, author_name: str):
        if len(author_name) > 1 and author_name[0] == "@":
            author_name = author_name[1:]
        return self.console.get_flows_by_author(author_name)

    def deploy_flow(self, flow_name: str, flow_config: dict):
        org, flow_name = split_name(flow_name)
        return self.console.deploy_flow(org, flow_name, flow_config)

    def get_prompt(self, prompt_name: str):
        org, prompt_name = split_name(prompt_name)
        version = None
        if len(prompt_name.split("/")) > 2:
            version = prompt_name.split("/")[-1]
        return self.console.get_prompt_version(org, prompt_name, version)

    def create_prompt(self, prompt_name: str, content: str, variables=None, version="1.0.0"):
        if variables is None:
            variables = {}
        org, prompt_name = split_name(prompt_name)
        # return self.console.add_prompt(org, prompt_name)
        return self.console.create_prompt(org, prompt_name, content, variables, version)

    # def create_prompt_version(self, prompt, version: str, content: str, variables=None):
    #     return self.console.add_prompt_version(prompt.id, version, content, variables)

    def get_prompts_by_author(self, author_name: str):
        if len(author_name) > 1 and author_name[0] == "@":
            author_name = author_name[1:]
        return self.console.get_prompts_by_author(author_name)

    def get_all_versions_by_prompt(self, prompt):
        return self.console.get_all_versions_by_prompt(prompt.id)

    def add_knowledge(self, file_path: str, author_name: str, knowledge_name: str):
        # Check if the file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")

        # Check if the file is readable
        if not os.access(file_path, os.R_OK):
            raise PermissionError(f"The file {file_path} is not readable.")

        # Check file size
        max_size = 200 * 1024 * 1024  # 200MB in bytes
        if os.path.getsize(file_path) > max_size:
            raise ValueError(f"The file {file_path} exceeds the maximum allowed size of 200MB.")

        # Check file type
        allowed_types = ['.csv', '.txt', '.pdf', '.zip']
        file_extension = os.path.splitext(file_path)[1].lower()
        if file_extension not in allowed_types:
            raise ValueError(f"Unsupported file type. Allowed types are: {', '.join(allowed_types)}")

        return self.console.add_knowledge(file_path, author_name, knowledge_name)

    def get_knowledge_context_for_prompt(self, knowledge_name: str, prompt_text: str):
        org, knowledge_name = split_name(knowledge_name)
        return self.console.get_knowledge_context_for_prompt(org, knowledge_name, prompt_text)
