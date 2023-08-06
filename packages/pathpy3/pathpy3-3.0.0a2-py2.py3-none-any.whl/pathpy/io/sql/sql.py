"""Functions to read and write sql database tables."""
# !/usr/bin/python -tt
# -*- coding: utf-8 -*-
# =============================================================================
# File      : sql.py -- Read and write sql database tables
# Author    : Jürgen Hackl <hackl@ifi.uzh.ch>
# Time-stamp: <Sat 2020-08-22 18:04 juergen>
#
# Copyright (c) 2016-2020 Pathpy Developers
# =============================================================================

from __future__ import annotations
from typing import TYPE_CHECKING, Any, Optional, cast, Union

import sqlite3
import pandas as pd  # pylint: disable=import-error

from pathpy import logger
from pathpy.io.io import to_network, to_temporal_network, to_dataframe

# pseudo load class for type checking
if TYPE_CHECKING:
    from pathpy.core.network import Network
    from pathpy.models.temporal_network import TemporalNetwork


# create logger
LOG = logger(__name__)


def read_dataframe(filename: Optional[str] = None,
                   con: Optional[sqlite3.Connection] = None,
                   sql: Optional[str] = None,
                   table: Optional[str] = None) -> pd.DataFrame:
    """Read sql database as a pandas data frame."""

    LOG.debug('Load sql file as pandas data frame.')

    if con is None and filename is None:
        LOG.error('Either an SQL connection or a filename is required')
        raise IOError

    con_close = False
    # connect to database if not given
    if con is None and filename is not None:
        con_close = True
        con = sqlite3.connect(filename)

    # if sql query is not given check availabe tables
    if sql is None:

        # create cursor and get all tables availabe
        cursor = cast(sqlite3.Connection, con).cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = list(sum(cursor.fetchall(), ()))

        # check if table is given
        if table is None:
            table = tables[0]
        elif table not in tables:
            LOG.error('Given table "%s" not in database!', table)
            raise IOError

        # generate sql query
        sql = 'SELECT * from {}'.format(table)

    # read to pandas data frame
    frame = pd.read_sql(sql, con)

    # close connection to the database
    if con_close:
        _con = cast(sqlite3.Connection, con)
        _con.close()

    # return pandas data frame
    return frame


def read_network(filename: Optional[str] = None,
                 loops: bool = True,
                 directed: bool = True,
                 multiedges: bool = False,
                 con: Optional[sqlite3.Connection] = None,
                 sql: Optional[str] = None,
                 table: Optional[str] = None,
                 **kwargs: Any) -> Network:
    """Read network from a sqlite database."""
    # pylint: disable=too-many-arguments

    frame = read_dataframe(filename=filename, con=con, sql=sql, table=table)

    net = to_network(frame, loops=loops, directed=directed,
                     multiedges=multiedges, **kwargs)

    return net


def read_temporal_network(filename: Optional[str] = None,
                          loops: bool = True,
                          directed: bool = True,
                          multiedges: bool = False,
                          con: Optional[sqlite3.Connection] = None,
                          sql: Optional[str] = None,
                          table: Optional[str] = None,
                          **kwargs: Any) -> TemporalNetwork:
    """Read temporal network from a sqlite database."""
    # pylint: disable=too-many-arguments

    frame = read_dataframe(filename=filename, con=con, sql=sql, table=table)

    net = to_temporal_network(frame, loops=loops, directed=directed,
                              multiedges=multiedges, **kwargs)

    return net


def write_dataframe(frame: pd.DataFrame,
                    table: str,
                    filename: Optional[str] = None,
                    con: Optional[sqlite3.Connection] = None,
                    **pdargs: Any) -> None:
    """Stores all edges including edge attributes in an sqlite database table.

    Node and network-level attributes are not included.

    Parameters
    ----------

    network: Network

        The network to store in the sqlite database

    filename: str

        The name of the SQLite database in which the network will be stored

    con: sqlite3.Connection

        The SQLite3 connection in which the network will be stored

    table: str

        Name of the table in the database in which the network will be stored.

    **pdargs:

        Keyword args that will be passed to pandas.DataFrame.to_sql.

    """

    LOG.debug('Store network as sql database.')

    if con is None and filename is None:
        LOG.error('Either an SQL connection or a filename is required')
        raise IOError

    con_close = False

    # connect to database if not given
    if con is None:
        con = sqlite3.connect(cast(str, filename))
        con_close = True

    frame.to_sql(table, con, **pdargs)

    if con_close:
        _con = cast(sqlite3.Connection, con)
        _con.close()


def write(network: Union[Network, TemporalNetwork],
          table: str,
          filename: Optional[str] = None,
          con: Optional[sqlite3.Connection] = None,
          exclude_edge_uid: bool = False,
          export_indices: bool = False,
          **pdargs: Any) -> None:
    """Stores all edges including edge attributes in a sql file."""
    frame = to_dataframe(network=network, exclude_edge_uid=exclude_edge_uid,
                         export_indices=export_indices)

    return write_dataframe(frame, table=table, filename=filename,
                           con=con, **pdargs)
# =============================================================================
# eof
#
# Local Variables:
# mode: python
# mode: linum
# mode: auto-fill
# fill-column: 79
# End:
