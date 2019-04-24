.. _run_tests:

####################
How to run the tests
####################

Introduction
------------

This framework uses Pytest and Selenium WebDriver together to create a robust
automated test framework. The ``pytest`` command will be used in the terminal to
run all the tests for each product.

Supported products
------------------

The os-automation framework includes tests for the following products:

* openstax.org (Web)
* Accounts
* Tutor (work-in-progress)

How to run tests for a specific product system and browser
----------------------------------------------------------

Each of the products is intended to be ran as a system. When ran as a system the
tests included in the run will test the product plus other interconnected parts
of the product.

To run the product system using a specific browser you can run the appropriate
command in the terminal:

.. code-block:: bash

   pytest --driver Chrome  --system web         # Chrome
   pytest --driver Firefox --system accounts    # Firefox
   pytest --driver Safari  --system web         # Safari

As shown above there are two parts to running the tests. The ``--driver`` which
defines the browser and ``--system`` which defines the product system.

For every kind of test the ``--driver`` argument is required.

How to run tests for a specific instance
----------------------------------------

By default, the instance selected by the framework is `qa`. To select a different
instance the ``--instance <instance_name>`` is used. The instances available are:

* dev (supported but rarely used)
* qa
* staging
* prod

To override the default instance or be more explicit, run the following in the
terminal:

.. code-block:: bash

   pytest --driver Chrome  --instance staging --system web         # Chrome + staging
   pytest --driver Firefox --instance qa      --system accounts    # Firefox + qa
   pytest --driver Safari  --instance prod    --system web         # Safari + production


How to hide the browser when running tests
------------------------------------------

.. warning::
   The Safari browser does not support `headless` mode. Safari creates a
   "glass surface" over the browser that also seems to take over the system.
   When Safari tests are running it's recommended to not move the mouse cursor
   over the Safari browser window as that may trigger the glass cover pausing
   the test run, don't save passwords in Safari because those may be autofilled
   during testing, and to avoid typing on the keyboard, especially the
   return/enter key, as that may interrupt the test run as well as disable
   remote automation

By default all the tests will run and open a browser window. At times,
this can be annoying as it will take control of your system for a moment. If you
want the browser to not be displayed and hidden in order to use your system
normally use the ``--headless`` option.

.. code-block:: bash

   pytest --driver Chrome  --system web --headless
   pytest --driver Firefox --system web --headless

Speed up test runs by running multiple tests in parallel
--------------------------------------------------------

.. warning::
   The Safari browser will not work with the ``-n`` as it does not support
   running tests in parallel.

To speed up the test run you can run them across multiple processes using
the ``-n`` option. This command will not work with Safari. The number that comes
after the ``-n`` is the number of processes you want to use. To run these at the
full capability of your computer the number provided to ``-n`` should be
``number_of_cores - 1``.

.. code-block:: bash

   pytest -n 4 --driver Chrome  --system web      # Opens 4 Browser windows
   pytest -n 2 --driver Firefox --system accounts # Opens 2 Browser windows

Bringing it all together
------------------------

You can combine these options to run 4 processes in `headless` mode.

.. code-block:: bash

   pytest -n 4 --driver Chrome --instance qa       --system web       --headless
   pytest -n 2 --driver Firefox --instance staging --system accounts  --headless

How to run all the tests!
-------------------------

If you need to run all the tests in the framework you can simply leave off the
``--system <product>`` from the command line.

.. code-block:: bash

   pytest -n 4 --driver Chrome --headless     # All tests w/ Chrome, 4 processes, hidden, on qa
   pytest --driver Firefox --instance prod    # All tests w/ Firefox sequentially on production
