import click


@click.command()
@click.option('--variable', type=str, required=True, help='Variable name')
@click.option('--variable-type', type=str, required=True, help='Variable type')
def take_user_input(variable, variable_type):
    if variable_type == "int":
        variable_input = click.prompt(f'Please enter {variable}', type=int)
    elif variable_type in {"string"}:
        variable_input = click.prompt(f'Please enter {variable}', type=str)
    else:
        variable_input = click.prompt(f'Please enter {variable}')
    return variable_input
