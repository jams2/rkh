RKH
===

Installation
------------

To get the install up and running

.. code-block:: bash

   $ git clone https://github.com/jams2/rkh.git && cd rkh
   $ python3 -m venv venv
   $ . venv/bin/activate
   $ pip install -r requirements.txt
   $ python manage.py migrate
   $ python manage.py createsuperuser
   $ python manage.py runserver

You should then be able to access the site at the usual place, http://localhost:8000.
