# -*- coding: utf-8 -*-
from flow.core.management import BaseCommand
from flow.core.utils import copy_template
import os

class Command(BaseCommand):
    help = "Creates a Flow project directory for the given project name in"\
        " the current directory."
    args = "[projectname]"

    def handle(self, *args, **options):
        if not args or len(args) != 1:
            raise CommandError('You must specify a single project name')
        project_name = args[0]
        # TODO Check the name doesn't conflict on python path
        # use copy_template to create the directory
        context = {
                'name': project_name,
            }
        copy_template('project', os.getcwd(), project_name, context)
