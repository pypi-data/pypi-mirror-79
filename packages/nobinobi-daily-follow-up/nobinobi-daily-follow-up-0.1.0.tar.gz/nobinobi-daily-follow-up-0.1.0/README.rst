=============================
Nobinobi Daily Follow-Up
=============================

.. image:: https://badge.fury.io/py/nobinobi-daily-follow-up.svg
    :target: https://badge.fury.io/py/nobinobi-daily-follow-up

.. image:: https://travis-ci.org/Sicilia04/nobinobi-daily-follow-up.svg?branch=master
    :target: https://travis-ci.org/Sicilia04/nobinobi-daily-follow-up

.. image:: https://codecov.io/gh/Sicilia04/nobinobi-daily-follow-up/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/Sicilia04/nobinobi-daily-follow-up

Module Daily follow-up for nobinobi

Documentation
-------------

The full documentation is at https://nobinobi-daily-follow-up.readthedocs.io.

Quickstart
----------

Install Nobinobi Daily Follow-Up::

    pip install nobinobi-daily-follow-up

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'nobinobi_daily_follow_up.apps.NobinobiDailyFollowUpConfig',
        ...
    )

Add Nobinobi Daily Follow-Up's URL patterns:

.. code-block:: python

    from nobinobi_daily_follow_up import urls as nobinobi_daily_follow_up_urls


    urlpatterns = [
        ...
        url(r'^', include(nobinobi_daily_follow_up_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox


Development commands
---------------------

::

    pip install -r requirements_dev.txt
    invoke -l


Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
