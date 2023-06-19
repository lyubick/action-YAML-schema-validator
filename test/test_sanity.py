import validator
import jsonschema


class Test:
    def test1_load_schema(self):
        schema = validator.load_schema('./schema/json_schema.json')
        assert schema['title'] == 'TestConfig'
        assert schema['description'] == 'Test Basic YAML File'

    def test2_get_files(self):
        files = validator.get_yaml_json_files_list('./YAMLs', is_recursive=True)
        assert len(files) == 2

    def test3_validate_valid_file(self):
        schema = validator.load_schema('./schema/json_schema.json')
        files = validator.get_yaml_json_files_list('./YAMLs/yaml_valid.yaml', False)
        assert validator.validate_files(files, schema)

    def test4_validate_invalid_file(self):
        schema = validator.load_schema('./schema/json_schema.json')
        files = validator.get_yaml_json_files_list('./YAMLs/yaml_invalid.yaml', False)
        try:
            validator.validate_files(files, schema)
            assert False
        except jsonschema.exceptions.ValidationError as exc:
            assert exc.instance == {'field2': 'Value2'}

    def test5_validate_valid_file_json(self):
        schema = validator.load_schema('./schema/json_schema.json')
        files = validator.get_yaml_json_files_list('./JSONs/yaml_valid.json', False)
        assert validator.validate_files(files, schema)

    def test6_validate_invalid_file_json(self):
        schema = validator.load_schema('./schema/json_schema.json')
        files = validator.get_yaml_json_files_list('./JSONs/yaml_invalid.json', False)
        try:
            validator.validate_files(files, schema)
            assert False
        except jsonschema.exceptions.ValidationError as exc:
            assert exc.instance == {'field2': 'Value2'}

    def test7_validate_folder_yaml(self):
        schema = validator.load_schema('./schema/json_schema.json')
        files = validator.get_yaml_json_files_list('./YAMLs/', False)
        try:
            validator.validate_files(files, schema)
            assert False
        except jsonschema.exceptions.ValidationError as exc:
            assert exc.instance == {'field2': 'Value2'}

    def test8_validate_folder_json(self):
        schema = validator.load_schema('./schema/json_schema.json')
        files = validator.get_yaml_json_files_list('./JSONs/', False)
        try:
            validator.validate_files(files, schema)
            assert False
        except jsonschema.exceptions.ValidationError as exc:
            assert exc.instance == {'field2': 'Value2'}
