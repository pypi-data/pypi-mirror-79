***********
IDEM_DARWIN
***********
**Grains, execution modules, and state modules common to all darwin systems**

INSTALLATION
============

Install idem-darwin directly from pip::

    pip install idem-darwin

DEVELOPMENT INSTALLATION
========================


Clone the `idem_darwin` repo and install with pip::

    git clone https://gitlab.com/saltstack/pop/idem-darwin.git idem_darwin
    pip install -e idem_darwin

EXECUTION
=========
After installation the `grains` command should now be available

TESTING
=======
install `requirements-test.txt` with pip and run pytest::

    pip install -r idem_darwin/requirements-test.txt
    pytest idem_darwin/tests

VERTICAL APP-MERGING
====================
Instructions for extending idem-darwin into an OS-specific idem project

Install pop::

    pip install --upgrade pop

Create a new directory for the project::

    mkdir idem_{specific_darwin_os}
    cd idem_{specific_darwin_os}


Use `pop-seed` to generate the structure of a project that extends `grains` and `idem`::

    pop-seed -t v idem_{specific_darwin_os} -d grains exec states

* "-t v" specifies that this is a vertically app-merged project
*  "-d grains exec states" says that we want to implement the dynamic names of "grains", "exec", and "states"

Add "idem_darwin" to the requirements.txt::

    echo idem-darwin >> requirements.txt

And that's it!  Go to town making grains, execution modules, and state modules specific to your specific darwin-based platform.
Follow the conventions you see in idem_darwin.

For information about running idem states and execution modules check out
https://idem.readthedocs.io
