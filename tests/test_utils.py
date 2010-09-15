import os
import unittest
import shutil
import uuid

from flow.utils import copy_template

class TestUtils(unittest.TestCase):

    def test_copy_template(self):
        """
        Although the original based upon work from Django, they don't
        seem to have a unit-test for this method, ergo I wrote this one
        (I like all methods to be tested)
        """
        # some safe values
        template = 'project'
        name = 'a' + str(uuid.uuid4()).replace('-', '_')
        context = { 'name': name }
        cwd = os.getcwd()
        new_dir = os.path.join(cwd, name)
        try:
            # run the method
            copy_template(template, cwd, name, context)
            # we should be able to find the directory/files locally
            self.assertTrue(os.path.isdir(new_dir))
            # there should be a settings.py file in there
            path_to_settings = os.path.join(new_dir, 'settings.py')
            self.assertTrue(os.path.isfile(path_to_settings))
            # it should have the name of the project in it (so we know jinja2
            # worked)
            settings_file = open(path_to_settings, 'r')
            settings = settings_file.read()
            settings_file.close()
            self.assertTrue(name in settings)
        finally:
            # tidy up
            shutil.rmtree(new_dir)
