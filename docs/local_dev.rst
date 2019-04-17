.. _local_dev:

##########################################
Prepare your local development environment
##########################################

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

Activate the virtual environment
--------------------------------

Every command used to run the test framework will require that the virtualenv
created earlier is activated.

In order to activate the virtualenv type the following in your terminal:

.. code-block:: bash

    source ./.venv/bin/activate

When the virtualenv is activated you should see a change to your terminal prompt.

An activated terminal prompt will look something like this:

.. code-block:: bash

    (.venv) $

The ``(.venv)`` before the prompt indicates that the virtualenv is active.

Install dependencies
--------------------

The os-automation project depends on a number of python packages to operate properly.
Each dependency is installed into the the virtualenv created earlier.

To install all dependencies using the `make` command enter the following into
the terminal:

.. code-block:: bash

    make install

You can also install the dependencies using Python's ``pip`` command. To use ``pip``
enter the following into your terminal:

.. code-block:: bash

    pip install -r requirements.txt

.. seealso::
   One of the practices of the `Twelve-Factor App <https://12factor.net/dependencies>`_
   is proper dependency management. According to the 3rd factor,

       "A twelve-factor app never relies on implicit existence of system-wide packages."

Copy the .env.template file
---------------------------

The os-automation framework has the ability to utilize `dotenv` to load
environment variables from a ``.env`` file located in the root of the directory.
To get started with filling out the necessary values copy the ``.env.example``
file.

.. code-block:: bash

    cp .env.example ./.env

The `.env` file is not checked into the rest of the project files. This allows
the ability to place secrets in the file and them not to make into source control.
