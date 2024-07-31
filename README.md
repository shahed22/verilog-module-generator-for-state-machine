# Verilog Module Creator

## Overview
This application allows users to create Verilog modules with various features such as state machines, input and output ports, and more.

## Files
- `main.py`: Entry point of the application.
- `gui.py`: Contains the GUI layout and related functions.
- `utils.py`: Utility functions for parsing and validation.
- `verilog_generator.py`: Functions for generating Verilog code.
- `graph_utils.py`: Functions for generating state diagrams using Graphviz.

## Working Flow

The Verilog Module Generator application follows these steps to create a Verilog module with a state machine:

1. **Start Application**
   - Launch the GUI application.

2. **Enter File Name**
   - Input the desired name for the Verilog module file.

3. **Select Clock and Reset Type**
   - Choose the clock edge type (posedge/negedge).
   - Choose the reset type (rst/rstn).

4. **Specify Ports**
   - Enter details for input ports (name:size).
   - Enter details for output ports (name:size).
   - Enter details for wire ports (name:size).
   - Enter details for register ports (name:size).

5. **Choose Machine Type**
   - Select the type of state machine (Mealy/Moore).

6. **State Machine Encoding**
   - Choose whether to use automatic or manual encoding for state names.

7. **Enter Number of States**
   - Input the total number of states in the state machine.

8. **Define State Names and Codes**
   - **Automatic Encoding:**
     - Enter state names, and the application will automatically generate codes based on the selected encoding style (Binary, Gray, One-hot).
   - **Manual Encoding:**
     - Enter state names and their corresponding codes manually.

9. **Generate State Diagram (Optional)**
   - Define state transitions and conditions between states to generate a state diagram.

10. **Create Verilog Module**
    - The application generates a Verilog module file with the specified parameters and state machine description.

11. **File Output**
    - Save the generated Verilog module file (.v) to the specified location.

### Working Flow Tree

```plaintext
+--------------------------------------+
|          Start Application           |
+--------------------------------------+
                   |
                   v
+--------------------------------------+
|         Enter File Name              |
+--------------------------------------+
                   |
                   v
+--------------------------------------+
|  Select Clock and Reset Type         |
+--------------------------------------+
                   |
                   v
+--------------------------------------+
|        Specify Ports                 |
|  - Input Ports                       |
|  - Output Ports                      |
|  - Wire Ports                        |
|  - Register Ports                    |
+--------------------------------------+
                   |
                   v
+--------------------------------------+
|        Choose Machine Type           |
+--------------------------------------+
                   |
                   v
+--------------------------------------+
|    State Machine Encoding            |
|  - Automatic                         |
|  - Manual                            |
+--------------------------------------+
                   |
                   v
+--------------------------------------+
|   Enter Number of States             |
+--------------------------------------+
                   |
                   v
+--------------------------------------+
| Define State Names and Codes         |
|  - Automatic Encoding                |
|  - Manual Encoding                   |
+--------------------------------------+
                   |
                   v
+--------------------------------------+
| Generate State Diagram (Optional)    |
+--------------------------------------+
                   |
                   v
+--------------------------------------+
|     Create Verilog Module            |
+--------------------------------------+
                   |
                   v
+--------------------------------------+
|        File Output                   |
+--------------------------------------+


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
<img width="369" alt="image" src="https://github.com/user-attachments/assets/921d4bdf-3330-4b03-9ff0-c33f7b9f0459">

