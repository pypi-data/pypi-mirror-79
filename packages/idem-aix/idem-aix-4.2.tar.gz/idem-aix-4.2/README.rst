********
IDEM-AIX
********
**Grains, execution modules, and state modules common to all aix systems**

INSTALLATION
============

Install with pip::

    pip install idem-aix

DEVELOPMENT INSTALLATION
========================


Clone the `idem-aix` repo and install with pip::

    git clone https://gitlab.com/saltstack/pop/idem-aix.git idem_aix
    pip install -e idem_aix

EXECUTION
=========
After installation the `grains` command should now be available

TESTING
=======
install `requirements-test.txt` with pip and run pytest::

    pip install -r idem-aix/requirements-test.txt
    pytest idem-aix/tests

VERTICAL APP-MERGING
====================
Instructions for extending idem-aix into an OS or os specific pop project

Install pop::

    pip install --upgrade pop

Create a new directory for the project::

    mkdir idem-{specific_aix_os}
    cd idem-{specific_aix_os}


Use `pop-seed` to generate the structure of a project that extends `grains` and `idem`::

    pop-seed -t v idem-{specific_aix_os} -d grains exec states

* "-t v" specifies that this is a vertically app-merged project
*  "-d grains exec states" says that we want to implement the dynamic names of "grains", "exec", and "states"

Add "idem-aix" to the requirements.txt::

    echo "idem-aix @ git+https://gitlab.com/saltstack/pop/idem-aix.git" >> requirements.txt

And that's it!  Go to town making grains, execution modules, and state modules specific to your aix os.
Follow the conventions you see in idem-aix.

For information about running idem states and execution modules check out
https://idem.readthedocs.io
