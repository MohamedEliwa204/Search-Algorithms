import heapq
from collections import deque
import time

# list of available actions
actions = ["Up", "Down", "Left", "Right"]


class PuzzleNode:
    def __init__(self, state, parent_node=None, parent_action=None, g=0, h_func=None):
        self.state = tuple(state)  # to be able too put it in set
        self.parent_node = parent_node
        self.g = g  # cost from the start
        self.parent_action = parent_action  # to be able to keep track the path
        self.h_func = h_func  # to save it to the neighbors

        # calculate heuristic if provided
        if h_func:
            self.h = h_func(self.state)
            self.f = self.h + self.g

    # methods for priority queue
    def __lt__(self, other):
        return self.f < other.f

    # --- Methods for 'visited' set ---
    def __eq__(self, other):
        return self.state == other.state

    def __hash__(self):
        return hash(self.state)

    def get_neighbors(self):
        neighbors = []

        idx = self.state.index("0")
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
                        h_func=self.h_func  # to pass the h_func to the neighbor if it exists
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
                        h_func=self.h_func  # to pass the h_func to the neighbor if it exists
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
                        h_func=self.h_func  # to pass the h_func to the neighbor if it exists
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
                        h_func=self.h_func  # to pass the h_func to the neighbor if it exists
                    )
                    neighbors.append(new_node)

        return neighbors
