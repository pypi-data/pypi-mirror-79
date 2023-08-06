import json

import click


def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    https://stackoverflow.com/a/295466
    """
    import re
    value = re.sub('[^\w\s-]', '', value).strip().lower()
    value = re.sub('[-\s]+', '-', value)
    # ...
    return value


def read_config_json(filepath):
    try:
        with click.open_file(filepath) as f:
            return json.load(f)
    except FileNotFoundError:
        raise click.ClickException("Unable to find config.json. To create an app use 'flowmagic new'")
    except json.JSONDecodeError:
        raise click.ClickException("Invalid config.json file")
