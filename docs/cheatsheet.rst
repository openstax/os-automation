.. _cheatsheet:

##################
Command Cheatsheet
##################

This is not meant to be an exhaustive list of all the commands. It serves as a
quick reference but also to display the patterns of all the commands.

Chrome
------

**Running all the tests w/ Chrome on qa**

.. code-block:: bash

   pytest --driver Chrome

**Running all the tests w/ Chrome in headless mode on qa**

.. code-block:: bash

   pytest --driver Chrome --headless

**Running all the tests w/ Chrome, headless, 4 processes, and on qa**

.. code-block:: bash

   pytest -n 4 --driver Chrome --headless

**Running all the tests w/ Chrome, headless, w/ 4 processes, and on staging**

.. code-block:: bash

   pytest -n 4 --driver Chrome --instance staging --headless

**Running all the web tests w/ Chrome on qa**

.. code-block:: bash

   pytest --driver Chrome --system web

**Running all the web tests w/ Chrome, headless, and on qa**

.. code-block:: bash

   pytest --driver Chrome --system web --headless

**Running all the web tests w/ Chrome, headless, 4 processes, and on staging**

.. code-block:: bash

   pytest -n 4 --driver Chrome --instance staging --system web --headless

**Running all the accounts tests w/ Chrome, headless, and on qa**

.. code-block:: bash

   pytest --driver Chrome --system accounts --headless

**Running all the accounts tests w/ Chrome, headless, and on staging**

.. code-block:: bash

   pytest --driver Chrome --instance staging --system accounts --headless


Firefox
-------

**Running all the tests w/ Firefox on qa**

.. code-block:: bash

   pytest --driver Firefox

**Running all the tests w/ Firefox in headless mode on qa**

.. code-block:: bash

   pytest --driver Firefox --headless

**Running all the tests w/ Firefox, headless, 4 processes, and on qa**

.. code-block:: bash

   pytest -n 4 --driver Firefox --headless

**Running all the tests w/ Firefox, headless, w/ 4 processes, and on staging**

.. code-block:: bash

   pytest -n 4 --driver Firefox --instance staging --headless

**Running all the web tests w/ Firefox on qa**

.. code-block:: bash

   pytest --driver Firefox --system web

**Running all the web tests w/ Firefox, headless, and on qa**

.. code-block:: bash

   pytest --driver Firefox --system web --headless

**Running all the web tests w/ Firefox, headless, 4 processes, and on staging**

.. code-block:: bash

   pytest -n 4 --driver Firefox --instance staging --system web --headless

**Running all the accounts tests w/ Firefox, headless, and on qa**

.. code-block:: bash

   pytest --driver Firefox --system accounts --headless

**Running all the accounts tests w/ Firefox, headless, and on staging**

.. code-block:: bash

   pytest --driver Firefox --instance staging --system accounts --headless

Safari
------

**Running all the tests w/ Safari on qa**

.. code-block:: bash

   pytest --driver Safari

**Running all the tests w/ Safari on staging**

.. code-block:: bash

   pytest --driver Safari --instance staging

**Running all the web tests w/ Safari on qa**

.. code-block:: bash

   pytest --driver Safari --system web

**Running all the web tests w/ Safari on staging**

.. code-block:: bash

   pytest --driver Safari --instance staging --system web

**Running all the accounts tests w/ Safari on qa**

.. code-block:: bash

   pytest --driver Safari --system accounts

**Running all the accounts tests w/ Safari on staging**

.. code-block:: bash

   pytest --driver Safari --instance staging --system accounts
