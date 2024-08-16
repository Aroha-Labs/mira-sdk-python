import os
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
import requests
import yaml
from abc import ABC, abstractmethod
from typing import Optional
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader




class MiraComponent(ABC):
    @abstractmethod
    def list(self):
        pass

class Mira:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self._model = MiraModel()
        self._retriever = MiraRetriever()
        self._prompt = MiraPrompt()
        self._system_prompt = MiraPrompt()

    def set_model(self, model_name: str) -> 'MiraModel':
        self._model.set_model(model_name)
        return self._model
    
    def set_prompt(self, prompt_id: str) -> 'MiraPrompt':
        self._prompt.set_prompt(prompt_id)
        return self._prompt

    def set_system_prompt(self, prompt_id: str) -> 'MiraPrompt':
        self._system_prompt.set_prompt(prompt_id)
        return self._system_prompt

    def set_retriever(self, retriever_name: str, local_folder: Optional[str] = None) -> 'MiraRetriever':
        self._retriever.set_retriever(retriever_name, local_folder)
        return self._retriever

    def flow(self, flow_name: str) -> 'Flow':
        return Flow(self, flow_name)

class Flow:
    def __init__(self, mira: Mira, flow_name: str):
        self.mira = mira
        self.flow_name = flow_name

    def generate_yml(self):
        yml_data = {
            self.flow_name: {
                "retriever": {"name": self.mira._retriever.retriever_name},
                "model": {"name": self.mira._model.model_name},
                "prompt": {"id": self.mira._prompt.prompt_id},
                "system_prompt": {"id": self.mira._system_prompt.prompt_id}
            }
        }
        with open(f"{self.flow_name}.yml", "w") as f:
            yaml.dump(yml_data, f, default_flow_style=False, sort_keys=False)
    
    def run(self):
        self._validate_components()
        prompt = self.mira._prompt.generate()
        system_prompt = self.mira._system_prompt.generate()
        
        print("------------------")
        print("Retrieving documents...")
        retrieved_docs = self.mira._retriever.retrieve(prompt, format=True)
        print("Documents retrieved", retrieved_docs)
        print("------------------")
        
        system_prompt = system_prompt.format(context=retrieved_docs)
        
        print("Generating response...")
        model_response = self.mira._model.generate(prompt, system_prompt)
        print("Response generated:")
        print(model_response['response'])

    def _validate_components(self):
        if not self.mira._prompt.is_set() or not self.mira._system_prompt.is_set():
            raise ValueError("Both prompt and system prompt must be set")
        if not self.mira._model.is_set():
            raise ValueError("Model must be set")
        if not self.mira._retriever.is_set():
            raise ValueError("Retriever must be set")

class MiraRetriever(MiraComponent):
    retriever_list = {
        'klok': {
            'description': 'Klok is a retriever that retrieves information from the Klok database.',
            'url': 'http://10.147.19.140:8800/v1/retrieve'
        },
        'local': {
            'description': 'Local retriever that uses embeddings from a specified folder.',
            'url': None
        }
    }


    def __init__(self):
        self.retriever_name = None
        self.local_folder = None
        self.embeddings = None
        self.documents = None

    def set_retriever(self, retriever_name: str, local_folder: Optional[str] = None):
        if retriever_name not in self.retriever_list:
            raise ValueError(f"Unknown retriever: {retriever_name}")
        self.retriever_name = retriever_name
        if retriever_name == 'local':
            if local_folder is None:
                raise ValueError("Local folder path is required for local retriever")
            self.local_folder = local_folder
            self._process_local_folder()

    def _process_local_folder(self):
        # This method will process the local folder and create embeddings
        # You'll need to implement this based on your specific requirements
        # For example, you might use a library like sentence-transformers
        if self.local_folder is None:
            raise ValueError("Local folder path is required")
        documents = DirectoryLoader(self.local_folder).load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200, add_start_index=True
        )
        all_splits = text_splitter.split_documents(documents)

        chroma_vectorstore = Chroma.from_documents(
            documents=all_splits, embedding=OpenAIEmbeddings(), persist_directory="./chroma_db")

        self.documents = documents


    def retrieve(self, query: str, format: bool = False):
        if not self.is_set():
            raise ValueError("Retriever name is required")
        
        if self.retriever_name == 'local':
            return self._local_retrieve(query, format)
        else:
            if self.retriever_name is None:
                raise ValueError("Retriever name is required")
            # Existing code for other retrievers
            url = self.retriever_list[self.retriever_name]['url']
            response = requests.post(
                url,
                headers={'Content-Type': 'application/json'},
                json={'query': query, 'k': 1}
            )

            if format:
                return "\n\n".join(doc['text'] for doc in response.json())
            return response.json()

    def _local_retrieve(self, query: str, format: bool = False):
        # Implement local retrieval logic here
        # This should use the embeddings and documents created in _process_local_folder
        # Return results in the same format as the API-based retriever
        chroma_vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=OpenAIEmbeddings())
        retriever = chroma_vectorstore.as_retriever()
        

        retrieved_docs = retriever.invoke(query)

        if format:
            return "\n\n".join(doc.page_content for doc in retrieved_docs)
        return retrieved_docs

    def list(self):
        return self.retriever_list

    def is_set(self):
        return self.retriever_name is not None

