"""
Thermodynamic package for hydrocarbon modeling.

This module provides equations of state and thermodynamic calculations
suitable for process simulation of hydrocarbon systems.
"""

import numpy as np
from scipy.optimize import fsolve

class PengRobinsonEOS:
    """
    Peng-Robinson Equation of State for hydrocarbons.
    
    P = RT/(V-b) - a/(V(V+b) + b(V-b))
    """
    
    def __init__(self, Tc, Pc, omega):
        """
        Initialize with critical properties.
        
        Parameters:
        Tc: Critical temperature (K)
        Pc: Critical pressure (Pa)
        omega: Acentric factor
        """
        self.Tc = Tc
        self.Pc = Pc
        self.omega = omega
        
        # Calculate EOS parameters
        self.a = 0.45724 * (self.R * self.Tc)**2 / self.Pc
        self.b = 0.07780 * self.R * self.Tc / self.Pc
        
        # Temperature-dependent alpha
        self.kappa = 0.37464 + 1.54226*self.omega - 0.26992*self.omega**2
    
    @property
    def R(self):
        return 8.314  # J/mol·K
    
    def alpha(self, T):
        """Temperature-dependent alpha function"""
        Tr = T / self.Tc
        return (1 + self.kappa*(1 - np.sqrt(Tr)))**2
    
    def pressure(self, T, V, n=1.0):
        """Calculate pressure from T and V"""
        a_alpha = self.a * self.alpha(T)
        b = self.b
        
        term1 = n * self.R * T / (V - n*b)
        term2 = a_alpha * n**2 / (V*(V + n*b) + n*b*(V - n*b))
        
        return term1 - term2
    
    def compressibility_factor(self, T, P):
        """Calculate Z from T and P using EOS"""
        from scipy.optimize import fsolve
        
        def f(Z):
            V = Z * self.R * T / P
            b = self.b
            a_alpha = self.a * self.alpha(T)
            term1 = self.R * T / (V - b)
            term2 = a_alpha / (V**2 + 2 * b * V - b**2)
            return P - term1 + term2
        
        Z_guess = 0.5
        Z = fsolve(f, Z_guess)[0]
        return Z

# Example component data for methane
METHANE = {
    'Tc': 190.56,  # K
    'Pc': 4.599e6,  # Pa
    'omega': 0.011
}

# More components can be added here