# -*- coding: utf-8 -*-
#
# Newman_Modularity.py - Greedy method of Newman to maximize modularity

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

def finding_pair(e):
    """
    do a single iteration of greedy-modularity algorithm

    Parameters
    ----------
    e : numpy.array

    Returns
    -------
    link : tuple
    """
    J = nx.from_numpy_matrix(e - np.diag(np.diag(e)))
    e_in  = np.diag(e)
    e_out = list(dict(J.degree(weight='weight')).values())
    com_links = J.edges()

    delta = []
    for link in com_links:
        d = 2 * (com_links[link[0], link[1]]['weight'] - (e_out[link[0]] + e_in[link[0]]) * (e_out[link[1]] + e_in[link[1]]))
        delta.append(d)

    max_index = np.array(delta).argmax()
    link = list(com_links)[max_index]
    return link


def update_community(e, link, Community):
    """
    update Community
    """
    e[link[0]] += e[link[1]]
    e[:, link[0]] += e[:, link[1]]
    e = np.delete(np.delete(e, link[1], 0), link[1], 1)
    c = Community.pop(link[1])
    Community[link[0]] |= c
    return e, Community


def modularity(e):
    mod = np.sum(np.diag(e) - np.square(np.sum(e, axis=0)))
    return mod


def draw_graph(G, Community, label):
    """
    drawing a graph
    """
    color = [0 for _ in range(G.number_of_nodes())]
    pos = nx.spring_layout(G)
    for i, c in enumerate(Community):
        for j in c:
            color[j] = i
    nx.draw_networkx(G, pos, with_labels=label, node_color=color)
    plt.show()


def predict(G):
    """

    Parameters
    ----------
    G : networkx.Graph

    Returns
    -------

    """

    A = nx.adjacency_matrix(G)
    A = A.toarray()
    M = G.number_of_edges()
    e = A / (2*M)
    Community = [set([i]) for i in range(len(A[0]))]

    for _ in range(len(Community)-1):
        link = finding_pair(e)
        e, Community = update_community(e, link, Community)
        print(modularity(e))
        draw_graph(G, Community, True)


def main():
    G = nx.karate_club_graph()
    predict(G)

main()
