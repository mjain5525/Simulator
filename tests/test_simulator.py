"""
Tests for the simulator package.
"""

import pytest
from src.simulator.units import Stream, Pump, Mixer
from src.simulator.thermodynamics import PengRobinsonEOS, METHANE

def test_stream_creation():
    """Test stream creation and validation"""
    composition = {'CH4': 0.8, 'C2H6': 0.2}
    stream = Stream(10.0, 300, 1e5, composition)
    
    assert stream.flow_rate == 10.0
    assert stream.T == 300
    assert stream.P == 1e5
    assert stream.composition == composition

def test_stream_invalid_composition():
    """Test that invalid composition raises error"""
    composition = {'CH4': 0.8, 'C2H6': 0.3}  # Sums to 1.1
    
    with pytest.raises(ValueError):
        Stream(10.0, 300, 1e5, composition)

def test_pump_simulation():
    """Test pump unit operation"""
    inlet = Stream(10.0, 300, 1e5, {'CH4': 1.0})
    pump = Pump("TestPump")
    pump.add_inlet(inlet)
    
    outlets = pump.simulate()
    
    assert len(outlets) == 1
    outlet = outlets[0]
    assert outlet.flow_rate == inlet.flow_rate
    assert outlet.T == inlet.T
    assert outlet.P == inlet.P * 2  # Simple doubling
    assert outlet.composition == inlet.composition

def test_mixer_simulation():
    """Test mixer unit operation"""
    inlet1 = Stream(10.0, 300, 1e5, {'CH4': 0.8, 'C2H6': 0.2})
    inlet2 = Stream(5.0, 300, 1e5, {'CH4': 0.9, 'C2H6': 0.1})
    
    mixer = Mixer("TestMixer")
    mixer.add_inlet(inlet1)
    mixer.add_inlet(inlet2)
    
    outlets = mixer.simulate()
    
    assert len(outlets) == 1
    outlet = outlets[0]
    assert outlet.flow_rate == 15.0
    assert outlet.T == 300
    assert outlet.P == 1e5
    expected_ch4 = (10*0.8 + 5*0.9) / 15
    expected_c2h6 = (10*0.2 + 5*0.1) / 15
    assert abs(outlet.composition['CH4'] - expected_ch4) < 1e-6
    assert abs(outlet.composition['C2H6'] - expected_c2h6) < 1e-6

def test_peng_robinson():
    """Test Peng-Robinson EOS"""
    eos = PengRobinsonEOS(**METHANE)
    
    # Test at critical point
    Z_crit = eos.compressibility_factor(eos.Tc, eos.Pc)
    assert abs(Z_crit - 0.32) < 0.01  # Approximate value for PR EOS