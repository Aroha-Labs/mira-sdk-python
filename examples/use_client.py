import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.mira.client.mira_client import MiraClient

client = MiraClient({"API_KEY": "<your_api_key>"})
result = client.execute_flow("@sarim2/itenary", {"city": "Brussels"})
print(result)
