# math_operations.py

def addition(a, b):
    return a + b


def subtraction(a, b):
    return a - b


def multiplication(a, b):
    return a * b


def execute_operation(operation, a, b):
    operations = {
        'addition': addition,
        'subtraction': subtraction,
        'multiplication': multiplication
    }
    return operations[operation](a, b)
