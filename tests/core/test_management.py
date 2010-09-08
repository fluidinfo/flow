import unittest
import tempfile
from optparse import OptionParser

from flow.core.management import BaseCommand

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
        tmp_file = os.path.join(tempfile.gettempdir(), 'flow_mock_test')
        if os.path.exists(tmp_file):
            os.remove(tmp_file)
        f = open(tmp_file, w)
        f.write(arg[0])
        f.close()

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
        pass

    def test_run_from_argv(self):
        pass

    def test_execute(self):
        pass

    def test_handle(self):
        pass

class TestCommandHandler(unittest.TestCase):

    def test_init(self):
        pass

    def test_help(self):
        pass

    def test_run_command(self):
        pass

class TestManagementFunctions(unittest.TestCase):

    def test_find_commands(self):
        pass

    def test_get_commands(self):
        pass
