""" Functions for preparing the data to construct multi-state life tables """

import numpy as np
import pandas as pd
import copy


def wide_format(data, transition_names, exit):
    """
    Take data with transitions as calendar dates and expand for life table construction. If multiple transitions occur at the same time (i.e. in the same year or day) then only the final transition is counted as occuring.

    Parameters
    ----------
    data : pandas dataframe
        the data, with dates of all transitions, with one subject per line

    transition_names: list
        a list of the names of the columns that contain the transition years

    exit: string
        the name of the column indicating final follow-up date for each subject

    Returns
    ----------
    pandas dataframe
        a dataframe with additional columns for:

        - transitions as time from study entry
        - transition status columns indicating whether such a transition ever occurred
        - a column final_age, for age at study close-out

    """
    df = data.copy()
    df = df.replace(({np.nan: None}))
    df['final age'] = df[exit] - df[transition_names[0]]
    for i in range(1, len(transition_names) - 1):
        # here we ensure that a later transition in the same year always supersedes
        df[transition_names[i]] = np.where(df[transition_names[i]] == df[transition_names[i+1]], None, df[transition_names[i]])
    for i in transition_names:
        df[i + "_status"] = [0 if x is None else 1 for x in df[i]]
        df[i + "_age"] = np.where(df[i + "_status"] == 0, df['final age'], df[i] - df[transition_names[0]])
    return df


def allowed_transitions(states):
    """
    this function takes a set of states and uses it to compute the allowed transitions
    it assumes the model is acyclic ie. individuals can only transition towards states
    to the right of it in the list

    Parameters
    ----------

    states: a list with the set of states in the desired model (eg. ["Person", "Performer", "Death"])

    Returns
    ----------

    a list that has all of the transitions possible as pairs (two-element lists)

    """
    lst = []
    for i in range(0, len(states)):
        for j in range(i+1, len(states)):
            lst.append([i, j])
    return lst


def censor(data, transition, transition_names):
    """

    censor all individuals in a dataframe at a given state

    Parameters
    ----------

    transition: the column name in the original dataset that represented transitions into the state
    you want to censor at (ex. First_Film)

    transition_names: a list of the names of the columns that contain the transition years
    ex. ['Birth', 'First_Film', 'Death'] with first taken as study entry

    data: the dataframe in wide format as created by the wide_format function

    Returns
    ----------

    a new dataframe where all individuals have been censored at the desired state

    """
    newdata = data.copy()
    t_number = transition_names.index(transition)
    for i in range(t_number, len(transition_names) - 1):
        newdata['final age'] = np.where(data[transition_names[i] + "_status"] == 1, data[transition_names[i] + "_age"], data['final age'])
        newdata[transition_names[-1] + "_status"] = np.where(data[transition_names[i] + "_status"] == 1, 0, data[transition_names[-1] + "_status"])
        newdata[transition_names[-1] + "_age"] = np.where(data[transition_names[i] + "_status"] == 1, float('NaN'), data[transition_names[-1] + "_age"])
    return newdata
