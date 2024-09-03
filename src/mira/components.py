class Generator:
    def __init__(self, config, resource_manager):
        self.config = config
        self.resource_manager = resource_manager
        self.prompt = self._resolve_prompt()
        self.model = self._resolve_model()

    def _resolve_prompt(self):
        prompt_ref = self.config['config']['prompt']
        # Remove the curly braces and split by dots
        prompt_parts = prompt_ref.strip('{}').split('.')
        prompt_name = prompt_parts[-1]  # Get the last part
        prompt = self.resource_manager.get_prompt(prompt_name)
        if prompt is None:
            raise ValueError(f"Prompt '{prompt_name}' not found in resources")
        return prompt

    def _resolve_model(self):
        model_ref = self.config['config']['model']
        # Remove the curly braces and split by dots
        model_parts = model_ref.strip('{}').split('.')
        model_name = model_parts[-1]  # Get the last part
        model = self.resource_manager.get_model(model_name)
        if model is None:
            raise ValueError(f"Model '{model_name}' not found in resources")
        return model

    def execute(self, input_text):
        prompt_content = self.prompt.get_content()
        formatted_prompt = prompt_content.format(**input_text)
        return self.model.generate(formatted_prompt)
