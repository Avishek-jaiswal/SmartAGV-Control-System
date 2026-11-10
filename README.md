# Smart AGV Control System

This project includes a C++17 AGV component simulation and a Flask dashboard
for an automated, browser-based pickup and delivery simulation.

## Run the dashboard

From the repository root:

```bash
.venv/bin/python -m web.app
```

Open `http://127.0.0.1:5000`. Select **Start / Resume Mission** to simulate the
AGV travelling from Home `(0, 0)` to the Product Loading Station `(-4, 0)`,
loading a simulated product, then travelling to the Plant Production Station
`(4, 0)` to deliver it. Position, direction, speed, sensor state, mission
phase, and delivery count update on the dashboard.

The safety controls simulate an obstacle and an emergency stop. An obstacle
pauses movement until cleared; an emergency requires a manual reset and a
separate mission restart. Use **Restock Simulated Product** to run another
delivery after completion.

## Run the C++ simulation

```bash
cmake -S . -B build
cmake --build build
./build/SmartAGV
```

## Run the simulation tests

```bash
.venv/bin/python -m unittest discover -s tests
```

The Flask dashboard is simulation-only. `web/controller.py` defines the
controller interface and simulated implementation; no physical motors,
sensors, PLCs, or emergency-stop hardware are connected.