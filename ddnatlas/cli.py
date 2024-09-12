import json
import logging
import os
import click
from pyfiglet import Figlet
from dotenv import load_dotenv
from importlib.metadata import version, PackageNotFoundError
from ddnatlas.get_entities import get_entities
from ddnatlas.supergraph_atlas_types import generate_supergraph_types
from ddnatlas.update import update_supergraph_metadata

def get_version(package_name):
    try:
        return version(package_name)
    except PackageNotFoundError:
        return "Package not found"

# setting up logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s",
                    handlers=[
                        logging.FileHandler("../debug.log"),
                        logging.StreamHandler()
                    ])
atlas_logger = logging.getLogger('apache_atlas')
atlas_logger.setLevel(logging.DEBUG)

# Load .env file if it exists
load_dotenv()


def generate_banner(text="DDN ATLAS", font="slant"):
    f = Figlet(font=font)
    return f.renderText(text)


class BannerGroup(click.Group):
    def __call__(self, *args, **kwargs):
        click.echo(generate_banner())
        return super().__call__(*args, **kwargs)


def update_env(_ctx, param, value):
    if value is not None:
        os.environ[param.name.upper()] = value
    return value


def display_configuration():
    click.echo("Current configuration:")
    for key in ['ATLAS_URL', 'SUPERGRAPH', 'ATLAS_USERNAME', 'ATLAS_PASSWORD',
                'ANTHROPIC_API_KEY', 'ANTHROPIC_URI', 'ANTHROPIC_VERSION']:
        value = os.environ.get(key, "Not defined")
        if key in ['ATLAS_PASSWORD', 'ANTHROPIC_API_KEY']:
            value = '********' if value != "Not defined" else value
        click.echo(f"{key}: {value}")


@click.group(cls=BannerGroup)
@click.version_option(version=get_version("DdnAtlas"))
@click.option('--atlas-url', required=True, envvar='ATLAS_URL', callback=update_env,
              help='Atlas URL (required if ATLAS_URL env var is not set)')
@click.option('--supergraph', required=True, envvar='SUPERGRAPH', callback=update_env,
              help='Supergraph identifier (required if SUPERGRAPH env var is not set)')
@click.option('--atlas-username', default='admin', envvar='ATLAS_USERNAME', callback=update_env,
              show_default='admin or ATLAS_USERNAME env var', help='Atlas username')
@click.option('--atlas-password', default='admin', envvar='ATLAS_PASSWORD', callback=update_env,
              show_default='admin or ATLAS_PASSWORD env var', help='Atlas password')
@click.option('--anthropic-api-key', envvar='ANTHROPIC_API_KEY', callback=update_env,
              help='Anthropic API Key')
@click.option('--anthropic-uri', default='https://api.anthropic.com', envvar='ANTHROPIC_URI', callback=update_env,
              show_default='https://api.anthropic.com or ANTHROPIC_URI env var', help='Anthropic API URI')
@click.option('--anthropic-version', default='2023-06-01', envvar='ANTHROPIC_VERSION', callback=update_env,
              show_default='2023-06-01 or ANTHROPIC_VERSION env var', help='Anthropic API Version')
def cli(atlas_url, supergraph, atlas_username, atlas_password, anthropic_api_key, anthropic_uri, anthropic_version):
    """
    DDN Atlas CLI - A command-line tool for managing supergraph metadata within Apache Atlas.

    This tool provides commands to initialize configuration, update metadata,
    and download supergraph metadata from Apache Atlas.
    """
    pass


@cli.command()
def init():
    """
    Initialize the configuration for DDN Atlas.

    This command updates Apache Atlas with the supergraph metadata types.
    """
    display_configuration()
    click.echo("Adding supergraph metadata types to Atlas...")
    generate_supergraph_types()


@click.option(
    '--include',
    '-i',
    multiple=True,
    default=None,
    help=('Include specific components in the update. '
          'Options: subgraph, supergraph, entity, relationship, business_metadata, '
          'glossary, data_connector, model, object_type, scalar, descriptions')
)
@click.option(
    '--exclude',
    '-e',
    multiple=True,
    default=None,
    help=('Exclude specific components from the update. '
          'Options: subgraph, supergraph, entity, relationship, business_metadata, '
          'glossary, data_connector, model, object_type, scalar, descriptions')
)
@cli.command()
def update(include, exclude):
    """
    Update the supergraph metadata in Apache Atlas.

    This command allows you to update the supergraph metadata stored in Apache Atlas.
    It uses the configuration settings to connect to Atlas and update the specified
    supergraph's metadata.
    """
    display_configuration()
    click.echo("Updating the supergraph metadata to atlas...")
    include = list(include) if len(include) > 0 else None
    exclude = list(exclude) if len(exclude) > 0 else None
    update_supergraph_metadata(include, exclude)


@cli.command()
@click.option('--output', '-o', help='Output file path')
def dump(output):
    """
    Download the Apache Atlas supergraph metadata.

    This command retrieves the supergraph metadata from Apache Atlas and saves it
    to a file. If no output file is specified, it will display the metadata in the console.
    """
    display_configuration()
    click.echo("Downloading supergraph metadata from Apache Atlas...")
    if output:
        with open(output, 'w') as f:
            json.dump(get_entities(), f, indent=2)
        click.echo(f"Supergraph metadata has been written to {output}")
    else:
        print(json.dumps(get_entities(), indent=2))


