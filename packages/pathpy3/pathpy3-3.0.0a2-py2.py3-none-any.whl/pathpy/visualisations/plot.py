"""Class to plot pathpy networks."""
# !/usr/bin/python -tt
# -*- coding: utf-8 -*-
# =============================================================================
# File      : plot.py -- Module to plot pathoy networks
# Author    : Jürgen Hackl <hackl@ifi.uzh.ch>
# Time-stamp: <Sat 2020-09-05 19:14 juergen>
#
# Copyright (c) 2016-2019 Pathpy Developers
# =============================================================================
from __future__ import annotations
from typing import Any, List, Optional, Union, Dict
from collections import defaultdict
from copy import deepcopy
from singledispatchmethod import singledispatchmethod  # remove for python 3.8
from datetime import datetime
import numpy as np
import pandas as pd

from pathpy import logger, config
from pathpy.core.base import (BaseModel)
from pathpy.visualisations.utils import UnitConverter

from pathpy.visualisations.backends import (D3js,
                                            Tikz,
                                            Matplotlib)

from pathpy.visualisations.fileformats import (HTML,
                                               TEX,
                                               PDF,
                                               PNG)

from pathpy.models.models import (ABCTemporalNetwork)

# create logger for the Plot class
LOG = logger(__name__)
TIMESTAMP = config['temporal']['timestamp']

# config: defaultdict = defaultdict(dict)
# config['environment']['interactive'] = False

# General config
config['plot']['width'] = 800
config['plot']['height'] = 550
config['plot']['unit'] = 'px'
config['plot']['dpi'] = 96
config['plot']['margin'] = None
config['plot']['layout'] = 'force'
config['plot']['temporal'] = False
config['plot']['coordinates'] = False
config['plot']['euclidean'] = False
config['plot']['min_max_node_size'] = None
config['plot']['min_max_edge_size'] = None
config['plot']['keep_aspect_ratio'] = True

config['plot']['forceCharge'] = -20  # -30
config['plot']['forceRepel'] = -300  # -100
config['plot']['forceAlpha'] = 0.1
config['plot']['restartAlpha'] = 1
config['plot']['alphaMin'] = 0.001  # 0.1
config['plot']['targetAlpha'] = 0  # 0.2
config['plot']['chargeDistance'] = config['plot']['width']
config['plot']['repelDistance'] = 200
config['plot']['velocityDecay'] = 0.4  # .2
config['plot']['lookoutStrokeWidth'] = 1
config['plot']['lookoutOpacity'] = .5
config['plot']['lookoutWeight'] = 0.
config['plot']['radiusMinSize'] = 4
config['plot']['radiusMaxSize'] = 16
config['plot']['nodeTransitionDuration'] = 100
config['plot']['nodeTransitionDuration'] = 100
config['plot']['defaultEdgeWeight'] = 1

config['plot']['targetAlphaDragStarted'] = 0.3
config['plot']['targetAlphaDragEnd'] = 0.0


config['plot']['linkStrengthMin'] = 0.0
config['plot']['linkStrengthMax'] = .45


config['plot']['template'] = None
config['plot']['css'] = None

config['plot']['backend'] = ['tikz']
config['plot']['fileformat'] = ['tex']
config['plot']['latex_class_options'] = ''

config['plot']['interactiv'] = {}
config['plot']['interactiv']['backend'] = ['d3js']
config['plot']['interactiv']['fileformat'] = ['html']

# Animation config
config['plot']['animation'] = {}
config['plot']['animation']["enabled"] = False
config['plot']['animation']["begin"] = None
config['plot']['animation']["end"] = None
config['plot']['animation']["steps"] = 20
config['plot']['animation']["speed"] = 100
config['plot']['animation']["unit"] = "seconds"

# Label config
config['plot']['label'] = {}
config['plot']['label']['centered'] = True
config['plot']['label']['enabled'] = True
config['plot']['label']['color'] = 'white'

