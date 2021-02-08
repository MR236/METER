""" Functions for generating plots from multi-state life tables """
import matplotlib.pyplot as plt


def survivorship_graph(survdf, states, colors, order='default'):
    """

    Take data with transitions as calendar dates and expand for life table construction

    Parameters
    ----------

    survdf: a dataframe containing the given probabilities of being in each state at each age for some
    initial condition. This is precisely the output of survivorship_vector.

    states:  a python list with the set of states in a given model
    (eg. ["Person", "Performer", "Nominee", "Dead"])

    order: the order you want the states to be from top to bottom in the graph. The default is reverse order,
    which is fairly visually appealing. If an input is passed it should be something like [0,1,2,3] with 0
    representing the first state, 1 the second state, etc.

    colors: a list of colors accepted by matplotlib (as strings) that matches the number of states

    Returns
    ----------

    a graph of state proportions for some initial conditions

    """
    if order == 'default':
        order = [i for i in range(len(states)-1, -1, -1)]
    survacc = survdf.divide(survdf.sum(axis=1), axis=0)
    for i in states:
        survacc[i] *= 100
    newstates = []
    for i in order:
        newstates.append(states[i])
    barWidth = 1.0
    plt.bar(survacc.index, survacc[newstates[0]], color=colors[0], edgecolor=colors[0], width=barWidth, label=newstates[0])
    bot = survacc[newstates[0]]
    for i in range(1, len(newstates)):
        plt.bar(survacc.index, survacc[newstates[i]], bottom=bot, color=colors[i], edgecolor=colors[i], width=barWidth, label=newstates[i])
        bot += survacc[newstates[i]]
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1), ncol=1, title="State")
    plt.box(on=False)
    plt.subplots_adjust(right=0.75)
    plt.margins(0, 0)
    plt.title("Probability of being in State by Age")
    plt.xlabel("Age, y")
    plt.ylabel("Probability, %")
    return plt


