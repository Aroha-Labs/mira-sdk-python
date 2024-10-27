import sys
import os
import yaml
import asyncio

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.mira.client.mira_client import MiraClient, FlowConfig, Flow, Prompt
from src.mira.client.async_mira_client import AsyncMiraClient

# from mira_sdk import MiraClient

client = MiraClient({"API_KEY": "<YOUR_API_KEY>"})
async_client = AsyncMiraClient({"API_KEY":"<YOUR_API_KEY>"})

with open('src/mira/templates/person.yaml', 'r') as file:
    data = yaml.safe_load(file)



async def main():
    # This is correct:
    prompt = await async_client.prompt.get("@yash/city")
    print(prompt)

# Run the async function
asyncio.run(main())

# # Prompts
prompt = client.prompt.get("@yash/city")
print(prompt)
# created_prompt = client.prompt.create(Prompt(prompt_name="@friday/city", content="What is the best cuisine of {city}?", version="0.0.1", variables={"city": "string"}))
# updated_prompt = client.prompt.update(Prompt(prompt_name="@yash/city", content="What is the best cuisine of {city}?", version="1.4.3", variables={"city": "string"}))
# prompts_by_author = client.prompt.get_by_author("@test")
# all_prompt_versions = client.prompt.get_all_versions(prompt)

# # Flows
# flow = client.flow.get("@aroha-labs/coin-flow")
# result = client.flow.execute(flow, input_dict)
# run_result = client.flow.run(FlowConfig(data), input_dict)
# flows_by_author = client.flow.get_by_author("@test")
# deployed_flow = client.flow.deploy(flow)

# # Knowledge
# knowledge = client.knowledge.add("@sarim/test", "/path/to/file.csv")
# knowledge_context = client.knowledge.get_context_for_prompt("@sarim/test", "Who is the founder of Mira?")

# print(data)
#
# flow1 = Flow(flow_name="@test/flower", config=FlowConfig(data), private=True, version="1.2.0")
# flow1.to_yaml("abcd.yaml")
# print(flow1.config.dict())
# print(flow1.name)
# print(flow1.org)

# flow2 = client.get_flow("@aroha-labs/coin-flow")
# flow2 = async_client.update_prompt(Prompt(prompt_name="@yash/city", content="What is the best cuisine of {city}?", version="1.4.3", variables={"city": "string"}))
# print(flow2)
# async def main():
#     flow2 = await client.update_prompt(Prompt(prompt_name="@yash/city", content="What is the best cuisine of {city}?", version="1.1.3", variables={"city": "string"}))
#     print(flow2)

# asyncio.run(main())
# async def main():
#     flow2 = await client.update_prompt(Prompt(prompt_name="@yash/city", content="What is the best cuisine of {city}?", version="1.1.3", variables={"city": "string"}))
#     print(flow2)

# asyncio.run(main())
# print(flow2.version)
# print(flow2.config)

# test_flows = client.get_flows_by_author("@test")
# print(test_flows)
# created_prompt = client.create_prompt(prompt_name="@friday/city", content="What is the best cuisine of {city}?", version="0.0.1", variables={"city": "string"})

# new_prompt = client.get_prompt("@friday/city")
# print(new_prompt)
# updated_prompt = client.update_prompt("@friday/city", "0.0.3", "What is famous about {city}? List it's prominent restaurants and their ratings", {"city": "string"})
# print(updated_prompt)
# prompts_by_author = client.get_prompts_by_author("@test")
# print(prompts_by_author)
# all_prompt_versions = client.get_all_versions_by_prompt(new_prompt)
# print(all_prompt_versions)
# # all_prompts = client.get_prompts_by_author("")
# result = client.get_flows_by_author("@sarim")
# print(result)

# flow1 = client.get_flow("@sarim/itenary")
# print(flow1)
# required_vars = flow1["input"]["required"]

# Take input from user
# input_vars_dict = {
#     "coin": "Solana",
#     "date": "1945"
# }
# #
# result = client.run_flow(FlowConfig(data), input_vars_dict)
# print(result)
# # #
# # knowledge = client.add_knowledge("@sarim/test", "/Users/sanchay/Downloads/urls.csv")
# # knowledge1 = client.add_knowledge("@sarim/test", "/Users/sanchay/Downloads/scores.md")
# # print(knowledge)
# # knowledge_context = client.get_knowledge_context_for_prompt("@sarim/test", "Who is the founder of Mira?")
# # print(knowledge_context)
# """
# {
#     "context": ""
# }
# """


# deployed_flow = client.deploy_flow(flow1)
# result = client.execute_flow(flow1, input_vars_dict)
# print(result)



# deployed_flow = client.deploy_flow("@test/flow", {
#     "flow": {
#       "flow": [
#         {
#           "itinerary_generator": {
#             "inputs": [
#               {
#                 "city": "request"
#               }
#             ],
#             "outputs": [
#               {
#                 "target": "response"
#               }
#             ]
#           }
#         }
#       ],
#       "name": "DetailedItineraryGenerator",
#       "resources": {
#         "models": {
#           "itinerary_generator": {
#             "type": "tric/llama"
#           }
#         },
#         "prompts": [
#           {
#             "type": "local",
#             "itinerary_prompt": "give me a detailed itinerary for a trip to {city}"
#           }
#         ]
#       },
#       "components": {
#         "itinerary_generator": {
#           "type": "Generator",
#           "config": {
#             "model": "{resources.models.itinerary_generator}",
#             "prompt": "{resources.prompts.itinerary_prompt}"
#           }
#         }
#       },
#       "description": "Generate a detailed itinerary based on the given city"
#     }
# })
# print(deployed_flow)
#
# class Prompt:
#   def __init__(self):
#       self.content = "What is the best cuisine of {country}?"
#       self.version = "1.0.0"
#
#
# prompt["content"]
# prompt.content

"""
MiraClient:

Prompts ->
- create_prompt(prompt_name: str, content: str, version: str = "1.0.0", variables: dict = None) -> Prompt
- update_prompt(prompt_name: str, version: str, content: str, variables: dict = None) -> Prompt
- get_prompt(prompt_name: str) -> Prompt
- get_prompts_by_author(author_name: str) -> List[Prompt]
- get_all_versions_by_prompt(prompt: Prompt) -> List[Prompt]

Flows ->
- execute_flow(flow_name: str, input_dict: dict) -> PromptResponse
- get_flow(flow_name: str) -> Flow
- get_flows_by_author(author_name: str) -> List[Flow]
- deploy_flow(flow_name: str, flow: Flow) -> Flow

Knowledge ->
- add_knowledge(knowledge_name: str, absolute_file_path: str) -> (open to suggestion, polling or callback URL?)
- get_knowledge_context_for_prompt(knowledge_name: str, prompt_text: str) -> dict({"context": str})

Not implemented yet:
- remove_knowledge(knowledge_name: str, "abcd.md")
"""


