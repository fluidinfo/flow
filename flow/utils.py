#-*- coding: utf-8 -*-
"""
Generic utility classes and functions used by flow
"""
import os
import sys
import re

from jinja2 import Environment, FileSystemLoader

import flow

def copy_template(source, target, name, context):
    """
    Copies a template file/directory structure to the specified
    directory.

    source -- the template to use as a path underneath flow/templates.
        e.g. "project", "apps/default"
    target -- the directory in which the new template is to be copied
    name -- the name of the newly created directory in the target
    context -- a dictionary holding values to use whilst processing the
        templates.
    """
    # check the name is valid
    if not re.search(r'^[_a-zA-Z]\w*$', name):
        # Try to be helpful
        if not re.search(r'^[_a-zA-Z]', name):
            message = 'make sure the name begins with a letter or underscore'
        else:
            message = 'use only numbers, letters and underscores'
        raise ValueError("%r is not a valid name. Please %s." % (name, message))
    target_directory = os.path.join(target, name)
    os.mkdir(target_directory)
    template_dir = os.path.join(flow.__path__[0], 'templates', source)
    # set up the Jinja2 environment
    env = Environment(loader=FileSystemLoader(template_dir))
    for d, subdirs, files in os.walk(template_dir):
        relative_dir = d[len(template_dir)+1:].replace(target, name)
        if relative_dir:
            os.mkdir(os.path.join(target_directory, relative_dir))
        for i, subdir in enumerate(subdirs):
            if subdir.startswith('.'):
                del subdirs[i]
        for f in files:
            root, extension = os.path.splitext(f)
            if extension not in flow.VALID_TEMPLATE_EXTENSIONS:
                # Ignore .pyc, .pyo, .py.class etc, as they cause various
                # breakages. We only want python, html, js or css source files
                # copied over
                continue
            template_path = os.path.join(d, f).replace(template_dir, '')
            #path_old = os.path.join(d, f)
            #fp_old = open(path_old, 'r')
            template = env.get_template(template_path)
            path_new = os.path.join(target_directory, relative_dir, f.replace(target, name))
            fp_new = open(path_new, 'w')
            # ToDo Add Jinja template processing here... better than simple
            # call to replace()
            #fp_new.write(fp_old.read().replace('{{ name }}', name))
            fp_new.write(template.render(context))
            fp_new.close()
