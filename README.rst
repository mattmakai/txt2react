============
Txt 2 React
============


Contact Information
===================
Matt Makai (matthew.makai@gmail.com) is the primary maintainer of this
project.


Environment Configuration
=========================
I develop and test in the Ubuntu 12.04 LTS environment.
 
Code
----
Grab the code grab Github::
    
    $ git clone git@github.com:makaimc/txt2react.git

The rest of the installation instructions will assume you cloned the repo
to ~/devel/py/txt2react/.


Dependencies
------------
Isolate the program in its own virtualenv and install the project
dependencies::
 
    $ virtualenv --distribute ~/Envs/t2r

If you're using 
`virtualenvwrapper <http://virtualenvwrapper.readthedocs.org/en/latest/>`_
use this command instead::

    $ mkvirtualenv t2r

Activate your environment and install the dependencies::

    $ source ~/Envs/t2r/bin/activate
    $ cd ~/devel/t2r
    $ pip install -r requirements.txt
    $ pip install -r requirements/local.txt


Environment Variables
---------------------
This project does not use a local_settings.py template file, instead there's 
a template for exporting environment variables in your local operatins system. 
Copy set_envs.sh.template to set_envs.sh and fill in your development 
environment settings.

You'll need to run the environment variables script after you activate
your virtualenv::

    (t2r)$ cd ~/devel/t2r
    (t2r)$ . ./set_envs.sh

Now your database and other settings such as the DEBUG flag are set so
the settings.py file can pick them up from the shell environment.

For convenience I usually set a line in my ~/.bashrc file to quickly switch
to the environment. This requires virtualenv and virtualenvwrapper::

    alias t2r='workon t2r; cd ~/devel/py/txt2react; . ./set_envs.sh;'


License and Documentation
-------------------------
Txt 2 React is free software under the MIT license. 

