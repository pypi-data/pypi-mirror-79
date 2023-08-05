from heapq import heappush, heappop
from itertools import count

__all__ = ["astar"]

def astar(G, source, target, heuristic=None, weight="weight"):
    if heuristic == None:
        def heuristic(u, v): return 0

    def weight(u, v, data): return data.get(weight, 1)

    c = count()
    queue = [(0, next(c), source, 0, None)]

    enqueued = {}
    explored = {}

    while queue:
        _, _, curnode, dist, parent = heappop(queue)

        if curnode == target:
            path = [curnode]
            node = parent
            while node is not None:
                path.append(node)
                node = explored[node]
            path.reverse()
            return path

        if curnode in explored:
            if explored[curnode] is None:
                continue

            qcost, h = enqueued[curnode]
            if qcost < dist:
                continue

        explored[curnode] = parent

        for neighbor, w in G[curnode].items():
            ncost = dist + weight(curnode, neighbor, w)
            if neighbor in enqueued:
                qcost, h = enqueued[neighbor]
                if qcost <= ncost:
                    continue
            else:
                h = heuristic(neighbor, target)
            enqueued[neighbor] = ncost, h
            heappush(queue, (ncost + h, next(c), neighbor, ncost, curnode))

    raise RuntimeError("No feasible path")
