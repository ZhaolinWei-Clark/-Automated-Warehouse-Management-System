###################################################################################
#  Project:      Automated Warehouse Management System                            #
#  File:         itemrobot.py                                                     #
#  Team members: Kushal Sedhai     Haoyuan Jiang     Zhaolin Wei                  #
#  Student ID:   60286127          14636898          89282347                     #
#  Purpose:      Define core classes Item and Robot.                              #
#  Description:  This module contains the core definitions of the Item and Robot  #
#                classes. It includes methods for item management, robot movement #
#                using A* path planning, load handling, and task execution in a   #
#                dynamic warehouse environment.                                   #
###################################################################################

#################################### IMPORTS ######################################

import time
from path import PathPlanner
from collections import deque

############################### CLASS DEFINITIONS #################################

#===============================================================
#  Class:       Item
#  Attributes: 
#               item_name   : The name of the item
#               item_id     : The ID of the item
#               position    : The position of the item
#               unit_weight : The weight of each item
#               quantity    : The number of the item
#               weight      : The total weight of the item
#               state       : Determine whether the item can be operated on; True means it can, and the default is True.
#
class Item:
    def __init__(self, item_name, item_id, position, unit_weight, quantity, state = True):  # Added weight parameter
        self.item_name = item_name
        self.item_id = item_id
        self.position = position
        self.unit_weight = unit_weight
        self.quantity = quantity
        self.weight = self.quantity * self.unit_weight
        self.state = state

    def add_quantity(self, quantity):
        # add quantity
        self.quantity += quantity

    def add_weight(self, weight):
        # add weight
        self.weight += weight

