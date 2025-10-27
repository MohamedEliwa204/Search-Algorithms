import heapq
import math
from collections import deque
import time

# list of available actions
actions = ["Up", "Down", "Left", "Right"]
GOAL_STATE = (0, 1, 2, 3, 4, 5, 6, 7, 8)


class PuzzleNode:
    def __init__(self, state, parent_node=None, parent_action=None, g=0, heuristic_name=None):
        self.state = tuple(state)  # to be able too put it in set
        self.parent_node = parent_node
        self.g = g  # cost from the start
        self.parent_action = parent_action  # to be able to keep track the path
        self.heuristic_name = heuristic_name  # to save it to the neighbors

        # calculate heuristic if provided
        if heuristic_name == "Manhattan":
            self.h = self.calculate_manhattan()
            self.f = self.h + self.g

        elif heuristic_name == "Euclidean":
            self.h = self.calculate_euclidean()
            self.f = self.h + self.g

    # methods for priority queue
    def __lt__(self, other):
        return self.f < other.f

    # Methods for 'visited' set
    def __eq__(self, other):
        return self.state == other.state

    def __hash__(self):
        return hash(self.state)

    def calculate_manhattan(self):
        dis = 0
        n = 3
        for idx, elem in enumerate(self.state):
            if elem == 0:
                continue
            curr_row, curr_col = divmod(idx, n)
            goal_row, goal_col = divmod(elem, n)
            dis += abs(curr_row - goal_row) + abs(curr_col - goal_col)
        return dis

    def calculate_euclidean(self):
        dis = 0
        n = 3
        for idx, elem in enumerate(self.state):
            if elem == 0:
                continue
            curr_row, curr_col = divmod(idx, n)
            goal_row, goal_col = divmod(elem, n)
            dis += math.sqrt(math.pow((curr_row - goal_row), 2) + math.pow((curr_col - goal_col), 2))
        return dis

    def get_neighbors(self):
        neighbors = []

        idx = self.state.index(0)
        for action in actions:
            if action == "Up":
                if idx < 3:  # if it in the first row it can't move UP
                    continue

                else:
                    neighbor = list(self.state)  # if it available to move the 0 up then swap it
                    temp = neighbor[idx - 3]
                    neighbor[idx - 3] = neighbor[idx]
                    neighbor[idx] = temp
                    new_node = PuzzleNode(
                        neighbor,
                        parent_node=self,
                        parent_action=action,
                        g=self.g + 1,
                        heuristic_name=self.heuristic_name  # to pass the heuristic_name to the neighbor if it exists
                    )
                    neighbors.append(new_node)

            elif action == "Down":
                if idx > 5:
                    continue

                else:
                    neighbor = list(self.state)  # if it available to move the 0 down then swap it
                    temp = neighbor[idx + 3]
                    neighbor[idx + 3] = neighbor[idx]
                    neighbor[idx] = temp
                    new_node = PuzzleNode(
                        neighbor,
                        parent_node=self,
                        parent_action=action,
                        g=self.g + 1,
                        heuristic_name=self.heuristic_name  # to pass the heuristic_name to the neighbor if it exists
                    )
                    neighbors.append(new_node)

            elif action == "Left":
                if idx % 3 == 0:
                    continue

                else:
                    neighbor = list(self.state)  # if it available to move the 0 left then swap it
                    temp = neighbor[idx - 1]
                    neighbor[idx - 1] = neighbor[idx]
                    neighbor[idx] = temp
                    new_node = PuzzleNode(
                        neighbor,
                        parent_node=self,
                        parent_action=action,
                        g=self.g + 1,
                        heuristic_name=self.heuristic_name  # to pass the heuristic_name to the neighbor if it exists
                    )
                    neighbors.append(new_node)

            elif action == "Right":
                if idx % 3 == 2:
                    continue

                else:
                    neighbor = list(self.state)  # if it available to move the 0 right then swap it
                    temp = neighbor[idx + 1]
                    neighbor[idx + 1] = neighbor[idx]
                    neighbor[idx] = temp
                    new_node = PuzzleNode(
                        neighbor,
                        parent_node=self,
                        parent_action=action,
                        g=self.g + 1,
                        heuristic_name=self.heuristic_name  # to pass the heuristic_name to the neighbor if it exists
                    )
                    neighbors.append(new_node)

        return neighbors


def goal_test(state):
    return state == GOAL_STATE


# search algorithms
def bfs(initial_state):
    queue = deque()
    start_node = PuzzleNode(initial_state)
    queue.append(start_node)
    if goal_test(start_node.state):
        print("you pass the goal😂")
        return start_node, [start_node], 0  # goal, visited_nodes, count

    visited = set()
    visited.add(start_node.state)

    nodes_expanded = []
    nodes_expanded_count = 0

    while (len(queue) != 0):
        f = queue.popleft()
        nodes_expanded.append(f)  # track expanded node
        nodes_expanded_count += 1

        for neighbor in f.get_neighbors():
            if neighbor.state not in visited:

                # Check the neighbor's state
                if goal_test(neighbor.state):
                    print("Goal Found!🥳🥳")
                    nodes_expanded.append(neighbor)

                    return neighbor, nodes_expanded, nodes_expanded_count

                visited.add(neighbor.state)
                queue.append(neighbor)

    print("failed to find the solution!😓")
    return None, nodes_expanded, nodes_expanded_count


def dfs(initial_state):
    stack = deque()
    start_node = PuzzleNode(initial_state)
    stack.append(start_node)
    if goal_test(start_node.state):
        print("you pass the goal😂")
        return start_node, [start_node], 0  # goal, visited_nodes, count

    visited = set()

    nodes_expanded = []
    nodes_expanded_count = 0

    while (len(stack) > 0):
        f = stack.pop()

        if f.state in visited:
            continue

        nodes_expanded.append(f)  # track expanded node
        nodes_expanded_count += 1

        for neighbor in f.get_neighbors():
            if neighbor.state not in visited:

                # Check the neighbor's state
                if goal_test(neighbor.state):
                    print("Goal Found!🥳🥳")
                    nodes_expanded.append(neighbor)

                    return neighbor, nodes_expanded, nodes_expanded_count
                visited.add(neighbor.state)
                stack.append(neighbor)

    print("failed to find the solution!😓")
    return None, nodes_expanded, nodes_expanded_count


def dldfs():
    pass


def A_star():
    pass
