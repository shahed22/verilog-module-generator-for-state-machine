import re
import datetime
from graphviz import Digraph

def is_valid_verilog_identifier(name):
    """Check if the given name is a valid Verilog identifier."""
    return re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', name) is not None

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
            while True :
                state = simpledialog.askstring("State Name", f"Enter state {i}name:", parent=parent)
                if is_valid_verilog_identifier(state):
                    break
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

def generate_state_diagram(state_name, file_name):
    """Generate a PNG state diagram from the state machine definition."""
    dot = Digraph(comment='State Machine')

    for state in state_name:
        dot.node(state, state)

    for state in state_name:
        for next_state in state_name:
            condition = input(f"Condition for Transition {state} -> {next_state}: "
                              "Condition to go from {state} to {next_state} (enter 0 if no condition): ")
            if condition != "0":
                dot.edge(state, next_state, label=condition)

    # Save the diagram to a file
    dot.format = 'png'
    dot.filename = file_name
    dot.render()

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


def grey_converter(n):
    """Convert a binary number to its Gray code equivalent."""
    return n ^ (n >> 1)


class CustomDialog(tk.Toplevel):
    def __init__(self, parent, title, prompt, options):
        super().__init__(parent)
        self.transient(parent)
        self.grab_set()
        self.title(title)

        tk.Label(self, text=prompt).pack(pady=10)

        self.var = tk.StringVar()
        self.var.set(options[0])

        self.option_menu = ttk.OptionMenu(self, self.var, options[0], *options)
        self.option_menu.pack(pady=10)

        self.ok_button = tk.Button(self, text="OK", command=self.on_ok)
        self.ok_button.pack(pady=10)

        self.result = None

    def on_ok(self):
        self.result = self.var.get()
        self.destroy()


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
    raise ValueError("File name must start with a letter or underscore, followed by letters, digits, or underscores.")

def get_reset_state(parent, state_name):
    """Prompt the user for the reset state."""
    reset_state = input(f"Enter your reset state (available states: {list(state_name.keys())}): ")
    if reset_state in state_name:
        return reset_state
    raise ValueError("Please enter an available state only.")

def write_ports(f, ports, direction):
    """Write the Verilog port declarations to the file."""
    for size in sorted(set(ports.values()), reverse=True):
        port_list = [name for name, port_size in ports.items() if port_size == size]
        if direction == "output":
            k = " reg "
        else:
            k = " "
        f.write(f"{direction}{k}[{size - 1}:0] " if size > 1 else f"{direction}{k}")
        f.write(", ".join(port_list) + ";\n")

def write_state_transitions(f, file_name, state_name, input_ports):
    """Write the state transitions to the file."""
    dot = Digraph(comment='State Machine')
    for state in state_name:
        dot.node(state, state)
    for state in state_name:
        f.write(f"\n\t\t{state}: begin\n\t\t\tns <= {state};")
        for tran_state in state_name:
            if tran_state != state:
                while True:
                    condition = input(f"Condition for Transition {state} -> {tran_state}: "
                                      "Condition to go from {state} to {tran_state} (enter 0 if no condition): ")
                    if condition == "0" or is_valid_verilog_expression(condition, input_ports):
                        break
                    print("Invalid condition. Please enter a valid Verilog expression using input ports.")
                if condition != "0":
                    f.write(f"\n\t\t\tif({condition}) ns <= {tran_state};")
                    dot.edge(state, tran_state, label=condition)
        dot.format = 'png'
        dot.filename = file_name[:-2]
        dot.render()
        f.write("\n\t\tend")

def is_valid_verilog_expression(expr, input_ports):
    """Check if the given string is a valid Verilog expression and uses only valid input ports."""
    if not expr:
        return False

    # Check for balanced parentheses
    stack = []
    stack1 = []
    for char in expr:
        if char == '(':
            stack.append(char)
        elif char == ')':
            if not stack:
                return False
            stack.pop()
        if char == '?':
            stack1.append(char)
        elif char == ':':
            if not stack1:
                return False
            stack1.pop()

    if stack or stack1:
        return False

    # Verilog operators and identifiers pattern
    valid_pattern = re.compile(
        r'^[\s]*(?:\+|\-|\*|\/|\%|\*\*|<|>|<=|>=|==|===|!=|!==|'
        r'\!|\&\&|\|\||\&|\||<<|>>|<<<|>>>|\d+|\d+\'[bBoOdDhH][0-9a-fA-F]+)[\s]*$'
    )

    # Split the expression into tokens
    tokens = re.split(r'(\W+)', expr)
    if '?' in tokens or ':' in tokens:
        tokens.remove('?')
        tokens.remove(':')
    # Check each token
    for token in tokens[0:len(tokens) - 2]:
        token = token.strip()
        if not token:
            continue
        if not valid_pattern.match(token) and token not in input_ports.keys() and re.fullmatch(r'^[+-]?\d+(\.\d+)?([eE][+-]?\d+)?$', tokens[-1]) is not None:
            return False

    return True