#===============================================================
#  Class:       Robot
#  Attributes: 
#               robot_id      : The ID of the robot
#               capacity      : The cargo capacity of the robot
#               speed         : The speed of the robot
#               position      : The current position of the robot
#               robot_type    : The type of the robot
#               current_load  : The current load of the robot
#               carried_items : The current carried items of the robot
#               state         : Determine whether the robot can be assigned task; True means it can, and the default is True.
#
class Robot:
    def __init__(self, robot_id, initial_position=(0, 0)):
        self.robot_id = robot_id
        self.capacity = 20   # kg (default capacity)
        self.speed = 5        # grid/s (default speed)
        self.position = initial_position
        self.robot_type = 'standard'  # Added robot type attribute
        self.current_load = 0
        self.carried_items = []
        self.state = True

    def calculate_distance(self, point1, point2):
        # calculate distance
        return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])
    
    def can_complete_task(self, item_position, destination):
        # Determine whether the task can be completed
        distance_to_item = self.calculate_distance(self.position, item_position)
        distance_to_destination = self.calculate_distance(item_position, destination)
        distance_to_return = self.calculate_distance(destination, self.return_position)
        total_distance = distance_to_destination + distance_to_item + distance_to_return
        return total_distance <= self.max_travel_distance
    
    def can_carry(self, item, quantity):
        # Determine whether the robot can carry the item
        return item.unit_weight * quantity + self.current_load<= self.capacity
    
    def pick_item(self, item, quantity):
        # The parameters will change accordingly after picking up the item
        if self.can_carry(item, quantity):
            self.carried_items.append(item)
            self.current_load += item.unit_weight * quantity
            return True
        return False
    
    def release_load(self):
        # Release load
        self.current_load = 0

    def free_position(self, gui):
        # Reference chatGPT. Find the positions where neither items nor robots have been placed.
        x, y = self.position
    
        queue = deque([(x, y)])
        visited = set()
        visited.add((x, y))
    
        max_x = gui.warehouse.length
        max_y = gui.warehouse.width

        while queue:
            current_x, current_y = queue.popleft()

            if not any(item.position == (current_x, current_y) for item in gui.warehouse.items) and \
               not any(robot.position == (current_x, current_y) for robot in gui.warehouse.robots):
                return (current_x, current_y)

            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_x, new_y = current_x + dx, current_y + dy
                if 0 <= new_x < max_x and 0 <= new_y < max_y and (new_x, new_y) not in visited:
                    queue.append((new_x, new_y))
                    visited.add((new_x, new_y))
    
        return None

    def concession(self, gui):
        # If the robot is docked at the target location, it needs to move to a different position
        planner = PathPlanner(gui.warehouse.length, gui.warehouse.width)
        for item in gui.warehouse.items:
            planner.set_obstacle(item.position)


        for other_robot in gui.warehouse.robots:
            if other_robot != self:
                planner.set_obstacle(other_robot.position)
        
        rest_position = self.free_position(gui)
        path_to_rest = planner.find_path(self.position, rest_position)
        if gui.warehouse.destination:
            gui.warehouse.destination.pop(0)
        if path_to_rest:
            for step in path_to_rest:
                self.position = step
                gui.update_display()
                gui.root.update()
                time.sleep(1/self.speed)
        else:
            gui.update_task_info(f"Robot {self.robot_id} cannot find a valid rest position.")
        return

    def perform_task(self, item, destination, gui, quantity):
        """
        Perform the task of moving to the selected item's location, picking it up,
        and delivering it to the destination using A* path planning.
        """

        warehouse = gui.warehouse  # Use gui.warehouse to access the warehouse

        if not self.can_carry(item, quantity):
            print(f"Robot {self.robot_id} cannot carry item {item.item_id}: "
                  f"weight {item.weight * quantity} exceeds capacity {self.capacity}.")
            gui.update_task_info(f"Robot {self.robot_id} cannot carry {item.item_name}.")
            item.state = True
            if warehouse.destination:
                warehouse.destination.pop(0)
            return False

        # Initialize the path planner
        planner = PathPlanner(warehouse.length, warehouse.width)

        # Set obstacles: all other item positions and other robots' positions
        for other_item in warehouse.items:
            if other_item != item and other_item.position != destination:  # Exclude the target item
                planner.set_obstacle(other_item.position)
            if other_item.position == destination and other_item.item_name != item.item_name:
                gui.update_task_info(f"Destination is occupied by {other_item.item_name}.")
                item.state = True
                return False

        for other_robot in warehouse.robots:
            if other_robot != self and other_robot.position != destination:  # Exclude the current robot
                planner.set_obstacle(other_robot.position)

        # Step 1: Move to the item's position
        print(f"Robot {self.robot_id} moving to pick up {item.item_name}.")
        path_to_item = planner.find_path(self.position, item.position)
        if not path_to_item:
            gui.update_task_info(f"Robot {self.robot_id} cannot reach {item.item_name} at {item.position}.")
            item.state = True
            if warehouse.destination:
                warehouse.destination.pop(0)
            return False

        while path_to_item and self.position != item.position:
            step = path_to_item[1]  # Take the first step in the path
            self.position = step
            gui.update_display()
            gui.root.update()
            time.sleep(1 / self.speed)
            # Clear all obstacles and reset them
            planner.clear_obstacle()

            # Re-set the obstacles again (all other items and robots)
            for other_item in warehouse.items:
                if other_item != item and other_item.position != destination:
                    planner.set_obstacle(other_item.position)
                if other_item.position == destination and other_item.item_name != item.item_name:
                    gui.update_task_info(f"Destination is occupied by {other_item.item_name}.")
                    item.state = True
                    if warehouse.destination:
                        warehouse.destination.pop(0)
                    return False

            for other_robot in warehouse.robots:
                if other_robot != self and other_robot.position != destination:
                    planner.set_obstacle(other_robot.position)

            # Find a new path to the item
            path_to_item = planner.find_path(self.position, item.position)
            if not path_to_item:
                gui.update_task_info(f"Robot {self.robot_id} cannot reach {item.item_name} at {item.position}.")
                item.state = True
                if warehouse.destination:
                    warehouse.destination.pop(0)
                return False

        # Step 2: Check the path to the destination
        print(f"Robot {self.robot_id} delivering {item.item_name} to destination {destination}.")
        path_to_destination = planner.find_path(item.position, destination)
        while not path_to_destination:
            gui.update_task_info(f"Robot {self.robot_id} cannot reach destination {destination}. Redirecting to rest.")
            rest_position = self.free_position(gui)
            gui.update_task_info(f"Robot {self.robot_id} moving to rest position {rest_position}.")
            path_to_rest = planner.find_path(self.position, rest_position)
            item.state = True
            if warehouse.destination:
                warehouse.destination.pop(0)
            if path_to_rest:
                for step in path_to_rest:
                    self.position = step
                    gui.update_display()
                    gui.root.update()
                    time.sleep(1 / self.speed)
            else:
                gui.update_task_info(f"Robot {self.robot_id} cannot find a valid rest position.")
            return False

        # Step 3: Pick up the item
        if self.pick_item(item, quantity):
            gui.update_task_info(f"Robot {self.robot_id} picked up {item.item_name}.")
            print(f"Robot {self.robot_id} picked up {item.item_name}.")
            item.quantity -= quantity
            item.weight -= item.unit_weight * quantity
            if item.quantity > 0:
                item.state = True
            warehouse.remove_item()

        # Step 4: Move to the destination
        while path_to_destination and self.position != destination:
            step = path_to_destination[1]  # Take the first step in the path
            self.position = step
            gui.update_display()
            gui.root.update()
            time.sleep(1 / self.speed)
            # Clear all obstacles and reset them
            planner.clear_obstacle()

            # Re-set the obstacles again (all other items and robots)
            for other_item in warehouse.items:
                if other_item != item and other_item.position != destination:
                    planner.set_obstacle(other_item.position)
                if other_item.position == destination and other_item.item_name != item.item_name:
                    gui.update_task_info(f"Destination is occupied by {other_item.item_name}.")
                    return False

            for other_robot in warehouse.robots:
                if other_robot != self and other_robot.position != destination:
                    planner.set_obstacle(other_robot.position)

            # Find a new path to the item
            path_to_destination = planner.find_path(self.position, destination)
            if not path_to_destination:
                gui.update_task_info(f"Robot {self.robot_id} cannot reach {item.item_name} at {item.position}.")
                if warehouse.destination:
                    warehouse.destination.pop(0)
                return False

        # Step 5: Complete the task
        new_item = Item(item_name=item.item_name, item_id=item.item_id, position=destination, unit_weight=item.unit_weight, quantity=quantity)
        warehouse.create_item(new_item)
        self.release_load()
        gui.update_display()
        gui.root.update()
        gui.update_task_info(f"Robot {self.robot_id} delivered {item.item_name} to destination {destination}.")
        if warehouse.destination:
            warehouse.destination.pop(0)

        # Step 6: Return to rest
        rest_position = self.free_position(gui)
        gui.update_task_info(f"Robot {self.robot_id} returning to rest {rest_position}.")
        path_to_rest = planner.find_path(destination, rest_position)
        if not path_to_rest:
            gui.update_task_info(f"Robot {self.robot_id} cannot return to origin.")
            return

        for step in path_to_rest:
            self.position = step
            gui.update_display()
            gui.root.update()
            time.sleep(1 / self.speed)

        self.state = True

        return True

class LargeRobot(Robot):
    def __init__(self, robot_id, initial_position=(0, 0)):
        super().__init__(robot_id, initial_position)
        self.robot_type = 'large'
        self.capacity = 30 # kg  
        self.speed = 2 # grid/s (slower due to larger size)         

    def max_distance(self):
        return 5000  # max working distance of large robot

class SmallRobot(Robot):
    def __init__(self, robot_id, initial_position=(0, 0)):
        super().__init__(robot_id, initial_position)
        self.robot_type = 'mini'
        self.capacity = 10   # kg 
        self.speed = 5        # grid/s (faster due to smaller size)

    def max_distance(self):
        return 6000  # max working distance of small robot