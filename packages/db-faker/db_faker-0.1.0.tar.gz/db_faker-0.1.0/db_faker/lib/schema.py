"""
Utility library for managing the JSON schemas
"""
import json
import db_faker.lib.utils as utils

from jsonschema import validate, ValidationError
from pathlib import Path


class SchemaValidationResult:
    """
    Class that stores the result of a JSON schema validation
    """
    def __init__(self, valid: bool, error_message: str = None):
        self.valid = valid
        self.validation_errors = error_message


def validate_schema(path: Path, json_schema) -> SchemaValidationResult:
    with open(utils.get_file_abs_path(path)) as schema_file:
        schema_to_validate_json = json.load(schema_file)
        try:
            # Validate the desired JSON file against the JSON schema for the database definition
            validate(schema_to_validate_json, json_schema)
            return SchemaValidationResult(True)
        except ValidationError as e:
            return SchemaValidationResult(False, error_message=e.message)
