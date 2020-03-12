.. _ci:

######################
Continuous Integration
######################

os-automation uses a combination of Concourse CI and CircleCI to run tests upon 
the detection of new deployments. The tasks that are used to do this are executed 
within a pipeline and are run one after the other. Concourse CI acts as the 
"listener" for new deployments. When a new deployment is detected it will 
execute a task that starts the UI tests in Circle CI for the environment that has 
a new deployment.

Concourse CI
============

.. seealso::
   It's recommended that the `Concourse Tutorial <https://concoursetutorial.com/>`_ 
   by Stark and Wayne be done in order to understand how Concourse CI works or if 
   there are any maintenance tasks to update the pipeline.

We'll cover Concourse CI from a high level by going over the pipeline file for ``os-web``.

Pipeline File
=============

Concourse CI pipeline configuration is all done using yaml. Here is the pipeline file for 
running os-web UI tests in CircleCI:

.. literalinclude:: ../.concourse/ui-tests-os-web.pipeline.yml
   :language: yaml
   :linenos:

When looking at the pipeline file from a high level it's useful to drop down towards 
the end of the file and look at each of the steps that will be executed as part of the 
the pipeline.

Below are all the steps that are defined in the ``jobs`` area:

.. literalinclude:: ../.concourse/ui-tests-os-web.pipeline.yml
   :language: yaml
   :emphasize-lines: 4,6,7,9,11
   :lines: 31-44
   :linenos:

Each of the highlighted lines is a step in the pipeline that will get executed sequentially.

The first is a ``get`` step. If you refer to the top of the file you'll see this 
is named after a resource called ``listen-os-cms``. This resource is configured as a 
slack resource that is configured to listen to the ``#deployments`` channel for the 
specified regular expression shown below:

.. literalinclude:: ../.concourse/ui-tests-os-web.pipeline.yml
   :language: yaml
   :emphasize-lines: 7
   :lines: 10-16
   :linenos:

When a message is detected that matches this regular expression the pipeline will 
be triggered as is shown by ``trigger: true``. This step also saves a couple files 
we'll use in later steps. It saves ``listen-os-cms/message_text`` which has all 
the text of the message, ``listen-os-cms/message_text_0`` which has the instance, and 
``listen-os-cms/message_text_1`` which has the instance@sha specification.

The next step which is labeled ``get: os-automation`` is a git resource which pulls 
over the source code of the os-automation repository. The source code will be used 
later in the pipeline to run tasks.

The ``task: defer-to-circle`` is defined in the task file shown in that step. That's 
why we do a ``get`` step to get the source code of os-automation, to be able to access 
those files and run the script. This step runs a python script that reads in the instance,
sends a POST request to CircleCI to start tests for ``os-web`` for that instance.

.. literalinclude:: ../.concourse/tasks/test-osweb-ui-circleci/script.py
   :language: python
   :lines: 48-55 
   :linenos:

The ``task: create-version-message`` takes a template of text and fills it in to 
be posted to the ``#qa-stream`` channel to show that a deployment was detected 
and a link to the Circle CI job that was started.

.. literalinclude:: ../.concourse/tasks/version-message/script.py
   :language: python
   :lines: 13-24
   :linenos:

The ``put: notify`` step posts the message created in the previous step to slack.

Configuring the Pipeline in Concourse
=====================================

Installing fly
--------------

In order to update the pipeline or add the pipeline to a Concourse server you must
first have the ``fly`` cli tool installed on your machine. You can get this tool
by visiting `https://concourse-dev0.openstax.org <https:/concourse-dev0.openstax.org`_ 
and clicking the appropriate operating system from the home page.

Log into Concourse
------------------

Use the fly cli tool to login to Concourse.

.. code-block:: bash

   fly -t dev0 login -c https://concourse-dev0.openstax.org 

A browser will open where you can login to the server using ldap.

Update or upload the Pipeline
-----------------------------

Use the set-pipeline command to upload/update the pipeline to Concourse.

.. code-block:: bash

   fly -t dev0 set-pipeline -p ui-tests-os-web -c ./concourse/ui-tests-os-web.pipeline.yml
