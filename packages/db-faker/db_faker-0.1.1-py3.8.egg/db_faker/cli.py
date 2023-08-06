"""Console script for db_faker."""
import sys

from cliff.app import App
from cliff.commandmanager import CommandManager


class DatabaseFakerApp(App):

    def __init__(self):
        super(DatabaseFakerApp, self).__init__(
            description='Database Faker CLI app',
            version='0.0.1',
            command_manager=CommandManager('db_faker.commands'),
            deferred_help=True
        )

    def initialize_app(self, argv):
        self.LOG.debug("Initializing Database Faker CLI app")

    def prepare_to_run_command(self, cmd):
        self.LOG.debug("Preparing to run command %s", cmd.__class__.__name__)

    def clean_up(self, cmd, result, err):
        self.LOG.debug("Cleaning up %s", cmd.__class__.__name__)
        if err:
            self.LOG.debug("There was an error: %s", err)


def main(argv=sys.argv[1:]):
    """Console script for db_faker."""
    cli = DatabaseFakerApp()
    return cli.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
