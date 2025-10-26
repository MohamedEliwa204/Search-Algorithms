import heapq
from collections import deque
import time


class PuzzleNode:
    def __init__(self, state, parent_node=None, parent_action=None, g=0, h_func=None):
        self.state = tuple(state) #to be able too put it in set
        self.parent_node = parent_node
        self.g = g #cost from the start
        self.parent_action = parent_action  # to be able to keep track the path

        #calculate heuristic if provided
        if h_func:
            self.h = h_func(self.state)
            self.f = self.h + self.g



