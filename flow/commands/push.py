# -*- coding: utf-8 -*-
from flow.command import BaseCommand

class Command(BaseCommand):
    help = "Generates HTML, Javascript and CSS from your templates and pushes"\
        " the result to FluidDB using the credentials supplied in settings.json"
    args = ""

    def handle(self, *args, **options):
        raise NotImplemented("To be done when flimp is capable enough")
