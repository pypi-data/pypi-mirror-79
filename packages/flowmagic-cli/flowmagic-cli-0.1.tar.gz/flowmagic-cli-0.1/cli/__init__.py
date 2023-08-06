import click
import os
import shutil
from pathlib import Path
import json
from .utils import slugify, read_config_json
import requests
import configparser
import tempfile
import zipfile

file_dir_path = Path(os.path.dirname(os.path.realpath(__file__)))

current_dir = Path(os.getcwd())
config_overrides_file = '.config'
CONF_PREFIX = 'FMV1_CONF_'
MOCK_INPUT_DIR = '.inputs'
MOCK_OUTPUT_DIR = '.outputs'
APP_NAME = 'flowmagic-cli'
config_file = Path(click.get_app_dir(APP_NAME), 'config.ini')
config_file.parent.mkdir(exist_ok=True)


def validate_ui_port(value):
    if 5000 <= value <= 6000:
        return value
    else:
        raise click.BadParameter("Ui port needs to be between 5000-6000")


def store_token(endpoint, token, profile='default'):
    config = configparser.ConfigParser()

    if config_file.exists():
        config.read(config_file)

    config[profile] = {}
    config[profile]['endpoint'] = endpoint
    config[profile]['token'] = token
    with open(config_file, 'w+') as configfile:
        config.write(configfile)


def fetch_config(profile='default'):
    if config_file.exists():
        config = configparser.ConfigParser()
        config.read(config_file)
        return config[profile]
    else:
        raise click.ClickException("Token not found. Please login.")


@click.group(invoke_without_command=False)
@click.pass_context
def flowmagic(ctx):
    pass


@flowmagic.command(name='new')
@click.option('--ui', is_flag=True, help="Create new ui app")
@click.pass_context
def new_app(ctx, ui):
    """Creates new app"""
    cwd = Path(os.getcwd())

    name = click.prompt("App name", type=str)
    description = click.prompt("Description", type=str)
    dest_dir_path = Path(slugify(name))

    with open(file_dir_path / 'data/config.json') as f:
        config = json.load(f)
        config['name'] = name
        config['description'] = description

        if ui:
            port = click.prompt("UI port", default=5000, type=int)
            port = validate_ui_port(port)
            config['port'] = port
        else:
            del config['type']
            del config['port']

    dest_dir_path.mkdir(exist_ok=True)
    with open(dest_dir_path / 'config.json', 'wt') as f:
        json.dump(config, f, indent=4)

    shutil.copy2(file_dir_path / 'data/Dockerfile', dest_dir_path)
    shutil.copy2(file_dir_path / 'data/.gitignore', dest_dir_path)

    click.echo(f"Created new app in '{dest_dir_path}'")


@flowmagic.command(name='run', context_settings=dict(allow_extra_args=True, ignore_unknown_options=True))
@click.option('-envs', '--only-envs', is_flag=True, help="Prints only required environment variables")
@click.argument('cmd', nargs=-1)
@click.pass_context
def run_app(ctx, only_envs, cmd):
    """Runs the app with the required environment variables set

        CMD: The command to run after setting the environment variables (e.g. python app.py)
    """
    config_json = read_config_json(current_dir / 'config.json')

    configs = {}

    # Collect default config
    for config in config_json['config_required']:
        value = config.get('value')
        if value:
            configs[config['name']] = value

    # Collect config overrides
    overrides_file = current_dir / config_overrides_file
    if overrides_file.exists():
        with overrides_file.open() as f:
            current_line = f.readline()
            while current_line:
                key_value = current_line.split('=', 1)
                if len(key_value) != 2:
                    raise click.ClickException(f"Invalid config override format, {current_line}")
                key, value = key_value
                configs[key.strip()] = value.strip()
                current_line = f.readline()

    # Set environment variables
    for key, value in configs.items():
        os.environ[key] = value

    # Set mock inputs, outputs
    mock_inputs_dir = Path(current_dir, MOCK_INPUT_DIR)
    mock_outputs_dir = Path(current_dir, MOCK_OUTPUT_DIR)
    if not (mock_inputs_dir.exists() and mock_outputs_dir.exists()):
        create_mock_dirs.invoke(ctx)

    fmv1_inputs, fmv1_outputs = {}, {}

    for input_dir in mock_inputs_dir.iterdir():
        if input_dir.is_dir():
            fmv1_inputs[input_dir.stem] = str(input_dir)

    for output_dir in mock_outputs_dir.iterdir():
        if output_dir.is_dir():
            fmv1_outputs[output_dir.stem] = str(output_dir)

    envs = {}
    # Set environment variables
    for key, value in configs.items():
        envs[key] = value
        envs[f"{CONF_PREFIX}{key}"] = value

    envs["fmv1_inputs"] = json.dumps(fmv1_inputs)
    envs["fmv1_outputs"] = json.dumps(fmv1_outputs)

    if only_envs or not cmd:
        for key, value in envs.items():
            click.echo(f"{key}={value}")
    else:
        os.environ.update(envs)
        os.system(' '.join(cmd))


