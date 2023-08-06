import logging
import json
import db_faker.lib.utils as utils

from cliff.command import Command
from db_faker.lib.schema import validate_schema


class ValidateSchema(Command):
    """
    Command that will validate the given JSON file to the JSON schema
    """
    def __init__(self, app, app_args):
        super(ValidateSchema, self).__init__(app, app_args, cmd_name="validate-schema")
        self.log = logging.getLogger(__name__)
        schema_path = utils.get_root_path() / 'schemas' / 'dbSchema.json'
        with open(schema_path) as path:
            self.json_schema = json.load(path)

    def get_parser(self, prog_name):
        parser = super(ValidateSchema, self).get_parser(prog_name)
        parser.add_argument('-s', '--schema', default='./schema.json', metavar='',
                            help='The schema to be used for generating the fake data', type=str)
        return parser

    def take_action(self, parsed_args):
        self.log.debug("Selected schema: %s", parsed_args.schema)

        schema = parsed_args.schema
        schema_file = utils.get_file_abs_path(schema)

        if schema_file.exists():
            vr = validate_schema(schema_file, self.json_schema)
            if vr.valid:
                self.log.info("The schema is valid")
            else:
                self.log.error("The schema passed is not valid")
                self.log.error(vr.validation_errors)
        else:
            self.log.error("The file could not be found")
