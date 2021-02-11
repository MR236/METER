Constructing Multi-State Life Tables
======================================

The first step to using METER is to have your data in the correct format. The data should have one subject per row, and have columns containing each of the transition times. Transition times can be specified as calendar dates or time from study entry, as the wide_format function will convert everything into the latter format. 

To obtain the transition matrices of the multi-state model you should do the following:
    1. Use :py:func:`.wide_format` to obtain the data in wide format.
    2. Use :py:func:`.atrisk_and_transitions` to obtain the risk sets and number of transitions made at each time point. 
    3. Use :py:func:`.transitionprobs_and_samplesizes` to obtain the transition matrices for each time point, and the associated sample sizes. 

If you don't need the transition probabilities directly, and just want associated life expectancies or other survival estimates, you can just do step one and then skip forward to the section on generating estimates. 

.. note:: You should still be running wide_format even if your data already has transition times specified as time from study entry. This is because the wide_format function creates status columns that indicate whether each transition ever occured for a given subject, and ensures that there is only one transition per year. 

METER also allows you to censor data at a given state. This is often useful for reasons mentioned in :ref:`Life Expectancies`. If you want to censor your data, you should do this immediately after step 1 above, using :py:func:`.censor`.

.. autofunction:: METER.wrangler.wide_format

.. autofunction:: METER.table.atrisk_and_transitions

.. autofunction:: METER.table.transitionprobs_and_samplesizes

.. autofunction:: METER.wrangler.censor