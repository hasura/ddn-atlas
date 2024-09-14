import json
import logging
import os
from apache_atlas.client.base_client import AtlasClient


def generate_supergraph_types():

    atlas_url = os.getenv('ATLAS_URL')
    username = os.getenv('ATLAS_USERNAME')
    password = os.getenv('ATLAS_PASSWORD')

    logging.info('Generating supergraph types')

    client = AtlasClient(atlas_url, (username, password))

    try:
        current_file_dir = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(current_file_dir, 'supergraph_types.json')) as json_file:
            types = json.load(json_file)
            response = client.typedef.create_atlas_typedefs(types)

        logging.info('Request execution completed.')
        print(response)
    except Exception as e:
        logging.info('Request execution completed with errors.')
        logging.error(e)
