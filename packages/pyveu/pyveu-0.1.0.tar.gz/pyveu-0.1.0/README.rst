pyveu -- Value Error Unit
=================================

.. image:: https://gitlab.sauerburger.com/frank/pyveu/badges/master/pipeline.svg
        :target: https://gitlab.sauerburger.com/frank/pyveu/-/pipelines

.. image:: https://gitlab.sauerburger.com/frank/pyveu/badges/master/coverage.svg
        :target: https://gitlab.sauerburger.com/frank/pyveu

.. image:: https://gitlab.sauerburger.com/frank/pyveu/-/jobs/artifacts/master/raw/license.svg?job=badges
        :target: https://gitlab.sauerburger.com/frank/pyveu/-/blob/master/LICENSE

.. image:: https://gitlab.sauerburger.com/frank/pyveu/-/jobs/artifacts/master/raw/pypi.svg?job=badges
        :target: https://pypi.org/project/pyveu/

.. image:: https://readthedocs.org/projects/pyveu/badge/?version=latest&amp;style=flat
        :target: https://pyveu.readthedocs.io/en/latest/

.. image:: https://mybinder.org/badge_logo.svg
        :target: https://mybinder.org/v2/git/https%3A%2F%2Fgitlab.sauerburger.com%2Ffrank%2Fpyveu-playground.git/master?filepath=pyveu-playground.ipynb


The python package pyveu (Value Error Unit) handles real-life experimental
data which includes uncertainties and physical units. The package implements
arithmetic operations and many mathematical functions for physical quantities.
Gaussian error propagation is used to calculate the uncertainty of derived
quantities.

The package is built with the day-to-day requirements of people working a
laboratory kept in mind. The package offers an imperative programming style,
which means that the operations are evaluated when they are typed
interactively in python, giving researchers the freedom and flexibility they
need.


Quickstart
==========

Install the package using pip

.. code-block:: console

   $ pip install pyveu


The working horse of the package is the `pyveu.Quantity
<https://pyveu.readthedocs.io/en/latest/api_reference.html#quantity>`_ class. It can be
used to convert units, for example, it can convert meter per second into kilometer
per hour.

>>> from pyveu import Quantity
>>> speed = Quantity("32 +- 3 m / s")
>>> speed.str("km / hr")
'(115 +- 11) km / hr'

Quantities from a measurement usually come with a measurement uncertainty. The
class `pyveu.Quantity
<https://pyveu.readthedocs.io/en/latest/api_reference.html#quantity>`_ propagates the uncertainty automatically.

>>> time = Quantity("3.23 +- 0.1 min")
>>> distance = speed * time
>>> distance.str("km")
'(6.2 +- 0.6) km'

Binder
======

Try pyveu without installation right from your browser:

.. image:: https://mybinder.org/badge_logo.svg
 :target: https://mybinder.org/v2/git/https%3A%2F%2Fgitlab.sauerburger.com%2Ffrank%2Fpyveu-playground.git/master?filepath=pyveu-playground.ipynb


Links
=====

 * `GitLab Repository <https://gitlab.sauerburger.com/frank/pyveu>`_
 * `Documentation <https://pyveu.readthedocs.io/>`_
 * `pyveu on PyPi <https://pypi.org/project/pyveu>`_
