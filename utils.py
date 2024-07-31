# utils.py
import re
import datetime
from tkinter import simpledialog, messagebox

def is_valid_verilog_identifier(name):
    """Check if the given name is a valid Verilog identifier."""
    return re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', name) is not None

def parse_ports(ports_str):
    """Parse ports from a string in format (name:size, separated by commas)."""
    ports = {}
    for port in ports_str.split(','):
        if ':' in port:
            name, size = port.split(':')
            size = int(size)
            if is_valid_verilog_identifier(name) and size > 0:
                ports[name.strip()] = size
    return ports

def get_file_name(entry):
    """Retrieve the file name from the entry widget."""
    file_name = entry.get()
    if not file_name:
        file_name = "untitled_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    if is_valid_verilog_identifier(file_name):
        return file_name + ".v"
    messagebox.showerror("Invalid File Name",
                         "File name must start with a letter or underscore, followed by letters, digits, "
                         "or underscores.")
    return None

def get_encoding_style(parent):
    """Prompt the user for the encoding style using a dropdown in a popup dialog."""
    dialog = CustomDialog(parent, "Encoding Style", "Choose encoding style to be used:", ["Binary", "Gray", "One-hot"])
    parent.wait_window(dialog)
    encoding_style = dialog.result
    if encoding_style == "Binary":
        return 1
    elif encoding_style == "Gray":
        return 2
    elif encoding_style == "One-hot":
        return 3
    messagebox.showerror("Invalid Choice", "Invalid choice. Please try again.")
    return None

def get_state_machine_states(parent, state_num, seq):
    """Get the state names and their corresponding encodings for the state machine."""
    state_name = {}
    length = len(bin(state_num - 1)) - 2
    code = ""
    if seq == 1:
        encoding_style = get_encoding_style(parent)
        if encoding_style is None:
            return state_name

        for i in range(state_num):
            state = simpledialog.askstring("State Name", f"Enter state {i} name:", parent=parent)
            if encoding_style == 1:
                code = format(i, f'0{length}b')
            elif encoding_style == 2:
                code = format(grey_converter(i), f'0{length}b')
            elif encoding_style == 3:
                code = format(1 << i, f'0{state_num}b')
            state_name[state] = code
    else:
        for i in range(state_num):
            state = simpledialog.askstring("State Name", "Enter state name:", parent=parent)
            code = simpledialog.askstring("State Code", "Enter code:", parent=parent)
            state_name[state] = code

    return state_name

def grey_converter(n):
    """Convert a binary number to its Gray code equivalent."""
    return n ^ (n >> 1)
