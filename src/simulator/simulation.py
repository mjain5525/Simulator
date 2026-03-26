"""
Simulation engine for process flowsheets.

This module provides the main simulation class that solves the flowsheet.
"""

from .units import Stream, Pump, Mixer
from .thermodynamics import PengRobinsonEOS
import numpy as np

class Flowsheet:
    """
    Process flowsheet containing units and streams.
    """
    
    def __init__(self):
        self.units = []
        self.streams = []
    
    def add_unit(self, unit):
        self.units.append(unit)
    
    def add_stream(self, stream):
        self.streams.append(stream)
    
    def simulate(self):
        """
        Simulate the flowsheet.
        
        For now, simple sequential simulation.
        In full HYSYS-like simulator, this would solve the entire system simultaneously.
        """
        # Sort units in topological order (simplified)
        # For now, assume units are added in order
        
        for unit in self.units:
            unit.simulate()
        
        return True

# Example usage
def example_simulation():
    """Simple example of pump and mixer"""
    
    # Create flowsheet
    fs = Flowsheet()
    
    # Create streams
    stream1 = Stream(10.0, 300, 1e5, {'CH4': 0.8, 'C2H6': 0.2})
    stream2 = Stream(5.0, 300, 1e5, {'CH4': 0.9, 'C2H6': 0.1})
    
    fs.add_stream(stream1)
    fs.add_stream(stream2)
    
    # Create units
    pump = Pump("Pump1")
    pump.add_inlet(stream1)
    
    mixer = Mixer("Mixer1")
    mixer.add_inlet(pump.outlets[0] if pump.outlets else stream1)  # After pump
    mixer.add_inlet(stream2)
    
    fs.add_unit(pump)
    fs.add_unit(mixer)
    
    # Simulate
    fs.simulate()
    
    # Print results
    print("Outlet from mixer:")
    outlet = mixer.outlets[0]
    print(f"Flow rate: {outlet.flow_rate} mol/s")
    print(f"Temperature: {outlet.T} K")
    print(f"Pressure: {outlet.P} Pa")
    print(f"Composition: {outlet.composition}")

if __name__ == "__main__":
    example_simulation()