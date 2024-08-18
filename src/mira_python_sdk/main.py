# klokc_flow:
#   id: klokc_flow_001
#   tasks:
#     data:
#       namespace:
#         - hapchap_content_source
#       src: data/prompt_engineering.md
#     retriever:
#       namespace:
#         - hapchap_content_source
#       index_name: rag_pipeline.chunks_to_embeddings.embedding
#       query: prompt engineering
#     model:
#       name: llama3:instruct
#     prompt:
#       id: extract_entities

import yaml
from indexify import Content, IndexifyClient, ExtractionGraph, Document
import os
import csv
from langchain_openai import ChatOpenAI

flow = None
documents = []

def parse_flow(flow_path: str):
    with open(flow_path, "r") as f:
        flow = yaml.load(f, Loader=yaml.FullLoader)
    return flow


def ingest_data(namespace: str, src: str):
    print(src)
    print(namespace)
    client = IndexifyClient(namespace=namespace)

    for doc in os.listdir(src):
        print(doc)
        doc_path = os.path.join(src, doc)
        with open(doc_path, "r") as f:
            data = f.read()
            documents.append(
                Document(
                    data,
                    {
                        "namespace": namespace,
                    },
                    None,
                )
            )

    content_ids = client.add_documents("rag_pipeline", documents)

    for content_id in content_ids:
        print(content_id)
        client.wait_for_extraction(content_id)
        metadata = client.get_content_metadata(content_id)
        print("metadata", metadata)

    return documents


def retriever_data(query: str, namespace: str):
    print(query)
    print(namespace)
    client = IndexifyClient(namespace=namespace)
    retriever = client.search_index(
        "rag_pipeline.chunks_to_embeddings.embedding", query, top_k=1
    )
    retriever_data = ""
    for doc in retriever:
        retriever_data += doc.get("text", "") + "\n\n"
    return retriever_data

def retriever_data_local(src: str):
    retriever_data = ""
    for doc in os.listdir(src):
        doc_path = os.path.join(src, doc)
        with open(doc_path, "r") as f:
            retriever_data += f.read() + "\n\n"
    return retriever_data


def get_response(prompt_id: str, retrieved_data: str, model: str):
    llm = ChatOpenAI(model=model, base_url="https://ollama.stg.arohalabs.dev/v1")
    csv_reader = csv.reader(open("src/prompts/db.csv", "r"))
    prompt = ""
    for row in csv_reader:
        if row[0] == prompt_id:
            prompt_location = row[1]
            with open(prompt_location, "r") as f:
                prompt = f.read()
            # variables = row[2]

    prompt = prompt.replace("{context}", retrieved_data)

    resp = llm.invoke(prompt)
    return resp


# print(retrieved_data)
# print(prompt.format(variables, retrieved_data))
# for variable in variables:
#   prompt = prompt.replace(variable, retrieved_data)
# return prompt


flow_data = parse_flow("flow/entities.yml")["tasks"]
print(flow_data)


src = flow_data["data"]["src"]
# namespace = flow_data["data"]["namespace"][0]

# query = flow_data["retriever"]["query"]
retrieved_data = retriever_data_local(src)

# retriever_data = retriever_data(query, namespace)
model = flow_data["model"]["name"]
print(model)

print(get_response(flow_data["prompt"]["id"], retrieved_data, model))
# print(ingest_data(namespace, src))
