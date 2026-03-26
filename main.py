#!/usr/bin/env python3
"""
Main entry point for the Simulator application.

For graphical interface, run: streamlit run app.py
"""

from src.simulator.simulation import example_simulation

if __name__ == "__main__":
    print("Running Process Simulator...")
    print("For GUI, run: streamlit run app.py")
    example_simulation()