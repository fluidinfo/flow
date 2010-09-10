import os
import unittest
import shutil

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
        name = 'test_project'
        context = { 'name': name }
        cwd = os.getcwd()
        new_dir = os.path.join(cwd, name)
        shutil.rmtree(new_dir, ignore_errors=True)
        # run the method
        copy_template(template, cwd, name, context)
        # we should be able to find the directory/files locally
        self.assertTrue(os.path.isdir(new_dir))
        # there should be a manage.py file in there
        self.assertTrue(os.path.isfile(os.path.join(new_dir, 'manage.py')))
        # tidy up
        shutil.rmtree(new_dir)
