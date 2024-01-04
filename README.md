# YAML/JSON File(s) Validation against JSON Schema

## Overview
This action can validate YAML or JSON files against provided JSON Schema. In case if provided file is in full compliance
with provided JSON Schema, action will exit gracefully, crash (unhandled exception) will occur otherwise.

The JSON Schema format used, should be in compliance with https://json-schema.org/. 

## Usage
To use action one can use code snippet below.
```yaml
jobs:
  my_cool_validation:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Check my YAML/JSON file with my JSON schema
        id: validation
        uses: lyubick/action-YAML-schema-validator@v2
        with:
          json-schema-file: path/to/my/cool/schema.json
          yaml-json-file-dir: path/to/my/cool/yaml/file.yaml,path/to/my/cool/yaml/another/file.yaml
          recursive: false
          ignore-empty: false
          schema-mapping: 'path/to/my/cool/yaml/file.yaml->path/to/my/cool/schema.json,path/to/my/cool/yaml/another/file.yaml->https://path/to/schema'
```
One should provide two parameters:
- `json-schema-file`, required, points to legit JSON Schema files. In case of mapping this schema will be used as default (fallback) schema. Can point to online schemas that can be obtained via http(s), without authorization.
- `yaml-json-file-dir`, is a comma separated list that contains:
  - Single YAML or JSON files
  - Directories that will be parsed for `.yaml` or `.yml` or `.json` files
- `recursive`, optional, True/False depending on if recursive scan for YAML or JSON files in directory required. Default is False.
- `ignore-empty`, optional, True/False depends if one want to cause failure on empty files or not, default is True.
- `schema-mapping`, optional, one can provide file-to-schema mapping, if specific files require specific schema.

## Results
### Success
In case of success action will end gracefully (exit code 0).

### Failure
In case of failure action will end with crash (unhandled exception), like on example below:
```text
File `invalid/yaml/file/here.yaml` failed validation with >>>`failure reason here`<<<

Traceback ...
```

## Examples
### JSON Schema
```json
{
  "title": "SampleJSONSchema",
  "description": "Just a sample and very simple JSON Schema",
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "field1": {
      "type": "string"
    }
  }
}
```

### Valid file (compliant with Schema)
#### YAML
```yaml
field1: Value1
```
#### JSON
```json
{
  "field1": "Value1"
}
```

### Invalid file (not compliant with Schema)
#### YAML
```yaml
field2: Value2
```

#### JSON
```json
{
  "field2": "Value1"
}
```

Validating this file will cause error (Exception) thus failing an action
```text
Failed validating 'additionalProperties' in schema:
    {'additionalProperties': False,
     'description': 'Just a sample and very simple JSON Schema',
     'properties': {'field1': {'type': 'string'}},
     'title': 'SampleJSONSchema',
     'type': 'object'}

On instance:
    {'field2': 'Value2'}
```

## Organisations Use
* [Printify](https://printify.com)
