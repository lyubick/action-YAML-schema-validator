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
          yaml-json-file-dir: path/to/my/cool/yaml/file.yaml
          recursive: false
```
One should provide two parameters:
- `json-schema-file`, points to legit JSON Schema file
- `yaml-json-file-dir`, is a comma separated list that contains
  - Single YAML or JSON files
  - Directories that will be parsed for `.yaml` or `.yml` or `.json` files
- `recursive`, True/False depending on if recursive scan for YAML or JSON files in directory required

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

## Supported & Used by
* [Printify](https://github.com/printify)
