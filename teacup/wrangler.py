""" Functions for preparing the data to construct multi-state life tables """

import pandas as pd
import numpy as np

def wide_format(data, transitions, entry, exit):
    """
    Take data with transitions as calendar dates and expand for life table construction

    Parameters
    ----------

    data: the data, with year dates of all transitions, with one subject per line

    transitions: a list of the names of the columns that contain the transition years ex. ["Birth", "Death"]

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
