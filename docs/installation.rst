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

Install Homebrew
----------------

We recommend installing Python using Homebrew. In order to install Homebrew run
the following in your terminal:

.. code-block:: bash

    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

Install Python
----------------

Install Python3 using the appropriate ``brew`` command.

.. code-block:: bash

    brew install python

Install git
----------------

Install git using ``brew``:

.. code-block:: bash

    brew install git

Clone this project
------------------

If you have cloned this project already you can skip this, otherwise you'll need
clone this repo using Git. *if you do not know how to clone a GitHub repository,
check out this* `help page <https://help.github.com/articles/cloning-a-repository/>`_
*from GitHub.*

Basically, you use the `git` command line application in a terminal to clone the
project locally like so:

.. code-block:: bash

    git clone git@github.com:openstax/os-automation.git

Git will clone down the code into a new folder called `os-automation`. Most of
the commands in this guide will require you to be in this folder. Run the
following in your terminal to change directories:

.. code-block:: bash

    cd os-automation

Create a virtual environment
----------------------------

It's a best practice in Python to create a virtual environment (virtualenv) for
your project. Virtual environments isolate dependencies required for different
projects in their own environment. There are various ways to do this depending
on how long you have been using Python.

If you are already familiar with how to create virtual environments you can
manage that how you like. If not, run the following `make` command in your
terminal.

.. code-block:: bash

    make venv

This command will also install all dependencies defined in the `requirements.txt`
file into your virtual environment.

.. seealso::
   One of the practices of the `Twelve-Factor App <https://12factor.net/dependencies>`_
   is proper dependency management. According to the 3rd factor,

       "A twelve-factor app never relies on implicit existence of system-wide packages."

Install Selenium WebDrivers
---------------------------

This test framework uses the following WebDrivers to run automated tests.

* GeckoDriver - Mozilla Firefox
* ChromeDriver - Google Chrome
* SafariDriver - Apple Safari (Installed locally with OSX)


Install GeckoDriver
^^^^^^^^^^^^^^^^^^^

.. note::
   You'll need to have Firefox installed on your computer. You can download
   Firefox at their `website <https://www.mozilla.org/en-US/firefox/new/>`_

Use the ``brew`` command line tool to install GeckoDriver. You can do this by
running the following in your terminal:

.. code-block:: bash

    brew install geckodriver

Install ChromeDriver
^^^^^^^^^^^^^^^^^^^^

.. note::
   You'll need to have Chrome installed on your computer. You can download Chrome
   at their `website <https://www.google.com/chrome/>`_

Use the ``brew cask`` command to install ChromeDriver:

.. code-block:: bash

    brew cask install chromedriver
