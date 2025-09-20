# Campus Pathfinding App

A Python-based campus navigation application that helps users find the shortest path between buildings on the GSU campus using Dijkstra's algorithm.

## Features

- Interactive GUI with building selection dropdowns
- Visual campus map with building positions and distances
- Shortest path calculation using NetworkX
- Real-time path visualization with highlighted routes
- Distance display in meters
- Reset functionality to clear selections

## Demo

![App Walkthrough](path/to/your/walkthrough.gif)

*App demonstration showing pathfinding between campus buildings*

## Campus Buildings

The application includes the following GSU campus buildings:
- Library South
- Langdale Hall
- 25 Park Place
- 55 Park Place
- Petit Science Center
- Aderhold
- University Commons
- University Lofts

## Installation

1. Make sure you have Python 3.7+ installed
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python campus_navigator.py
   ```

2. Select a starting building from the "Start" dropdown
3. Select a destination building from the "End" dropdown
4. Click "Find Path" to see the shortest route highlighted on the map
5. Use "Reset" to clear your selections and start over

## Technical Details

- Built with Python Tkinter for the GUI
- Uses NetworkX for graph algorithms and shortest path calculation
- Matplotlib integration for interactive campus map visualization
- Graph-based representation of campus with weighted edges (distances in meters)

## Requirements

- Python 3.7+
- tkinter (usually included with Python)
- networkx>=3.0
- matplotlib>=3.7.0
