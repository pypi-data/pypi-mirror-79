"""Random graphs for pathpy."""
# !/usr/bin/python -tt
# -*- coding: utf-8 -*-
# =============================================================================
# File      : random_graphs.py -- Module to generate random graphs
# Author    : Ingo Scholtes <scholtes@uni-wuppertal.de>
# Time-stamp: <Sat 2020-09-05 11:35 juergen>
#
# Copyright (c) 2016-2020 Pathpy Developers
# =============================================================================
from __future__ import annotations
from functools import singledispatch

from typing import Optional, Union, Dict

import numpy as np

from pathpy import logger, tqdm

from pathpy.core.edge import Edge
from pathpy.core.node import Node
from pathpy.core.network import Network

import scipy

# create logger
LOG = logger(__name__)


def max_edges(n: int, directed: bool = False, multiedges: bool = False, loops: bool = False) -> Union[int, float]:
    """Returns the maximum number of edges that a directed or undirected network with n nodes can
    possible have (with or without loops).

    Parameters
    ----------
    n : int 

        The number of nodes in the network

    directed : bool

        If True, return the maximum number of edges in a directed network.

    multiedges : bool 

        If True, multiple edges between each node pair are allowed. In this case np.inf is returned.

    loops : bool 

        If True, include self-loops.

    Examples
    --------
    Compute maximum number of edges in directed/undirected network with/without self-loops and 100 nodes

    >>> import pathpy as pp
    >>> print(pp.generators.max_edges(100)
    4950

    >>> print(pp.generators.max_edges(100, directed=True)
    9900

    >>> print(pp.generators.max_edges(100, directed=True, loops=True)
    10000
    """

    if multiedges:
        return np.inf
    elif loops and directed:
        return int(n**2)
    elif loops and not directed:
        return int(n*(n+1)/2)
    elif not loops and not directed:
        return int(n*(n-1)/2)
    elif not loops and directed:
        return int(n*(n-1))


def ER_nm(n: int, m: int,
          directed: bool = False,
          loops: bool = False,
          multiedges: bool = False,
          node_uids: Optional[list] = None) -> Union[Network, None]:
    """(n, m) Erdös-Renyi model.

    Generates a random graph with a fixed number of n nodes and m edges based on
    the Erdös-Renyi model.

    Parameters
    ----------
    n : int

        The number of nodes in the generated network

    m : int

        The number of randomly generated edges in the network

    directed : bool

        Whether a directed network should be generated

    loops : bool

        Whether or not the generated network may contain
        loops.

    multi_edge : bool

        Whether or not the same edge can be added multiple times

    node_uids : list

        Optional list of node uids that will be used.

    Examples
    --------
    Generate random undirected network with 10 nodes and 25 edges

    >>> import pathpy as pp
    >>> random_graph = pp.algorithms.random_graphs.ER_nm(n=10, m=25)
    >>> print(random_graph.summary())
    ...

    """
    # Check parameter sanity
    M = max_edges(n, directed=directed, loops=loops, multiedges=multiedges)
    if m > M:
        LOG.error('Given network type with n nodes can have at most {} edges.'.format(M))
        return None

    network = Network(directed=directed)

    if node_uids is None or len(node_uids) != n:
        LOG.info('No valid node uids given, generating numeric node uids')
        node_uids = []
        for i in range(n):
            node_uids.append(str(i))
    
    for i in range(n):
        network.add_node(node_uids[i])

    edges = 0
    while edges < m:
        v, w = np.random.choice(node_uids, size=2, replace=loops)
        if multiedges or network.nodes[w] not in network.successors[v]:
            network.add_edge(v,w)
            edges += 1
    return network


def ER_nm_randomize(network: Network, loops: bool = False, multiedges: bool = False) -> Union[Network, None]:
    """Generates a random graph whose number of nodes, edges, edge directedness and node uids 
    match the corresponding values of a given network instance. Useful to generate a randomized 
    version of a network.
    
    Parameters
    ----------
    network : pathpy.Network

        Given network used to determine number of nodes, edges, node uids, and edge directedness    

    loops : bool

        Whether or not the generated network can contain loops.

    multi_edge : bool

        Whether or not multiple edges can be added to the same node pair

    Examples
    --------
    Generate random undirected network with 10 nodes and 25 edges

    >>> import pathpy as pp
    >>> n = pp.Network(directed=False)
    >>> n.add_edge('a', 'b')
    >>> n.add_edge('b', 'c')
    >>> n.add_edge('d', 'e')
    >>> r = pp.generators.ER_nm(n)
    >>> print(r)
    Uid:		0x...
    Type:		Network
    Directed:	False
    Unique nodes:	5
    Unique edges:	3
    Unique paths:	0
    Total paths:	0
    >>> print(r.nodes.uids)
    { 'a', 'b', 'c', 'd', 'e'}

    """

    return ER_nm(network.number_of_nodes(), network.number_of_edges(), 
                    directed=network.directed, loops=loops, multiedges=multiedges,
                    node_uids=list(network.nodes.uids))


