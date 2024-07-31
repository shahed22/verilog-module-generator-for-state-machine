# Verilog Module Creator

## Overview
This application allows users to create Verilog modules with various features such as state machines, input and output ports, and more.

## Files
- `main.py`: Entry point of the application.
- `gui.py`: Contains the GUI layout and related functions.
- `utils.py`: Utility functions for parsing and validation.
- `verilog_generator.py`: Functions for generating Verilog code.
- `graph_utils.py`: Functions for generating state diagrams using Graphviz.

## Dependencies
- `tkinter`
- `graphviz`
- `re`

## Usage
1. Run `main.py` to start the application.
2. Enter the file name, select clock and reset types, and specify ports.
3. Choose encoding style and state machine type.
4. Click "Create Verilog Module" to generate the Verilog code and state diagram.

## License
This project is licensed under the MIT License.
