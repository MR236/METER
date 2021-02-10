Should I use METER?
===================

METER is specifically designed for discrete-time, time-inhomogenous, and acyclic multi-state markov models. To go through each of these elements individually:

- The main assumption of a **markov model** is that the past states of a process do not affect transition probabilites going forward. If you have an application where the previous states of a process are likely to have an effect (if you are studying radiation exposure, for example) this assumption will not hold and you should consider using a semi-markov model.

"""""""""""""""

- **Discrete-time** means that observations are taken at regular time intervals that can be indexed by natural numbers. Typically this means that the data is indexed by days or years. This assumption will not hold for data with inconsistent intervals between observations, which would be typical for clinical data on cancer relapse and many types of survey data. 

"""""""""""""""

- **Acyclic** means that states have a defined order and it is not possible to move backwards to a preceding state. For the time being, METER does not support cyclic models, although this is high on the list of planned improvements. 

"""""""""""""""

- **Time-inhomogenous** means that time from study entry affects the probability of transitions between states. This is typical for data that stretches over long periods of time, where subject age may be a relevant factor. For example, an individual diagnosed with type 2 diabetes at age 20 is going to have a much better short-term survival prognosis than an 80-year-old with the same diagnosis. 

You can still use METER if believe that your process is time-homogenous, but you might have simpler options available. If you want to model a continuous time process, I suggest using the R package `MSM <https://cran.r-project.org/web/packages/msm/index.html>`_.

Installation
===================

Run the following in your command line or python console::

    pip install METER

For a look at past versions or to download files directly, visit `PyPI <https://pypi.org/project/METER/>`_.

