import requests


class Console:
    def __init__(self, api_key):
        self.api_key = api_key
        # self.base_url = "https://console-bff.stg.arohalabs.dev"
        self.base_url = "http://0.0.0.0:8000"

    def _request(self, method, path, query_params=None, json_data=None, files=None):
        url = f"{self.base_url}/{path}"
        headers = {
            "MiraAuthorization": f"{self.api_key}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.request(
                method,
                url,
                params=query_params,
                json=json_data,
                headers=headers,
                files=files
            )
            if response.status_code != 200:
                raise Exception(f"Response status: {response.status_code}, detail: {response.json() if response.headers.get('content-type') == 'application/json' else response.text}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            # Handle any request-related errors
            print(f"An error occurred: {e}")
            return None

    def add_prompt(self, author_name, prompt_name):
        path = f"v1/prompts/"
        json_data = {
            "name": prompt_name,
            "author_name": author_name
        }
        return self._request(method="post", path=path, json_data=json_data)

    def create_prompt(self, author_name, prompt_name, content, variables, version):
        path = f"v1/prompts/"
        json_data = {
            "name": prompt_name,
            "author_name": author_name,
            "content": content,
            "variables": variables,
            "version": version
        }
        return self._request(method="post", path=path, json_data=json_data)

    def add_prompt_version(self, prompt_id, version, content, variables=None):
        if variables is None:
            variables = {}
        path = f"v1/prompts/version"
        json_data = {
            "prompt_id": prompt_id,
            "version": version,
            "content": content,
            "variables": variables
        }
        return self._request(method="post", path=path, json_data=json_data)

    def get_prompt_version(self, author_name: str, prompt_name: str, version=None):
        path = f"v1/prompts/{author_name}/{prompt_name}"
        params = {}
        if version:
            params["version"] = version
        return self._request(method="get", path=path, query_params=params)

    def execute_flow(self, author_name, flow_name, input_dict):
        path = f"v1/flows/{author_name}/{flow_name}"
        return self._request(method="post", path=path, json_data=input_dict)

    def get_flow(self, author_name, flow_name):
        path = f"v1/flows/{author_name}/{flow_name}"
        return self._request(method="get", path=path)

    def get_flows_by_author(self, author_name):
        path = f"v1/flows/{author_name}"
        return self._request(method="get", path=path)

    def deploy_flow(self, author_name, flow_name, flow_config):
        path = f"v1/flows/deploy/{author_name}/{flow_name}"
        json_data = {
            "flow": flow_config
        }
        return self._request(method="post", path=path, json_data=json_data)

    def get_prompts_by_author(self, author_name):
        path = f"v1/prompts/{author_name}"
        return self._request(method="get", path=path)

    def get_all_versions_by_prompt(self, prompt_id):
        path = f"v1/prompts/{prompt_id}/versions"
        return self._request(method="get", path=path)

    def add_knowledge(self, file_path, author_name, knowledge_name):
        path = "v1/knowledge/upload"
        files = {'file': open(file_path, 'rb')}
        data = {
            'author_name': author_name,
            'knowledge_name': knowledge_name
        }
        return self._request(method="post", path=path, files=files, json_data=data)

    def get_knowledge_context_for_prompt(self, author_name: str, knowledge_name: str, prompt_text: str):
        path = f"v1/knowledge/{author_name}/{knowledge_name}"
        params = {}
        if prompt_text:
            params["prompt"] = prompt_text
        return self._request(method="get", path=path, query_params=params)