config['plot']['label_centered'] = True
config['plot']['label_enabled'] = True
config['plot']['label_color'] = 'white'


# Node config
config['plot']['node'] = {}
config['plot']['node']['size'] = 15
config['plot']['node']['color'] = 'CornflowerBlue'
config['plot']['node']['opacity'] = .2
config['plot']['node']['id_as_label'] = True

config['plot']['curved'] = False
config['plot']['directed'] = False

# Edge config
config['plot']['edge'] = {}
config['plot']['edge']['size'] = 2
config['plot']['edge']['color'] = 'black'
config['plot']['edge']['opacity'] = 1
config['plot']['edge']['directed'] = False
config['plot']['edge']['curved'] = .5

# Widges config
config['plot']['widgets'] = {}

# tooltip
config['plot']['widgets']['tooltip'] = {}
config['plot']['widgets']['tooltip']['enabled'] = False
config['plot']['widgets']['tooltip']['size'] = '100px'

# save
config['plot']['widgets']['save'] = {}
config['plot']['widgets']['save']['title'] = 'Save'
config['plot']['widgets']['save']['enabled'] = True
config['plot']['widgets']['save']['tooltip'] = "Save the network as [svg] or [png]."

# zoom
config['plot']['widgets']['zoom'] = {}
config['plot']['widgets']['zoom']['title'] = 'Zoom'
config['plot']['widgets']['zoom']['enabled'] = True
config['plot']['widgets']['zoom']['tooltip'] = "Zoom-in with [+] <br> zoom-out with [-] <br> or reset zoom with [Reset]. <br> Furthermore, with [Shift+mouse wheel] you can also zoom."

# filter
config['plot']['widgets']['filter'] = {}
config['plot']['widgets']['filter']['title'] = 'Filter'
config['plot']['widgets']['filter']['enabled'] = False
config['plot']['widgets']['filter']['tooltip'] = "Filter the nodes base on given groups."
config['plot']['widgets']['filter']['groups'] = ["all"]

# search
config['plot']['widgets']['search'] = {}
config['plot']['widgets']['search']['title'] = 'Search'
config['plot']['widgets']['search']['enabled'] = True
config['plot']['widgets']['search']['tooltip'] = "Search for a node in the network."

# layout
config['plot']['widgets']['layout'] = {}
config['plot']['widgets']['layout']['title'] = 'Layout'
config['plot']['widgets']['layout']['enabled'] = False
config['plot']['widgets']['layout']['tooltip'] = "Change the layout of the Network. Per default a [Force] directed layout is used. If x and y coordinates are given, an [Coord] layout can be used."

# animation
config['plot']['widgets']['animation'] = {}
config['plot']['widgets']['animation']['title'] = 'Animation'
config['plot']['widgets']['animation']['enabled'] = True
config['plot']['widgets']['animation']['tooltip'] = "Play and pause animation of the temproal network."

# aggregation
config['plot']['widgets']['aggregation'] = {}
config['plot']['widgets']['aggregation']['title'] = 'Aggregation'
config['plot']['widgets']['aggregation']['enabled'] = True
config['plot']['widgets']['aggregation']['tooltip'] = "Aggregate time steps."
config['plot']['widgets']['aggregation']['past'] = 2
config['plot']['widgets']['aggregation']['future'] = 2
config['plot']['widgets']['aggregation']['aggregation'] = 1


