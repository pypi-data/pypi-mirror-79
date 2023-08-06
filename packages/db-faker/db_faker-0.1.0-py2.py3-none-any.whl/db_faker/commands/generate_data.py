import logging
import json
import db_faker.lib.utils as utils

from pathlib import Path
from itertools import repeat
from cliff.command import Command
from db_faker.lib.schema import validate_schema
from db_faker.lib.output_handlers import ConsoleHandler, FileHandler
from faker import Faker


def output_param_is_valid(output: str, force: bool) -> bool:
    """
    This method will check if the output parameter is either "console", or a valid file path that does not exists.
    """
    if "console" == output:
        return True
    else:
        return True if force else utils.file_not_exists(output)


class GenerateData(Command):
    """
    Command that will generate the fake data from the schema
    """

    def __init__(self, app, app_args):
        super(GenerateData, self).__init__(app, app_args, cmd_name="generate-data")
        self.log = logging.getLogger(__name__)
        schema_path = utils.get_root_path() / 'schemas' / 'dbSchema.json'
        with open(schema_path) as path:
            self.json_schema = json.load(path)

    def get_parser(self, prog_name):
        parser = super(GenerateData, self).get_parser(prog_name)
        parser.add_argument('-s', '--schema', default='./schema.json', metavar='',
                            help='The schema to be used for generating the fake data', type=str)
        parser.add_argument('-o', '--output', default='console', metavar='',
                            help='The output of the command. It can be either console, '
                                 'or a path to a file.',
                            type=str)
        parser.add_argument('-f', '--force', help='Forces the overwrite of the destination file', default=False,
                            type=bool)
        return parser

    def take_action(self, parsed_args):
        self.log.debug("Selected schema: %s", parsed_args.schema)
        self.log.debug("Selected output: %s", parsed_args.output)

        schema = parsed_args.schema
        schema_file = utils.get_file_abs_path(schema)

        if schema_file.exists():
            vr = validate_schema(schema_file, self.json_schema)
            if vr.valid:
                self.log.debug("The schema is valid")
                if output_param_is_valid(parsed_args.output, parsed_args.force):
                    # Actually create the data!
                    self.generate_data_from_schema(schema_file, parsed_args.output)
                else:
                    self.log.error("The output parameter is not valid, please specify either 'console' "
                                   "or a valid pathname")
            else:
                self.log.error("The schema passed is not valid")
                self.log.error(vr.validation_errors)
        else:
            self.log.error("The file could not be found")

    def generate_data_from_schema(self, schema: Path, output: str):
        with (generate_handler(output, self.log.name)) as output_handler:

            with open(schema) as schema_file:
                schema_json = json.load(schema_file)

                # Generate the Faker instance
                fake = Faker(schema_json["locale"]) if schema_json.__contains__("locale") else Faker()

                db_name = schema_json["name"]

                # We need to create here, for each table, a set of rows like the following:
                # INSERT INTO <table_name> ([<fields>]) values ([<values>])
                tables = schema_json["tables"]
                for table in tables:
                    n_rows = table["rows"] if table.__contains__("rows") else 50
                    for _ in repeat(None, n_rows):
                        insert_stmt = generate_row_data(fake, db_name, table["name"], table["fields"])
                        output_handler.handle(insert_stmt)


def generate_handler(output: str, logger: str):
    if "console" == output:
        return ConsoleHandler(logger_name=logger)
    else:
        return FileHandler(file=output)


def generate_row_data(fake: Faker, db_name: str, table_name: str, fields: list) -> str:
    sql_insert = f"INSERT INTO {db_name}.{table_name} ("
    sql_values = " VALUES ("

    for field in fields:
        sql_insert += field["name"] + ","
        value = generate_fake_data(fake, field["type"])
        sql_values += value + ","

    # Remove last comma and end statement
    sql_insert = sql_insert[:-1] + ")"
    sql_values = sql_values[:-1] + ");"

    return sql_insert + sql_values


def generate_fake_data(fake: Faker, value_type: str):
    switch = {
        "name": fake.name(),
        "username": fake.user_name(),
        "address": fake.address(),
        "creditcard": fake.credit_card_number(),
        "company": fake.company(),
        "phone": fake.phone_number(),
        "email": fake.ascii_safe_email(),
        "vehicle_license": fake.license_plate(),
        "iban": fake.iban(),
        "color": fake.color_name(),
        "string": fake.text(),
        "integer": fake.random_int(max=99999),
        "numeric": fake.pyfloat(),
        "date": fake.date(),
        "time": fake.time(),
        "timestamp": fake.iso8601(),
        "binary": fake.binary(length=64),
        "bool": fake.boolean(),
        "uuid": fake.uuid4(),
        "inet": fake.ipv4(),
        "macaddr": fake.mac_address()
    }

    return switch.get(value_type)
