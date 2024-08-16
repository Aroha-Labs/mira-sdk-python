# workflow_manager.py

import yaml
from math_custom import execute_operation

class WorkflowManager:
    def __init__(self):
        self.workflows = {}

    def load_workflow(self, name, file_path):
        with open(file_path, 'r') as file:
            workflow = yaml.safe_load(file)
        self.workflows[name] = workflow
        print(f"Workflow '{name}' loaded successfully.")

    def execute_workflow(self, name):
        if name not in self.workflows:
            raise ValueError(f"Workflow '{name}' not found.")

        workflow = self.workflows[name]
        print(f"Executing workflow: {workflow['name']}")
        print(f"Description: {workflow['description']}")

        variables = {}
        for step in workflow['steps']:
            print(f"Executing step: {step['name']}")
            inputs = {}
            for key, value in step['inputs'].items():
                if isinstance(value, str) and value.startswith('$'):
                    inputs[key] = variables[value[1:]]
                else:
                    inputs[key] = value

            result = execute_operation(
                step['operation'], inputs['a'], inputs['b'])
            variables[step['output']] = result
            print(f"  Result: {result}")

        final_result = variables[workflow['output']]
        print(f"Workflow execution completed. Final result: {final_result}")
        return final_result


# Example usage
if __name__ == "__main__":
    manager = WorkflowManager()

    # Load workflows
    manager.load_workflow("workflow1", "test.yml")
    # manager.load_workflow("workflow2", "workflow2.yml")

    # Execute workflows
    result1 = manager.execute_workflow("workflow1")
    print(f"Workflow 1 result: {result1}")

    # result2 = manager.execute_workflow("workflow2")
    # print(f"Workflow 2 result: {result2}")
