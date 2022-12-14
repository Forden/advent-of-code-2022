import queue
import typing

T = typing.TypeVar('T')


def bfs(
        connections_list: typing.Dict[T, typing.List[T]],
        start: T,
        target: T,
) -> typing.Tuple[typing.Dict[T, T], typing.Dict[T, int], bool]:
    vertexes_queue = queue.Queue()
    visited = {start: True}
    dists_from_start = {start: 0}
    parents = {}
    vertexes_queue.put(start)
    while not vertexes_queue.empty():
        checking_vertex = vertexes_queue.get()
        if checking_vertex not in connections_list:  # some vertexes dont have any connections
            continue
        for neighbour_vertex in connections_list[checking_vertex]:
            if not visited.get(neighbour_vertex, False):
                visited[neighbour_vertex] = True
                dists_from_start[neighbour_vertex] = dists_from_start[checking_vertex] + 1
                parents[neighbour_vertex] = checking_vertex
                vertexes_queue.put(neighbour_vertex)
                if neighbour_vertex == target:
                    return parents, dists_from_start, True
    return parents, dists_from_start, False


def construct_path_from_bfs(paths: typing.Dict[int, T], start: T, target: T) -> typing.List[T]:
    res_path = []
    cur_vertex = target
    while cur_vertex != start:
        res_path.append(cur_vertex)
        cur_vertex = paths[cur_vertex]
    res_path = list(reversed(res_path))
    return res_path
