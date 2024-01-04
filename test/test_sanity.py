import json
from pathlib import Path

import validator


class Test:
    abs_path = Path(__file__).parent

    def test1_load_schema(self):
        schemas = validator.get_all_schemas(
            schema_file_path='',
            default_schema_path=f'{self.abs_path}/schema/json_schema.json'
        )
        assert len(schemas.keys()) == 1
        assert list(schemas.values())[0]['title'] == 'TestConfig'
        assert list(schemas.values())[0]['description'] == 'Test Basic YAML File'

    def test2_get_files(self):
        files = validator.get_testing_filenames(f'{self.abs_path}/YAMLs', is_recursive=True)
        assert len(files) == 2

    def test3_validate_valid_file(self):
        schemas = validator.get_all_schemas(
            schema_file_path='',
            default_schema_path=f'{self.abs_path}/schema/json_schema.json'
        )
        files = validator.get_testing_filenames(f'{self.abs_path}/YAMLs/valid.yaml', False)
        files_schemas = validator.get_filenames_with_schema(files, schemas, None)
        assert validator.validate_files(files_schemas)

    def test4_validate_invalid_file(self):
        schemas = validator.get_all_schemas(
            schema_file_path='',
            default_schema_path=f'{self.abs_path}/schema/json_schema.json'
        )
        files = validator.get_testing_filenames(f'{self.abs_path}/YAMLs/invalid.yaml', False)
        files_schemas = validator.get_filenames_with_schema(files, schemas, None)
        try:
            validator.validate_files(files_schemas)
            assert False
        except Exception as exc:
            assert len(exc.args) == 1
            assert len(exc.args[0]) == 1
            assert exc.args[0][0][1] == {'field2': 'Value2'}

    def test5_validate_valid_file_json(self):
        schemas = validator.get_all_schemas(
            schema_file_path='',
            default_schema_path=f'{self.abs_path}/schema/json_schema.json'
        )
        files = validator.get_testing_filenames(f'{self.abs_path}/JSONs/valid.json', False)
        files_schemas = validator.get_filenames_with_schema(files, schemas, None)
        assert validator.validate_files(files_schemas)

    def test6_validate_invalid_file_json(self):
        schemas = validator.get_all_schemas(
            schema_file_path='',
            default_schema_path=f'{self.abs_path}/schema/json_schema.json'
        )
        files = validator.get_testing_filenames(f'{self.abs_path}/JSONs/invalid1.json', False)
        files_schemas = validator.get_filenames_with_schema(files, schemas, None)
        try:
            validator.validate_files(files_schemas)
            assert False
        except Exception as exc:
            assert len(exc.args) == 1
            assert len(exc.args[0]) == 1
            assert exc.args[0][0][1] == {'field2': 'Value2'}

    def test7_validate_folder_yaml(self):
        schemas = validator.get_all_schemas(
            schema_file_path='',
            default_schema_path=f'{self.abs_path}/schema/json_schema.json'
        )
        files = validator.get_testing_filenames(f'{self.abs_path}/YAMLs/', False)
        files_schemas = validator.get_filenames_with_schema(files, schemas, None)
        try:
            validator.validate_files(files_schemas)
            assert False
        except Exception as exc:
            assert len(exc.args) == 1
            assert len(exc.args[0]) == 1
            assert exc.args[0][0][1] == {'field2': 'Value2'}

    def test8_validate_folder_json(self):
        schemas = validator.get_all_schemas(
            schema_file_path='',
            default_schema_path=f'{self.abs_path}/schema/json_schema.json'
        )
        files = validator.get_testing_filenames(f'{self.abs_path}/JSONs/', False)
        files_schemas = validator.get_filenames_with_schema(files, schemas, None)
        try:
            validator.validate_files(files_schemas)
            assert False
        except Exception as exc:
            assert len(exc.args) == 1
            assert len(exc.args[0]) == 2
            assert exc.args[0][0][1] == {'field2': 'Value2'}
            assert exc.args[0][1][1] == {'field2': 'Value2_2'}

    def test9_validate_empty_json(self):
        schemas = validator.get_all_schemas(
            schema_file_path='',
            default_schema_path=f'{self.abs_path}/schema/json_schema.json'
        )
        files = validator.get_testing_filenames(f'{self.abs_path}/emptyJSONs/empty.json', False, True)
        files_schemas = validator.get_filenames_with_schema(files, schemas, None)
        validator.validate_files(files_schemas)

    def test9_validate_empty_json_fail(self):
        schemas = validator.get_all_schemas(
            schema_file_path='',
            default_schema_path=f'{self.abs_path}/schema/json_schema.json'
        )
        files = validator.get_testing_filenames(f'{self.abs_path}/emptyJSONs/empty.json', False, False)
        files_schemas = validator.get_filenames_with_schema(files, schemas, None)
        try:
            validator.validate_files(files_schemas)
            assert False
        except json.JSONDecodeError as exc:
            assert True

    def test10_validate_file_with_schema_map(self):
        schemas = validator.get_all_schemas(
            schema_file_path=f'{self.abs_path}/schema/json_schema.json',
            default_schema_path=f'{self.abs_path}/schema/json_schema.json'
        )
        files = validator.get_testing_filenames(f'{self.abs_path}/emptyJSONs/empty.json', False, False)
        files_schemas = validator.get_filenames_with_schema(
            files,
            schemas,
            f"{self.abs_path}/emptyJSONs/empty.json->{self.abs_path}/schema/json_schema.json"
        )
        try:
            validator.validate_files(files_schemas)
            assert False
        except json.JSONDecodeError as exc:
            assert True

    def test11_validate_http_schema(self):
        schemas = validator.get_all_schemas(
            schema_file_path=f'https://json-schema.org/draft-04/schema',
            default_schema_path=f'https://json-schema.org/draft-04/schema'
        )

        files = validator.get_testing_filenames(f'{self.abs_path}/schema/json_schema.json', False, False)
        files_schemas = validator.get_filenames_with_schema(
            files,
            schemas,
            f"{self.abs_path}/schema/json_schema.json->https://json-schema.org/draft-04/schema"
        )
        validator.validate_files(files_schemas)
        assert True

        files = validator.get_testing_filenames(f'{self.abs_path}/schema/json_schema.json', False, False)
        files_schemas = validator.get_filenames_with_schema(files, schemas, None)
        validator.validate_files(files_schemas)
        assert True

        files = validator.get_testing_filenames(f'{self.abs_path}/schema/json_invalid_schema.json', False, False)
        files_schemas = validator.get_filenames_with_schema(
            files,
            schemas,
            f"{self.abs_path}/schema/json_invalid_schema.json->https://json-schema.org/draft-04/schema"
        )

        try:
            validator.validate_files(files_schemas)
            assert False
        except Exception as exc:
            assert True

        files = validator.get_testing_filenames(f'{self.abs_path}/schema/', False, False)
        files_schemas = validator.get_filenames_with_schema(files, schemas, None)

        try:
            validator.validate_files(files_schemas)
            assert False
        except Exception as exc:
            assert True