@flowmagic.command(name='create-mock-dirs', context_settings=dict(allow_extra_args=True))
@click.pass_context
def create_mock_dirs(ctx):
    """Creates mock input and output directories for running on local system"""
    config_json = read_config_json(current_dir / 'config.json')
    click.echo("Creating mock directories for inputs and outputs")

    base_input_dir = Path(current_dir, MOCK_INPUT_DIR)
    base_input_dir.mkdir(parents=True, exist_ok=True)
    for input in config_json['inputs']:
        input_name = input['name']
        input_label = input['label']
        dir = Path(base_input_dir, input_name)
        click.echo(f"Creating input dir {input_label} -> {dir}")
        dir.mkdir(parents=True, exist_ok=True)

    base_output_dir = Path(current_dir, MOCK_OUTPUT_DIR)
    base_output_dir.mkdir(parents=True, exist_ok=True)
    for output in config_json['outputs']:
        output_name = output['name']
        output_label = output['label']
        dir = Path(base_output_dir, output_name)
        click.echo(f"Creating output dir {output_label} -> {dir}")
        dir.mkdir(parents=True, exist_ok=True)


@flowmagic.command(name='login')
@click.option('--endpoint', default='https://dev2.flowmagic.io', prompt=True)
@click.option('--username', prompt=True)
@click.option('--password', prompt=True, hide_input=True)
def login(endpoint, username, password):
    """Login on the platform"""
    if endpoint.endswith('/'):
        endpoint = endpoint[:-1]
    try:
        payload = {'username': username, 'password': password}
        resp = requests.post("{}/api/account/token/".format(endpoint), json=payload)
        resp.raise_for_status()
        resp_json = resp.json()
        try:
            access_token = resp_json['access']
        except KeyError:
            raise click.ClickException("Invalid api response. Please contact system administrator.")
        store_token(endpoint=endpoint, token=access_token)
        click.echo("Successfully logged in")
    except requests.HTTPError as e:
        if e.response.status_code == 401:
            click.echo("Invalid username or password")
        else:
            raise click.ClickException(e)
    except requests.RequestException as e:
        raise click.ClickException(e)


@flowmagic.command(name='upload')
@click.pass_context
def upload(ctx):
    """Upload the app"""
    exclude = ['.git', MOCK_INPUT_DIR, MOCK_OUTPUT_DIR, config_overrides_file]
    files = [file for file in current_dir.rglob('*') if not any(file.name.startswith(e) for e in exclude)]

    ctx.invoke(validate_app)

    config = fetch_config()
    token, endpoint = config['token'], config['endpoint']
    headers = {'Authorization': 'Bearer {}'.format(token)}

    with tempfile.NamedTemporaryFile(suffix='.zip') as temp_f:
        with zipfile.ZipFile(temp_f, mode='w') as zf:
            with click.progressbar(files, label='Creating zip') as bar:
                for file in bar:
                    zf.write(file, arcname=file.relative_to(current_dir))
        try:
            files = {'file': ('file', open(temp_f.name, 'rb'), 'application/zip')}
            click.echo("Uploading app...")
            resp = requests.post("{}/api/apps/".format(endpoint), files=files, headers=headers)
            resp.raise_for_status()
            click.echo("App uploaded successfully")
        except requests.HTTPError as e:
            click.echo("App upload error:")
            if e.response.status_code == 422:
                try:
                    errors_json = e.response.json()
                    errors = errors_json['errors']
                    for error in errors:
                        click.echo(" • {}".format(error['message']))
                except Exception:
                    raise click.ClickException(e)
            if e.response.status_code == 401:
                raise click.ClickException("Invalid or expired token. Please login again.")
        except requests.RequestException as e:
            raise click.ClickException(e)


@flowmagic.command(name='validate')
@click.pass_context
def validate_app(ctx):
    """Validates app configuration (config.json)"""
    config = read_config_json(current_dir / 'config.json')

    errors = []

    if not isinstance(config['version'], str):
        errors.append('Version must be a string. Hint: Quote ("1.2") the version number.')

    if not (current_dir / 'Dockerfile').exists():
        errors.append('Dockerfile is not found')

    if config.get('trainable', False):
        for model in config.get('models', []):
            model_name = model['name']
            model_path = model['path']
            sample = model['sample']
            model_dockerfile = model['dockerfile']

            if not (current_dir / model_path).exists():
                errors.append(f"Model path {model_path} is not found")

            if not (current_dir / sample).exists():
                errors.append(f"Model sample file {sample} is not found")

            if not (current_dir / model_dockerfile).exists():
                errors.append(f"Model dockerfile {model_dockerfile} is not found")

    if errors:
        msg = "App validation failed "
        for error_msg in errors:
            msg += "\n" + " • {}".format(error_msg)
        raise click.ClickException(msg)


@flowmagic.command(name='build-logs')
@click.pass_context
def build_logs(ctx):
    """Fetches and displays the latest build log"""
    config = read_config_json(current_dir / 'config.json')
    payload = {'name': config['name'], 'version': config['version']}

    config = fetch_config()
    token, endpoint = config['token'], config['endpoint']
    headers = {'Authorization': 'Bearer {}'.format(token)}

    try:
        resp = requests.get('{}/api/apps/build-logs/'.format(endpoint), json=payload, headers=headers)
        resp.raise_for_status()
        resp_json = resp.json()

        click.echo("App name: {}".format(resp_json['name']))
        click.echo("Version: {}".format(resp_json['version']))
        click.echo("Build Status: {}".format(resp_json['build_status']))
        click.echo("Log:")
        click.echo(resp_json['log'])
    except requests.HTTPError as e:
        if e.response.status_code == 404:
            raise click.ClickException("Unable to find app. Make sure you have uploaded the app.")
        else:
            raise click.ClickException(e)
    except requests.RequestException as e:
        raise click.ClickException(e)


