###################################################################################
#  Project:      Automated Warehouse Management System                            #
#  File:         path.py                                                          #
#  Team members: Kushal Sedhai     Haoyuan Jiang     Zhaolin Wei                  #
#  Student ID:   60286127          14636898          89282347                     #
#  Purpose:      Plan appropriate paths for the robots.                           #
#  Description:  A class designed to model a path planning system in a warehouse  #
#                grid. It uses the A* algorithm to determine the shortest path    #
#                while avoiding obstacles. The grid is represented as a 2D matrix.#
###################################################################################

#################################### IMPORTS ######################################

import heapq

############################### CLASS DEFINITIONS #################################

#===============================================================
#  Class:       Pathplanner
#  Attributes:  length    : The length (rows) of the warehouse grid.
#               width     : The width (columns) of the warehouse grid.
#               grid      : A 2D list representing the grid, where 0 indicates 
#                           a free space and 1 indicates an obstacle.
#               obstacles : A set containing the positions of all obstacles.
#
class PathPlanner:
    def __init__(self, warehouse_length, warehouse_width):
        self.length = warehouse_length
        self.width = warehouse_width
        self.grid = [[0 for _ in range(warehouse_width)] for _ in range(warehouse_length)]
        self.obstacles = set()

    def set_obstacle(self, position):
        """Mark a position as an obstacle."""
        x, y = position
        if 0 <= x < self.length and 0 <= y < self.width:
            self.grid[x][y] = 1
            self.obstacles.add(position)
        else:
            raise ValueError("Obstacle position out of bounds.")

    def clear_obstacle(self):
        """Clear all obstacles by setting all grid cells to 0."""
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.length)]
        self.obstacles.clear()

    def is_valid(self, position):
        """Check if a position is valid (within bounds and not an obstacle)."""
        x, y = position
        return 0 <= x < self.length and 0 <= y < self.width and self.grid[x][y] == 0

    def heuristic(self, start, goal):
        """Manhattan distance heuristic for A*."""
        return abs(start[0] - goal[0]) + abs(start[1] - goal[1])

    def find_path(self, start, goal):
        """
        Find the shortest path from start to goal using A* algorithm.
        Returns a list of tuples representing the path.
        """
        if not self.is_valid(start) or not self.is_valid(goal):
            return None
            """
            raise ValueError("Start or goal position is invalid.")
            """

        # Priority queue for the open set
        open_set = []
        heapq.heappush(open_set, (0, start, start))  # (f_cost, current, start)

        # Dictionaries to track costs and path
        g_cost = {start: 0}
        came_from = {}
        closed_set = set()

        while open_set:
            # Get the position with the lowest F-cost
            _, current, original_start = heapq.heappop(open_set)

            # If we reach the goal, reconstruct the path
            if current == goal:
                return self.reconstruct_path(came_from, current)

            # Add current to closed set to avoid revisiting
            closed_set.add(current)

            # Explore neighbors
            neighbors = self.get_neighbors(current)
            for neighbor in neighbors:
                # Skip if already evaluated
                if neighbor in closed_set:
                    continue

                # Calculate tentative g cost
                tentative_g_cost = g_cost[current] + 1  # Assuming uniform cost

                # Check if this is a better path
                if neighbor not in g_cost or tentative_g_cost < g_cost[neighbor]:
                    # Update path and costs
                    came_from[neighbor] = current
                    g_cost[neighbor] = tentative_g_cost
                    f_cost = tentative_g_cost + self.heuristic(neighbor, goal)

                    # Add to open set if not already present
                    if neighbor not in [pos for _, pos, _ in open_set]:
                        heapq.heappush(open_set, (f_cost, neighbor, original_start))

        # If the loop ends without returning, no path exists
        return None

    def get_neighbors(self, position):
        """Return valid neighboring positions (up, down, left, right)."""
        x, y = position
        potential_neighbors = [
            (x - 1, y),  # Up
            (x + 1, y),  # Down
            (x, y - 1),  # Left
            (x, y + 1),  # Right
        ]
        return [n for n in potential_neighbors if self.is_valid(n)]

    def reconstruct_path(self, came_from, current):
        """Reconstruct the path from start to goal."""
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path