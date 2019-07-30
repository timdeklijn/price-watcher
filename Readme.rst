price-watcher
=============

Short description
-----------------

Scrape the webpage given in the config to find the price of the product. For now this code works for the Playstation network. And then send the resulting plot to the user's email adress.

Local install
-------------

- Create ``bucket/config.json`` from ``bucket/config.example.json`` and add links to PSN sites to scrape
- Install dependencies::

    pip install -r requirements.txt

- Run the package::

    python -m main.py

Docker (local)
--------------

- Build docker container (local)::

    ./docker_build_command.sh

- Run docker container (local)::

    ./docker_run_command.sh

Github page
-----------

`github <https://github.com/timdeklijn/price-watcher>`_

TODO
----

#. [x] Convert to package
#. [x] Finish email module

    #. [x] Create email
    #. [x] Finish code

#. [x] Dockerize the code

    #. [x] Install and test Docker
    #. [x] Create docker file and test

#. [ ] Connect to bucket on cloud platform
#. [ ] Register to container registry
#. [ ] Add CI/CD flow to project.
#. [ ] Finish documentation