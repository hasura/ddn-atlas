from ddnatlas import primitives


def create_fields(supergraph_name, subgraph_name, object_name, object_type, entities):
    field_ids = []
    for field in object_type['definition']['fields']:
        field_name = field['name']
        column_id = ""
        for mapping in object_type['definition']['dataConnectorTypeMapping']:
            elem = mapping['fieldMapping'][field_name]
            column_id = f"{supergraph_name}.{subgraph_name}.{mapping['dataConnectorObjectType']}.{elem['column']['name']}"
        qualified_name = f"{supergraph_name}.{subgraph_name}.{object_name}.{field_name}"
        field_ids.append(qualified_name)
        entities.append({
            "typeName": "field",
            "attributes": {
                "name": field_name,
                "qualifiedName": qualified_name,
                "primitive": primitives.apache_primitives[field['type'].upper().replace('!', '')],
                "column": {
                    "typeName": "column",
                    "uniqueAttributes": {
                        "qualifiedName": column_id
                    },
                }
            }
        })
    return field_ids
