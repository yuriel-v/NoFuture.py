from os import getenv
from ruamel.yaml import YAML
from typing import Iterable, Union

yaml = YAML(typ='safe')
def load_configs():
    try:
        with open('./src/config.yml', mode='r', encoding='utf-8') as file:
            nf_configs = yaml.load(file)['nofuture']
    except Exception as e:
        if isinstance(e, OSError):
            # load from environment variables instead
            nf_configs = dict({})
            nf_configs['version'] = float(getenv("NF_VERSION"))
            nf_configs['discord_token'] = getenv("NF_DISCORD_TOKEN")
            nf_configs['owner_id'] = int(getenv("NF_OWNER_ID"))
            nf_configs['hub_guild'] = int(getenv("NF_HUB_GUILD"))
            nf_configs['api_tokens'] = dict({})
            nf_configs['api_tokens']['imgur'] = getenv("NF_APIS_IMGUR")
            nf_configs['api_tokens']['ggl_images_api'] = getenv("NF_APIS_GGL_IMAGES_API")
            nf_configs['api_tokens']['ggl_images_cx'] = getenv("NF_APIS_GGL_IMAGES_CX")
        else:
            print(f"Exception thrown while loading configs: {e}")
            nf_configs = None
    return nf_configs
nf_configs = load_configs()


def nround(number: float, decimals=1):
    """Normalized round. nround(0.5) = 1"""
    number = str(number)
    # if decimal places <= decimals
    if len(number[number.index('.')::]) <= decimals + 1:
        return float(number)
    if number[-1] == '5':
        number = number[:-1:] + '6'
    return round(float(number), decimals)


def avg(items: Union[list, tuple, set]):
    """Average between items in list/tuple/set."""
    return sum(items) / len(items)


def split_args(arguments: str, islist=True) -> Union[list[str], str]:
    """
    Splits a command's arguments into a list and returns it.
    If `islist = False` then this returns a full string without the command prefix.
    """
    arguments = arguments.split(' ')
    arguments.pop(0)  # prefix
    arguments.pop(0)  # command
    if islist:
        return arguments
    else:
        return ' '.join(arguments)


def arg_types(arguments: Union[list, tuple, set], repr=False):
    """Splits arguments into strings, floats or integers."""
    arg_with_types = {0: [], 1: [], 2: []}
    for x in arguments:
        x = str(x)
        # if one dot and string without dots is numeric = float
        if x.count('.') == 1 and x.replace('.', '').isnumeric():
            arg_with_types[0].append(x)
        elif x.isnumeric():
            arg_with_types[1].append(x)
        else:
            arg_with_types[2].append(x)
    if not repr:
        return arg_with_types
    else:
        return f"{{\n  Strings: `{arg_with_types.get(2)}`\n  Integers: `{arg_with_types.get(1)}`\n  Floats: `{arg_with_types.get(0)}`\n}}"


def smoothen(message: Iterable):
    """
    Receives an iterable and encases it into a neat box.
    - Made to deal specifically with strings, lists, tuples, sets and dictionaries.
    - For dictionaries, only the values, cast to strings, will be "boxed".
    """
    if isinstance(message, Union[list, tuple, set].__args__):
        message = tuple([str(x) for x in message])
        dashes = len(max(message, key=len))
    elif isinstance(message, dict):
        message = [str(x) for x in message.values()]
        dashes = len(max(message, key=len))
    else:
        message = str(message)
        dashes = len(message)
    dashes += 2

    formatted_message = f'\n+{"-" * dashes}+\n'
    if isinstance(message, str):
        formatted_message += f'| {message} |\n'
    else:
        for string in message:
            if string == len(string) * '-':
                formatted_message += '|' + '-'.ljust(dashes, '-') + '|\n'
            else:
                formatted_message += '| ' + string.ljust(dashes - 2) + ' |\n'

    formatted_message += f'+{"-" * dashes}+\n'
    return formatted_message
