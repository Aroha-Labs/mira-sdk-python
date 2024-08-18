from typing import Optional, List
import requests
import yaml


class Document:
    def __init__(self, content: str):
        self.content = content


class InMemoryDocumentStore:
    def __init__(self):
        self.documents = []

    def write_documents(self, documents: List[Document]):
        self.documents.extend(documents)


class MiraRetriever:
    def __init__(self, document_store: InMemoryDocumentStore):
        self.document_store = document_store
        self.type = "MiraRetriever"
        self.config = {"document_store": document_store}

    def run(self, query: str):
        # Simplified retrieval logic
        return self.document_store.documents


class MiraPromptBuilder:
    def __init__(self, template: str):
        self.template = template
        self.type = "MiraPromptBuilder"
        self.config = {"template": template}

    def run(self, documents: List[Document], question: str):
        # Simple template formatting
        docs_content = "\n".join([doc.content for doc in documents])
        return self.template.format(documents=docs_content, question=question)


class MiraGenerator:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.type = "MiraGenerator"
        self.config = {"api_key": api_key}

    def run(self, prompt: str):
        # Simplified API call
        response = requests.post(
            "http://10.147.19.152:11434/api/generate",
            headers={"Content-Type": "application/json",
                     "accept": "application/json"},
            json={"model": "llama3:instruct", "prompt": prompt, "stream": False}
        )
        # print(response.json())
        return response.json()["response"]


class MiraPipeline:
    def __init__(self):
        self.components = {}
        self.connections = {}
        self.documents = []
        self.query = ""

    def add_component(self, name: str, component):
        self.components[name] = component

    def connect(self, from_component: str, to_component: str):
        if from_component not in self.connections:
            self.connections[from_component] = []
        self.connections[from_component].append(to_component)

    def run(self, inputs: dict):
        results = {}
        for component_name, component in self.components.items():
            if component_name in inputs:
                print(component_name, component)
                results[component_name] = component.run(
                    **inputs[component_name])
            else:
                input_data = {}
                for from_comp, to_comps in self.connections.items():
                    print(from_comp, to_comps)
                    if component_name in to_comps:
                        # Handle the case where the result is not a dictionary
                        if isinstance(results[from_comp], dict):
                            input_data.update(results[from_comp])
                        else:
                            input_data[from_comp] = results[from_comp]
                results[component_name] = component.run(**input_data)
        return results

    def generate_mermaid_diagram(self) -> str:
        mermaid_str = "graph TD\n"
        for from_component, to_components in self.connections.items():
            for to_component in to_components:
                mermaid_str += f"    {from_component} --> {to_component}\n"

        with open("mermaid.md", "w") as f:
            f.write(mermaid_str)
        return mermaid_str

    def generate_yaml_file(self) -> None:
        pipeline_structure = {
            "pipeline": {
                "name": "RAG_Pipeline",
                "components": [
                    {
                        "name": component_name,
                        "type": component.type,
                        "config": component.config
                    }
                    for component_name, component in self.components.items()
                ],
                "connections": [
                    {"from": from_component, "to": to_component}
                    for from_component, to_components in self.connections.items()
                    for to_component in to_components
                ]
            },
            "documents": [
                {"content": doc.content} for doc in self.documents
            ],
            "query": self.query
        }
        
        with open("pipeline_structure.yaml", "w") as f:
            yaml.dump(pipeline_structure, f, default_flow_style=False, sort_keys=False)


# Usage example:
document_store = InMemoryDocumentStore()
document_store.write_documents([
    Document(content="My name is Jean and I live in Paris."),
    Document(content="My name is Mark and I live in Berlin."),
    Document(content="My name is Giorgio and I live in Rome.")
])

prompt_template = """
Given these documents, answer the question.
Documents:
{documents}
Question: {question}
Answer:
"""

retriever = MiraRetriever(document_store=document_store)
prompt = MiraPromptBuilder(template=prompt_template)
generator = MiraGenerator(api_key="your_api_key_here")

rag_pipeline = MiraPipeline()
rag_pipeline.add_component("retriever", retriever)
rag_pipeline.add_component("prompt", prompt)
rag_pipeline.add_component("generator", generator)
rag_pipeline.connect("retriever", "prompt")
rag_pipeline.connect("prompt", "generator")
  
# Ask a question
question = "Who lives in Paris?"
results = rag_pipeline.run(
    {
        "retriever": {"query": question},
        "prompt": {"question": question, "documents": document_store.documents},
    }
)

# print(results["generator"])

mermaid_diagram = rag_pipeline.generate_mermaid_diagram()
print("Mermaid Diagram:")
print(mermaid_diagram)


rag_pipeline.generate_yaml_file()
