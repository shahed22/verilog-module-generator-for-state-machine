# verilog_generator.py
from graph_utils import generate_state_diagram
from tkinter import simpledialog, messagebox
import utils

def create_verilog_module(parent, file_name, clock_type, reset_type, input_ports, output_ports, wires, regs,
                          state_name, machine_type):
    """Create a Verilog module file with user-specified input and output ports and a state machine."""
    if not state_name:
        return
    reset_state = get_reset_state(parent, state_name)
    print(machine_type)
    with open(file_name, "w") as f:
        f.write(f"module {file_name[:-2]}(clk, {reset_type}")

        if input_ports:
            f.write(", " + ", ".join(input_ports.keys()))
        if output_ports:
            f.write(", " + ", ".join(output_ports.keys()))

        f.write(");\n")
        f.write("parameter ")
        f.write(", ".join([f"{name}={len(code)}'b{code}" for name, code in state_name.items()]) + ";\n")

        f.write(f"input clk, {reset_type};\n")

        write_ports(f, input_ports, "input")
        write_ports(f, output_ports, "output")
        k = dict(input_ports)
        k.update(output_ports)
        write_ports(f, wires, "wire")
        k.update(wires)
        write_ports(f, regs, "reg")
        k.clear()
        if reset_state is None:
            reset_state = get_reset_state(parent, state_name)
            if not reset_state:
                return

        lent=len(list(state_name.values())[0]) - 1
        if lent>0:
            f.write(f"reg [{lent}:0] ps, ns;\n")
        else:
            f.write(f"reg ps, ns;\n")
        f.write(f"always @({clock_type} clk or ")
        if reset_type == "rst":
            f.write("posedge ")
        else:
            f.write("negedge ")
        f.write(f"{reset_type}) begin\n")
        if reset_type == "rst":
            f.write(f"\tif ({reset_type})\n")
        else:
            f.write(f"\tif ({reset_type} == 0)\n")
        f.write(f"\t\tps <= {reset_state};\n")
        f.write("\telse\n")
        f.write("\t\tps <= ns;\n")
        f.write("end\n")

        f.write("always @(*) begin\n")
        f.write("\tcase(ps)")
        k.update(input_ports)
        k.update(wires)
        k.update(regs)
        write_state_transitions(f, file_name, state_name, k)
        f.write("\n\tendcase\n")
        f.write("end\n")

        f.write(f"always @(ps{(',' + ', '.join(input_ports.keys())) if machine_type == 'Mealy' else ''}) begin\n")
        f.write(f"\tcase (ps)")
        for state in state_name:
            f.write(f"\n\t\t{state}: begin\n\t\t\t")
            oo = True
            st = ""
            while oo != "Done":
                if oo != "Delete":
                    output_stmt = simpledialog.askstring(f"Output Logic for State {state}",
                                                         f"Already present logic is:{st}\nEnter output logic:",
                                                         parent=parent)
                tt = CustomDialog(parent, "Need to add or delete statement",
                                  f"Already present logic is:{st}\nchoose the option", ["Done", "Add more", "Delete"])
                parent.wait_window(tt)
                oo = tt.result
                if oo != "Delete":
                    st = st + "\n\t\t\t" + output_stmt
                else:
                    st = st[:st.rfind('\n')]

            f.write(f"{st};\n")
            f.write("\t\tend\n")
        f.write("\tendcase\n")
        f.write("end\n")
        f.write("endmodule\n")

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
                    condition = simpledialog.askstring(f"Condition for Transition {state} -> {tran_state}",
                                                       f"Condition to go from {state} to {tran_state} (enter 0 if no "
                                                       f"condition):",
                                                       parent=root)
                    if condition == "0" or is_valid_verilog_expression(condition, input_ports):
                        break
                    messagebox.showerror("Invalid Condition",
                                         "Invalid condition. Please enter a valid Verilog expression using input ports.")
                if condition != "0":
                    f.write(f"\n\t\t\tif({condition}) ns <= {tran_state};")
                    dot.edge(state, tran_state, label=condition)
    dot.format = 'png'
    dot.filename = file_name[:-2]
    dot.render()
    f.write("\n\t\tend")

def get_reset_state(parent, state_name):
    """Prompt the user for the reset state."""
    reset_state = simpledialog.askstring("Reset State",
                                         f"Enter your reset state (available states: {list(state_name.keys())}):",
                                         parent=parent)
    if reset_state in state_name:
        return reset_state
    messagebox.showerror("Invalid State", "Please enter an available state only.")
    return None
