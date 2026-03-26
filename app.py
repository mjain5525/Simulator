"""
Streamlit GUI for Process Simulator
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from src.simulator.units import Stream, Pump, Mixer
from src.simulator.thermodynamics import PengRobinsonEOS, METHANE

st.title("Process Simulator GUI")

st.sidebar.header("Simulation Setup")

# Component selection
st.sidebar.subheader("Components")
components = st.sidebar.multiselect("Select components", ["CH4", "C2H6", "C3H8"], default=["CH4", "C2H6"])

# Unit operations
st.sidebar.subheader("Unit Operations")
units = st.sidebar.multiselect("Select units", ["Pump", "Mixer"], default=["Pump", "Mixer"])

# Stream inputs
st.header("Feed Streams")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Stream 1")
    flow1 = st.number_input("Flow rate (mol/s)", value=10.0, key="flow1")
    temp1 = st.number_input("Temperature (K)", value=300.0, key="temp1")
    press1 = st.number_input("Pressure (Pa)", value=1e5, key="press1")

    comp1 = {}
    for comp in components:
        comp1[comp] = st.slider(f"{comp} fraction", 0.0, 1.0, 0.5 if comp == "CH4" else 0.3, key=f"comp1_{comp}")

with col2:
    st.subheader("Stream 2")
    flow2 = st.number_input("Flow rate (mol/s)", value=5.0, key="flow2")
    temp2 = st.number_input("Temperature (K)", value=300.0, key="temp2")
    press2 = st.number_input("Pressure (Pa)", value=1e5, key="press2")

    comp2 = {}
    for comp in components:
        comp2[comp] = st.slider(f"{comp} fraction", 0.0, 1.0, 0.9 if comp == "CH4" else 0.1, key=f"comp2_{comp}")

# Normalize compositions
total1 = sum(comp1.values())
comp1 = {k: v/total1 for k, v in comp1.items()}

total2 = sum(comp2.values())
comp2 = {k: v/total2 for k, v in comp2.items()}

# Simulation button
if st.button("Run Simulation"):
    try:
        # Create streams
        stream1 = Stream(flow1, temp1, press1, comp1)
        stream2 = Stream(flow2, temp2, press2, comp2)

        # Create units
        results = []

        if "Pump" in units:
            pump = Pump("Pump")
            pump.add_inlet(stream1)
            pump.simulate()
            pumped_stream = pump.outlets[0]
            results.append({
                "Unit": "Pump",
                "Flow": pumped_stream.flow_rate,
                "T": pumped_stream.T,
                "P": pumped_stream.P,
                "Composition": pumped_stream.composition
            })

        if "Mixer" in units:
            mixer = Mixer("Mixer")
            if "Pump" in units:
                mixer.add_inlet(pumped_stream)
            else:
                mixer.add_inlet(stream1)
            mixer.add_inlet(stream2)
            mixer.simulate()
            mixed_stream = mixer.outlets[0]
            results.append({
                "Unit": "Mixer",
                "Flow": mixed_stream.flow_rate,
                "T": mixed_stream.T,
                "P": mixed_stream.P,
                "Composition": mixed_stream.composition
            })

        # Display results
        st.header("Simulation Results")

        for result in results:
            st.subheader(f"{result['Unit']} Output")
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Flow Rate", f"{result['Flow']:.2f} mol/s")
                st.metric("Temperature", f"{result['T']:.1f} K")

            with col2:
                st.metric("Pressure", f"{result['P']/1000:.1f} kPa")

            with col3:
                st.write("Composition:")
                for comp, frac in result['Composition'].items():
                    st.write(f"{comp}: {frac:.3f}")

        # Simple flowsheet visualization
        st.header("Flowsheet Diagram")

        fig, ax = plt.subplots(figsize=(8, 4))

        # Draw units
        y_pos = 2
        x_pos = 1

        if "Pump" in units:
            ax.add_patch(plt.Rectangle((x_pos, y_pos-0.5), 1, 1, fill=True, color='blue', alpha=0.5))
            ax.text(x_pos+0.5, y_pos, 'Pump', ha='center', va='center')
            x_pos += 2

        if "Mixer" in units:
            ax.add_patch(plt.Rectangle((x_pos, y_pos-0.5), 1, 1, fill=True, color='green', alpha=0.5))
            ax.text(x_pos+0.5, y_pos, 'Mixer', ha='center', va='center')

        # Draw streams
        ax.arrow(0, 2, 1, 0, head_width=0.1, head_length=0.1, fc='black', ec='black')
        ax.arrow(0, 1.5, 1, 0, head_width=0.1, head_length=0.1, fc='black', ec='black')

        if len(units) > 1:
            ax.arrow(3, 2, 1, 0, head_width=0.1, head_length=0.1, fc='black', ec='black')

        ax.set_xlim(0, 6)
        ax.set_ylim(0.5, 3.5)
        ax.axis('off')

        st.pyplot(fig)

    except Exception as e:
        st.error(f"Simulation error: {str(e)}")

# Thermodynamics calculator
st.header("Thermodynamics Calculator")

col1, col2 = st.columns(2)

with col1:
    calc_temp = st.number_input("Temperature (K)", value=300.0, key="calc_temp")
    calc_press = st.number_input("Pressure (Pa)", value=1e5, key="calc_press")

with col2:
    if st.button("Calculate Z"):
        eos = PengRobinsonEOS(**METHANE)
        Z = eos.compressibility_factor(calc_temp, calc_press)
        st.metric("Compressibility Factor Z", f"{Z:.4f}")

st.markdown("---")
st.markdown("Built with Streamlit for easy process modeling")