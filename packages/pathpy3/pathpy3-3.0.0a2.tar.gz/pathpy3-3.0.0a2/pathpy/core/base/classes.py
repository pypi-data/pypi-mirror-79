#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
# =============================================================================
# File      : classes.py -- Base classes for pathpy
# Author    : Jürgen Hackl <hackl@ifi.uzh.ch>
# Time-stamp: <Wed 2020-06-24 10:41 juergen>
#
# Copyright (c) 2016-2019 Pathpy Developers
# =============================================================================
from abc import ABC
from typing import Any, Optional
from copy import deepcopy

from pathpy import config
from pathpy.core.base.attributes import (Attributes,
                                         TemporalAttributes)


class AbstractNode(ABC):
    """Abstract base class for a Node.

    Warning: This class should not be used directly.
    Use derived classes instead.
    """
    pass


class AbstractEdge(ABC):
    """Abstract base class for an Edge.

    Warning: This class should not be used directly.
    Use derived classes instead.
    """
    pass


class AbstractPath(ABC):
    """Abstract base class for a Path.

    Warning: This class should not be used directly.
    Use derived classes instead.
    """
    pass


class AbstractNetwork(ABC):
    """Abstract base class for networks.

    Warning: This class should not be used directly.
    Use derived classes instead.
    """
    pass


class AbstractHigherOrderNetwork(ABC):
    """Abstract base class for higer order networks.

    Warning: This class should not be used directly.
    Use derived classes instead.
    """
    pass


class AbstractTemporalNetwork(ABC):
    """Abstract base class for temporal networks.

    Warning: This class should not be used directly.
    Use derived classes instead.
    """
    pass


