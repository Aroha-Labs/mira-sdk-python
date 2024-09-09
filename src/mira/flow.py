import yaml
from .components import Generator
from .resources import ResourceManager

class Flow:
    def __init__(self, yaml_path, config=None):
        if config:
            self.config = config
        else:
            with open(yaml_path, 'r') as file:
                self.config = yaml.safe_load(file)
        print("Loaded configuration:", self.config)
        self.resources = ResourceManager(self.config.get('resources', {}))
        self.components = self._load_components()

    def _load_components(self):
        components = self.config.get('components', {})
        loaded_components = {}
        for k, v in components.items():
            try:
                loaded_components[k] = Generator(v, self.resources)
            except ValueError as e:
                print(f"Error loading component '{k}': {str(e)}")
                raise
        return loaded_components

    def execute(self, request):
        flow_steps = self.config.get('flow', [])
        response = request
        for step in flow_steps:
            for component_name, config in step.items():
                component = self.components[component_name]
                response = component.execute(response)
        return response