def ER_np(n: int, p: float, directed: bool = False, loops: bool = False,
          node_uids: Optional[list] = None) -> Network:
    """(n, p) Erdös-Renyi model

    Generates a random graph with a fixed number of n nodes and edge probability
    p based on the Erdös-Renyi model.

    Parameters
    ----------
    n : int

        The number of nodes in the generated network

    p : float

        The probability with which an edge will be created
        between each pair of nodes

    directed : bool

        Whether a directed network should be generated

    loops : bool

        Whether or not the generated network may contain
        loops.

    node_uids : list

        Optional list of node uids that will be used.

    Examples
    --------
    Generate random undirected network with 10 nodes

    >>> import pathpy as pp
    >>> random_graph = pp.algorithms.random_graphs.ER_np(n=10, p=0.03)
    >>> print(random_graph.summary())
    ...

    """
    network = Network(directed=directed)

    if node_uids is None or len(node_uids) != n:
        LOG.info('No valid node uids given, generating numeric node uids')
        node_uids = []
        for i in range(n):
            node_uids.append(str(i))
    
    for i in range(n):
        network.add_node(node_uids[i])

    for s in tqdm(range(n), 'generating G(n,p) network'):
        if directed:
            x = n
        else:
            x = s+1
        for t in range(x):
            if t == s and not loops:
                continue
            if np.random.random_sample() < p:
                network.add_edge(node_uids[s], node_uids[t])
    return network


def ER_np_randomize(network: Network, loops: bool = False) -> Network:
    """Generates a random microstate based on the G(n,p) model. The number of nodes,
    the expected number of edges, the edge directedness and the node uids of the 
    generated network match the corresponding values of a given network instance.
    """

    n = network.number_of_nodes()
    m = network.number_of_edges()
    M = max_edges(n, directed=network.directed, loops=loops)
    p = m/M
    return ER_np(n=n, p=p, directed=network.directed, loops=loops, node_uids=list(network.nodes.uids))


def Watts_Strogatz(n: int, s: int, p: float = 0.0, loops: bool = False,
                   node_uids: Optional[list] = None) -> Network:
    """Undirected Watts-Strogatz lattice network

    Generates an undirected Watts-Strogatz lattice network with lattice
    dimensionality one.

    Parameters
    ----------
    n : int

        The number of nodes in the generated network

    s : float

        The number of nearest neighbors that will be connected
        in the ring lattice

    p : float

        The rewiring probability

    Examples
    --------
    Generate a Watts-Strogatz network with 100 nodes

    >>> import pathpy as pp
    >>> small_world = pp.algorithms.random_graphs.Watts_Strogatz(n=100, s=2, p=0.1)
    >>> print(small_world.summary())
    ...

    """
    network = Network(directed=False)
    if node_uids is None or len(node_uids) != n:
        LOG.info('No valid node uids given, generating numeric node uids')
        node_uids = []
        for i in range(n):
            network.add_node(Node(str(i)))
            node_uids.append(str(i))
    else:
        for i in range(n):
            network.add_node(node_uids[i])

    # construct a ring lattice (dimension 1)
    for i in range(n):
        if loops:
            x = 0
            y = s
        else:
            x = 1
            y = s+1
        for j in range(x, y):
            v = network.nodes[node_uids[i]]
            w = network.nodes[node_uids[(i+j) % n]]
            if (v.uid, w.uid) not in network.edges:
                network.add_edge(v, w)

    if p == 0:
        # nothing to do here
        return network

    # Rewire each link with probability p
    for edge in tqdm(list(network.edges.values()), 'generating WS network'):
        if np.random.rand() < p:
            # Delete original link and remember source node
            v = edge.v.uid
            network.remove_edge(edge)

            # Find new random tgt, which is not yet connected to src
            new_target = None

            # This loop repeatedly chooses a random target until we find
            # a target not yet connected to src. Note that this could potentially
            # result in an infinite loop depending on parameters.
            while new_target is None:
                x = str(np.random.randint(n))
                if (x != v or loops) and (v, x) not in network.edges:
                    new_target = x
            network.add_edge(v, new_target)
    return network


