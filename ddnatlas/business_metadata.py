import json
import os

from apache_atlas.client.base_client import AtlasClient

from ddnatlas.anthropic_prompt_data_type import data_type_prompt
from ddnatlas.camel_to_title import camel_to_title
from ddnatlas.claude import process_json_with_claude


def add_business_metadata(supergraph, entities, include, exclude):
    url = os.getenv('ATLAS_URL')
    username = os.getenv('ATLAS_USERNAME')
    password = os.getenv('ATLAS_PASSWORD')

    if include and 'business_metadata' not in include:
        return
    if exclude and 'business_metadata' in exclude:
        return

    api_key = os.getenv('ANTHROPIC_API_KEY')
    if api_key:
        testing_types = process_json_with_claude(
            data_type_prompt
            .replace('{{entities}}', json.dumps(entities))
            .replace('{{supergraph}}', supergraph),
            api_key
        )
    else:
        testing_types = {}

    client = AtlasClient(host=url, auth=(username, password))
    for entity in entities:
        if entity.get('typeName') and entity['attributes'].get('qualifiedName') and entity['attributes'].get(
                'name') and entity.get('typeName') in ["field", "column", "query", "collection", "subgraph",
                                                       "supergraph", "object_type"]:
            qualified_name = entity['attributes']['qualifiedName']
            testing_type = testing_types.get(qualified_name)
            technical_name = entity['attributes']['name']
            business_name = camel_to_title(technical_name.replace('_', ' '))
            result = client.discovery.attribute_search(type_name='Asset', attr_name='qualifiedName',
                                                       attr_value_prefix=qualified_name, limit=1, offset=0)
            guid = result['entities'][0]['guid']
            if guid:
                full_entity = client.entity.get_entity_by_guid(guid=guid)
                business_attributes = full_entity['entity'].get('businessAttributes', {})
                data_analysis = business_attributes.get('data_analysis', {})
                business_names = data_analysis.get('businessNames', [])
                business_names.append(business_name)
                business_names = list(set(business_names))
                data_analysis["testingType"] = data_analysis.get('testingType', testing_type)
                data_analysis["businessNames"] = business_names
                business_attributes['data_analysis'] = data_analysis

                try:
                    client.entity.add_or_update_business_attributes(entity_guid=guid, is_overwrite=True,
                                                                    business_attributes=business_attributes)
                except Exception as e:
                    pass
