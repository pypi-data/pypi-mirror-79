=====
proma
=====


.. image:: https://img.shields.io/pypi/v/proma.svg
        :target: https://pypi.python.org/pypi/proma

.. image:: https://readthedocs.org/projects/proma/badge/?version=latest
        :target: https://proma.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://gitlab.com/ydethe/proma/badges/master/pipeline.svg
   :target: https://gitlab.com/ydethe/proma/pipelines

.. image:: https://codecov.io/gl/ydethe/proma/branch/master/graph/badge.svg
  :target: https://codecov.io/gl/ydethe/proma


A set of tools to manipulate a python package without a setup.py


Documentation
-------------

Pour générer la documentation du code, lancer::

    python setup.py doc

Tests
-----

Pour lancer les tests::

    tox -e py

Si tout va bien, vous devriez avoir la sortie suivante::

    Ran 1 tests in 2.56s

    ---------------------------- generated xml file: /Users/ydethe/Documents/repos/proma/test-results/junit.xml -----------------------------

    ---------- coverage: platform darwin, python 3.8.5-final-0 -----------
    Name                Stmts   Miss  Cover
    ---------------------------------------
    proma/__init__.py      13      0   100%
    proma/__main__.py      18     14    22%
    proma/proma.py         64     36    44%
    ---------------------------------------
    TOTAL                  95     50    47%


    OK
    ________________________________________________________________ summary ________________________________________________________________
    py: commands succeeded
    congratulations :)

Rapport de couverture des tests
-------------------------------

Une fois les tests lancés, le rapport de couverture des tests est disponible ici:

https://codecov.io/gl/ydethe/proma

Installation
------------

Pour installer la librairie et les outils associés, lancer::

    python setup.py install --user

