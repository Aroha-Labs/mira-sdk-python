import os
from src.mira import Flow


# Initialize the flow from the YAML file
flow = Flow('example_flow.yaml')

# Define the input for our story generation
input_text = {"topic": "Cristiano Ronaldo"}

# Execute the flow
result = flow.execute(input_text)

# Print the generated story
print("Generated Story:")
print(result)