class MiraModel(MiraComponent):
    url = "http://10.147.19.152:11434"

    def __init__(self):
        self.model_name = None

    def set_model(self, model_name: str):
        self.model_name = model_name

    def list(self):
        list_url = f"{self.url}/api/tags"
        response = requests.get(list_url)
        
        return response.json()

    def generate(self, prompt: str, system_prompt: str = "Be a helpful assistant that can answer questions."):
        if not self.is_set():
            raise ValueError("Model name is required")

        generate_url = f"{self.url}/api/generate"
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        data = {
            "model": self.model_name,
            "prompt": prompt,
            "system": system_prompt,
            "stream": False
        }
        response = requests.post(generate_url, headers=headers, json=data)
        return response.json()

    def is_set(self):
        return self.model_name is not None

class MiraPrompt(MiraComponent):
    prompt_list = {
        "prompt1": {
            "value": "What is {entity} and also tell me about this {coin}",
            "variables": ["entity", "coin"],
        },
        "prompt2": {
            "value": "Be a helpful assistant that can answer questions about \n\n{context}.",
            "variables": ["context"]
        }
    }
    
    def __init__(self):
        self.prompt_id = None

    def set_prompt(self, prompt_id: str):
        if prompt_id not in self.prompt_list:
            raise ValueError(f"Unknown prompt ID: {prompt_id}")
        self.prompt_id = prompt_id

    def list(self):
        return self.prompt_list
    
    def generate(self):
        if not self.is_set():
            raise ValueError("Prompt ID is required")
        if self.prompt_id is None:
            raise ValueError("Prompt ID is required")
        if self.prompt_id not in self.prompt_list:
            raise ValueError(f"Unknown prompt ID: {self.prompt_id}")

        prompt = self.prompt_list[self.prompt_id]['value']
        variables = self.prompt_list[self.prompt_id]['variables']
        for variable in variables:
            if variable != "context":
                value = input(f"Please provide the value for the variable '{variable}': ")
                prompt = prompt.replace(f"{{{variable}}}", value)
        
        return prompt

    def is_set(self):
        return self.prompt_id is not None

# Usage example:
mira = Mira(api_key="123")
# mira._model.list()
mira.set_model("llama3:instruct")


mira.set_retriever(
    "local", local_folder="/Users/sarim/projects/work/mira-python-sdk/src/data/")

mira.set_prompt("author/prompt-name")  
mira.set_system_prompt("prompt2")
mcq_flow = mira.flow("mcq")
mcq_flow.run()
# mira.set_retriever("klok")
# mira.set_prompt("prompt1")
# mira.set_system_prompt("prompt2")
# mcq_flow = mira.flow("mcq")
# mcq_flow.run()
    