glossary_prompt = """
This is an array of Apache Atlas entities: {{entities}}. 

Review all entities and derive a single glossary entry that encompasses the principal topics referenced in the 
entities. Add this into the response as the value of the "glossary" key.

Review all entities and derive a list of relevant terms and relevant categories.

Associate the terms with a category by the category guid and with a glossary by the glossary guid.
Associate the categories with a glossary by the glossary guid.

Add the terms into the response as the value of the "terms" key.

Add the categories into the response as the value of the "categories" key.

Associate the terms with one or more collections, object_types, queries, columns, or fields using an 
AtlasGlossarySemanticAssignment.

Add the term-entity associations into the response as the value of the "relationships" key.

Review field and column entities and assign any relevant data governance classifications, then add those to the 
"classification" entry. The classification entry should be a dictionary of entity qualified names whose value is an 
array of "PII","Confidential","Internal","Public","Restricted".

Use these definitions when considering classification:

Public Data: Information that is freely available to the public and poses no risk if disclosed. Examples include 
press releases and publicly available reports.

Internal Data: Data intended for internal use within the organization. While not highly sensitive, it should still be 
protected to avoid misuse. Examples include internal memos and internal project documents.

Confidential Data: Sensitive information that, if disclosed, could harm the organization or individuals. This data 
requires strict access controls. Examples include employee records, financial data, and proprietary information.

Restricted Data: Highly sensitive data that requires the highest level of protection due to its critical nature. 
Unauthorized access could lead to severe consequences. Examples include trade secrets, classified government 
information, and personal health information (PHI).

Personally Identifiable Information (PII): Data that can be used to identify an individual, either on its own or when 
combined with other information. This includes names, addresses, social security numbers, email addresses, 
and phone numbers. PII requires stringent protection measures to prevent identity theft and ensure privacy.

Enter the classifications into the response as the value of the "classifications": key.

The complete answer must be a JSON dictionary following this format:

{
  "glossary": {
    "guid": "<temporary guid as a unique negative number>",
    "qualifiedName": "<<the name of the glossary in title case without spaces>@{{supergraph_name}}>",
    "name": "<the name of the glossary>",
    "shortDescription": "<a short description of the glossary>",
    "longDescription": "<a longer description of the glossary>",
    "language": "English",
    "usage": "<a short description of when to use this glossary>"
  },
  "categories": [
    {
      "guid": "<temporary guid as a unique negative number>",
      "qualifiedName": "<<the name of the term in category in title case without spaces>@.<glossary name in lower case>.{{supergraph_name}}>",
      "name": "<the category name>",
      "shortDescription": "<a short description of the category>",
      "longDescription": "<a long description of the category>",
      "anchor": {
        "glossaryGuid": "<the guid of the glossary>"
      }
    }
  ],
  "terms": [
    {
      "guid": "<temporary guid as a unique negative number>",
      "qualifiedName": "<<the name of the term in title case without spaces>@.<glossary name in lower case>.{{supergraph_name}}>",
      "name": "<the term>",
      "shortDescription": "<a short description of the term>",
      "longDescription": "<a long description of the term>",
      "examples": [
        "<an array of examples of using the term>"
      ],
      "abbreviation": "<an abbreviation of the term>",
      "usage": "<describe the scenarios where the term might be used>",
      "status": "ACTIVE",
      "anchor": {
        "glossaryGuid": "<the guid of the glossary>"
      },
      "categories": [
        {
          "categoryGuid": "<the category guid associated with the term>"
        }
      ]
    }
  ],
  "relationships": [
    {
      "typeName": "AtlasGlossarySemanticAssignment",
      "end1": {
        "typeName": "AtlasGlossaryTerm",
        "guid": "<glossary_term_guid>"
      },
      "end2": {
        "typeName": "<entity_type_name>",
        "uniqueAttributes": {
          "qualifiedName": "<entity_qualified_name>"
        }
      }
    }
  ],
  "classifications": {
    "<entity qualified name>": [
      "<classification category>"
    ]
  }
}
"""
