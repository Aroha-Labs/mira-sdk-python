import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.mira.client.mira_client import MiraClient

client = MiraClient("my_flow.yaml")
result = client.execute({"topic": "Artificial Intelligence"})
print(result)
