import json
from pathlib import Path

import validator
import jsonschema


class Test:
    abs_path = Path(__file__).parent

    def test1_load_schema(self):
        schema = validator.load_schema(f'{self.abs_path}/schema/json_schema.json')
        assert schema['title'] == 'TestConfig'
        assert schema['description'] == 'Test Basic YAML File'

    def test2_get_files(self):
        files = validator.get_yaml_json_files_list(f'{self.abs_path}/YAMLs', is_recursive=True)
        assert len(files) == 2

    def test3_validate_valid_file(self):
        schema = validator.load_schema(f'{self.abs_path}/schema/json_schema.json')
        files = validator.get_yaml_json_files_list(f'{self.abs_path}/YAMLs/valid.yaml', False)
        assert validator.validate_files(files, schema)

    def test4_validate_invalid_file(self):
        schema = validator.load_schema(f'{self.abs_path}/schema/json_schema.json')
        files = validator.get_yaml_json_files_list(f'{self.abs_path}/YAMLs/invalid.yaml', False)
        try:
            validator.validate_files(files, schema)
            assert False
        except Exception as exc:
            assert len(exc.args) == 1
            assert len(exc.args[0]) == 1
            assert exc.args[0][0][1] == {'field2': 'Value2'}

    def test5_validate_valid_file_json(self):
        schema = validator.load_schema(f'{self.abs_path}/schema/json_schema.json')
        files = validator.get_yaml_json_files_list(f'{self.abs_path}/JSONs/valid.json', False)
        assert validator.validate_files(files, schema)

    def test6_validate_invalid_file_json(self):
        schema = validator.load_schema(f'{self.abs_path}/schema/json_schema.json')
        files = validator.get_yaml_json_files_list(f'{self.abs_path}/JSONs/invalid.json', False)
        try:
            validator.validate_files(files, schema)
            assert False
        except Exception as exc:
            assert len(exc.args) == 1
            assert len(exc.args[0]) == 1
            assert exc.args[0][0][1] == {'field2': 'Value2'}

    def test7_validate_folder_yaml(self):
        schema = validator.load_schema(f'{self.abs_path}/schema/json_schema.json')
        files = validator.get_yaml_json_files_list(f'{self.abs_path}/YAMLs/', False)
        try:
            validator.validate_files(files, schema)
            assert False
        except Exception as exc:
            assert len(exc.args) == 1
            assert len(exc.args[0]) == 1
            assert exc.args[0][0][1] == {'field2': 'Value2'}

    def test8_validate_folder_json(self):
        schema = validator.load_schema(f'{self.abs_path}/schema/json_schema.json')
        files = validator.get_yaml_json_files_list(f'{self.abs_path}/JSONs/', False)
        try:
            validator.validate_files(files, schema)
            assert False
        except Exception as exc:
            assert len(exc.args) == 1
            assert len(exc.args[0]) == 2
            assert exc.args[0][1][1] == {'field2': 'Value2'}
            assert exc.args[0][0][1] == {'field2': 'Value2_2'}

    def test9_validate_empty_json(self):
        schema = validator.load_schema(f'{self.abs_path}/schema/json_schema.json')
        files = validator.get_yaml_json_files_list(f'{self.abs_path}/emptyJSONs/empty.json', False, True)
        validator.validate_files(files, schema)

    def test9_validate_empty_json_fail(self):
        schema = validator.load_schema(f'{self.abs_path}/schema/json_schema.json')
        files = validator.get_yaml_json_files_list(f'{self.abs_path}/emptyJSONs/empty.json', False, False)
        try:
            validator.validate_files(files, schema)
            assert False
        except json.JSONDecodeError as exc:
            assert True
