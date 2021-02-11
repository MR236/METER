Generating Survival Estimates
====================================

Survival Predictions
-----------------------

First, make sure that you have generated the :ref:`transition matrices<Constructing Multi-State Life Tables>`. 

Future state probabilites for any population of individuals from an initial time can be generated using :py:func:`.survivorship_vector`. The most common application is likely to be generating future state probabilities for one individual, which can be obtained by specifying a radix with a 1 in the position of the state you want to predict from. At this point you can also generate a life expectancy for an individual starting in any state at any time from study entry using :py:func:`.life_expectancy`, although it is possible to use :py:func:`.censorLE` to obtain this directly from the data in wide format. 

.. note:: It is implicitly assumed that the final state in your model is death, but this will also work for other outcomes that are the terminal state of a study. For example, if your study outcome is the age of reaching menopause then the life expectancy function will still give you a valid estimate. 

.. autofunction:: METER.table.survivorship_vector

.. autofunction:: METER.table.life_expectancy

Life Expectancies
------------------------

For the methods in this section, it is not necessary to have obtained the transition matrices. However, make sure that you have used :py:func:`.wide_format` to get the data in the correct format. 

METER permits 4 different ways of characterizing an individual when computing life expectancies:

- The **initial state** is the state that the individual starts in, and is required whenever you ask METER to compute life expectancy point estimates or confidence intervals. 

"""""""""""""""""""""""""""""""""""""

- The **initial time** is the time point that you are predicting from. METER always gives life expectancy from this point forwards, so if you want absolute life expectancy estimates from study entry you should add this on after you've obtained the estimates. 

"""""""""""""""""""""""""""""""""""""

- A **censor state** is a state that you want to restrict the individual from moving beyond. This is useful for applications where you want to assess the life expectancy effect of attaining a certain state (eg. an award or military rank) and want to prevent your estimates for the control group from being affected by potential future transitions to that state. 

"""""""""""""""""""""""""""""""""""""

- Finally, you can specify any arbitrary set of **covariate conditions** for subgroup analysis. For the time being these need to be categorical covariates, although this is on the list of improvements for future versions. 

Point estimates of life expectancy can be obtained using :py:func:`.censorLE` directly from the data in wide format. As mentioned above, the initial state is a mandatory input. Unless the other conditions mentioned are specified, METER will assume that you want estimates from study entry (time point 0), with no censoring, and with no covariate restrictions.

To obtain confidence intervals by non-parametric bootstrap, you can use :py:func:`.bootstrapLE` to get a dataframe of bootstrap runs, and then use :py:func:`.summary_results` to obtain the confidence intervals and point estimates. METER allows you to run the bootstrap for any arbitrary set of groups, each defined by different initial states, censor states, and covariate restrictions. The initial time must be constant over each of these groups, because METER also provides confidence intervals and point estimates for the difference between these groups, and those measures only make sense if each group begins at the same time point from study entry.

METER is fast. 1000 bootstraps on a dataset of 5000 individuals with less than 10 states in the model for less than 5 groups should take under 15 minutes. If you want a log of how far your bootstrap has progressed printed to the console set loud=TRUE, and you will know whether you have time to go get a coffee. 

.. note:: If you are comparing life expectancies for a number of different groups, I highly recommend using the group_names input to bootstrapLE. By default the groups will be named based on the initial states and these names may not be unique, which could cause a great deal of confusion. 

.. autofunction:: METER.table.censorLE

.. autofunction:: METER.summaries.bootstrapLE

.. autofunction:: METER.summaries.summary_results
