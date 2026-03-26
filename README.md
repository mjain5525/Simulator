# Simulator

A process simulation software inspired by HYSYS, designed for modeling chemical processes with a focus on hydrocarbon systems.

## Features

- **Thermodynamic Package**: Peng-Robinson equation of state for accurate phase behavior calculations
- **Process Units**: Basic unit operations like pumps, mixers, and more to be added
- **Flowsheet Simulation**: Sequential and simultaneous equation solving capabilities
- **Hydrocarbon Modeling**: Specialized for oil and gas processing applications

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -e .
   ```

## Usage

### Command Line
Run the example simulation:
```bash
python main.py
```

### Graphical Interface
Launch the web-based GUI:
```bash
streamlit run app.py
```

Or run the desktop GUI (requires display):
```bash
python gui.py
```

Both GUIs allow you to:
- Set feed stream properties
- Run simulations with pumps and mixers
- View results and flowsheet diagrams
- Calculate thermodynamic properties (web GUI)

## Development

- Source code in `src/simulator/`
- Tests in `tests/`
- Documentation in `docs/`

## Components

- `thermodynamics.py`: Equation of state implementations
- `units.py`: Process unit operations
- `simulation.py`: Flowsheet simulation engine

## Future Enhancements

- GUI interface
- More unit operations (distillation, reactors, heat exchangers)
- Advanced thermodynamics (multicomponent mixtures, phase equilibria)
- Optimization capabilities
- Database of component properties
