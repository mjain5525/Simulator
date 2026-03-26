"""
Process units for simulation.

This module contains classes for various process units like pumps, valves,
heat exchangers, etc.
"""

import numpy as np

class Stream:
    """
    Material stream with thermodynamic properties.
    """
    
    def __init__(self, flow_rate, temperature, pressure, composition):
        """
        Parameters:
        flow_rate: molar flow rate (mol/s)
        temperature: T (K)
        pressure: P (Pa)
        composition: dict of component fractions {component: fraction}
        """
        self.flow_rate = flow_rate
        self.T = temperature
        self.P = pressure
        self.composition = composition
        
        # Validate composition
        if abs(sum(composition.values()) - 1.0) > 1e-6:
            raise ValueError("Composition fractions must sum to 1")

class UnitOperation:
    """
    Base class for unit operations.
    """
    
    def __init__(self, name):
        self.name = name
        self.inlets = []
        self.outlets = []
    
    def add_inlet(self, stream):
        self.inlets.append(stream)
    
    def add_outlet(self, stream):
        self.outlets.append(stream)

class Pump(UnitOperation):
    """
    Centrifugal pump unit.
    """
    
    def __init__(self, name, efficiency=0.75):
        super().__init__(name)
        self.efficiency = efficiency
    
    def simulate(self):
        """Simple pump simulation - increases pressure"""
        if not self.inlets:
            raise ValueError("No inlet stream")
        
        inlet = self.inlets[0]
        
        # Assume outlet pressure is higher
        # In real simulation, this would be calculated based on head, etc.
        outlet_P = inlet.P * 2  # Simple doubling for demo
        
        # Calculate work required (simplified)
        # work = (outlet_P - inlet.P) * inlet.flow_rate / (inlet.density * efficiency)
        # For now, just copy stream with new pressure
        
        outlet_composition = inlet.composition.copy()
        outlet = Stream(inlet.flow_rate, inlet.T, outlet_P, outlet_composition)
        
        self.outlets = [outlet]
        return self.outlets

class Mixer(UnitOperation):
    """
    Mixer unit for combining streams.
    """
    
    def simulate(self):
        """Mix multiple inlet streams"""
        if len(self.inlets) < 2:
            raise ValueError("Mixer needs at least 2 inlet streams")
        
        # Calculate total flow
        total_flow = sum(s.flow_rate for s in self.inlets)
        
        # Mix compositions (assuming same T and P for simplicity)
        mixed_composition = {}
        components = set()
        for s in self.inlets:
            components.update(s.composition.keys())
        
        for comp in components:
            mixed_composition[comp] = sum(s.flow_rate * s.composition.get(comp, 0) for s in self.inlets) / total_flow
        
        # Use inlet conditions (simplified)
        T = self.inlets[0].T
        P = self.inlets[0].P
        
        outlet = Stream(total_flow, T, P, mixed_composition)
        self.outlets = [outlet]
        return self.outlets