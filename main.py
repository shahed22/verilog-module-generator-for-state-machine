# main.py
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from gui import create_gui
from verilog_generator import create_verilog_module
from utils import parse_ports, get_file_name, get_state_machine_states
from graph_utils import generate_state_diagram

def main():
    root = tk.Tk()
    root.title("Verilog Module Creator")

    create_gui(root)

    root.mainloop()

if __name__ == "__main__":
    main()
