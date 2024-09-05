import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.mira.client.mira_client import MiraClient

client = MiraClient("flows/person.yaml")
result = client.execute({"coin": "Solana"})
print(result)
