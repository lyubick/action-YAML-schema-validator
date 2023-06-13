import json
import os.path
import sys

import yaml
from jsonschema import validate

if __name__ == '__main__':
    args = sys.argv[1:]

    schema_file = args[0]

    if os.path.exists(schema_file):
        if os.path.isfile(schema_file):
            with open(args[0], 'r') as stream:
                schema = json.loads("".join(stream.readlines()))
        else:
            raise f'Provided file `{schema_file}` is not a file! Please provide legit JSON Schema file.'
    else:
        raise f'Provided file `{schema_file}` does not exist!'

    yaml_file = args[1]

    if os.path.exists(schema_file):
        if os.path.isfile(schema_file):
            with open(yaml_file, 'r') as stream:
                json = json.loads(json.dumps(yaml.safe_load(stream)))
            validate(instance=json, schema=schema)
        else:
            raise f'Provided `{yaml_file}` is not a file! Please provide legit YAML file.'
    else:
        raise f'Provided `{yaml_file}` does not exist!'
