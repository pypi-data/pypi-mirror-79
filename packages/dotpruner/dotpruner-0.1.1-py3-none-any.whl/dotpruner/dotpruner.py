import pydot

from .utils import *

def process_from_file(filename: str, *,
                      node_picker = DEFAULT_NODE_PICKER) -> pydot.Graph:
    initial_graph = parse_graph_from_file(filename)
    final_graph = process_graph(initial_graph, node_picker)
    return final_graph

def process_from_string(data: str, *,
                        node_picker = DEFAULT_NODE_PICKER) -> pydot.Graph:
    initial_graph = parse_graph_from_string(data)
    final_graph = process_graph(initial_graph, node_picker)
    return final_graph

def process_graph(graph: pydot.Graph, node_picker) -> pydot.Graph:
    
    node_to_edges = parse_edges(graph)

    node_to_metadata = parse_nodes(graph)

    initial_lookup = {node: node for node in node_to_metadata}
    pruned_lookup = prune_graph(node_to_edges,
                                initial_lookup,
                                pick_node=node_picker)
    
    new_graph = pydot.Graph(graph_name=graph.get_name(),
                            **graph.get_attributes())
    added = set()
    for node in node_to_metadata:
        actual_node = pruned_lookup[node]
        if actual_node not in added:
            new_graph.add_node(pydot.Node(name=actual_node, **node_to_metadata[actual_node]))
            added.add(actual_node)

    for src in added:
        node = node_to_edges[src]
        for dst, attrs in node.edges():
            new_graph.add_edge(pydot.Edge(src=src, dst=pruned_lookup[dst], **attrs))

    return new_graph