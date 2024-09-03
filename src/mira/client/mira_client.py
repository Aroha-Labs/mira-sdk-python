from ..flow import Flow


class MiraClient:
    def __init__(self, config_path):
        self.flow = Flow(config_path)

    def execute(self, input_data):
        return self.flow.execute(input_data)