def is_graphic_Erdos_Gallai(degrees):
    """Check Erdös and Gallai condition.

    Checks whether the condition by Erdös and Gallai (1967) for a graphic degree
    sequence is fulfilled.

    Parameters
    ----------
    degrees : list

        List of integer node degrees to be tested.

    Examples
    --------
    Test non-graphic degree sequence with uneven sum

    >>> import pathpy as pp
    >>> pp.generators.is_graphic_Erdos_Gallai([1,0])
    False

    Test non-graphic degree sequence with even sum

    >>> import pathpy as pp
    >>> pp.generators.is_graphic_Erdos_Gallai([1,3])
    False

    Test graphic degree sequence:

    >>> import pathpy as pp
    >>> pp.generators.is_graphic_Erdos_Gallai([1,1])
    True

    """
    degree_sequence = sorted(degrees, reverse=True)
    S = sum(degree_sequence)
    n = len(degree_sequence)
    if S % 2 != 0:
        return False
    for r in range(1, n):
        M = 0
        S = 0
        for i in range(1, r+1):
            S += degree_sequence[i-1]
        for i in range(r+1, n+1):
            M += min(r, degree_sequence[i-1])
        if S > r * (r-1) + M:
            return False
    return True


def generate_degree_sequence(n, distribution: Union[Dict[float, float], scipy.stats.rv_continuous, scipy.stats.rv_discrete], **distribution_args) -> np.array:
    """Generates a random graphic degree sequence drawn from a given degree distribution"""

    s = [ 1 ]

    # create rv_discrete object with custum distribution
    if isinstance(distribution, dict):
        degrees = [ k for k in distribution ]
        probs = [ distribution[k] for k in degrees ]

        distribution = scipy.stats.rv_discrete(name='custom', values=(degrees, probs))

    # use scipy rv objects to generate graphic degree sequence
    if isinstance(distribution, scipy.stats.rv_discrete):
        while not is_graphic_Erdos_Gallai(s):
            s = distribution.rvs(size=n, **distribution_args)

    elif isinstance(distribution, scipy.stats.rv_continuous):
        while not is_graphic_Erdos_Gallai(s):
            s = np.rint(distribution.rvs(size=n, **distribution_args))
    else:
        LOG.error('Distribution must be either dict, scipy.stats.rv_continuous or scipy.stats.rv_discrete')
        return None

    return s


def Molloy_Reed(degrees: Union[np.array, Dict[str, float]], multiedge: bool = False, relax: bool=False, node_uids: Optional[list] = None) -> Network:
    """Generate Molloy-Reed graph.

    Generates a random undirected network with given degree sequence based on
    the Molloy-Reed algorithm.

    .. note::

        The condition proposed by Erdös and Gallai (1967) is used to test
        whether the degree sequence is graphic, i.e. whether a network with the
        given degree sequence exists.

    Parameters
    ----------
    degrees : list

        List of integer node degrees. The number of nodes of the generated
        network corresponds to len(degrees).

    relax : bool

        If True, we conceptually allow self-loops and multi-edges, but do not
        add them to the network This implies that the generated network may not
        have exactly sum(degrees)/2 links, but it ensures that the algorithm
        always finishes.

    Examples
    --------
    Generate random undirected network with given degree sequence

    >>> import pathpy as pp
    >>> random_network = pp.algorithms.random_graphs.Molloy_Reed([1,0])
    >>> print(random_network.summary())
    ...

    Network generation fails for non-graphic sequences

    >>> import pathpy as pp
    >>> random_network = pp.algorithms.random_graphs.Molloy_Reed([1,0])
    >>> print(random_network)
    None

    """

    # assume that we are given a graphical degree sequence
    if not is_graphic_Erdos_Gallai(degrees):
        return

    # create empty network with n nodes
    n = len(degrees)
    network = Network(directed=False, multiedges=multiedge)

    if node_uids is None or len(node_uids) != n:
        LOG.info('No valid node uids given, generating numeric node uids')
        node_uids = []
        for i in range(n):
            node_uids.append(str(i))
    
    for i in range(n):
        network.add_node(node_uids[i])

    # generate link stubs based on degree sequence
    stubs = []
    for i in range(n):
        for k in range(int(degrees[i])):
            stubs.append(str(node_uids[i]))

    # connect randomly chosen pairs of link stubs
    while(len(stubs) > 0):
        v, w = np.random.choice(stubs, 2, replace=False)

        if v == w or (multiedge == False and relax == False and network.nodes[w] in network.successors[v]):
            # remove random edge and add stubs
            if network.number_of_edges()>0:
                edge = np.random.choice(list(network.edges))
                stubs.append(edge.v.uid)
                stubs.append(edge.w.uid)
                network.remove_edge(edge)
        else:
            if not network.nodes[w] in network.successors[v]:
                network.add_edge(v, w)
            stubs.remove(v)
            stubs.remove(w)            
            

    return network


def Molloy_Reed_randomize(network: Network) -> Network:

    # degrees are listed in order of node indices 
    degrees = network.degree_sequence()    

    # generate node uids in same order
    node_uids = ['-']*len(degrees)
    for v in network.nodes.uids:
        node_uids[network.nodes.index[v]] = v

    return Molloy_Reed(degrees, node_uids=node_uids)
