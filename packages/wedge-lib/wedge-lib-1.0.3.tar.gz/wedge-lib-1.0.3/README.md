Django Wedge lib
====================

Django Wedge lib is a Django app to conduct and test REST API based projects.

Quick start
-----------

1. Add "polls" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'w',
    ]

2. Include pytest settings in the pytest config file like this::

    from w.settings.pytest import *

