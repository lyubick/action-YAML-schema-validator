import json
import sys

import yaml
from jsonschema import validate

if __name__ == '__main__':
    args = sys.argv[1:]

    with open(args[0], 'r') as stream:
        schema = json.loads("".join(stream.readlines()))

    with open(args[1], 'r') as stream:
        json = json.loads(json.dumps(yaml.safe_load(stream)))

    validate(instance=json, schema=schema)
