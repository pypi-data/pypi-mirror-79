************
IDEM_SOLARIS
************
**Grains, execution modules, and state modules common to all solaris systems**

INSTALLATION
============

Install idem-solaris directly from pip::

    pip install idem-solaris

DEVELOPMENT INSTALLATION
========================


Clone the `idem_solaris` repo and install with pip::

    git clone https://gitlab.com/saltstack/pop/idem-solaris.git idem_solaris
    pip install -e idem_solaris

EXECUTION
=========
After installation the `grains` command should now be available

TESTING
=======
install `requirements-test.txt` with pip and run pytest::

    pip install -r idem_solaris/requirements-test.txt
    pytest idem_solaris/tests

VERTICAL APP-MERGING
====================
Instructions for extending pop-solaris into an OS-specific pop project

Install pop::

    pip install --upgrade pop

Create a new directory for the project::

    mkdir pop_{specific_solaris}
    cd pop_{specific_solaris_os}


Use `pop-seed` to generate the structure of a project that extends `grains` and `idem`::

    pop-seed -t v pop_{specific_solaris_os} -d grains exec states

* "-t v" specifies that this is a vertically app-merged project
*  "-d grains exec states" says that we want to implement the dynamic names of "grains", "exec", and "states"

Add "idem_solaris" to the requirements.txt::

    echo "idem_solaris @ git+https://gitlab.com/saltstack/pop/idem_solaris.git" >> requirements.txt

And that's it!  Go to town making grains, execution modules, and state modules specific to your specific solaris-based platform.
Follow the conventions you see in idem_solaris.

For information about running idem states and execution modules check out
https://idem.readthedocs.io
