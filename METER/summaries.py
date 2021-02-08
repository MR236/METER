""" Functions for generating statistical summaries from multi-state life tables """
import numpy as np
import pandas as pd
import itertools
import METER.table as tb


def bootstrapLE(data, transition_names, states, censor_states, n=1000, initial_age=0, initial_states='default', group_names='default', conditions='default', loud=False):
    """

    Run a bootstrap on the life expectancy for a given set of groups and their differences

    Parameters
    ----------

    data: the data in wide format as generated by wide_format function

    transition_names: a list of the names of the columns that contain the transition years
    ex. ['Birth', 'First_Film', 'Death'] with first taken as study entry.

    states: the names of the states in the model, the entry into each of which should
    correspond to the columns in transition_names.

    censor_states: the states you want each group's life expectancy to be censored at. If you don't want
    any censoring then just pick the final non-death state for every group.

    n: the number of bootstraps to run, by default 1000.

    initial_age: optional input if you want to estimate life expectancy after a given age

    initial_states: by default the same as the censor states above, should be a list of the same length as groups
    that governs which initial state you want to estimate life expectancy for individuals in that group
    from.

    group_names: what the groups (whose structure is defined both by the initial states and censor states given)
    are to be called. by default this is the same as the censor states.

    conditions: a list of sets of conditions you want each group to be subject to (by default none).
    ex. [{'Male_1': 0}, {'Male_1': 1}

    loud: by default this is false. If it is set to true a small summary of the results of each bootstrap
    as well as the best estimate calculated initially are printed to the console.

    Returns
    ----------

    A dataframe containing the results of each run of the bootstrap. Each row will include that
    bootstrap life expectancy for each group as well as each of the possible group differences.

    """
    if initial_states == 'default':
        initial_states = censor_states
    if group_names == 'default':
        group_names = censor_states
    if conditions == 'default':
        conditions = [{}] * len(censor_states)
    rows = []
    colnames = []
    results = []
    for i in range(0, len(censor_states)):
        results.append(tb.censorLE(data, transition_names, states, censor_states[i], initial_age, initial_states[i], conditions[i]))
    if loud:
        print("BEST ESTIMATE")
    for i in range(0, len(results)):
        if loud:
            print(group_names[i] + " Life Expectancy: " + str(results[i]))
        colnames.append(group_names[i] + " Life Expectancy")
    pair_results = []
    for pair in itertools.combinations([i for i in range(0, len(results))], 2):
        diff = results[pair[0]] - results[pair[1]]
        pair_results.append(diff)
        colnames.append(group_names[pair[0]] + "-" + group_names[pair[1]] + " Difference")
        if loud:
            print(group_names[pair[0]] + "-" + group_names[pair[1]] + " Difference: " + str(diff))
    rows.append(results + pair_results)
    for i in range(0, len(rows[0])):
        rows[0][i] = round(rows[0][i], 1)
    for i in range(0, n):
        boot_df = data.sample(frac=1, replace=True)
        results = []
        for y in range(0, len(censor_states)):
            results.append(tb.censorLE(boot_df, transition_names, states, censor_states[y], initial_age, initial_states[y], conditions[y]))
        if loud:
            print("BOOT RUN " + str(i + 1))
        if loud:
            for y in range(0, len(results)):
                print(group_names[y] + " Life Expectancy: " + str(results[y]))
        pair_results = []
        for pair in itertools.combinations([x for x in range(0, len(results))], 2):
            diff = results[pair[0]] - results[pair[1]]
            pair_results.append(diff)
            if loud:
                print(group_names[pair[0]] + "-" + group_names[pair[1]] + " Difference: " + str(diff))
        rows.append(results + pair_results)
    boot_results = pd.DataFrame(rows,columns=colnames)
    boot_results.index.name = "Bootstrap Run"
    boot_results.rename(index={0: 'Best Estimate'}, inplace=True)
    return boot_results


def confidence_interval(data, column_name, confidence_level):
    """

    get a 95% confidence interval from a bootstrap dataframe column

    Parameters
    ----------

    data: the bootstrap results dataframe

    column_name: the statistic that you want the interval for, specified by the name of the column
    containing it (eg. "Nominee Life Expectancy").

    confidence_level: a real number between 0 and 1 that represents the desired confidence level.
    eg. 0.95 for 95%.

    Returns
    ----------

    A two-element list with the lower bound and upper bound.

    """
    results = data[column_name].tolist()
    results.sort()
    lower_bound = int((1 - confidence_level) / 2 * len(results)) - 1
    upper_bound = int((confidence_level + 1) / 2 * len(results)) - 1
    if lower_bound < 0:
        lower_bound = 0
    return [round(float(results[lower_bound]), 1), round(float(results[upper_bound]), 1)]


def summary_results(bootstrap):
    """

    Summarize the results of a bootstrap.

    Parameters
    ----------

    bootstrap: the dataframe containing all the bootstrap runs, with the topline result in the first row.

    Returns
    ----------

    A dataframe summarizing the point estimates and confidence intervals for each quantity.

    """
    best_estimates = []
    confidence_intervals = []
    for col in bootstrap.columns:
        best_estimates.append(bootstrap[col]['Best Estimate'])
    boot_df = bootstrap.drop(['Best Estimate'])
    boot_df.index.name = 'Bootstrap Run'
    for col in boot_df.columns:
        confidence_intervals.append(confidence_interval(boot_df, col, 0.95))
    summary_column = []
    for i in range(0, len(best_estimates)):
        summary_column.append(str(best_estimates[i]) + " " + str(confidence_intervals[i]))
    index = boot_df.columns
    sum_df = pd.DataFrame(list(zip(summary_column, index)),columns=['Multi-State Modelling (Estimate [CI])', 'Measure'])
    return sum_df