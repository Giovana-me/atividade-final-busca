import heapq
from itertools import count
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class AStar(BaseSearch):

    def heuristic(self, state: State) -> int:
        distance = 0
        for index, tile in enumerate(state.tiles):
            if tile == 0:
                continue
            goal_index = tile - 1
            distance += abs(index // 3 - goal_index // 3)
            distance += abs(index % 3 - goal_index % 3)
        return distance

    def search(self, initial: State) -> SearchResult:
        tie_breaker = count()
        frontier = [
            (initial.cost + self.heuristic(initial), next(tie_breaker), initial)
        ]
        best_cost = {initial: initial.cost}
        best_depth = {initial: 0}
        nodes_expanded = 0
        nodes_generated = 1
        max_frontier_size = 1

        while frontier:
            _, _, current = heapq.heappop(frontier)
            if current.cost != best_cost[current]:
                continue

            if current.is_goal:
                return SearchResult(
                    solution=current,
                    nodes_expanded=nodes_expanded,
                    nodes_generated=nodes_generated,
                    max_frontier_size=max_frontier_size,
                    depth=best_depth[current],
                )

            nodes_expanded += 1
            for child in current.neighbors():
                known_cost = best_cost.get(child)
                if known_cost is not None and known_cost <= child.cost:
                    continue
                best_cost[child] = child.cost
                best_depth[child] = best_depth[current] + 1
                priority = child.cost + self.heuristic(child)
                heapq.heappush(
                    frontier, (priority, next(tie_breaker), child)
                )
                nodes_generated += 1

            max_frontier_size = max(max_frontier_size, len(frontier))

        return SearchResult(
            solution=None,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier_size,
        )