class BaseClass:
    """Base class for all pathpy objects."""

    def __init__(self, uid: Optional[str] = None, **kwargs: Any) -> None:
        """Initialize the base class."""

        # initialize attributes object
        # self.attributes: Attributes = Attributes()
        self.attributes: Attributes = Attributes()

        # check code
        self.check: bool = kwargs.get(
            'check_code', config['computation']['check_code'])

        # declare variable
        self._uid: str
        self._python_uid: bool

        # assign node identifier
        if uid is not None:
            self._uid = str(uid)
            self._python_uid = False
        else:
            self._uid = hex(id(self))
            self._python_uid = True

    def __setitem__(self, key: Any, value: Any) -> None:
        """Add a specific attribute to the object.

        An attribute has a key and the corresponding value expressed as a pair,
        key: value.

        Parameters
        ----------
        key: Any
            Unique identifier for a corrisponding value.

        value: Any
            A value i.e. attribute which is associated with the object.

        Examples
        --------

        Generate new node.

        >>> from pathpy import Node
        >>> u = Node('u')

        Add atribute to the node.

        >>> u['color'] = 'blue'

        """

        self.attributes[key] = value

    def __getitem__(self, key: Any) -> Any:
        """Returns a specific attribute of the object.

        Parameters
        ----------
        key: any
            Key value for the attribute of the object.

        Returns
        -------
        any
            Returns the attribute of the node associated with the given key
            value.

        Raises
        ------
        KeyError
            If no attribute with the assiciated key is defined.

        Examples
        --------

        Generate new node with blue color

        >>> from pathpy import Node
        >>> u = Node('u', color='blue')

        Get the node attribute.

        >>> u['color']
        'blue'

        """
        return self.attributes[key]

    def __eq__(self, other: object) -> bool:
        """Returns True if two objects are equal, otherwise False."""
        return self.__hash__() == other.__hash__()

    def __repr__(self) -> str:
        """Return the description of the object.

        Returns
        -------
        str

            Returns the description of the object with the class and assigned
            node uid.

        Examples
        --------
        Genarate new node.

        >>> from pathpy import Node
        >>> u = Node('u')
        >>> print(u)
        Node u

        """
        # declare variable
        string: str

        # check if python id is used as uid or not
        if self._python_uid:
            # if python id is used dont show in the object description
            string = super().__repr__()
        else:
            # if user uid is used show in the object description
            string = '{} {}'.format(self.__class__.__name__, self.uid)

        return string

    def __hash__(self) -> Any:
        """Returns the unique hash of the object.

        Here the hash value is defined by the unique node id!

        """
        return hash(id(self))

    @property
    def uid(self) -> str:
        """Return the unique identifier (uid) of the object.

        Returns
        -------
        str

            Return the node identifier (uid) as a string.

        Examples
        --------
        Generate a single node and print the uid.

        >>> from pathpy import Node
        >>> u = Node('u')
        >>> u.uid
        u

        """
        return self._uid

    def update(self, **kwargs: Any) -> None:
        """Update the attributes of the object.

        Parameters
        ----------
        kwargs : Any
            Attributes to add or update for the object as key=value pairs.

        Examples
        --------

        Generate simple node with attribute.

        >>> from pathpy import Node
        >>> u = Node('u',color='red')
        >>> u.attributes
        {'color': 'red'}

        Update attributes.

        >>> u.update(color='green',shape='rectangle')
        >>> u.attributes
        {'color': 'green', 'shape': 'rectangle'}

        """

        self.attributes.update(**kwargs)

    def copy(self):
        """Return a copy of the node.

        Returns
        -------
        :py:class:`Node`
            A copy of the node.

        Examples
        --------
        >>> from pathpy import Node
        >>> u = Node('u')
        >>> v = u.copy()
        >>> v.uid
        u
        """
        return deepcopy(self)

    def weight(self, weight: str = 'weight', default: float = 1.0) -> float:
        """Returns the weight of the object.

        Per default the attribute with the key 'weight' is used as
        weight. Should there be no such attribute, a new one will be crated
        with weight = 1.0.

        If an other attribute should be used as weight, the option weight has
        to be changed.

        If a weight is assigned but for calculation a weight of 1.0 is needed,
        the weight can be disabled with False or None.

        Parameters
        ----------
        weight : str, optional (default = 'weight')
            The weight parameter defines which attribute is used as weight. Per
            default the attribute 'weight' is used. If `None` or `False` is
            chosen, the weight will be 1.0. Also any other attribute of the
            edge can be used as a weight

        Returns
        -------
        float
            Returns the attribute value associated with the keyword.

        Examples
        --------

        Create new edge and get the weight.

        >>> form pathpy import Edge
        >>> vw = Edge('v','w')
        >>> vw.weight()
        1.0

        Change the weight.

        >>> vw['weight'] = 4
        >>> vw.weight()
        4.0

        >>> vw.weight(False)
        1.0

        Add an attribute and use this as weight.

        >>> vw['length'] = 5
        >>> vw.weight('length')
        5.0

        Create new path and get the weight.

        >>> form pathpy import Path
        >>> p = Path('a','b','c')
        >>> p.weight()
        1.0

        Change the weight.

        >>> p['weight'] = 4
        >>> p.weight()
        4.0

        >>> p.weight(False)
        1.0

        Add an attribute and use this as weight.

        >>> p['length'] = 5
        >>> p.weight('length')
        5.0

        """
        if weight is None:
            weight = False
        if not weight:
            return default
        elif isinstance(weight, str) and weight != 'weight':
            return float(self.attributes.get(weight, 0.0))
        else:
            return float(self.attributes.get('weight', default))


class BaseCollection(BaseClass):
    """Base class for collecting objects"""
    pass


class BaseNode(AbstractNode, BaseClass):
    """Base class for nodes."""
    pass


class BaseEdge(AbstractEdge, BaseClass):
    """Base class for edges."""
    pass


class BasePath(AbstractPath, BaseClass):
    """Base class for paths."""
    pass


class BaseModel(AbstractNetwork, BaseClass):
    """Base class for networks."""
    pass


class BaseTemporalNetwork(BaseModel):
    """Base class for temporal networks."""
    pass


class BaseStaticNetwork(BaseModel):
    """Base class for temporal networks."""
    pass


class BaseDirectedNetwork(BaseStaticNetwork):
    """Base class for networks."""
    pass


class BaseUndirectedNetwork(BaseStaticNetwork):
    """Base class for networks."""
    pass


class BaseDirectedTemporalNetwork(BaseTemporalNetwork):
    """Base class for networks."""
    pass


class BaseUndirectedTemporalNetwork(BaseTemporalNetwork):
    """Base class for networks."""
    pass


class BaseHigherOrderNetwork(AbstractHigherOrderNetwork, BaseClass):
    """Base class for higher order networks."""
    pass


# =============================================================================
# eof
#
# Local Variables:
# mode: python
# mode: linum
# mode: auto-fill
# fill-column: 79
# End:
