
# Campus Micro-Economy Simulator  
*A modular agent-based simulation of university life, policies, and interactions.*

This project is a Python–Streamlit simulation of a miniature **university economy**, where students, teachers, clubs, and admins act as autonomous agents responding to campus policies and environmental changes. The platform is designed for:

- studying emergent behavior,
- experimenting with institutional policies,
- simulating stress/effort/reputation dynamics,
- running “what-if” evaluations of academic environments.

The app runs fully in the browser through Streamlit, with a clean, interactive UI and modular backend.

---

## Features

### Agent-Based Simulation  
The world is populated by four actor types:

- **Students**
- **Teachers**
- **Clubs**
- **Admins**

Each actor maintains internal state variables (stress, workload, satisfaction, etc.) and performs actions each timestep. Agents react to global environment variables and policy settings.

### Dynamic Environment  
The simulation tracks campus-level factors such as:

- Institutional reputation  
- Ambient stress  
- Policy satisfaction  
- Class load  
- Campus energy  

These change every timestep based on aggregated agent states.

### Policy Controls  
Policies can be adjusted in the sidebar during runtime:

- Class starting time  
- Break frequency  
- Assessment load  
- More as you extend the system

Policy changes immediately influence how agents behave.

### Interactive Simulation Controls  

- **Run 1 step**  
- **Run 10 steps**  
- **Reset world**  
- **Save & load snapshots**

All updates propagate through the UI in real time.

### Live Dashboard  
The Overview panel shows:

- Key campus metrics  
- Time-series plots for each actor group  
- Mini summary bar for timestep & actor counts  

Graphs update dynamically as the simulation progresses.

### Actor Inspector  
A dedicated inspector allows you to select any individual actor and view:

- Full internal state (`actor.__dict__`)
- Their most recent action

Useful for debugging and exploring detailed behavior.

### Trend Analytics  
The Trends tab provides quick insights such as:

- Most common actions  
- Most changed variables  
- Actor-specific behavior summaries  

---

## Project Structure

```
micro-economy-simulator/
│
├── app.py                    # Main Streamlit app entrypoint
├── world.py                  # Core simulation environment & global state
├── actors/                   # All actor classes (Students, Teachers, Clubs, Admins)
│   ├── student.py
│   ├── professor.py
│   ├── club.py
│   └── admin.py
│
├── components/               # Modular frontend UI panels
│   ├── sidebar_controls.py
│   ├── actor_inspector.py
│   ├── simulation_controls.py
│   ├── state_dashboard.py
│   └── trends_sidebar.py
│
├── data/                     # Saved simulation states (via Save/Load)
└── README.md
```

Each UI file is independent and talks to the backend only through well-defined methods (`world.step()`, `world.save_data()`, etc.).

---

##  Running the App

### 1. Install dependencies  
```
pip install -r requirements.txt
```

### 2. Launch Streamlit  
```
streamlit run app.py
```

### 3. Visit in browser  
Streamlit will open automatically; if not, visit:

```
http://localhost:8501
```

---

## Saving & Loading Simulation State

You can save the entire simulation (world + actors + history) using the **Save Data** button in the Controls panel.

Saved files appear in:

```
/data/
```

You can reload any saved run using the **Load Data** tool.

---

## Extending the Project

This project is designed to be modular and extendable. You can easily:

- Add new actor types  
- Add new state variables  
- Add new policies in the sidebar  
- Implement new actions  
- Add new plots in the dashboard  

The UI automatically adapts to new history variables as long as they are logged by the backend.

---

## Future Goals

The goal for this project is to expand it into something useful for actual decision 
making. This could be used by universities all around the world as a testbed for
their policy making ideas.

- include RL in the actor decision making
- expand and scale the project to include diverse variables
- use real life data to make connections

---

## Development Philosophy

The project follows three principles:

1. **Backend authoritative**  
   All logic lives in the `World` and actor classes. The UI never fakes or invents state.

2. **Frontend modularity**  
   Each section of the UI is a separate file. Swapping or restyling a panel never touches backend logic.

3. **Data transparency**  
   Simulation history is logged at every step and fully inspectable.



## License

MIT License.  
Feel free to use, modify, and extend.
