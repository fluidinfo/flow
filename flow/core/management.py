# -*- coding: utf-8 -*-
"""
Framework for making commands for use by flow. Loosely based upon the way it's
implemented in Django.

(c) 2010 Fluidinfo Inc
"""
from optparse import OptionParser
import sys
import os
import flow
from flow.core import __path__

class CommandError(Exception):
    """
    Thrown when a command fails
    """
    pass

class BaseCommand(object):
    """
    Base class for all commands
    """
    help = ''
    args =''
    option_list = ()

    def get_usage(self, subcommand):
        """
        Return a description for how to use the command
        """
        usage = "%prog" + " %s [options] %s" % (subcommand, self.args)
        if self.help:
            return "%s\n\n%s" % (usage, self.help)
        else:
            return usage

    def get_parser(self, prog_name, subcommand):
        """
        Returns an OptionParser for processing the arguments for this command
        """
        return OptionParser(prog=prog_name, usage=self.get_usage(subcommand),
            option_list=self.option_list)

    def get_help(self, prog_name, subcommand):
        """
        Prints the help message for this command
        """
        parser = self.get_parser(prog_name, subcommand)
        parser.print_help()

    def run_from_argv(self, argv):
        """
        Run the command
        """
        parser = self.get_parser(argv[0], argv[1])
        options, args = parser.parse_args(argv[2:])
        self.execute(*args, **options.__dict__)

    def execute(self, *args, **options):
        """
        Executes the command in a "clean" fashion (wrapped in try/except)
        """
        try:
            self.handle(*args, **options)
        except CommandError, e:
            sys.stderr.write("Error: %s\n" % e)

    def handle(self, *args, **options):
        """
        The logic of the command. Subclasses to implement
        """
        raise NotImplementedError()

def find_commands(directory):
    """
    Given a directory will list all the python modules in the directory
    called "commands" underneath
    """
    command_dir = os.path.join(directory, 'commands')
    try:
        return [f[:-3] for f in os.listdir(command_dir)
            if not f.startswith('_') and f.endswith('.py')]
    except OSError:
        return []

def get_commands():
    """
    Populates a dictionary with all the available commands it can find
    """
    # so far only commands specified in flow.core should be loaded. In future
    # I hope to allow users to add their own commands to projects
    return dict([(name, 'flow.core.commands') for name in find_commands(__path__[0])])

# The following two functions are taken ultimately from Python 2.7 by way of
# Django

def _resolve_name(name, package, level):
    """Return the absolute name of the module to be imported."""
    if not hasattr(package, 'rindex'):
        raise ValueError("'package' not set to a string")
    dot = len(package)
    for x in xrange(level, 1, -1):
        try:
            dot = package.rindex('.', 0, dot)
        except ValueError:
            raise ValueError("attempted relative import beyond top-level "
                              "package")
    return "%s.%s" % (package[:dot], name)


def import_module(name, package=None):
    """Import a module.

    The 'package' argument is required when performing a relative import. It
    specifies the package to use as the anchor point from which to resolve the
    relative import to an absolute import.

    """
    if name.startswith('.'):
        if not package:
            raise TypeError("relative imports require the 'package' argument")
        level = 0
        for character in name:
            if character != '.':
                break
            level += 1
        name = _resolve_name(name[level:], package, level)
    __import__(name)
    return sys.modules[name]

class CommandHandler(object):
    """
    Encapsulates all the behaviour required for loading, processing and
    running the various commands that are available to flow
    """

    def __init__(self, argv=None):
        """
        command_name will be either flow or manage.py
        """
        self.argv = argv or sys.argv[:]
        self.prog_name = os.path.basename(self.argv[0])

    def help(self):
        """
        Returns a global help text
        """
        usage = ['',"Type '%s help <subcommand>' for help on a specific"\
            " subcommand." % self.prog_name, '']
        usage.append('Available subcommands:')
        commands = get_commands().keys()
        commands.sort()
        for cmd in commands:
            usage.append('    %s' % cmd)
        return '\n'.join(usage)

    def fetch_command(self, subcommand):
        """
        Tries to fetch the passed subcommand
        """
        try:
            namespace = get_commands()[subcommand]
            module = import_module('%s.%s' % (namespace, subcommand))
        except KeyError:
            sys.stderr.write("Unknown command: %r\nType '%s help' for usage.\n"
                % (subcommand, self.prog_name))
            sys.exit(1)
        return module.Command()

    def run_command(self):
        """
        Attempt to find and run the command
        """
        parser = OptionParser(usage="%prog subcommand [options] [args]")

        try:
            options, args = parser.parse_args(self.argv)
        except:
            pass # ignore errors for now

        try:
            subcommand = self.argv[1]
        except IndexError:
            subcommand = 'help' # Just display help if no subcommand is given

        if subcommand == 'help':
            if len(args) > 2:
                self.fetch_command(args[2]).get_help(self.prog_name, args[2])
            else:
                sys.stderr.write(self.help() + '\n')
        elif not "--version" in args:
            self.fetch_command(subcommand).run_from_argv(self.argv)
