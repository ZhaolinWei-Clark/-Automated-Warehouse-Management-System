###################################################################################
#  Project:      Automated Warehouse Management System                            #
#  File:         Auto_warehouse_management_system.py                              #
#  Team members: Kushal Sedhai     Haoyuan Jiang     Zhaolin Wei                  #
#  Student ID:   60286127          14636898          89282347                     #
#  Purpose:      To provide a GUI-based platform for managing an automated        #
#                warehouse system. It allows for placing items, robots, assigning #
#                tasks, and visualizing the warehouse layout and operations.      #
#  Description:  This script defines a Tkinter-based GUI for warehouse management #
#                where users can configure warehouse size, place items and robots,#
#                assign transport tasks, and display system information.          #
###################################################################################

#################################### IMPORTS ######################################

import tkinter as tk
import threading
from itemrobot import Item, Robot, LargeRobot, SmallRobot

############################### CLASS DEFINITIONS #################################

#===============================================================
#  Class:       GUI
#  Attributes: 
#               warehouse  : The warehouse object associated with this GUI
#               root       : The main Tkinter window
#               left_frame : Frame for the left section of the window (use to contain the grid)
#               canvas     : Canvas widget to display the warehouse layout
#               main_frame : Frame for the main section of the window (use to contain operation menu)
#        
class GUI:
    def __init__(self, warehouse):
        self.warehouse = warehouse
        self.warehouse.gui = self
        self.root = tk.Tk()
        self.root.title('Automated Warehouse Management System')

        self.left_frame = tk.Frame(self.root)
        self.left_frame.pack(side='left', fill='both')
        self.canvas = tk.Canvas(self.left_frame, width=1000, height=1000)
        self.canvas.pack()

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill='both')


        self.center_window(2000, 1200)

        self.update_display()

        self.main_menu()


    def main_menu(self):
        # Place components on the main menu
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Label(self.main_frame, text="Main Menu", font=("Arial", 16, "bold")).pack(pady=10, anchor='w')

        tk.Button(self.main_frame, text="Set Warehouse Size", command=self.show_size_settings).pack(pady=10, anchor='w')
        tk.Button(self.main_frame, text="Place Items", command=self.show_items_settings).pack(pady=10, anchor='w')
        tk.Button(self.main_frame, text="Place Robots", command=self.show_robots_settings).pack(pady=10, anchor='w')
        tk.Button(self.main_frame, text="Assign Task", command=self.show_tasks_settings).pack(pady=10, anchor='w')
        tk.Button(self.main_frame, text="Warehouse Imformation", command=self.show_details).pack(pady=10, anchor='w')

    def back_to_main_menu(self):
        # Unbind and return to the main menu
        self.canvas.unbind('<Button-1>')
        self.main_menu()

    def show_size_settings(self):
        # Place components on the first sub-menu, which is the menu entered by clicking 'Set Warehouse Size'
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        tk.Button(self.main_frame, text="Back to Main Menu", command=self.back_to_main_menu).pack(pady=10, anchor='w')

        tk.Label(self.main_frame, text="Set Warehouse Size", font=("Arial", 14, "bold")).pack(pady=10, anchor='w')

        size_frame = tk.Frame(self.main_frame)
        size_frame.pack(pady=10, anchor='w')

        tk.Label(size_frame, text="Length:").grid(row=0, column=0)
        self.length_entry = tk.Entry(size_frame, width=5)
        self.length_entry.insert(0, str(self.warehouse.length))
        self.length_entry.grid(row=0, column=1)

        tk.Label(size_frame, text="Width:").grid(row=0, column=2)
        self.width_entry = tk.Entry(size_frame, width=5)
        self.width_entry.insert(0, str(self.warehouse.width))
        self.width_entry.grid(row=0, column=3)

        tk.Button(self.main_frame, text="Set Size", command=self.set_warehouse_size).pack(pady=10, anchor='w')

        self.size_info_text = tk.Text(self.main_frame, height=5, width=40)
        self.size_info_text.pack(pady=5, anchor='w')

    def show_items_settings(self):
        """
        Place components on the second sub-menu, which is the menu entered by clicking 'Place Items'
        This menu is used to place items.
        """
        self.canvas.bind('<Button-1>', self.set_items_at_click)
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        tk.Button(self.main_frame, text="Back to Main Menu", command=self.back_to_main_menu).pack(pady=10, anchor='w')

        tk.Label(self.main_frame, text="Place Items", font=("Arial", 14, "bold")).pack(pady=10, anchor='w')

        info_frame = tk.Frame(self.main_frame)
        info_frame.pack(pady=10, anchor='w')

        tk.Label(info_frame, text="Item Name: ").grid(row=0, column=0)
        self.item_name_entry = tk.Entry(info_frame, width=5)
        self.item_name_entry.grid(row=0, column=1)

        tk.Label(info_frame, text="Unit Weight (kg): ").grid(row=1, column=0)
        self.item_weight_entry = tk.Entry(info_frame, width=5)
        self.item_weight_entry.insert(0, '1')
        self.item_weight_entry.grid(row=1, column=1)

        tk.Label(info_frame, text="Item Quantity: ").grid(row=2, column=0)
        self.item_quantity_entry = tk.Entry(info_frame, width=5)
        self.item_quantity_entry.insert(0, '1')
        self.item_quantity_entry.grid(row=2, column=1)

        self.item_info_label = tk.Label(self.main_frame, text="Item Information:", font=("Arial", 14, "bold"))
        self.item_info_label.pack(pady=5, anchor='w')

        self.item_info_text = tk.Text(self.main_frame, height=5, width=40)
        self.item_info_text.pack(pady=5, anchor='w')

        items_frame = tk.Frame(info_frame)
        items_frame.grid(row=4, column=0, columnspan=2)

    def show_robots_settings(self):
        """
        Place components on the third sub-menu, which is the menu entered by clicking 'Place Robots'
        This menu is used to place robots.
        """
        self.canvas.bind('<Button-1>', self.set_robots_at_click)
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        tk.Button(self.main_frame, text="Back to Main Menu", command=self.back_to_main_menu).pack(pady=10, anchor='w')

        tk.Label(self.main_frame, text="Place Robots", font=("Arial", 14, "bold")).pack(pady=10, anchor='w')

        tk.Label(self.main_frame, text="Robot Type:").pack(pady=10, anchor='w')
        self.robot_type_var = tk.StringVar(self.main_frame)
        self.robot_type_var.set('Standard Robot')  # Default value
        self.robot_type_menu = tk.OptionMenu(self.main_frame, self.robot_type_var, 
                                             'Standard Robot', 'Large Robot', 'Mini Robot')
        self.robot_type_menu.pack(pady=10, anchor='w')

        self.robot_info_label = tk.Label(self.main_frame, text="Robot Information:", font=("Arial", 14, "bold"))
        self.robot_info_label.pack(pady=5, anchor='w')

        self.robot_info_text = tk.Text(self.main_frame, height=5, width=40)
        self.robot_info_text.pack(pady=5, anchor='w')

    def show_tasks_settings(self):
        """
        Place components on the fourth sub-menu, which is the menu entered by clicking 'Assign Task'
        This menu is used to assign tasks.
        """
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        tk.Button(self.main_frame, text="Back to Main Menu", command=self.back_to_main_menu).pack(pady=10, anchor='w')

        tk.Label(self.main_frame, text="Assign Tasks", font=("Arial", 14, "bold")).pack(pady=10, anchor='w')

        self.destination_frame = tk.Frame(self.main_frame)
        self.destination_frame.pack(pady=10, anchor='w')

        self.move_label = tk.Label(self.destination_frame, text="Move:")
        self.move_label.grid(row=0, column=0)
        self.item_var = tk.StringVar(self.destination_frame)
        self.item_var.set('Select Item')  # Default value

        item_names = [item.item_name for item in self.warehouse.items]  # Get the item names from the warehouse
        if item_names:
            item_names = list(set(item_names)) 
        else:
            item_names = ['No Items Available'] 

        self.item_menu = tk.OptionMenu(self.destination_frame, self.item_var, *item_names)
        self.item_menu.grid(row=0, column=1)

        self.task_quantity_label = tk.Label(self.destination_frame, text='Quantity:')
        self.task_quantity_label.grid(row=0, column=2)
        self.quantity_entry = tk.Entry(self.destination_frame, width=5)
        self.quantity_entry.grid(row=0, column=3)
        
        self.destination_x_label = tk.Label(self.destination_frame, text='to X:')
        self.destination_x_label.grid(row=1, column=0)
        self.destination_x_entry = tk.Entry(self.destination_frame, width=5)
        self.destination_x_entry.grid(row=1, column=1)
        
        self.destination_y_label = tk.Label(self.destination_frame, text='Y:')
        self.destination_y_label.grid(row=1, column=2)
        self.destination_y_entry = tk.Entry(self.destination_frame, width=5)
        self.destination_y_entry.grid(row=1, column=3)

        tk.Button(self.main_frame, text="Assign task", command=self.start_task).pack(pady=10, anchor='w')

        self.task_info_label = tk.Label(self.main_frame, text="Task Allocation Status", font=("Arial", 10, "bold"))
        self.task_info_label.pack(pady=5, anchor='w')

        self.task_info_text = tk.Text(self.main_frame, height=5, width=40)
        self.task_info_text.pack(pady=5, anchor='w')

    def show_details(self):
        """
        Place components on the fifth sub-menu, which is the menu entered by clicking 'Warehouse Imformation'. 
        This menu is used to view the information of the items and robots placed in the warehouse.
        """
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Button(self.main_frame, text="Back to Main Menu", command=self.back_to_main_menu).pack(pady=10, anchor='w')

        tk.Label(self.main_frame, text="Warehouse Details", font=("Arial", 14, "bold")).pack(pady=10, anchor='w')

        self.size_label = tk.Label(self.main_frame, text=f"Warehouse Size: {self.warehouse.length} x {self.warehouse.width}")
        self.size_label.pack(pady=5, anchor='w')

        self.items_frame = tk.Frame(self.main_frame)
        self.items_frame.pack(pady=5, anchor='w')

        self.items_label = tk.Label(self.items_frame, text="Items in Warehouse:")
        self.items_label.grid(row=0, column=0)

        self.item_var = tk.StringVar(self.items_frame)
        self.item_var.set('Select Item')  # Default value

        item_names = [item.item_name for item in self.warehouse.items]  # Get the item names from the warehouse
        if item_names:
            item_names = list(set(item_names)) 
        else:
            item_names = ['No Items Available'] 

        self.item_menu = tk.OptionMenu(self.items_frame, self.item_var, *item_names)
        self.item_menu.grid(row=0, column=1)
        tk.Button(self.items_frame, text="Search Items", command=self.search_items).grid(row=0, column=2)

        self.robots_frame = tk.Frame(self.main_frame)
        self.robots_frame.pack(pady=5, anchor='w')
        self.robots_label = tk.Label(self.robots_frame, text="Robots in Warehouse:")
        self.robots_label.grid(row=0, column=0)
        self.robot_var = tk.StringVar(self.robots_frame)
        self.robot_var.set('standard')
        self.robot_menu = tk.OptionMenu(self.robots_frame, self.robot_var, 'standard', 'large', 'mini')
        self.robot_menu.grid(row=0, column=1)
        tk.Button(self.robots_frame, text="Search Robots", command=self.search_robots).grid(row=0, column=2)

        self.results_frame = tk.Frame(self.main_frame)
        self.results_frame.pack(pady=5, anchor='w')

    def set_warehouse_size(self):
        # set the size of the warehouse
        try:
            length = int(self.length_entry.get())
            width = int(self.width_entry.get())
            if length > 0 and width > 0:
                self.warehouse.length = length
                self.warehouse.width = width
                self.update_display()
            else:
                self.update_size_info('Please enter positive values for length and width.')
        except Exception as e:
            self.update_size_info('Invalid input. Please enter numeric value.')

    def set_items_at_click(self, event):
        # Place items in the warehouse by clicking with the mouse.

        # Convert mouse click coordinates to grid coordinates.
        cell_width = 700 // self.warehouse.width
        cell_height = 700 // self.warehouse.length
        x = event.x // cell_width
        y = event.y // cell_height

        if self.is_valid_grid_position(x, y):
            # Set item position.
            item_name = self.item_name_entry.get()
            try:
                item_weight = float(self.item_weight_entry.get())
                item_quantity = int(self.item_quantity_entry.get())
            except ValueError:
                self.update_item_info('Invalid value. Please set the weight and quantity correctly.')
                return

            if item_name:
                existing_item = next((item for item in self.warehouse.items if item.item_name == item_name), None)
                if existing_item:
                    item_id = existing_item.item_id
                else:
                    item_names = [item.item_name for item in self.warehouse.items]  # Get the item names from the warehouse
                    if item_names:
                        item_names = list(set(item_names)) 
                    else:
                        item_names = []
                    item_id = len(item_names) + 1
                new_item = Item(item_name=item_name, item_id=item_id, position=(x, y), unit_weight=item_weight, quantity=item_quantity)
                self.warehouse.add_item(new_item)
            else:
                self.update_item_info('Item name cannot be empty.')

            # Update display.
            self.update_display()
        else:
            self.update_item_info('Please place the item with in the gird.')

    def set_robots_at_click(self, event):
        # Place robots in the warehouse by clicking with the mouse.

        # Convert mouse click coordinates to grid coordinates.
        cell_width = 700 // self.warehouse.width
        cell_height = 700 // self.warehouse.length
        x = event.x // cell_width
        y = event.y // cell_height

        if self.is_valid_grid_position(x, y):

            # Create robot based on selected type
            if self.robot_type_var.get() == 'Large Robot':
                robot_id = len(self.warehouse.large_robots) + 1
                new_robot = LargeRobot(robot_id)
            elif self.robot_type_var.get() == 'Mini Robot':
                robot_id = len(self.warehouse.mini_robots) + 1
                new_robot = SmallRobot(robot_id)
            else:
                robot_id = len(self.warehouse.standard_robots) + 1
                new_robot = Robot(robot_id)
                
            new_robot.position = (x, y)
            self.warehouse.add_robot(new_robot)
            # Update display.
            self.update_display()
        else:
            self.update_robot_info('Please place the robot with in the gird.')
    
    def search_items(self):
        # Seach the information of certain item
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        if self.warehouse.items:
            for item in self.warehouse.items:
                if item.item_name == self.item_var.get():
                    item_info = f"Name: {item.item_name}, ID: {item.item_id}\nPosition: {item.position}, Unit Weight: {item.unit_weight} kg, Quantity: {item.quantity}, Total Weight: {item.weight} kg."
                    tk.Label(self.results_frame, text=item_info, font=("Arial", 10)).pack(pady=10, anchor='w')
        else:
            tk.Label(self.results_frame, text="No items available", font=("Arial", 10)).pack(pady=10, anchor='w')

    def search_robots(self):
        # Seach the information of certain type robot
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        if self.warehouse.robots:
            for robot in self.warehouse.robots:
                if robot.robot_type == self.robot_var.get():
                    robot_info = f"Type: {robot.robot_type}, ID: {robot.robot_id}, Speed: {robot.speed} grid/s, Position: {robot.position}."
                    tk.Label(self.results_frame, text=robot_info, font=("Arial", 10)).pack(pady=10, anchor='w')
        else:
            tk.Label(self.results_frame, text="No robots available", font=("Arial", 10)).pack(pady=10, anchor='w')

    def start_task(self):
        # start task
        try:
            x = int(self.destination_x_entry.get())
            y = int(self.destination_y_entry.get())
            
            if 0 <= x < self.warehouse.width and 0 <= y < self.warehouse.length:
                self.warehouse.append_destination((x, y))
                self.update_task_info(f"Added destination at ({x}, {y})")
                self.update_display()
            else:
                self.update_task_info("Invalid destination coordinates")
        except ValueError:
            self.update_task_info("Please enter valid numeric coordinates")
        task_thread = threading.Thread(target=self.warehouse.assign_task, args=(self,))
        task_thread.start()

    def update_display(self):
        # Update the display of the warehouse
        self.canvas.delete('all')

        # Draw warehouse grid.
        cell_width = 700 // self.warehouse.width
        cell_height = 700 // self.warehouse.length

        for x in range(self.warehouse.width):
            for y in range(self.warehouse.length):
                self.canvas.create_rectangle(x * cell_width, y * cell_height, (x + 1) * cell_width, (y + 1) * cell_height, outline='gray')

        # Draw robot position.
        for robot in self.warehouse.robots:
            x, y = robot.position
            color = 'blue' if robot.robot_type == 'standard' else ('green' if robot.robot_type == 'large' else 'red')
            self.canvas.create_rectangle(x * cell_width, y * cell_height, (x + 1) * cell_width, (y + 1) * cell_height, fill=color)
            self.canvas.create_text((x + 0.5) * cell_width, (y + 0.5) * cell_height, text=f'{robot.robot_type[0].upper()}{robot.robot_id}', fill='white')

        # Draw item position.
        for item in self.warehouse.items:
            x, y = item.position
            self.canvas.create_rectangle(x * cell_width, y * cell_height, (x + 1) * cell_width, (y + 1) * cell_height, fill='orange')
            self.canvas.create_text((x + 0.5) * cell_width, (y + 0.5) * cell_height, text=f'{item.item_name}\n{item.weight}kg', fill='white')

    def run(self):
        # Run the gui
        self.root.mainloop()

    def update_size_info(self, message):
        # Update the infomation displayed in 'Set Warehouse Size' menu
        "update"
        self.size_info_text.delete(1.0, tk.END)
        self.size_info_text.insert(tk.END, message)

    def update_item_info(self, message):
        # Update the infomation displayed in 'Place Items' menu
        "update"
        self.item_info_text.delete(1.0, tk.END)
        self.item_info_text.insert(tk.END, message)

    def update_robot_info(self, message):
        # Update the infomation displayed in 'Place Robots' menu
        "update"
        self.robot_info_text.delete(1.0, tk.END)
        self.robot_info_text.insert(tk.END, message)

    def update_task_info(self, message):
        # Update the infomation displayed in 'Assign task' menu
        "update"
        self.task_info_text.delete(1.0, tk.END)
        self.task_info_text.insert(tk.END, message)

    def add_task_info(self, message):
        # Add the infomation displayed in 'Assign task' menu
        "add"
        self.task_info_text.insert(tk.END, message)

    def center_window(self, width, height):
        # To ensure the GUI window appears in an appropriate position on the screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def is_valid_grid_position(self, x, y):
        # To check if a position is within the boundaries of the warehouse
        return 0 <= x < self.warehouse.length and 0 <= y < self.warehouse.width