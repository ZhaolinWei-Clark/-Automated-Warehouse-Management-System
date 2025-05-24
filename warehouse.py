###################################################################################
#  Project:      Automated Warehouse Management System                            #
#  File:         warehouse.py                                                     #
#  Team members: Kushal Sedhai     Haoyuan Jiang     Zhaolin Wei                  #
#  Student ID:   60286127          14636898          89282347                     #
#  Purpose:      To simulate and manage a warehouse using transport robots and    #
#                inventory tracking, incorporating tasks such as item assignment, #
#                robot navigation, and destination management via GUI.            #
#  Description:  This program defines a Warehouse class to manage robots, items,  #
#                and tasks in an automated warehouse. It includes functionality   #
#                for adding robots and items, assigning tasks, and tracking item  #
#                movement. The GUI provides visual updates and facilitates user   #
#                interactions.                                                    #
###################################################################################

#################################### IMPORTS ######################################

from path import PathPlanner

############################### CLASS DEFINITIONS #################################

#===============================================================
#  Class:       Warehouse
#  Attributes: 
#               length           : The length of the warehouse
#               width            : The width of the warehouse
#               stardard_robots  : The list of standard robots in the warehouse
#               large_robots     : The list of large robots in the warehouse
#               mini_robots      : The list of mini robots in the warehouse
#               robots           : The list of all robots in the warehouse
#               items            : The list of all items in the warehouse
#               destination      : The list of destinations for each task
#               assigned_items   : The list of assigned_items in the warehouse
#               unassigned_items : The list of unassigned_items in the warehouse
#               gui              : The gui that display the warehouse
#
class Warehouse:
    def __init__(self, length, width, gui=None):
        """
        Initialize the Warehouse object.

        Args:
            length (int): The length of the warehouse grid.
            width (int): The width of the warehouse grid.
            gui (object, optional): The GUI object to interact with. Defaults to None.
        """
        self.length = length
        self.width = width
        self.standard_robots = []
        self.large_robots = []
        self.mini_robots = []
        self.robots = []
        self.items = []
        self.destination = []
        self.assigned_items = []
        self.unassigned_items = []
        self.gui = gui

    def add_robot(self, robot):
        """
        Add a robot to the warehouse.

        Args:
            robot (object): The robot object to add.

        Returns:
            None
        """
        for existing_robot in self.robots:
            if existing_robot.position == robot.position:
                if self.gui:
                    self.gui.update_robot_info(f'Error: Position {robot.position} is already occupied. Cannot place new robot here.')
                return

        if robot.robot_type == "standard":
            self.standard_robots.append(robot)
        elif robot.robot_type == "large":
            self.large_robots.append(robot)
        else:
            self.mini_robots.append(robot)
        self.robots = self.large_robots + self.standard_robots + self.mini_robots
        if self.gui:
            self.gui.update_robot_info(f"A {robot.robot_type} size robot (ID: {robot.robot_id}) is added at position {robot.position}.")

    def add_item(self, item):
        """
        Add an item to the warehouse.

        Args:
            item (object): The item object to add.

        Returns:
            None
        """
        for existing_item in self.items:
            if existing_item.position == item.position:
                if existing_item.item_name == item.item_name:
                    if (item.unit_weight) == (existing_item.unit_weight):
                        existing_item.add_quantity(item.quantity)
                        existing_item.add_weight(item.weight)
                        if self.gui:
                            self.gui.update_item_info(
                                f"The number of {item.item_name} at position {item.position} increased by {item.quantity}.\n"
                                f"Now the Total Quantity is {existing_item.quantity} \n"
                                f"The Total Weight is {existing_item.weight}"
                            )
                        return
                    else:
                        if self.gui:
                            self.gui.update_item_info("Error: Unit Weight is different from before.")
                        return
                else:
                    if self.gui:
                        self.gui.update_item_info(
                            f"Error: Position {item.position} is already occupied by {existing_item.item_name}. Cannot place {item.item_name} here."
                        )
                    return
        for existing_item in self.items:
            if existing_item.item_name == item.item_name:
                if (item.unit_weight) == (existing_item.unit_weight):
                    self.items.append(item)
                    if self.gui:
                        self.gui.update_item_info(
                            f"Add Item {item.item_name} (ID: {item.item_id}) \n"
                            f"Quantity: {item.quantity} Total Weight: {item.weight} \n"
                            f"At position {item.position}."
                        )
                    return
                else:
                    if self.gui:
                        self.gui.update_item_info("Error: Unit Weight is different from that of the existing item.")
                    return

        self.items.append(item)
        if self.gui:
            self.gui.update_item_info(
                f"Add Item {item.item_name} (ID: {item.item_id}) \n"
                f"Quantity: {item.quantity} Total Weight: {item.weight} \n"
                f"At position {item.position}."
            )
        return

    def create_item(self, item):
        """
        Create an item in the warehouse.

        Args:
            item (object): The item object to create.

        Returns:
            None
        """
        for existing_item in self.items:
            if existing_item.position == item.position:
                if existing_item.item_name == item.item_name:
                    if (item.unit_weight) == (existing_item.unit_weight):
                        existing_item.add_quantity(item.quantity)
                        existing_item.add_weight(item.weight)
                        if self.gui:
                            self.gui.update_display()
                            self.gui.root.update()
                        return
                    else:
                        return
                else:
                    return
        for existing_item in self.items:
            if existing_item.item_name == item.item_name:
                if (item.unit_weight) == (existing_item.unit_weight):
                    self.items.append(item)
                    if self.gui:
                        self.gui.update_display()
                        self.gui.root.update()
                    return
                else:
                    return

        self.items.append(item)
        if self.gui:
            self.gui.update_display()
            self.gui.root.update()
        return

    def remove_item(self):
        """
        Remove items with zero quantity from the warehouse.

        Returns:
            None
        """
        self.items = [item for item in self.items if item.quantity > 0]

    def append_destination(self, destination):
        """
        Append a destination to the list.

        Args:
            destination (tuple): The destination coordinates.

        Returns:
            None
        """
        self.destination.append(destination)

    def assign_task(self, gui):
        """
        Assign a task to a robot.

        Args:
            gui (object): The GUI object for updating task information.

        Returns:
            None
        """
        if not self.destination:
            gui.update_task_info("No destination available. Please add a destination.")
            return

        destination = self.destination[0]
        if self.gui and self.gui.warehouse.destination:
            self.gui.warehouse.destination.pop(0)

        if not self.robots or not self.items:
            gui.update_task_info("No robots or items available.")
            return

        for robot in self.robots:
            if robot.position == destination:
                robot.concession(gui)

        selected_item_name = gui.item_var.get()
        selected_quantity = int(gui.quantity_entry.get())

        matching_items = [
            item
            for item in self.items
            if ((item.item_name == selected_item_name) and (item.position != destination) and item.state)
        ]

        if not matching_items:
            gui.update_task_info(f"There are no valid items that can be moved to {destination}.")
            if self.gui and self.gui.warehouse.destination:
                self.gui.warehouse.destination.pop(0)
            return

        if not selected_quantity or selected_quantity <= 0:
            gui.update_task_info("Please enter a valid quantity to move.")
            return

        def distance(robot, item):
            return abs(robot.position[0] - item.position[0]) + abs(robot.position[1] - item.position[1])

        matching_items.sort(key=lambda item: min(distance(robot, item) for robot in self.robots), reverse=True)

        remaining_quantity = selected_quantity
        processed_quantity = 0
        suitable_robot = None

        while remaining_quantity > 0 and matching_items:
            nearest_item = min(
                matching_items,
                key=lambda item: min(
                    abs(robot.position[0] - item.position[0]) + abs(robot.position[1] - item.position[1])
                    for robot in self.robots
                ),
            )
            pickup_quantity = min(remaining_quantity, nearest_item.quantity)
            suitable_robots = [
                robot
                for robot in self.robots
                if (robot.can_carry(nearest_item, selected_quantity) and robot.state)
            ]
            if not suitable_robots:
                gui.update_task_info(f"No robot can carry the selected item: {selected_item_name}")
                return
            suitable_robots.sort(key=lambda robot: distance(robot, nearest_item))

            for robot in suitable_robots:
                planner = PathPlanner(self.gui.warehouse.length, self.gui.warehouse.width)

                for other_item in self.gui.warehouse.items:
                    if other_item != nearest_item:
                        planner.set_obstacle(other_item.position)
                for other_robot in self.gui.warehouse.robots:
                    if other_robot != robot:
                        planner.set_obstacle(other_robot.position)

                path_to_item = planner.find_path(robot.position, nearest_item.position)
                if not path_to_item:
                    print(f"Robot {robot.robot_id} cannot reach {nearest_item.item_name} at {nearest_item.position}.")
                    continue

                gui.update_task_info(f"Task assigned to Robot {robot.robot_id} for item {nearest_item.item_name}.")
                suitable_robot = robot
                break

            if not suitable_robot:
                gui.update_task_info("No robot can reach the selected item due to obstacles.")
            else:
                suitable_robot.state = False
                nearest_item.state = False
            if suitable_robot.perform_task(nearest_item, destination, gui, pickup_quantity):
                processed_quantity += pickup_quantity
                remaining_quantity -= pickup_quantity
            else:
                return

            matching_items = [
                item for item in self.items if ((item.item_name == selected_item_name) and (item.position != destination))
            ]

            if not matching_items and remaining_quantity > 0:
                gui.add_task_info(
                    f"\nOnly quantity {processed_quantity} of item {selected_quantity} can be moved."
                )
                if self.gui and self.gui.warehouse.destination:
                    self.gui.warehouse.destination.pop(0)
                return

            matching_items.sort(key=lambda item: min(distance(robot, item) for robot in self.robots), reverse=True)

        gui.add_task_info(f"\nSuccessfully moved quantity {processed_quantity} of item {selected_item_name}")
        return