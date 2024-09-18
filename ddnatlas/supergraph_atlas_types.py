import json
import logging
import os
from apache_atlas.client.base_client import AtlasClient

from ddnatlas.supergraph_types import supergraph_types


def generate_supergraph_types():

    atlas_url = os.getenv('ATLAS_URL')
    username = os.getenv('ATLAS_USERNAME')
    password = os.getenv('ATLAS_PASSWORD')

    logging.info('Generating supergraph types')

    client = AtlasClient(atlas_url, (username, password))

    try:
        response = client.typedef.create_atlas_typedefs(supergraph_types)
        logging.info('Request execution completed.')
        print(response)
    except Exception as e:
        logging.info('Request execution completed with errors.')
        logging.error(e)
