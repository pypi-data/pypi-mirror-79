
Summit
======

.. image:: docs/source/_static/banner_4.png
   :target: docs/source/_static/banner_4.png
   :alt: summit_banner


Summit is a set of tools for optimising chemical processes. We’ve started by targeting reactions.

What is Summit?
---------------

Currently, reaction optimisation in the fine chemicals industry is done by intuition or design of experiments,  Both scale poorly with the complexity of the problem. 

Summit uses recent advances in machine learning to make the process of reaction optimisation faster. Essentially, it applies algorithms that learn which conditions (e.g., temperature, stoichiometry, etc.) are important to maximising one or more objectives (e.g., yield, enantiomeric excess). This is achieved through an iterative cycle.

Summit has two key features:


* **Strategies**\ : Optimisation algorithms designed to find the best conditions with the least number of iterations. Summit has eight strategies implemented.
* **Benchmarks**\ : Simulations of chemical reactions that can be used to test strategies. We have both mechanistic and data-driven benchmarks.

To get started, see the Quick Start below or follow our `tutorial <https://gosummit.readthedocs.io/en/latest/tutorial.html>`_. 

Installation
------------

To install summit, use the following command:

``pip install git+https://github.com/sustainable-processes/summit.git#egg=summit``

Quick Start
-----------

Below, we show how to use the Nelder-Mead  strategy  to optimise a benchmark representing a nucleophlic aromatic substitution (SnAr) reaction.

.. code-block:: python

   # Import summit
   from summit.benchmarks import SnarBenchmark, MultitoSingleObjective
   from summit.strategies import NelderMead
   from summit.run import Runner

   # Instantiate the benchmark
   exp = SnarBenchmark()

   # Since the Snar benchmark has two objectives and Nelder-Mead is single objective, we need a multi-to-single objective transform
   transform = MultitoSingleObjective(
       exp.domain, expression="-sty/1e4+e_factor/100", maximize=False
   )

   # Set up the strategy, passing in the optimisation domain and transform
   nm = NelderMead(exp.domain, transform=transform)

   # Use the runner to run closed loop experiments
   r = Runner(
       strategy=nm, experiment=exp,max_iterations=50
   )
   r.run()

Documentation
-------------

The documentation for summit can be found `here <https://gosummit.readthedocs.io/en/latest/index.html>`_.

Issues?
-------

Submit an `issue <https://github.com/sustainable-processes/summit/issues>`_ or send an email to kcmf2@cam.ac.uk.
