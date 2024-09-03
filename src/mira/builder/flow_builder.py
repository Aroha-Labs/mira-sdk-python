import yaml


class FlowBuilder:
    def __init__(self):
        self.config = {"name": "", "description": "", "resources": {}, "components": {}, "flow": []}

    def set_name(self, name):
        self.config["name"] = name

    def set_description(self, description):
        self.config["description"] = description

    def add_resource(self, resource_type, name, config):
        if resource_type not in self.config["resources"]:
            self.config["resources"][resource_type] = {}
        self.config["resources"][resource_type][name] = config

    def add_component(self, name, component_type, config):
        self.config["components"][name] = {"type": component_type, "config": config}

    def add_flow_step(self, component_name, inputs=None, outputs=None):
        step = {component_name: {}}
        if inputs:
            step[component_name]["inputs"] = inputs
        if outputs:
            step[component_name]["outputs"] = outputs
        self.config["flow"].append(step)

    def build(self):
        return self.config

    def save(self, file_path):
        with open(file_path, "w") as f:
            yaml.dump(self.config, f, default_flow_style=False, sort_keys=False)
