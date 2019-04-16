.. _installation:

Installation Guide
==================

.. note::
   This guide assumes the operating system used is OSX and the terminal shell is
   bash. If you are using a different operating system or shell you may need to
   adapt your commands.

Before you start
----------------

Excited for some automated testing? This page provides an introduction in how
to get started with os-automation. There is some important information on this
page, so we would like you to spend time to carefully read the entire thing from
the beginning to the end. This will familiarize you with the process and reduce
the chances that you do something wrong.

Clone this project
------------------

If you have cloned this project already you can skip this, otherwise you'll need
clone this repo using Git. *if you do not know how to clone a GitHub repository,
check out this* `help page <https://help.github.com/articles/cloning-a-repository/>`_
*from GitHub.*

Basically, you use the `git` command line application in a terminal to clone the
project locally like so:

.. code-block:: bash

    $ git clone git@github.com:openstax/os-automation.git

Install Python 3
------------

We recommend installing Python using Homebrew. In order to install Homebrew run
the following in your terminal:

.. code-block:: bash

    $ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"



Install Python3 using the appropriate `brew` command.

.. code-block:: bash

    $ brew install python

Create a virtual environment
----------------------------

It's a best practice in Python to create a virtual environment for your project.
There are various ways to do this. If you are already familiar with how to do
this create a virtualenv in that manner of your choosing. If not, run the
following `make` command in your terminal.

.. code-block:: bash

    $ make venv

.. seealso::
   One of the practices of the `Twelve-Factor App <https://12factor.net/dependencies>`_
   is proper dependency management. According to the 3rd factor,

       "A twelve-factor app never relies on implicit existence of system-wide packages."

