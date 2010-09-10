import unittest
import tempfile
from optparse import OptionParser
import sys
import os
import uuid
import shutil

from flow.command import (BaseCommand, find_commands, get_commands,
    CommandHandler)
from flow import __path__
from flow.commands.create import Command

TMP_FILE_PATH = os.path.join(tempfile.gettempdir(), 'flow_mock_test')

def get_tmp_content():
    try:
        f = open(TMP_FILE_PATH, 'r')
        result = f.read()
    finally:
        f.close()
    return result

class MockCommand(BaseCommand):
    """
    Inner class to test with
    """
    help = "This is some help"
    args = "[arg]"

    def handle(self, *args, **options):
        """
        This is where the action usually takes place. In this case we only
        want to drop a file in tmp containing the value of args[0]
        """
        if os.path.exists(TMP_FILE_PATH):
            os.remove(TMP_FILE_PATH)
        f = open(TMP_FILE_PATH, 'w')
        f.write(args[0])
        f.close()

class MockStdout(object):
    """
    Used for checking stuff that gets piped to stdout/stderr (e.g. from Optparse)
    """
    def write(self, text):
        self.output = text

class TestBaseCommand(unittest.TestCase):

    def setUp(self):
        # provide an instance of BaseCommand
        self.command = MockCommand()

    def test_get_usage(self):
        expected = "%prog mock [options] [arg]\n\nThis is some help"
        actual = self.command.get_usage('mock')
        self.assertEqual(expected, actual)
        self.help = ""
        self.args = ""
        expected = "%prog mock [options]"
        actual = self.command.get_usage('mock')

    def test_get_parser(self):
        p = self.command.get_parser('flow', 'mock')
        self.assertTrue(isinstance(p, OptionParser))
        expected = "Usage: flow mock [options] [arg]\n\nThis is some help\n"
        actual = p.get_usage()
        self.assertEqual(expected, actual)

    def test_get_help(self):
        # we need to monkey-patch stdout
        correct_stdout = sys.stdout
        sys.stdout = MockStdout()
        try:
            self.command.get_help('flow', 'mock')
            mock_stdout = sys.stdout
        finally:
            sys.stdout = correct_stdout
        expected = "Usage: flow mock [options] [arg]\n\nThis is some help\n\n"\
            "Options:\n  -h, --help  show this help message and exit\n"
        self.assertEqual(expected, mock_stdout.output)

    def test_run_from_argv(self):
        expected = 'test_run_from_argv'
        argv = ['flow', 'mock', expected]
        self.command.run_from_argv(argv)
        # The file should have the correct content
        self.assertEqual(expected, get_tmp_content())

class TestCommandHandler(unittest.TestCase):

    def test_init(self):
        ch = CommandHandler(['flow'])
        self.assertEqual('flow', ch.prog_name)
        ch = CommandHandler(['/foo/bar/baz/flow'])
        self.assertEqual('flow', ch.prog_name)

    def test_help(self):
        ch = CommandHandler(['flow'])
        expected = "\nType 'flow help <subcommand>' for help on a specific subcommand.\n\nAvailable subcommands:\n    app\n    create\n    push\n    test"
        actual = ch.help()
        self.assertEqual(expected, actual)

    def test_fetch_command(self):
        ch = CommandHandler(['flow'])
        result = ch.fetch_command('create')
        self.assertTrue(isinstance(result, Command))

    def test_run_command(self):
        ch = CommandHandler(['flow'])
        # we need to monkey-patch stderr since it'll print out the generic help
        # to stderr if no command is given in argv when __init__() is called
        correct_stderr = sys.stderr
        sys.stderr = MockStdout()
        try:
            ch.run_command()
            mock_stderr = sys.stderr
        finally:
            sys.stderr = correct_stderr
        expected = "\nType 'flow help <subcommand>' for help on a specific subcommand.\n\nAvailable subcommands:\n    app\n    create\n    push\n    test\n"
        self.assertEqual(expected, mock_stderr.output)
        # Get help for a specific command
        ch = CommandHandler(['flow', 'help', 'create'])
        correct_stdout = sys.stdout
        sys.stdout = MockStdout()
        try:
            ch.run_command()
            mock_stdout = sys.stdout
        finally:
            sys.stdout = correct_stdout
        expected = "Usage: flow create [options] [projectname]\n\nCreates a Flow project directory for the given project name in the current directory.\n\nOptions:\n  -h, --help  show this help message and exit\n"
        self.assertEqual(expected, mock_stdout.output)
        # The --help and -h commands are handled corectly
        for command in ['-h', '--h', '-help', '--help', 'help']:
            ch = CommandHandler(['flow', command])
            correct_stderr = sys.stderr
            sys.stderr = MockStdout()
            try:
                ch.run_command()
                mock_stderr = sys.stderr
            finally:
                sys.stderr = correct_stderr
            expected = "\nType 'flow help <subcommand>' for help on a specific subcommand.\n\nAvailable subcommands:\n    app\n    create\n    push\n    test\n"
            self.assertEqual(expected, mock_stderr.output)
        # Try to run the "create" command to make sure run_command passes
        # things along properly
        project_name = 'TEST' + str(uuid.uuid4()).replace('-', '_')
        try:
            ch = CommandHandler(['flow', 'create', project_name])
            ch.run_command()
            # we should be able to see the newly created project directory in the
            # cwd and find the correct files in there
            self.assertTrue(os.path.exists(project_name))
            self.assertTrue(os.path.isdir(project_name))
            manage_path = os.path.join(project_name, 'manage.py')
            self.assertTrue(os.path.exists(manage_path))
            self.assertTrue(os.path.isfile(manage_path))
        finally:
            # tidy up
            path = os.path.abspath(project_name)
            shutil.rmtree(path)

class TestManagementFunctions(unittest.TestCase):

    def test_find_commands(self):
        self.assertEqual(4, len(find_commands(__path__[0])))

    def test_get_commands(self):
        result = get_commands()
        self.assertTrue(isinstance(result, dict))
        self.assertEqual(4, len(result))
