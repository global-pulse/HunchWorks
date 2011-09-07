HunchWorks
==========

From http://www.unglobalpulse.org/blog/why-hunchworks:

> Hunchworks is a tool to enable experts of all kinds to post hypotheses that might warrant further exploration. We hope that it will provide the ability to capture the intuition, gut knowledge and situational awareness of the experts. HunchWorks is also a mechanism to make the membranes between silos of knowledge both inside and outside of the UN more permeable, surfacing the hunches of other researchers and promoting the cross-pollination of ideas and evidence.



Status
------

HunchWorks is currently under heavy development. Nothing works.


Requirements
------------

* Python `>= 2.6`
* Django `== 1.3`


Installation
------------

    # Create an isolated development environment.
    $ virtualenv --no-site-packages --python=python2.6 hunchworks
    $ cd hunchworks
    $ source bin/activate

    # Grab the latest source from GitHub.
    $ git clone git://github.com/global-pulse/HunchWorks.git src
    $ cd src

    # Install development dependencies with Pip.
    $ pip install -r requirements.txt

    # Start the development server.
    $ ./manage.py syncdb
    $ ./manage.py runserver


License
-------

HunchWorks is free software, available under the [GNU GPL v3](http://www.gnu.org/licenses/gpl-3.0.txt).