def plot(obj, filename: Optional[str] = None,
         backend: Optional[str] = None, **kwargs) -> None:
    """Plot the object"""
    # initialize variables
    figure: Any

    # supported backends
    backends: Dict[str, object] = {
        'd3js': D3js,
        'tikz': Tikz,
        'matplotlib': Matplotlib
    }

    # supported file fileformats and corresponding default backends
    figures: Dict[str, Dict[str, object]] = {
        'html': {'fileformat': HTML, 'backend': D3js},
        'tex': {'fileformat': TEX, 'backend': Tikz},
        # 'csv': {'fileformat': CSV, 'backend': Tikz},
        'pdf': {'fileformat': PDF, 'backend': Tikz},
        'png': {'fileformat': PNG, 'backend': Matplotlib},
    }

    # initialize object parser
    parser: Parser = Parser()

    _config = deepcopy(config['plot'])
    # _config = config['plot']
    # parse object to json like dict
    data: defaultdict = parser(obj, _config, **kwargs)

    # check filename
    # if no file name is given
    if filename is None:
        # generate default html figure with d3js
        figure = HTML()
        figure.draw(D3js(filename=False), data)
        figure.show()

        # if file name is given
    elif filename is not None:

        # get extension of the file
        extension = filename.split('.')[-1]

        # check if extension is supported
        if extension in figures:
            figure = figures[extension]['fileformat']()

            # check if an other backend is provided
            if backend is not None:
                if backend in backends:
                    _backend = backends[backend]
                else:
                    _backend = figures[extension]['backend']
                    LOG.warning('The backend "%s" is not available.'
                                'The standard backend was used!', backend)
            else:
                _backend = figures[extension]['backend']

            # draw the figure
            figure.draw(_backend(), data)

            # save the figure
            figure.save(filename)
        else:
            LOG.error('Plotting files in the format "%s" is not supported!',
                      extension)
            raise TypeError


