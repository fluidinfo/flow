# -*- coding: utf-8 -*-
from flow.core.management import BaseCommand
from flow.core.utils import generate, push
import os

class Command(BaseCommand):
    help = "Generates HTML, Javascript and CSS from your templates and pushes"\
        " the result to FluidDB using the credentials supplied in settings.json"
    args = ""

    def handle(self, *args, **options):
        # generate the raw web-application from the templates
        generate(os.getcwd(), TARGET)
        # run any tests that have been specified
        # push the result to FluidDB
        copy_template('project', os.getcwd(), project_name, context)
