import json
import logging
import os.path
import pathlib
import re
import sys
from typing import List, Tuple, Optional

import yaml
from jsonschema import validate
from jsonschema.exceptions import ValidationError


def get_all_filenames(input_path: str, endings: List[str], is_recursive: bool) -> List[str]:
    paths = list(input_path.split(','))

    regex_endings = f'.*\\.({"|".join(endings)})'

    output_files = []

    for path in paths:
        if os.path.exists(path):
            if os.path.isdir(path):
                output_files.extend(
                    list(
                        map(
                            lambda f: str(f),  # Convert all paths to string, instead of Posix Path
                            filter(
                                lambda f: len(re.findall(regex_endings, str(f))) > 0,
                                pathlib.Path(path).glob('**/*' if is_recursive else '*')
                            )
                        )
                    )
                )
            elif os.path.isfile(path):
                output_files.append(path)
            else:
                continue

    return output_files


def get_all_schemas(schema_file_path: str) -> dict[str, dict]:
    schema_files = get_all_filenames(schema_file_path, endings=['json'], is_recursive=False)
    schemas = list(map(lambda x: (x, json.loads(''.join(open(x, 'r').readlines()))), schema_files))
    return dict(schemas)


def get_testing_filenames(files_paths_list: str, is_recursive: bool, ignore_empty_files: bool = False) -> list[str]:
    yaml_files = get_all_filenames(files_paths_list, endings=['json', 'yaml', 'yml'], is_recursive=is_recursive)

    if ignore_empty_files:
        yaml_files = list(filter(lambda f: os.path.getsize(f) > 0, yaml_files))

    return sorted(yaml_files)


def get_filenames_with_schema(
        test_files: List[str],
        schemas: dict[str, dict],
        mapping_str: Optional[str]) -> List[Tuple[str, dict]]:
    def tuple_split(inp: str, separator: str) -> Tuple[str, str]:
        values = inp.split(separator)
        return values[0], values[1]

    def map_schema(filename: str, schema_map: dict[str, str]) -> Tuple[str, dict]:
        for s in schema_map.keys():
            if filename in get_all_filenames(input_path=s, endings=['yaml', 'json'], is_recursive=True):
                return filename, schemas[schema_map[s]]

        logging.error(f'{filename} does not match any schema!')
        raise 'Schema mapping is invalid - not all files matches schema'

    if mapping_str:
        mapping = dict(list(map(lambda x: tuple_split(x, ':'), list(mapping_str.split(',')))))
        files_schema = list(map(lambda x: map_schema(x, mapping), test_files))
    else:
        files_schema = list(map(lambda x: (x, list(schemas.values())[0]), test_files))

    return files_schema


def validate_files(files_with_schema: List[Tuple[str, dict]]):
    failed = []
    for file_with_schema in files_with_schema:
        yaml_file = file_with_schema[0]
        json_schema = file_with_schema[1]
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

    input_schemas = get_all_schemas(args[0])

    input_files = get_testing_filenames(
        files_paths_list=args[1],
        is_recursive=args[2].lower() == 'true',
        ignore_empty_files=args[3].lower() == 'true'
    )

    input_mapping = args[4]

    input_files_with_schema = get_filenames_with_schema(
        test_files=input_files,
        schemas=input_schemas,
        mapping_str=input_mapping
    )

    validate_files(input_files_with_schema)
