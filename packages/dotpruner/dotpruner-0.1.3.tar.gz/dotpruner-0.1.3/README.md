# DotPruner ![DotPruner Python package Status](https://github.com/ansonmiu0214/DotPruner/workflows/tests/badge.svg) [![PyPI version](https://badge.fury.io/py/dotpruner.svg)](https://badge.fury.io/py/dotpruner)
Pruning redundant nodes from DOT graphs

Before:

![DOT graph before pruning](assets/before.png)

After: 

![DOT graph after pruning](assets/after.png)

## Installation

To install DotPruner with pip, run: `pip install dotpruner`

To install DotPruner from source, first clone the repository and then run: `python setup.py install`

## Usage

### CLI

Prune graph "in-place":
```bash
python -m dotpruner path/to/original/graph.dot
```

Use `--dest` or `-d` to specify destination for new graph:
```bash
python -m dotpruner path/to/original/graph.dot --dest path/to/new/graph.dot
```

Use `--overwrite` or `-o` to overwrite existing file in destination:
```bash
python -m dotpruner path/to/original/graph.dot -d path/to/new/graph.dot --overwrite
```

### API
```python
import dotpruner

# string representation of DOT graph
original_graph_str = ...

# pruned graph represented using pydot
pruned_graph = dotpruner.process_from_string(original_graph_str)
```

Optionally pass in a `node_picker` function
to change which node is preserved in the pruning stage --
by default, the lexicographically smaller node is preserved.

```python
# keep the lexicographically larger node
dotpruner.process_from_string(original_graph_str, node_picker=max)
```

## Tests
```bash
python -m unittest discover dotpruner.tests --verbose
```
