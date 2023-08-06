import collections
import pydot
import typing
import sys

DEFAULT_NODE_PICKER = min

class Node:

    def __init__(self):
        self._edges = []

    def add_edge(self, dst, attrs):
        self._edges.append((dst, attrs))
    
    def edges(self, *, transform_key=None):
        if transform_key is None:
            transform_key = lambda key: key
        
        return sorted([(transform_key(key), value) for key, value in self._edges],
                       key=lambda pair: pair[0])


def parse_graph_from_file(filename: str) -> pydot.Graph:
    graph, *_ = pydot.graph_from_dot_file(filename)
    return graph

def parse_graph_from_string(data: str) -> pydot.Graph:
    graph, *_ = pydot.graph_from_dot_data(data)
    return graph

def parse_edges(graph: pydot.Graph) -> typing.Mapping[str, Node]:
    node_to_edges = collections.defaultdict(Node)

    for edge in graph.get_edges():
        src = edge.get_source()
        dst = edge.get_destination()
        attrs = edge.get_attributes()

        node_to_edges[src].add_edge(dst, attrs)

    return node_to_edges

def parse_nodes(graph: pydot.Graph) -> typing.Mapping[str, typing.Mapping[str, str]]:
    return {node.get_name(): node.get_attributes()
            for node in graph.get_nodes()}

def prune_graph(node_to_edges: typing.Mapping[str, Node],
                initial_lookup: typing.Mapping[str, str], *,
                pick_node):
    final_lookup = dict(**initial_lookup)
    should_prune_again = False

    for curr_node_name, curr_node in node_to_edges.items():
        for other_node_name, other_node in node_to_edges.items():

            if final_lookup[curr_node_name] == final_lookup[other_node_name]:
                continue

            # FIXME: let user customise definition of `edge equality`
            lookup_fn = lambda dst: final_lookup[dst]
            curr_edges = curr_node.edges(transform_key=lookup_fn)
            other_edges = other_node.edges(transform_key=lookup_fn)

            if curr_edges == other_edges:
                should_prune_again = True

                root_node_name = pick_node(curr_node_name, other_node_name)
                child_node_name = curr_node_name if root_node_name == other_node_name else other_node_name

                final_lookup[child_node_name] = root_node_name

    return prune_graph(node_to_edges, final_lookup, pick_node=pick_node) \
        if should_prune_again else final_lookup

def same_graph(graph_1: str, graph_2: str) -> bool:
    return sorted([line for line in graph_1.splitlines() if line.strip()]) \
        == sorted([line for line in graph_2.splitlines() if line.strip()])

def info(msg, **kwargs):
    print(f'INFO: {msg}', **kwargs, file=sys.stdout)

def error(msg, **kwargs):
    print(f'ERROR: {msg}', **kwargs, file=sys.stderr)