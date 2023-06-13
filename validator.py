import json
import os.path
import sys

import yaml
from jsonschema import validate
from jsonschema.exceptions import ValidationError

if __name__ == '__main__':
    args = sys.argv[1:]

    schema_file = args[0]

    if os.path.exists(schema_file):
        if os.path.isfile(schema_file):
            with open(args[0], 'r') as stream:
                schema = json.loads("".join(stream.readlines()))
        else:
            raise f'Provided JSON Schema is not a file! Please provide legit JSON Schema file.'
    else:
        raise f'Provided JSON Schema file does not exist!'

    yaml_input = list(args[1].split(','))

    yaml_files = []
    for yaml_object in yaml_input:
        if os.path.isdir(yaml_object):
            yaml_files.extend(
                list(
                    map(
                        lambda f: yaml_object + ('/' if not yaml_object.endswith('/') else '') + f,
                        filter(
                            lambda f: str(f).endswith('.yaml') or str(f).endswith('.yml'),
                            os.listdir(yaml_object)
                        )
                    )
                )
            )
        elif os.path.isfile(yaml_object):
            yaml_files.append(yaml_object)

    for yaml_file in yaml_files:
        if os.path.exists(yaml_file):
            if os.path.isfile(yaml_file):
                with open(yaml_file, 'r') as stream:
                    yaml_json = json.loads(json.dumps(yaml.safe_load(stream)))
                try:
                    validate(instance=yaml_json, schema=schema)
                except ValidationError as exc:
                    print(f'File `{yaml_file}` failed validation with >>>`{exc}`<<<', file=sys.stderr)
                    raise exc
            else:
                raise f'Provided YAML file is not a file! Please provide legit YAML file.'
        else:
            raise f'Provided YAML file does not exist!'
