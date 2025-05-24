# MECH524 Project: Automated Warehouse Management System

## Team Members
- Haoyuan Jiang (14636898)
- Zhaolin Wei (89282347)
- Kushal Sedhai (60286127)

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Compilation](#compilation)
- [Usage Guide](#usage-guide)
- [Technical Implementation](#technical-implementation)
- [Known Issues](#known-issues)
- [Future Development](#future-development)

## Overview
The Automated Warehouse Management System (AWMS) is a sophisticated simulation platform for warehouse operations management. It provides a two-dimensional environment where users can define warehouse parameters, manage items and robots, and execute automated tasks through an intuitive graphical interface.

## Features

### Core Functionality
- Dynamic warehouse size configuration
- Real-time task assignment and execution
- Automated robot selection and path planning
- Multi-threaded task processing
- Interactive GUI for warehouse management
- Comprehensive warehouse information display

### Robot Types
- **Large Robot**
  - Higher carrying capacity
  - Slower movement speed
  - Suitable for heavy items
  
- **Small Robot**
  - Lower carrying capacity
  - Faster movement speed
  - Optimal for light items

### Key Features Breakdown
1. **Warehouse Management**
   - Customizable warehouse dimensions
   - Dynamic obstacle placement
   - Real-time space utilization tracking

2. **Item Management**
   - Item categorization
   - Weight-based sorting
   - Location tracking
   - Quantity management

3. **Robot Control**
   - Automated path finding
   - Real-time position updates
   - Task queue management
   - Collision avoidance

4. **Task Execution**
   - Priority-based scheduling
   - Multi-threaded operations
   - Real-time progress tracking
   - Error handling and recovery

## System Architecture

### File Structure
- **main.py**: Application entry point and system initialization
- **itemrobot.py**: Item and robot class definitions
- **warehouse.py**: Warehouse management logic
- **gui.py**: Graphical user interface implementation
- **path.py**: Path planning algorithms

### Code Structure
```python
# Example class structure
class Warehouse:
    def __init__(self, length, width):
        self.length = length
        self.width = width
        self.grid = [[None for _ in range(width)] for _ in range(length)]

class Robot:
    def __init__(self, position, speed):
        self.position = position
        self.speed = speed
        self.status = "idle"

class Item:
    def __init__(self, name, weight, quantity):
        self.name = name
        self.weight = weight
        self.quantity = quantity
```

### Key Components
1. **Item Management System**
   - Item creation and tracking
   - Storage location management
   - Inventory updates

2. **Robot Control System**
   - Movement control
   - Task assignment
   - Status monitoring

3. **Path Planning Module**
   - A* algorithm implementation
   - Obstacle avoidance
   - Route optimization

4. **Multi-threading Task Manager**
   - Task queue handling
   - Thread synchronization
   - Resource management

5. **Interactive GUI System**
   - Real-time visualization
   - User input processing
   - Status updates


## Dependencies
- Python 3.x
- tkinter: GUI framework
- threading: Multi-threading support
- time: Robot movement simulation
- heapq: Priority queue for A* algorithm
- collections.deque: Position processing

## Installation

### Prerequisites
- Python 3.x
- pip package manager

### Setup Process
1. Clone the repository:
```bash
git clone [repository-url]
```
2. Run the script using the following command:
```bash
python main.py
```
Or simply run the **"main.exe"** file directly.

## Compilation:

### Install pyinstaller
Open your terminal and use the `pip` command to install pyinstaller:
```bash
pip install pyinstaller
```
### Navigate to the Code Directory
Use the `cd` command to navigate to the directory containing the code. For example:
```bash
cd path\to\your\project
```
### Generate the .exe File
Execute the following command to convert the script into an .exe file:
```bash
pyinstaller --onefile main.py
```
The .exe file in the package is compiled for the **Windows** platform.

## Usage Guide

### Warehouse Configuration
1. **Set Warehouse Size**
   - Default size: 20x20
   - Customizable through GUI
   - Click "Set Warehouse Size"
   - Enter desired dimensions
   - Confirm with "Set Size"

### Item Management
1. **Placing Items**
   ```
   Steps:
   1. Click "Place Items"
   2. Enter item details:
      - Name
      - Weight
      - Quantity
   3. Click desired location
   4. Confirm placement
   ```

2. **Item Properties**
   - Name (unique identifier)
   - Unit weight
   - Quantity per location
   - Total weight calculation

### Robot Management
1. **Deploying Robots**
   ```
   Steps:
   1. Click "Place Robots"
   2. Select robot type
   3. Choose location
   4. Confirm deployment
   ```

2. **Robot Types Configuration**
   - Large Robot: Heavy loads
   - Small Robot: Quick movement

### Task Assignment
1. **Creating Tasks**
   ```
   Process:
   1. Click "Assign Task"
   2. Select item and quantity
   3. Choose destination
   4. System assigns optimal robot
   5. Monitor execution
   ```

2. **Task Execution**
   - Automatic robot selection
   - Path planning
   - Real-time progress tracking

### Information Display
1. **Warehouse Information**
   - Dimensions display
   - Item locations
   - Robot positions
   - Task status

2. **Monitoring Features**
   - Real-time updates
   - Status indicators
   - Error notifications


## Technical Implementation

### Path Planning
```python
# A* Algorithm Example Structure
def find_path(start, goal, obstacles):
    open_set = []
    closed_set = set()
    came_from = {}
    
    # Implementation details
```

### Multi-threading
```python
# Threading Implementation Example
class TaskManager:
    def __init__(self):
        self.task_queue = Queue()
        self.active_threads = []
```

### GUI Implementation
```python
# GUI Example Structure
class GUI:
    def __init__(self, master):
        self.master = master
        self.setup_interface()
```

## Known Issues
1. **Destination Conflicts**
   - Multiple robots targeting same location
   - Resolution: Implemented queuing system

2. **Threading Issues**
   - Occasional synchronization delays
   - Resource contention in heavy loads

3. **Formation Limitations**
   - Cross-path blocking
   - Complex navigation scenarios

## Future Development

### Short-term Goals
1. **Performance Optimization**
   - Enhanced path finding
   - Better thread management
   - Improved GUI responsiveness

2. **Feature Additions**
   - Advanced analytics
   - More robot types
   - Enhanced visualization

### Long-term Vision
1. **System Expansion**

   - Machine learning integration
   - Real-time optimization

2. **Architecture Improvements**
   - Scalability enhancements
   - Module optimization
   - Performance tuning


## Contact
For questions or support, please contact team members:
- Haoyuan Jiang
- Zhaolin Wei
- Kushal Sedhai

## Documentation
For detailed technical documentation, please refer to the project documentation in the docs folder.

---


### Support
For technical support or bug reports, please create an issue in the project repository.