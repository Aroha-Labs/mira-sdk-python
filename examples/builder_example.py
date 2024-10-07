import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.mira.builder.flow_builder import FlowBuilder

builder = FlowBuilder()

builder.add_prompt("What is {coin}?", "local")
builder.add_knowledge("@sarim/youtube")
# ("@sanchay/youtube")
builder.add_model("tric/llama")

# Set flow name and description
builder.set_name("SimpleTextGenerator")
builder.set_description("Persona Impersonator")

# Add resources
builder.add_prompt([{"second_prompt": "Generate a short story about {person} at {club}", "type": "local"}, {"main_prompt": "@aroha-labs/klok/1.0.0", "type": "mira"}])
builder.add_resource("knowledge", "writing_tips", {"file": "writing_tips.txt"})
builder.add_resource("models", "story_generator", {"type": "tric/llama"})

# Add component
builder.add_component(
    "story_generator",
    "Generator",
    {
        "prompt": "{resources.prompts.main_prompt}",
        "model": "{resources.models.story_generator}",
    },
)

# Add flow step
builder.add_flow_step(
    "story_generator",
    inputs=[{"person": "request", "club": "request"}],
    outputs=[{"target": "response"}]
)

# Save the flow
builder.save("src/templates/person.yaml")
