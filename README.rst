timeflow
=======

CLI app for time logging

Usage
-----

Go to `timeflow` directory and install it.

.. code:: python

    pip install --editable .

To log your work events:

.. code:: python

    timeflow log 'My work'

In `~/.timeflow` log message will be added.

To edit your log file

.. code:: python

    timeflow edit # opens timeflow log with editor set in $EDITOR
    timeflow edit -e, --editor EDITOR # opens timeflow log with sepcified EDITOR
