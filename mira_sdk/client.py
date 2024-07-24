# class Client:
#     def __init__(self, api_key):
#         self.api_key = api_key

#     def exec(self, flow_name, input):
#         raise NotImplementedError("This method should be implemented.")

#     async def exec_async(self, flow_name, input):
#         raise NotImplementedError("This method should be implemented asynchronously.")


import requests
import aiohttp
import asyncio

class Client:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://console.mira.network/v1'

    def run(self, flow_name, input):
        url = f"{self.base_url}/{flow_name}"
        headers = {
            'Authorization': f"Bearer {self.api_key}",
            'Content-Type': 'application/json'
        }

        try:
            response = requests.post(url, json=input, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"HTTP Request failed: {e}")

    async def run_async(self, flow_name, input):
        url = f"{self.base_url}/{flow_name}"
        headers = {
            'Authorization': f"Bearer {self.api_key}",
            'Content-Type': 'application/json'
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, json=input, headers=headers) as response:
                    response.raise_for_status()
                    return await response.json()
            except aiohttp.ClientError as e:
                raise Exception(f"HTTP Request failed: {e}")
