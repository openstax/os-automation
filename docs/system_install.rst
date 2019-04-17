.. _system_install:

Installation Guide
==================

.. note::
   This guide assumes the operating system used is OSX and the terminal shell is
   bash. If you are using a different operating system or shell you may need to
   adapt your commands.

System Requirements
-------------------

The high level requirements installing os-automation are:

* Homebrew (OSX package manager)
* Python 3.7+
* git
* Firefox geckodriver
* Chrome chromedriver

Install Homebrew
----------------

We recommend installing Python using Homebrew. In order to install Homebrew run
the following in your terminal:

.. code-block:: bash

    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

Install Python
--------------

Install Python3 using the appropriate ``brew`` command.

.. code-block:: bash

    brew install python

Install git
-----------

Install git using ``brew``:

.. code-block:: bash

    brew install git

Clone os-automation from GitHub
-------------------------------

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

Install Selenium WebDrivers
---------------------------

This test framework uses the following WebDrivers to run automated tests.

* GeckoDriver - Mozilla Firefox
* ChromeDriver - Google Chrome
* SafariDriver - Apple Safari (Installed locally with OSX)


Install GeckoDriver
-------------------

.. note::
   You'll need to have Firefox installed on your computer. You can download
   Firefox at their `website <https://www.mozilla.org/en-US/firefox/new/>`_

Use the ``brew`` command line tool to install GeckoDriver. You can do this by
running the following in your terminal:

.. code-block:: bash

    brew install geckodriver

Install ChromeDriver
--------------------

.. note::
   You'll need to have Chrome installed on your computer. You can download Chrome
   at their `website <https://www.google.com/chrome/>`_

Use the ``brew cask`` command to install ChromeDriver:

.. code-block:: bash

    brew cask install chromedriver


