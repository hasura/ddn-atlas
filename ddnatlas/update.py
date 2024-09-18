import logging
from ddnatlas.business_metadata import add_business_metadata
from ddnatlas.descriptions import add_descriptions
from ddnatlas.generate_subgraph import generate_subgraph
from ddnatlas.glossary import create_glossary
from ddnatlas.parse_files import parse_files
from ddnatlas.relationships import create_relationships
from ddnatlas.update_entities import update_entities
import os
from typing import List, Optional


def update_supergraph_metadata(include: Optional[List[str]], exclude: Optional[List[str]]):

    supergraph_directory = os.getenv('SUPERGRAPH')

    logging.info("Parsing supergraph configuration files...")
    parsed_data = parse_files(supergraph_directory)

    logging.info("Filtering parsed data...")
    parsed_data = [item for item in parsed_data if isinstance(item, dict) and item.get('kind') is not None]

    logging.info("Generating supergraph object...")
    supergraph = [item for item in parsed_data if item.get('kind') == 'Supergraph'][0]

    logging.info("Generating subgraph names...")
    subgraph_names = [item.split('/')[0] for item in supergraph['definition']['subgraphs'] if
                      not item.startswith("globals/")]

    logging.info("Generating subgraph objects...")
    subgraphs = [item for item in parsed_data if
                 item.get('kind') == 'Subgraph' and item['definition']['name'] in subgraph_names]

    logging.info("Generating object types objects...")
    object_types = [item for item in parsed_data if item.get('kind') == 'ObjectType']

    logging.info("Generating data connector links objects...")
    data_connector_links = [item for item in parsed_data if item.get('kind') == 'DataConnectorLink']

    logging.info("Generating data connector objects...")
    data_connectors = [item for item in parsed_data if item.get('kind') == 'Connector']

    logging.info("Generating model objects...")
    models = [item for item in parsed_data if item.get('kind') == 'Model']

    logging.info("Generating relationship objects...")
    relationships = [item for item in parsed_data if item.get('kind') == 'Relationship']

    all_entities = [
        {
            "typeName": "transform",
            "attributes": {
                "name": "straight_through",
                "qualifiedName": f"{supergraph['definition'].get('name', 'enterprise')}.straight_through",
                "transformation": "NONE",
                "explanation": "No intentional logic was invoked to modify this value. Platforms may have "
                               "serialization and deserialization methods that are inherently invoked and may alter"
                               "the value."
            }
        }
    ]
    update_entities(all_entities, include, exclude)

    logging.info("Analyzing subgraphs...")
    for subgraph in subgraphs:
        all_entities.extend(
            generate_subgraph(supergraph, subgraph, data_connectors, data_connector_links, object_types, models,
                              include, exclude))

    subgraph_ids = [item['attributes']['qualifiedName'] for item in all_entities if item['typeName'] == 'subgraph']

    logging.info("Adding supergraph...")
    supergraph_entity = [{
        "typeName": "supergraph",
        "attributes": {
            "name": "enterprise",
            "console_url": "",
            "grpc_service_url": "",
            "openapi_ui_url": "",
            "openapi_service_url": "",
            "graphql_service_url": "http://localhost:3000/graphql",
            "qualifiedName": "enterprise",
            "description": "The enterprise supergraph.",
            "domains": [{"typeName": "subgraph", "uniqueAttributes": {"qualifiedName": item}} for item in
                        subgraph_ids]
        }
    }]
    entities = all_entities + supergraph_entity
    supergraph_name = supergraph['definition'].get('name', 'enterprise')

    try:
        remove_entities = add_descriptions(entities, include, exclude)
        logging.info("Updating entities..")
        update_entities(entities, include, exclude, force_updates=remove_entities)
    except Exception as e:
        logging.error(e)

    logging.info("Adding business metadata")
    try:
        add_business_metadata(supergraph_name, entities, include, exclude)
    except Exception as e:
        logging.error(e)

    logging.info("Adding business glossary")
    try:
        create_glossary(supergraph_name, entities, include, exclude)
    except Exception as e:
        logging.error(e)

    logging.info("Creating relationships..")
    try:
        create_relationships(relationships, object_types, entities)
    except Exception as e:
        logging.error(e)

    logging.info("Success!")
