from ..flow import Flow
import yaml



class MiraClient:
    def __init__(self, config_path=None, config=None):
        self.flow = Flow(config_path, config)

    def execute(self, input_data):
        return self.flow.execute(input_data)
    
    def init_flow(self, flow_name, template_path):
        with open(template_path, "r") as file:
            template = yaml.safe_load(file)

        # save in flows/flow_name.yaml
        with open(f"flows/{flow_name}.yaml", "w") as file:
            yaml.dump(template, file)   

        print(f"Flow {flow_name} initialized with template {template_path}")
