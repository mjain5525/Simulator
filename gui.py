"""
Tkinter GUI for Process Simulator (Desktop Version)
"""

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from src.simulator.units import Stream, Pump, Mixer

class SimulatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Process Simulator")
        self.root.geometry("800x600")

        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Input section
        input_frame = ttk.LabelFrame(main_frame, text="Feed Streams", padding="5")
        input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)

        # Stream 1
        ttk.Label(input_frame, text="Stream 1:").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(input_frame, text="Flow (mol/s):").grid(row=1, column=0, sticky=tk.W)
        self.flow1 = ttk.Entry(input_frame, width=10)
        self.flow1.insert(0, "10.0")
        self.flow1.grid(row=1, column=1)

        ttk.Label(input_frame, text="T (K):").grid(row=2, column=0, sticky=tk.W)
        self.temp1 = ttk.Entry(input_frame, width=10)
        self.temp1.insert(0, "300")
        self.temp1.grid(row=2, column=1)

        ttk.Label(input_frame, text="P (Pa):").grid(row=3, column=0, sticky=tk.W)
        self.press1 = ttk.Entry(input_frame, width=10)
        self.press1.insert(0, "100000")
        self.press1.grid(row=3, column=1)

        # Stream 2
        ttk.Label(input_frame, text="Stream 2:").grid(row=0, column=2, sticky=tk.W, padx=(20,0))
        ttk.Label(input_frame, text="Flow (mol/s):").grid(row=1, column=2, sticky=tk.W, padx=(20,0))
        self.flow2 = ttk.Entry(input_frame, width=10)
        self.flow2.insert(0, "5.0")
        self.flow2.grid(row=1, column=3)

        ttk.Label(input_frame, text="T (K):").grid(row=2, column=2, sticky=tk.W, padx=(20,0))
        self.temp2 = ttk.Entry(input_frame, width=10)
        self.temp2.insert(0, "300")
        self.temp2.grid(row=2, column=3)

        ttk.Label(input_frame, text="P (Pa):").grid(row=3, column=2, sticky=tk.W, padx=(20,0))
        self.press2 = ttk.Entry(input_frame, width=10)
        self.press2.insert(0, "100000")
        self.press2.grid(row=3, column=3)

        # Run button
        ttk.Button(main_frame, text="Run Simulation", command=self.run_simulation).grid(row=1, column=0, pady=10)

        # Results section
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding="5")
        results_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)

        self.results_text = tk.Text(results_frame, height=10, width=60)
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Matplotlib figure
        self.figure = plt.Figure(figsize=(6, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=main_frame)
        self.canvas.get_tk_widget().grid(row=3, column=0, pady=5)

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)

    def run_simulation(self):
        try:
            # Get inputs
            flow1 = float(self.flow1.get())
            temp1 = float(self.temp1.get())
            press1 = float(self.press1.get())
            flow2 = float(self.flow2.get())
            temp2 = float(self.temp2.get())
            press2 = float(self.press2.get())

            # Create streams
            stream1 = Stream(flow1, temp1, press1, {'CH4': 0.8, 'C2H6': 0.2})
            stream2 = Stream(flow2, temp2, press2, {'CH4': 0.9, 'C2H6': 0.1})

            # Simulate
            pump = Pump("Pump")
            pump.add_inlet(stream1)
            pump.simulate()

            mixer = Mixer("Mixer")
            mixer.add_inlet(pump.outlets[0])
            mixer.add_inlet(stream2)
            mixer.simulate()

            outlet = mixer.outlets[0]

            # Display results
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, f"Mixed Stream Results:\n")
            self.results_text.insert(tk.END, f"Flow Rate: {outlet.flow_rate:.2f} mol/s\n")
            self.results_text.insert(tk.END, f"Temperature: {outlet.T:.1f} K\n")
            self.results_text.insert(tk.END, f"Pressure: {outlet.P/1000:.1f} kPa\n")
            self.results_text.insert(tk.END, f"Composition:\n")
            for comp, frac in outlet.composition.items():
                self.results_text.insert(tk.END, f"  {comp}: {frac:.3f}\n")

            # Update plot
            self.ax.clear()
            self.ax.add_patch(plt.Rectangle((1, 1.5), 1, 1, fill=True, color='blue', alpha=0.5))
            self.ax.text(1.5, 2, 'Pump', ha='center', va='center')
            self.ax.add_patch(plt.Rectangle((3, 1.5), 1, 1, fill=True, color='green', alpha=0.5))
            self.ax.text(3.5, 2, 'Mixer', ha='center', va='center')

            # Draw streams
            self.ax.arrow(0, 2, 1, 0, head_width=0.1, head_length=0.1, fc='black', ec='black')
            self.ax.arrow(0, 1.8, 1, 0, head_width=0.1, head_length=0.1, fc='black', ec='black')
            self.ax.arrow(2, 2, 1, 0, head_width=0.1, head_length=0.1, fc='black', ec='black')
            self.ax.arrow(4, 2, 1, 0, head_width=0.1, head_length=0.1, fc='black', ec='black')

            self.ax.set_xlim(0, 6)
            self.ax.set_ylim(1, 3)
            self.ax.axis('off')
            self.ax.set_title("Process Flowsheet")

            self.canvas.draw()

        except ValueError as e:
            messagebox.showerror("Input Error", "Please enter valid numbers")
        except Exception as e:
            messagebox.showerror("Simulation Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = SimulatorGUI(root)
    root.mainloop()