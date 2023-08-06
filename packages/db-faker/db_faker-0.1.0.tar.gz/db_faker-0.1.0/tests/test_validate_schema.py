#!/usr/bin/env python

"""
Unit tests for ValidateSchema command
"""

from db_faker.lib.utils import get_root_path
from db_faker.commands.validate_schema import ValidateSchema
from db_faker.cli import DatabaseFakerApp

app = DatabaseFakerApp()
valid_schema = get_root_path() / 'tests' / 'sample-schema.json'
invalid_schema = get_root_path() / 'tests' / 'sample-invalid-schema.json'


def test_check_json_schema_loads():
    """Checks that the JSON schema is loading"""
    cmd = ValidateSchema(app, [])
    schema = cmd.json_schema
    assert schema is not None


def test_valid_schema():
    """Checks that the command is able to validate valid schemas"""
    cmd = ValidateSchema(app, ["-s", str(valid_schema)])
    parser = cmd.get_parser("validate-schema")
    cmd.take_action(parser.parse_args(cmd.app_args))
