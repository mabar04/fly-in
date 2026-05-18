*This project has been created as part of the 42 curriculum by \<mabar\>.*

# Fly In — Drone Network Simulation

Created by **mabar**

## Description

Fly In is a drone transportation and routing simulation project.
The goal of the project is to simulate drones moving through a network of hubs while respecting:

* Hub capacities
* Connection capacities
* Zone costs
* Priority and restricted zones
* Traffic conflicts
* Pathfinding constraints

The simulation uses graph theory and pathfinding algorithms to determine how drones travel from a start hub to an end hub.

---

# Features

## Core Features

* Graph-based network modeling
* Drone movement simulation
* Dijkstra shortest path algorithm
* Turn-by-turn simulation system
* Conflict resolution system
* Capacity management
* Priority/restricted zones
* Connection occupancy handling
* Dynamic drone states
* Logging system

---

# Project Architecture

## Main Components

### 1. Hubs

A hub represents a zone/node in the network.

Each hub contains:

* Name
* Coordinates
* Zone type
* Color
* Maximum drone capacity
* Current drones inside the hub
* Traversal cost

Example:

```txt
hub: A 1 0 [color=blue max_drones=3]
```

---

### 2. Connections

Connections link hubs together.

Each connection contains:

* Start hub
* End hub
* Maximum link capacity
* Current drones using the connection

Example:

```txt
connection: A-B
```

---

### 3. Drones

Each drone has:

* Unique ID
* Current zone
* Target zone
* Current connection
* Remaining travel time
* Status
* Current path
* Path index

Drone statuses:

* waiting
* travelling
* finished

---

### 4. Graph System

The graph system transforms hubs and connections into an adjacency list used for pathfinding.

Example:

```python
{
    "A": [("B", 1), ("C", 2)],
    "B": [("D", 1)]
}
```

---

### 5. Pathfinding

The project uses Dijkstra's algorithm to compute the shortest path between the start hub and the end hub.

The algorithm takes into account:

* Zone costs
* Path weights
* Alternative routes

---

# Simulation Pipeline

The simulation runs in turns.

Each turn follows this pipeline:

```txt
Update → Conflict Resolve → Decision → Transit → Logging
```

---

## 1. Update Phase

The update phase:

* Checks drone states
* Assigns next target hubs
* Finds target connections
* Marks finished drones

---

## 2. Conflict Resolution

This phase determines whether a drone is allowed to move.

Checks include:

* Hub capacity
* Connection capacity
* Current occupancy
* Predicted occupancy

Approved drones are marked for movement.

---

## 3. Decision Phase

Approved drones:

* Leave current zones
* Enter travelling state
* Reserve connection capacity
* Reserve target zone capacity

Rejected drones remain waiting.

---

## 4. Transit Phase

Travelling drones:

* Decrease remaining travel time
* Release connections when arriving
* Update current zone
* Advance path index

---

## 5. Logging Phase

The simulation prints all drone states for debugging and analysis.

Example:

```txt
D0 | status = travelling | zone = A
```

---

# Zones

## Normal Zone

Standard traversal behavior.

---

## Restricted Zone

Higher traversal cost.

May be used only when necessary.

---

## Priority Zone

Optimized traversal area.

Often preferred by the pathfinding algorithm.

---

# Drone Movement Logic

Drones move using:

* Path planning
* Turn-based execution
* Capacity-aware scheduling
* Conflict avoidance

The simulation prevents:

* Capacity overflow
* Multiple drones exceeding connection limits
* Invalid movements

---

# Predictive Reservation System

The project supports predictive movement logic.

Instead of waiting for a zone to become free:

* A drone may reserve a future slot
* Another drone can start moving early
* Pipeline movement becomes possible

Example:

```txt
D1 leaves Zone B → D2 starts moving to Zone B during same turn
```

This significantly improves throughput.


# Instructions

## Installation

## Requirements

* Python 3.11+

---

# Running the Project

## Run Simulation

```bash
python main.py maps/easy/01_linear_path.txt
```

---

# Makefile Example

