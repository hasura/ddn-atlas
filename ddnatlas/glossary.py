import json
import os

from apache_atlas.model.glossary import AtlasGlossaryTerm, AtlasGlossary, AtlasGlossaryHeader, AtlasGlossaryCategory
from apache_atlas.model.instance import AtlasClassification
from apache_atlas.model.relationship import AtlasRelationship

from ddnatlas.anthropic_prompt import glossary_prompt
from ddnatlas.claude import process_json_with_claude
from apache_atlas.client.base_client import AtlasClient, type_coerce


def create_glossary(supergraph, entities, include=None, exclude=None):

    url = os.getenv('ATLAS_URL')
    username = os.getenv('ATLAS_USERNAME')
    password = os.getenv('ATLAS_PASSWORD')
    api_key = os.getenv('ANTHROPIC_API_KEY')

    if not api_key:
        return
    if include and 'glossary' not in include:
        return
    if exclude and 'glossary' in exclude:
        return

    client = AtlasClient(host=url, auth=(username, password))
    glossary = process_json_with_claude(
        glossary_prompt
        .replace('{{entities}}', json.dumps(entities))
        .replace('{{supergraph}}', supergraph),
        api_key
    )
    glossaries = client.glossary.get_all_glossaries()
    existing_glossary = [item for item in glossaries if
                         item.get('qualifiedName') == glossary['glossary'].get('qualifiedName')]
    if not existing_glossary:
        atlas_glossary = AtlasGlossary(glossary['glossary'])
        new_glossary = client.glossary.create_glossary(glossary=atlas_glossary)
    else:
        new_glossary = existing_glossary[0]

    glossary_guid = new_glossary.get('guid')
    glossary_name = new_glossary.get('name')

    for category in glossary['categories']:
        anchor = AtlasGlossaryHeader({'glossaryGuid': glossary_guid, 'displayText': glossary_name})
        atlas_category = AtlasGlossaryCategory({
            'name': category.get('name'),
            'qualifiedName': category.get('qualifiedName'),
            'shortDescription': category.get('shortDescription'),
            'longDescription': category.get('longDescription'),
            'anchor': anchor})
        try:
            client.glossary.create_glossary_category(atlas_category)
        except Exception:
            pass

    new_glossary = client.glossary.get_glossary_by_guid(glossary_guid=glossary_guid)
    terms = glossary['terms']
    for term in terms:
        for category in term['categories']:
            guid = category['categoryGuid']
            temp_guid = [item for item in glossary['categories'] if item['guid'] == guid]
            if temp_guid:
                name = temp_guid[0]['name']
                new_guid = [item['categoryGuid'] for item in new_glossary['categories'] if item['displayText'] == name]
                if new_guid:
                    anchor = AtlasGlossaryHeader(
                        {'glossaryGuid': glossary_guid, 'displayText': glossary_name})
                    atlas_term = AtlasGlossaryTerm({
                        'name': term.get('name'),
                        'qualifiedName': term.get('qualifiedName'),
                        'shortDescription': term.get('shortDescription'),
                        'longDescription': term.get('longDescription'),
                        'examples': term.get('examples'),
                        'abbreviation': term.get('abbreviation'),
                        'usage': term.get('usage'),
                        'categories': [{'categoryGuid': new_guid[0]}],
                        'anchor': anchor})
                    try:
                        client.glossary.create_glossary_term(atlas_term)
                    except Exception:
                        pass

    new_glossary = client.glossary.get_glossary_ext_info(glossary_guid=glossary_guid)
    relationships = glossary['relationships']
    for qualified_name, data_type in glossary['data_types'].items():
        result = client.discovery.attribute_search(type_name='Asset', attr_name='qualifiedName',
                                                   attr_value_prefix=qualified_name, limit=1, offset=0)
        guid = result['entities'][0]['guid']
        if guid:
            business_metadata = {
                "data_analysis": {
                    "testingType": data_type
                }
            }
            try:
                client.entity.add_or_update_business_attributes(entity_guid=guid, is_overwrite=False,
                                                                business_attributes=business_metadata)
            except Exception:
                pass
    for relationship in relationships:
        temp_guid = relationship['end1']['guid']
        old_name = [item['name'] for item in glossary['terms'] if item['guid'] == temp_guid]
        if old_name:
            old_name = old_name[0]
            new_guid = [item['guid'] for item in new_glossary['termInfo'].values() if item['name'] == old_name]
            if new_guid:
                new_guid = new_guid[0]
                relationship['end1']['guid'] = new_guid
                atlas_relationship = type_coerce(relationship, AtlasRelationship)
                try:
                    client.relationship.create_relationship(relationship=atlas_relationship)
                except Exception:
                    pass

    for qualified_name, classifications in glossary['classifications'].items():
        result = client.discovery.attribute_search(type_name='Asset', attr_name='qualifiedName',
                                                   attr_value_prefix=qualified_name, limit=1, offset=0)
        guid = result['entities'][0]['guid']
        if guid:
            atlas_classification = [AtlasClassification({"typeName": item}) for item in classifications]
            try:
                client.entity.add_classifications_by_guid(guid=guid, classifications=atlas_classification)
            except Exception:
                pass
