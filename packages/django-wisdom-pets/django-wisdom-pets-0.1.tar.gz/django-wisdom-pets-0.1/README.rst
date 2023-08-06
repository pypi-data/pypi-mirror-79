=========
Adoptions
=========

Adoptions is a django app to manage pet adoptions.
For now, you can view all pets and view specific pet details

Detailed documentation is in the docs directory

Quick start
-----------
1. Add "adoptions" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'adoptions',
    ]


2. Include the adoptions URLconf in your project urls.py like this::

    path('adoptions/', include('adoptions.urls')),

3. Run ``python manage.py migrate`` to create the adoptions models.

4. Start the development server and visit http://127.0.0.1:8000/adoptions/
   to view adoptions.

5.