```makefile
PYTHON = python3
NAME = maps/easy/01_linear_path.txt

run:
	$(PYTHON) main.py $(NAME)
```

Run:

```bash
make run
```

---

# Project Structure

```txt
fly_in/
│
├── main.py
├── simulation.py
├── hub.py
├── connection.py
├── drone.py
├── graph_modeling.py
├── pathfinding.py
├── helper_functions.py
│
├── maps/
│   ├── easy/
│   ├── medium/
│   └── hard/
│__ main.py
|
└── README.md
```

---

# Algorithms Used

## Dijkstra Algorithm

Used for shortest path computation.

Complexity:

```txt
O((V + E) log V)
```

When implemented using a heap.

---

# Algorithm Choices and Implementation Strategy

## Why Dijkstra?

The project uses Dijkstra's algorithm because the drone network behaves as a weighted graph.

Each hub has:

* A traversal cost
* Capacity constraints
* Zone properties

The objective is to minimize the total travel cost while respecting movement constraints.

Dijkstra was chosen because:

* All edge weights are positive
* It guarantees the shortest path
* It is efficient when combined with a heap
* It is easy to extend for advanced scheduling

---

## Graph Representation

The network is represented as an adjacency list.

Example:

```python
{
    "A": [("B", 1)],
    "B": [("C", 2)]
}
```

This representation was chosen because:

* It is memory efficient
* Faster neighbor traversal
* Easier integration with pathfinding
* Scales better for large maps

---

## Conflict Resolution Strategy

The simulation uses a reservation-based movement system.

For every turn:

1. Drones compute their next target
2. Capacities are checked
3. Slots are temporarily reserved
4. Approved drones move
5. Travelling drones update their state

This avoids:

* Capacity overflow
* Invalid simultaneous movement
* Connection congestion

---

## Predictive Scheduling

A predictive reservation strategy can be implemented to improve throughput.

Instead of waiting for a hub to become empty:

* A drone predicts that another drone will leave
* The destination slot is reserved in advance
* Both drones move during the same turn

This creates pipeline movement.

Example:

```txt
D1 leaves B → D2 enters B during same turn
```

This significantly improves performance on congested maps.

---

## Simulation Design Choices

The project was implemented using object-oriented programming.

Each entity has its own responsibility:

* Hub → zone management
* Connection → link management
* Drone → movement state
* Graph → topology generation
* Dijkstra → pathfinding
* Simulation → orchestration

This separation improves:

* Maintainability
* Debugging
* Extensibility
* Testing

---

## Terminal Visualization

The terminal visualization uses:

* ANSI colors
* Structured logs
* Turn-by-turn progression

Different colors represent:

* Zone types
* Drone states
* Connections
* Warnings/errors

Benefits:

* Easy debugging
* Fast visualization
* Lightweight execution
* Clear simulation tracking

---

# Resources

## Documentation and References

* Python Official Documentation
* pygame Documentation
* Dijkstra Algorithm Documentation
* Graph Theory Tutorials
* Priority Queue and Heap Documentation
* 42 Curriculum Resources

---

## AI Usage

AI tools were used during the project for:

* Understanding Dijkstra optimization
* Improving architecture design
* Brainstorming visualization ideas
* Reviewing simulation logic
* Generating debugging suggestions
* Improving README structure and documentation

AI was not used to fully generate the project.

The core architecture, simulation logic, debugging, and implementation decisions were designed and implemented manually.

---

# Future Improvements

Potential upgrades:

* A* pathfinding
* Dynamic rerouting
* Multi-path scheduling
* Real-time visualization
* Path reservation system
* Collision prediction
* AI traffic optimization
* Heatmap visualization
* Statistics dashboard

---

# Learning Objectives

This project teaches:

* Graph theory
* Pathfinding algorithms
* Scheduling systems
* Turn-based simulation
* Conflict resolution
* Resource reservation
* Visualization systems
* Object-oriented programming
* Software architecture

---

# Author

Developed by **mabar**.

---

# License

This project is for educational and learning purposes.
