import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.mira import Flow


# Initialize the flow from the YAML file
flow = Flow('src/templates/person.yaml')

# Define the input for our story generation
input_text = {"coin": "ZRX", "date": "Ice age"}

# Execute the flow
result = flow.execute(input_text)

# Print the generated story
print("Generated Story:")
print(result)
