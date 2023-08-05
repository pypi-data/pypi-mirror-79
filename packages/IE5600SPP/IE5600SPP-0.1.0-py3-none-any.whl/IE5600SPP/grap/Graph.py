__all__ = ["Graph"]

class Graph():
    def __init__(self):
        self._node = dict()
        self._adj = dict()

    def add_node(self, node_for_adding, **attr):
        if node_for_adding not in self._node:
            self._adj[node_for_adding] = dict()
            attr_dict = self._node[node_for_adding] = dict()
            attr_dict.update(attr)
        else:  # update attr even if node already exists
            self._node[node_for_adding].update(attr)

    def add_edge(self, node1, node2, **attr):
        # print(attr)
        u, v = node1, node2
        if u not in self._node:
            self.add_node(u)
        if v not in self._node:
            self.add_node(v)

        data = self._adj[u].get(v, dict())
        data.update(attr)
        self._adj[u][v] = data
        self._adj[v][u] = data

    def __iter__(self):
        return iter(self._node)

    def __getitem__(self, n):
        return self._adj[n]

    def __contains__(self, n):
        try:
            return n in self._node
        except TypeError:
            return False
