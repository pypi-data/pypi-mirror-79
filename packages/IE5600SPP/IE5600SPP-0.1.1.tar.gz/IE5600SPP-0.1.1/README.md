
## How to install 

```sh
pip install IE5600SPP
```

## Generate a graph

```python
import IE5600SPP as spp

g = spp.Graph()
```

## Add nodes

```python
g.add_node((3,4))
g.add_node((5,6))
```
## Add edge
```python
g.add_edge((5,6),(3,4),weight = 1, name = "test_edge")
```

## A star algorithm
```python
heu = lambda x,y: abs(x[0]-y[0])

spp.astar(g,(3,4),(5,6),heuristic = heu, weight = 'weight')
```