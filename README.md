# Hasura DDN to Apache Atlas

This will convert a supergraph into an Apache Atlas data dictionary.

It adds several new types to Atlas including, supergraph, subgraph, query, object_type, data_connector, collection, column and field. 

* It will create lineage between the data_connectors collections and the subgraph object types.

* It will add many relationships to help understand and navigate the components.

* It will add a business name for each element by defaulting to a Title case version of the element's physical name.

* It will create a glossary with categories and terms and associate them with the technical metadata elements, using Anthropic (as a starter to get a glossary off the ground)

* It will derive technical metadata descriptions, if they don't already exist, using Anthropic.
* It will add a data steward business data to the subgraph

There are many flags and features you can use to focus updates to specific technical metadata element types.

To get started - just run `ddnatlas init` to initialize your instance of Apache Atlas with the supergraph types.

Follow up with `ddnatlas update` to add an existing supergraph to Atlas.

## General Instructions

```text
    ____  ____  _   __   ___  ________    ___   _____
   / __ \/ __ \/ | / /  /   |/_  __/ /   /   | / ___/
  / / / / / / /  |/ /  / /| | / / / /   / /| | \__ \ 
 / /_/ / /_/ / /|  /  / ___ |/ / / /___/ ___ |___/ / 
/_____/_____/_/ |_/  /_/  |_/_/ /_____/_/  |_/____/  
                                                     

Usage: ddnatlas [OPTIONS] COMMAND [ARGS]...

  DDN Atlas CLI - A command-line tool for managing supergraph metadata within
  Apache Atlas.

  This tool provides commands to initialize configuration, update metadata,
  and download supergraph metadata from Apache Atlas.

Options:
  --version                 Show the version and exit.
  --atlas-url TEXT          Atlas URL (required if ATLAS_URL env var is not
                            set)  [required]
  --supergraph TEXT         Supergraph identifier (required if SUPERGRAPH env
                            var is not set)  [required]
  --atlas-username TEXT     Atlas username  [default: (admin or ATLAS_USERNAME
                            env var)]
  --atlas-password TEXT     Atlas password  [default: (admin or ATLAS_PASSWORD
                            env var)]
  --anthropic-api-key TEXT  Anthropic API Key
  --anthropic-uri TEXT      Anthropic API URI  [default:
                            (https://api.anthropic.com or ANTHROPIC_URI env
                            var)]
  --anthropic-version TEXT  Anthropic API Version  [default: (2023-06-01 or
                            ANTHROPIC_VERSION env var)]
  --help                    Show this message and exit.

Commands:
  dump    Download the Apache Atlas supergraph metadata.
  init    Initialize the configuration for DDN Atlas.
  update  Update the supergraph metadata in Apache Atlas.

```

## Update Instructions

```text
    ____  ____  _   __   ___  ________    ___   _____
   / __ \/ __ \/ | / /  /   |/_  __/ /   /   | / ___/
  / / / / / / /  |/ /  / /| | / / / /   / /| | \__ \ 
 / /_/ / /_/ / /|  /  / ___ |/ / / /___/ ___ |___/ / 
/_____/_____/_/ |_/  /_/  |_/_/ /_____/_/  |_/____/  
                                                     

Usage: ddnatlas update [OPTIONS]

  Update the supergraph metadata in Apache Atlas.

  This command allows you to update the supergraph metadata stored in Apache
  Atlas. It uses the configuration settings to connect to Atlas and update the
  specified supergraph's metadata.

Options:
  -e, --exclude TEXT  Exclude specific components from the update. Options:
                      subgraph, supergraph, entity, relationship,
                      business_metadata, glossary, data_connector, model,
                      object_type, scalar, descriptions
  -i, --include TEXT  Include specific components in the update. Options:
                      subgraph, supergraph, entity, relationship,
                      business_metadata, glossary, data_connector, model,
                      object_type, scalar, descriptions
  --help              Show this message and exit.

```

## Build from Source Instructions

### Install build tools

`pip install poetry twine`

### Set Up a Virtual Environment:

It’s a good practice to use a virtual environment to manage your project’s dependencies. You can create one using the following command:

`python -m venv myenv`

#### Activate the virtual environment:

##### On Windows:
`myenv\Scripts\activate`

##### On macOS and Linux:
`source myenv/bin/activate`

### Install requirements

`pip install -r requirements.txt`

### Build ddn-atlas CLI
`pip install .`

### Test CLI

`ddnatlas --version`

Should return:

```text
    ____  ____  _   __   ___  ________    ___   _____
   / __ \/ __ \/ | / /  /   |/_  __/ /   /   | / ___/
  / / / / / / /  |/ /  / /| | / / / /   / /| | \__ \ 
 / /_/ / /_/ / /|  /  / ___ |/ / / /___/ ___ |___/ / 
/_____/_____/_/ |_/  /_/  |_/_/ /_____/_/  |_/____/  
                                                     

ddnatlas, version 1.0.0

```
