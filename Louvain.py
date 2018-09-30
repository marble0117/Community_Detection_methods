# -*- coding: utf-8 -*-

import networkx as nx
import numpy as np
import random
import matplotlib.pyplot as plt

def predict(G):
    # Gのedgesにweight属性をつける
    A = nx.adjacency_matrix(G)
    G = nx.from_scipy_sparse_matrix(A)
    nb_prev = 0

    while(G.number_of_nodes() != nb_prev):
        nb_prev = G.number_of_nodes()
        Community = first_phase(G)
        G = second_phase(G, Community)

def first_phase(G):
    N = G.number_of_nodes()
    M = int(G.size(weight='weight'))
    Community = {i: i for i in range(N)}

    # コミュニティと外部とを繋ぐエッジ数
    C_out = []
    for i in range(N):
        tmp = G.degree(i, weight='weight')
        if G.has_edge(i, i):
            tmp -= G.edges[i, i]['weight']
        C_out.append(tmp)
    # ランダムにノードを選択するCommunity.values()
    l = list(range(N))
    # random.shuffle(l)

    # Flags
    visited = [False for _ in range(N)]
    changed = True

    while(changed and len(l) > 0):
        changed = False
        new_l = []
        for i in l:
            if visited[i] == False:
                # 隣接ノードを取得しΔQを計算
                com_i = Community[i]
                delta = []
                links = list(G.edges(i))
                print(links)
                for link in links:
                    if link[0] == link[1]:
                        # self loop はスルー
                        continue

                    com_j = Community[link[1]]
                    # 同じコミュニティのノードを検索
                    neighbor = [k for k, v in Community.items() if v == com_j]
                    k_in = 0
                    k_i  = G.degree(i)
                    for j in neighbor:
                        if G.has_edge(i, j):
                            k_in += G.edges()[i, j]['weight']

                    s_tot = C_out[com_j] + k_i - k_in
                    d = k_in / (2*M) - s_tot * k_i / (2*M*M)
                    delta.append(d)
                if len(delta) > 0:
                    max_index = np.array(delta).argmax()
                    # ΔQの最も大きいコミュニティにmerge
                    if delta[max_index] > 0:
                        j = links[max_index][1]
                        com_j = Community[j]
                        Community[i] = com_j
                        C_out[com_j] += (k_i - k_in)
                        visited[i] = True
                        visited[j] = True
                        changed = True
                    else:
                        # isolated node list
                        new_l.append(i)
                else:
                    # self loopしか持たない
                    visited[i] = True
        l = new_l

    pos = nx.spring_layout(G)
    nx.draw_networkx(G, pos, node_color=list(Community.values()))
    plt.show()

    return Community

def second_phase(G_old, Community):
    # Communityの番号の振り直し
    com_list = list(set(list(Community.values())))
    com_dict = {}
    for i, key in enumerate(com_list):
        com_dict[key] = i

    for i in range(len(Community)):
        Community[i] = com_dict[Community[i]]

    G = nx.Graph()
    G.add_nodes_from(list(range(len(com_list))))

    for link in G_old.edges():
        i, j = Community[link[0]], Community[link[1]]
        # weightを計算
        if link[0] == link[1]:
            # self loop
            weight = G_old.edges()[link[0], link[1]]['weight']
        elif i==j:
            # 同一コミュニティ
            weight = G_old.edges()[link[0], link[1]]['weight'] * 2
        else:
            weight = G_old.edges()[link[0], link[1]]['weight']
        # 新しいグラフに追加
        if G.has_edge(i, j):
            G.edges()[i, j]['weight'] += weight
        else:
            G.add_edge(i, j, weight=weight)

    return G



def main():
    # G = nx.karate_club_graph()
    G = nx.Graph()
    G.add_edges_from([(0, 2), (0, 3), (0, 4), (0, 5), (1, 2), (1, 4), (1, 7), (2, 4), (2, 5), (2, 6)])
    G.add_edges_from([(3, 7), (4, 10), (5, 7), (5, 11), (6, 7), (6, 11), (8, 9), (8, 10), (8, 11), (8, 14), (8, 15)])
    G.add_edges_from([(9, 12), (9, 14), (10, 11), (10, 12), (10, 13), (10, 14), (11, 13)])

    predict(G)

main()