class Parser:
    """Object to parse pathpy objects into json like dict."""

    def __init__(self) -> None:
        """Initialize parser object."""
        # initialize variables
        self.figure: defaultdict = defaultdict(dict)
        self.figure['data'] = {}
        self.config: defaultdict = defaultdict(dict)

        self.default_node = {
            'uid': None,
            'label': None,
            'text': None,
            'size': None,
            'color': None,
            'opacity': None,
            'group': None,
            'time': None,
            'coordinates': None,
            'label_size': None,
            'id_as_label': None,
            'style': None,
        }
        self.default_edge = {
            'uid': None,
            'label': None,
            'text': None,
            'size': None,
            'color': None,
            'opacity': None,
            'time': None,
            'source': None,
            'target': None,
            'directed': None,
            'curved': None,
            'style': None,
        }
        self.default_properties = {
            'node': self.default_node,
            'edge': self.default_edge}

        self.default_animation = {
            "enabled": None,
            "begin": None,
            "end": None,
            "steps": None,
            "speed": None,
            "unit": None,
        }

        self.default_config = {
            'animation': self.default_animation
        }

    def __call__(self, obj: Any, plot_config: defaultdict,
                 **kwargs: Any) -> defaultdict:
        """Call the parse function."""
        return self.parse(obj, plot_config, **kwargs)

    @singledispatchmethod
    def parse(self, obj: Any, _config: defaultdict,
              **kwargs: Any) -> defaultdict:
        """Parses the pathpy network into a json like dict."""
        raise NotImplementedError

    @parse.register(ABCTemporalNetwork)
    def _parse_temporal(self, obj: Any, plot_config: defaultdict, **kwargs: Any) -> defaultdict:
        LOG.debug('Parse a temporal network')

        # get static network to start with
        self._parse_static(obj=obj, plot_config=plot_config, **kwargs)

        # TODO: Fix parse_config for temporal networks
        for key, values in self.parse_config(
                self.default_config, **kwargs).items():
            if isinstance(values, dict):
                for k, v in values.items():
                    self.config[key][k] = v

        # set temporal networkt to true
        self.config['temporal'] = True
        self.figure['data']['changes'] = []

        # get start and end time
        begin = obj.edges.begin(finite=True)
        end = obj.edges.end(finite=True)

        # raise error if time frame is not finite
        if begin == float('-inf') or end == float('inf'):
            LOG.error('The begin/end time is not finite!')
            raise ValueError

        # begin and end of the animation
        # TODO: make this more efficient
        animation_begin = self.config['animation']['begin']
        animation_end = self.config['animation']['end']
        steps = self.config['animation']['steps']
        # if no begin is given take the first observed temporal event
        if animation_begin is None:
            animation_begin = self._isotime(begin)
        elif isinstance(animation_begin, (int, float)):
            begin = animation_begin
            animation_begin = self._isotime(animation_begin)
        else:
            raise NotImplementedError

        if animation_end is None:
            animation_end = self._isotime(end)
        elif isinstance(animation_end, (int, float)):
            end = animation_end
            animation_end = self._isotime(animation_end)
        else:
            raise NotImplementedError

        # set animation begin and end for d3js
        self.config['animation']['begin'] = animation_begin
        self.config['animation']['end'] = animation_end

        # get static edges
        edges = {e['uid']: e for e in self.figure['data']['edges']}

        _intervals = obj.edges.intervals

        tree = _intervals.copy()
        tree.slice(begin)
        tree.slice(end)
        tree.remove_envelop(_intervals.begin(), begin)
        tree.remove_envelop(end, _intervals.end())

        edge_temp_attr: defaultdict = defaultdict(lambda: defaultdict(dict))
        for edge in obj.edges.values():
            df = edge.attributes.to_frame(history=True)
            df = df.where(pd.notnull(df), None)
            attr = list(df.to_dict('index').values())
            for values in attr:
                time = values.pop(TIMESTAMP, None)
                edge_temp_attr[edge.uid][time].update(**values)

        # generate temporal edges
        temporal_edges = []
        time = list(np.linspace(begin, end, num=steps))
        for t in time:
            for _, _, edge in tree[t]:

                # get default object
                _edge = edges[edge.uid]
                # get temporal attributes
                _attr = edge_temp_attr[edge.uid][int(round(t, 0))]
                # if temporal attributes given update old attributes:
                if _attr:
                    for key, value in _attr.items():
                        if key in _edge:
                            _edge[key] = value

                _edge['time'] = time.index(t)
                temporal_edges.append(_edge.copy())

        # add temporal edges to the data
        self.figure['data']['edges'] = temporal_edges

        # get static nodes
        nodes = {n['uid']: n for n in self.figure['data']['nodes']}

        node_temp_attr: defaultdict = defaultdict(lambda: defaultdict(dict))
        for node in obj.nodes.values():
            df = node.attributes.to_frame(history=True)
            df = df.where(pd.notnull(df), None)
            attr = list(df.to_dict('index').values())
            for values in attr:
                time = values.pop(TIMESTAMP, None)
                node_temp_attr[node.uid][time].update(**values)

        # generating initial nodes
        initial_nodes = []
        for node in obj.nodes.keys():
            _node = nodes[node]
            _attr = node_temp_attr[node][float('-inf')]
            if _attr:
                for key, value in _attr.items():
                    if key in _node:
                        _node[key] = value
            initial_nodes.append(_node.copy())

        # add initial nodes to the data
        self.figure['data']['nodes'] = initial_nodes

        temporal_nodes = []
        for initial_node in initial_nodes:
            _node = initial_node.copy()
            _node['time'] = 0
            temporal_nodes.append(_node)

        time = list(np.linspace(begin, end, num=steps))
        for t in time:
            for node in obj.nodes.keys():
                _node = nodes[node]
                _attr = node_temp_attr[node][int(round(t, 0))]
                if _attr:
                    for key, value in _attr.items():
                        if key in _edge:
                            _node[key] = value

                    _node['time'] = time.index(t)
                    temporal_nodes.append(_node.copy())

        self.figure['data']['changes'] = temporal_nodes

        # return the figure
        return self.figure

    @staticmethod
    def _isotime(time: Union[int, float]) -> str:
        """Convert float to ISO 8601 string."""
        return datetime.utcfromtimestamp(time).strftime("%Y-%m-%dT%H:%M:%S")

    @parse.register(BaseModel)
    def _parse_static(self, obj: Any, plot_config: defaultdict,
                      **kwargs: Any) -> defaultdict:
        """Parse static network."""

        # update default config
        self.config.update(plot_config)
        if obj.directed:
            self.config['directed'] = True
            self.config['curved'] = True
            self.config['edge']['directed'] = True

        # convert default units to units
        u2u = UnitConverter(self.config['unit'],
                            kwargs.get('unit', self.config['unit']),
                            dpi=self.config['dpi'])

        self.config['width'] = u2u(self.config['width'])
        self.config['height'] = u2u(self.config['height'])
        self.config['node']['size'] = u2u(self.config['node']['size'])
        self.config['edge']['size'] = u2u(self.config['edge']['size'])

        # generate default objects
        # iterate over the default config
        for key, values in self.config.items():

            # if objects such as node or edge are in the default config
            if key in self.default_properties:

                # iterate over the attributes
                for attr, value in values.items():

                    # add attributes if the are in the default element
                    if attr in self.default_properties[key]:
                        self.default_properties[key][attr] = value

        # check kwargs and update config
        self.config.update(self.parse_config(self.default_properties, **kwargs))

        # parse layout
        _layout = self.config.get('layout', None)
        if isinstance(_layout, dict):
            self.config['node'].update({'coordinates': _layout})
            self.config['layout'] = 'euclidean'

        # parse nodes an edges
        nodes = self.parse_static_objects(obj.nodes, otype='node', **kwargs)
        edges = self.parse_static_objects(obj.edges, otype='edge', **kwargs)

        # convert units to px
        u2px = UnitConverter(self.config['unit'], 'px', dpi=self.config['dpi'])
        for key in ['width', 'height']:
            self.config[key] = u2px(self.config[key])

        nodes = self._convert_size(nodes, u2px, otype='node')
        edges = self._convert_size(edges, u2px, otype='edge')

        # update layout
        try:
            layout = {n['uid']: n['coordinates'] for n in nodes}
        except KeyError:
            pass
        else:
            nodes = self._update_layout(nodes, layout, u2px)
            self.config['coordinates'] = True

        # add nodes, edges and config to the figure
        self.figure['data']['nodes'] = nodes
        self.figure['data']['edges'] = edges
        self.figure['config'] = self.config

        # return the figure
        return self.figure

    def _convert_size(self, objects, converter, otype='node'):
        """Helper function to convert the units  of the size of an object."""

        for obj in objects:
            obj['size'] = converter(obj['size'])

        return objects

    def _update_layout(self, nodes, layout, converter):
        """Helper function to update the layout"""
        # get canvas size and margins
        width = self.config['width']
        height = self.config['height']
        keep_aspect_ratio = self.config['keep_aspect_ratio']

        if self.config['margin'] is None:
            margin = max([n['size'] for n in nodes])/2+4
        elif isinstance(self.config['margin'], (int, float)):
            margin = converter(self.config['margin'])
        else:
            margin = 0

        margins = {'top': margin, 'left': margin,
                   'bottom': margin, 'right': margin}

        # calculate the scaling ratio
        ratio_x = float('inf')
        ratio_y = float('inf')

        # find min and max values of the points
        min_x = min(layout.items(), key=lambda item: item[1][0])[1][0]
        max_x = max(layout.items(), key=lambda item: item[1][0])[1][0]
        min_y = min(layout.items(), key=lambda item: item[1][1])[1][1]
        max_y = max(layout.items(), key=lambda item: item[1][1])[1][1]

        if max_x-min_x > 0:
            ratio_x = (width-margins['left']-margins['right']) / (max_x-min_x)
        if max_y-min_y > 0:
            ratio_y = (height-margins['top']-margins['bottom']) / (max_y-min_y)

        if keep_aspect_ratio:
            scaling = (min(ratio_x, ratio_y), min(ratio_x, ratio_y))
        else:
            scaling = (ratio_x, ratio_y)

        if scaling[0] == float('inf'):
            scaling = (1, scaling[1])
        if scaling[1] == float('inf'):
            scaling = (scaling[0], 1)

        # apply scaling to the points
        _layout = {}
        for n, (x, y) in layout.items():
            _x = (x)*scaling[0]
            _y = (y)*scaling[1]
            _layout[n] = (_x, _y)

        # find min and max values of new the points
        min_x = min(_layout.items(), key=lambda item: item[1][0])[1][0]
        max_x = max(_layout.items(), key=lambda item: item[1][0])[1][0]
        min_y = min(_layout.items(), key=lambda item: item[1][1])[1][1]
        max_y = max(_layout.items(), key=lambda item: item[1][1])[1][1]

        # calculate the translation
        translation = (((width-margins['left']-margins['right'])/2
                        + margins['left']) - ((max_x-min_x)/2 + min_x),
                       ((height-margins['top']-margins['bottom'])/2
                        + margins['bottom']) - ((max_y-min_y)/2 + min_y))

        # apply translation to the points
        for n, (x, y) in _layout.items():
            _x = (x)+translation[0]
            _y = (y)+translation[1]
            _layout[n] = (_x, _y)

        for node in nodes:
            node['coordinates'] = _layout[node['uid']]

        return nodes

    def parse_config(self, properties: dict, **kwargs: Any) -> defaultdict:
        """Parse the config file."""

        # initialize temporal dict
        _config: defaultdict = defaultdict(dict)

        # extend default dict
        for key in properties:
            _config[key] = defaultdict(dict)

        # iterate over kwargs
        for key, value in kwargs.items():

            # split key from kwargs
            _key = key.split("_", 1)

            # check if key is valid
            if _key[0] in properties:
                if _key[1] in properties[_key[0]]:

                    # add value to dictionary
                    _config[_key[0]][_key[1]] = value

            # check if key is in the default config
            elif key in self.config:
                _config[key] = value

        return _config

    def parse_static_objects(self, objects, otype='node', **kwargs) -> List:
        """Parse static objects such as nodes and edges."""

        # initialize temporal dict
        _obj: defaultdict = defaultdict(dict)

        # get mapping if defined
        mapping = kwargs.get('mapping', None)

        # iterate over objects
        for uid, obj in objects.items():

            # add default properties to the obj
            _obj[uid] = self.default_properties[otype].copy()

            # add obj uid
            _obj[uid]['uid'] = uid

            # if obj is an edge add source and target nodes
            if otype == 'edge':
                _obj[uid]['source'] = obj.v.uid
                _obj[uid]['target'] = obj.w.uid

            # add obj attributes
            for attr, value in obj.attributes.to_dict().items():

                # if mapping is given map the attribute
                if mapping is not None and attr in mapping:
                    attr = mapping[attr]

                # check if attribute is in the default object
                if attr in self.default_properties[otype]:

                    # update attribute if given
                    _obj[uid][attr] = value

        # update objects based on the kwargs
        # iterate over the kwargs config
        for key, values in self.config[otype].items():

            # check if new attribute is a single object
            if isinstance(values, (str, int, float, bool)):
                for obj in _obj.values():
                    obj.update({key: values})

            # check if new attribute is a list
            elif isinstance(values, list):
                for i, obj in enumerate(_obj.values()):
                    try:
                        obj[key] = values[i]
                    except KeyError:
                        pass

            # check if new attribute is a dict
            elif isinstance(values, dict):
                for k in _obj:
                    if k in values:
                        _obj[k][key] = values[k]
            # otherwise raise error
            else:
                LOG.error('Something went wrong, by formatting the values!')
                raise ValueError

        # remove None values from the objects
        for key, values in _obj.items():
            for attr, value in list(values.items()):
                if value is None:
                    _obj[key].pop(attr)

        return list(_obj.values())

# =============================================================================
# eof
#
# Local Variables:
# mode: python
# mode: linum
# mode: auto-fill
# fill-column: 79
# End:
