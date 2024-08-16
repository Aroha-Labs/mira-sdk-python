from src.mira_python_sdk.main import Mira

mira = Mira(api_key="mira")

mira.set_model("llama3:instruct")

mira.set_retriever("klok")

mira.set_prompt("prompt1")

mira.set_system_prompt("prompt2")

flow = mira.flow("klokc_flow")

flow.generate_yml()

flow.run()
