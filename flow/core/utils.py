#-*- coding: utf-8 -*-
"""
Generic utility classes and functions used by flow
"""
import os
import sys
import re
import shutil
import logging
if sys.version_info < (2, 6):
    import simplejson as json
else:
    import json
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
    for d, subdirs, files in os.walk(template_dir):
        relative_dir = d[len(template_dir)+1:].replace(target, name)
        if relative_dir:
            os.mkdir(os.path.join(target_dir, relative_dir))
        for i, subdir in enumerate(subdirs):
            if subdir.startswith('.'):
                del subdirs[i]
        for f in files:
            # ToDo NEEDS CHECKING SO WE CAN COPY JS AND HTML SOURCE CODE
            if not (f.endswith('.py') or f.endswith('.js')
                or f.endswith('.html') or f.endswith('.css')):
                # Ignore .pyc, .pyo, .py.class etc, as they cause various
                # breakages. We only want python, html, js or css source files
                # copied over
                continue
            path_old = os.path.join(d, f)
            path_new = os.path.join(target_directory, relative_dir, f.replace(target, name))
            fp_old = open(path_old, 'r')
            fp_new = open(path_new, 'w')
            # ToDo Add Jinja template processing here... better than simple
            # call to replace()
            #fp_new.write(fp_old.read().replace('{{ name }}', name))
            fp_new.write(fp_old.read())
            fp_old.close()
            fp_new.close()
            try:
                shutil.copymode(path_old, path_new)
                _make_writeable(path_new)
            except OSError:
                sys.stderr.write(style.NOTICE("Notice: Couldn't set permission bits on %s. You're probably using an uncommon filesystem setup. No problem.\n" % path_new))

def _make_writeable(filename):
    """
    Make sure that the file is writeable. Useful if our source is
    read-only.

    Borrowed from  Django
    """
    import stat
    if sys.platform.startswith('java'):
        # On Jython there is no os.access()
        return
    if not os.access(filename, os.W_OK):
        st = os.stat(filename)
        new_permissions = stat.S_IMODE(st.st_mode) | stat.S_IWUSR
        os.chmod(filename, new_permissions)

def generate(source, target):
    """
    Given the source directory will use Jinja2 to generate HTML (and possibly JS
    or CSS) from templates and create the resulting raw web-application in the
    target directory.

    The contents of the target directory *should* be in such a state that they
    can be "pushed" to FluidDB (see below).
    """
    pass
