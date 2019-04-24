.. _local_dev:

##############################
Prepare your local environment
##############################

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

    cp .env.template ./.env

The `.env` file is not checked into source control. This allows us the ability
to place secrets or other sensitive variables into the file and not check them
into source control.

Depending on the products and tests you are running you need to have specific
variables set. These are covered in the section about running tests.

At a minimum you'll want to make sure to set the production urls for the
following values:

.. code-block:: bash

    ACCOUNTS_BASE_URL=https://accounts.openstax.org
    EXERCISES_BASE_URL=https://exercises.openstax.org
    PAYMENTS_BASE_URL=https://payments.openstax.org/admin
    TUTOR_BASE_URL=https://tutor.openstax.org
    WEB_BASE_URL=https://openstax.org
