import json
import os.path
import pathlib
import sys

import yaml
from jsonschema import validate
from jsonschema.exceptions import ValidationError


def load_schema(schema_file_path: str) -> json:
    if os.path.exists(schema_file_path):
        if os.path.isfile(schema_file_path):
            with open(schema_file_path, 'r') as stream:
                return json.loads("".join(stream.readlines()))
        else:
            raise f'Provided JSON Schema is not a file! Please provide legit JSON Schema file.'
    else:
        raise f'Provided JSON Schema file does not exist!'


def get_yaml_json_files_list(files_paths_list: str, is_recursive: bool, ignore_empty_files: bool = False) -> list[str]:
    yaml_input = list(files_paths_list.split(','))

    yaml_files = []
    for yaml_object in yaml_input:
        if os.path.isdir(yaml_object):
            yaml_files.extend(
                list(
                    map(
                        lambda f: str(f),  # Convert all paths to string, instead of Posix Path
                        filter(
                            lambda f: str(f).endswith('.yaml') or str(f).endswith('.yml') or str(f).endswith('.json'),
                            pathlib.Path(yaml_object).glob('**/*' if is_recursive else '*')
                        )
                    )
                )
            )
        elif os.path.isfile(yaml_object):
            yaml_files.append(yaml_object)

    if ignore_empty_files:
        yaml_files = list(filter(lambda f: os.path.getsize(f) > 0, yaml_files))

    return yaml_files


def validate_files(yaml_files: list, json_schema: json):
    failed = []
    for yaml_file in yaml_files:
        if os.path.exists(yaml_file):
            if os.path.isfile(yaml_file):
                with open(yaml_file, 'r') as stream:
                    if not yaml_file.endswith('.json'):
                        yaml_json = json.loads(json.dumps(yaml.safe_load(stream)))
                    else:
                        yaml_json = json.load(stream)
                try:
                    validate(instance=yaml_json, schema=json_schema)
                except ValidationError as exc:
                    print(f'File `{yaml_file}` failed validation with >>>`{exc}`<<<', file=sys.stderr)
                    failed.append((yaml_file, exc.instance))
            else:
                raise f'Provided YAML file is not a file! Please provide legit YAML file.'
        else:
            raise f'Provided YAML file does not exist!'

    if failed:
        raise Exception(failed)

    return True


if __name__ == '__main__':
    args = sys.argv[1:]

    schema = load_schema(args[0])
    files = get_yaml_json_files_list(args[1], args[2].lower() == 'true')
    validate_files(files, schema)
