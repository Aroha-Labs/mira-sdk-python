import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mira_sdk.mira.client.mira_client import MiraClient
from mira_sdk.mira.flow import Flow
from mira_sdk.mira.integrations.composio import ComposioConfig
client = MiraClient(config={"API_KEY": ""})

flow = Flow(source="examples/roast.yaml")

input_dict = {"user": "frenzyScholar"}

client.flow.test(flow, input_dict, ComposioConfig(COMPOSIO_API_KEY="", ACTION="TWITTER_CREATION_OF_A_POST", TASK="Post the following tweet - {content}", ENTITY_ID=""))
