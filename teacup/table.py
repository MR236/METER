""" Functions for generating multi-state life tables """
import wrangler as wr
import numpy as np
import pandas as pd


def atrisk_and_transitions(data, transition_names, states):
    """
    Get the number of individuals in a given state at a given age, and number of transitions at each age.

    Parameters
    ----------

    data: the data in wide format as generated by wide_format function

    transition_names: a list of the names of the columns that contain the transition years
    ex. ['Birth', 'First_Film', 'Death'] with first taken as study entry

    states: the names of the states in the model, the entry into each of which should
    correspond to the columns in transition_names

    Returns
    ----------

    a two element list with:
    - first element a dataframe containing the risk sets for each year
    - second element a dataframe containing the number of transitions of each type in each year

    """
    t_statuses = ['{}_status'.format(a) for a in transition_names]
    t_ages = ['{}_age'.format(a) for a in transition_names]
    column_positions = {}
    for i in range(0, len(data.columns)):
        column_positions[data.columns[i]] = i
    for i in range(0, len(transition_names)):
        t_statuses[i] = column_positions[t_statuses[i]]
        t_ages[i] = column_positions[t_ages[i]]
    max_age = data['final age'].max() # need the final age so we know how many age specific arrays needed
    row_list = wr.df_to_list(data)
    allowable_transitions = wr.allowed_transitions(states)
    transitions = []
    at_risk = []
    for i in range(0, max_age+1): # create an array containing the number of people in each state for every age in the study
        at_risk.append([])
        transitions.append([[0 for x in range(len(states))] for y in range(len(states))])
    for i in at_risk:
        for z in states:
            i.append(0)
    at_risk[0][0] = len(data) # initially, everyone is in state 1
    for i in row_list:
        current_state = 0
        perf_max_age = i[column_positions["final age"]]
        n = 1
        while n <= perf_max_age:
            at_risk[n][current_state] += 1
            for z in range(current_state, len(states)):
                if i[t_ages[z]] == n and i[t_statuses[z]] == 1:
                    transitions[n][current_state][z] += 1
                    current_state = z
            n += 1
    riskdf = pd.DataFrame(at_risk, columns=states)
    riskdf.index.name = 'age'
    transitionsdf = []
    for z in range(0, max_age+1):
        translst = []
        for i in allowable_transitions:
            translst.append(transitions[z][i[0]][i[1]])
        transitionsdf.append(translst)
    names = []
    for i in allowable_transitions:
        names.append(states[i[0]] + "->" + states[i[1]])
    transdf = pd.DataFrame(transitionsdf, columns=names)
    transdf.index.name = 'age'
    return([riskdf, transdf])


def transitionprobs_and_samplesizes(riskdf, transdf, states):
    """
    Get the number of individuals in a given state at a given age, and number of transitions
    at each age.

    Parameters
    ----------

    riskdf: a dataframe with the number of individuals in each state, indexed at each age. This is
    the first output from the at_risk_and_transitions function.

    transdf: a dataframe containing the number of transitions of each type in each year. The second
    output from the at_risk_and_transitions function.

    states: the names of the states in the model, the entry into each of which should
    correspond to the columns in transition_names.

    Returns
    ----------

    a two element list with:
    - first element a list containing the transition matrix ("kernel") for each year
    - second element a list containing the sample size for each transition in each year

    """
    numstates = len(states)
    raw_transitions = np.full((numstates, numstates, len(riskdf)), 0)
    raw_SS = np.full((numstates, numstates, len(riskdf)), 0)
    allowable_transitions = wr.allowed_transitions(states)
    for n in range(0, len(allowable_transitions)):
        fromstate = states[allowable_transitions[n][0]]
        tostate = states[allowable_transitions[n][1]]
        transition = fromstate + "->" + tostate
        raw_transitions[allowable_transitions[n][0], allowable_transitions[n][1]] = transdf[transition].to_numpy()
        raw_SS[allowable_transitions[n][0], allowable_transitions[n][1]] = riskdf[fromstate].to_numpy()
    samplesizes = raw_SS.transpose((2, 1, 0))
    transmat = np.divide(raw_transitions.transpose((2, 1, 0)), samplesizes,out=np.zeros(samplesizes.shape, dtype=float), where=samplesizes!=0)
    for i in range(0, numstates):
        transitions_out = []
        for z in allowable_transitions:
            if i == z[0]:
                transitions_out.append(z)
        for x in range(0, len(transmat)):
            stay_prob = 1
            for q in transitions_out:
                stay_prob -= transmat[x][q[1], q[0]]
            transmat[x][i,i] = stay_prob
    return [transmat, samplesizes]


def survivorship_vector(transmat, radix, initial_age, states):
    """

    Predict the expected proportion of a population being in a given state at each age based on some
    initial age and number of individuals currently in each state. To get probabilities for one individual,
    simply proceed for a 1-individual population.

    Parameters
    ----------

    transmat: a list of numpy matrices that represent the transition probabilities at each
    age. This is the first output from transitionprobs_and_samplesizes

    states: the names of the states in the model, the entry into each of which should
    correspond to the columns in transition_names.

    radix: an initial condition for the number of performers in each state we want to model, specified
    as a numpy vector. For example, if we wanted the probabilities of being in each state for
    1 individual starting at the first state in a 6-state model the radix would be generated by
    np.array([[1],[0],[0],[0],[0],[0]], dtype=float).

    initial_age: the initial age to model the survivorship outcomes from, so an integer from 0 to
    the oldest age in the dataset


    Returns
    ----------

    a dataframe with the expected proportion of the population in each state at each age past the
    initial age given

    """
    rows = []
    l = radix
    for i in range(initial_age, len(transmat)):
        l = np.matmul(transmat[i], l)
        rows.append((l.transpose().flatten().tolist()))
    survdf = pd.DataFrame(rows, columns=states)
    survdf.index.name = "age"
    survdf.index += initial_age
    return survdf



