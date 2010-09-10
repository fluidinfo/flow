Flow
====

What?
+++++

Flow will become a small framework to automate and ease the creation of web-applications hosted within `FluidDB <http://fluidinfo.com/>`_. Currently, there isn't much here in terms of code but it's a start. Feedback and comments are most welcome.

How?
++++

So far there is a scaffolding in place for creating a suite of command-line utilities. For example, to create a new project your session might look something like the following::

    $ flow help
    
    Type 'flow help <subcommand>' for help on a specific subcommand.
    
    Available subcommands:
        app
        create
        push
        test

    $ flow help create
    Usage: flow create [options] [projectname]

    Creates a Flow project directory for the given project name in the current directory.

    Options:
      -h, --help  show this help message and exit

    $ flow create foo
    $ cd foo
    $ ls
    __init__.py  manage.py  objects.py  settings.py

The resulting files are for illustrative purposes. Nevertheless they'll work in the following ways:

* **manage.py** - a command-line utility used to interract with your project and FluidDB. For example, one might issue `./manage.py push` to build and deploy the application to FluidDB.
* **objects.py** - not sure about this one but it'd be where you use fom to specify the sort of objects and related fields your application will be using. I'm toying with the idea of generating javascript data-structures from these.
* **settings.py** - I'm not entirely convinced about this one either, but settings.py is where you store application settings.

The available sub-commands described in the help displayed above are also for illustrative purposes - only "create" works.

You might be thinking that this is a lot like the workflow used in Django or Ruby on Rails. Actually, you'd be right and it's supposed to be like that so developers feel right at home.

In terms of the layers involved in the flow stack here's how things look in my mind's eye (subject to change):

* **flow** - manages the high level stuff with the aim of keeping the nitty-gritty details of interracting with FluidDB hidden from the developer. We want the developer to concentrate on their application rather than FluidDB. Flow sits upon flimp.
* `flimp <http://github.com/fluidinfo/flimp>`_ - is used to import the resulting application and any related data into FluidDB. Flimp sits upon fom.
* `fom <http://bitbucket.org/aafshar/fom-main/src>`_ - the Fluid Object Mapper by Ali Afshar is used to communicate directly with FluidDB.

When
+++++

This project is currently under heavy development and we'd love feedback and suggestions. We're aiming for something usable by the end of October 2010 (there, I've committed myself you see).

:-)
