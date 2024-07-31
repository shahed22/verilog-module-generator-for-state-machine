# gui.py
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from utils import get_encoding_style, parse_ports, get_state_machine_states
from verilog_generator import create_verilog_module

def create_gui(root):
    tk.Label(root, text="Enter File Name:").grid(row=0, column=0)
    file_name_entry = tk.Entry(root)
    file_name_entry.grid(row=0, column=1)

    # Clock Type Dropdown
    tk.Label(root, text="Clock Type:").grid(row=1, column=0, padx=10, pady=5)
    clock_type_var = tk.StringVar(value="posedge")
    clock_type_dropdown = ttk.Combobox(root, textvariable=clock_type_var, values=["posedge", "negedge"])
    clock_type_dropdown.grid(row=1, column=1, padx=10, pady=5)

    # Reset Type Dropdown
    tk.Label(root, text="Reset Type:").grid(row=2, column=0, padx=10, pady=5)
    reset_type_var = tk.StringVar(value="rst")
    reset_type_dropdown = ttk.Combobox(root, textvariable=reset_type_var, values=["rst", "rstn"])
    reset_type_dropdown.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(root, text="Input Ports (name:size, separated by commas):").grid(row=3, column=0)
    input_ports_entry = tk.Entry(root)
    input_ports_entry.grid(row=3, column=1)

    tk.Label(root, text="Output Ports (name:size, separated by commas):").grid(row=4, column=0)
    output_ports_entry = tk.Entry(root)
    output_ports_entry.grid(row=4, column=1)

    tk.Label(root, text="Wire Ports (name:size, separated by commas):").grid(row=5, column=0)
    wire_ports_entry = tk.Entry(root)
    wire_ports_entry.grid(row=5, column=1)

    tk.Label(root, text="Register Ports (name:size, separated by commas):").grid(row=6, column=0)
    reg_ports_entry = tk.Entry(root)
    reg_ports_entry.grid(row=6, column=1)

    # Machine Type Dropdown
    tk.Label(root, text="Machine Type:").grid(row=8, column=0, padx=10, pady=5)
    machine_type_var = tk.StringVar(value="Mealy")
    machine_type_dropdown = ttk.Combobox(root, textvariable=machine_type_var, values=["Mealy", "Moore"])
    machine_type_dropdown.grid(row=8, column=1, padx=10, pady=5)

    state_machine_seq = tk.IntVar()
    state_machine_seq.set(1)
    tk.Label(root, text="State Machine Encoding:").grid(row=7, column=0)
    tk.Radiobutton(root, text="Automatic", variable=state_machine_seq, value=1).grid(row=7, column=1)
    tk.Radiobutton(root, text="Manual", variable=state_machine_seq, value=0).grid(row=7, column=2)

    tk.Button(root, text="Create Verilog Module",
              command=lambda: create_verilog_module(
                  root, get_file_name(file_name_entry), clock_type_var.get(),
                  reset_type_var.get(), parse_ports(input_ports_entry.get()),
                  parse_ports(output_ports_entry.get()), parse_ports(wire_ports_entry.get()),
                  parse_ports(reg_ports_entry.get()), get_state_machine_states(
                      root, int(simpledialog.askstring("Number of States", "Enter number of states:", parent=root)),
                      state_machine_seq.get()), machine_type_var.get())
              ).grid(row=10, column=0, columnspan=3)
