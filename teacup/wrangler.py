""" Functions for preparing the data to construct multi-state life tables """

import pandas as pd
import numpy as np


def wide_format(data, transitions, entry, exit):
    """
    Take data with transitions as calendar dates and expand for life table construction

    Parameters
    ----------

    data: the data, with year dates of all transitions, with one subject per line

    transitions: a list of the names of the columns that contain the transition years ex. ["Nominee", "Winner", "Death"]

    exit: the name of the column indicating final follow-up year for each subject ex. "Final"

    entry: the name of the column indicating year of study entry

    Returns
    ----------

    a dataframe in wide format with additional columns for:
    - transitions as years from birth
    - transition status columns indicating whether such a transition ever occurred
    - a column final_age, for age at study close-out

    """
    df = data.copy()
    df['final age'] = df[exit] - df[entry]
    for i in range(0, len(transitions) - 2):
        # here we ensure that a later transition in the same year always supersedes
        df[transitions[i]] = np.where(df[transitions[i]] == df[transitions[i+1]], None, df[transitions[i]])
    for i in transitions:
        df[i + "_status"] = [0 if x is None else 1 for x in df[i]]
        df[i + "_age"] = np.where(df[i + "_status"] == 0, df['final age'], df[i] - df[entry])
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


def df_to_list(data):
    """
    this function converts a pandas dataframe to a list of rows for faster computation

    Parameters
    ----------

    data: the dataframe

    Returns
    ----------

    the dataframe as a list of rows

    """
    row_list = []
    for i in range((data.shape[0])):
        row_list.append(list(data.iloc[i, :]))
    return row_list