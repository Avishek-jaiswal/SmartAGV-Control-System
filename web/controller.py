import time
from threading import Lock
from typing import Protocol, TypedDict


HOME = {"x": 0, "y": 0, "name": "AGV Home Position"}
PRODUCT_STATION = {"x": -4, "y": 0, "name": "Product Loading Station"}
PLANT_STATION = {"x": 4, "y": 0, "name": "Plant Production Station"}
ROUTE = [HOME, PRODUCT_STATION, PLANT_STATION]
SIMULATION_SPEED_UNITS_PER_SECOND = 2
PICKUP_SECONDS = 1
DELIVERY_SECONDS = 1


class ControllerError(ValueError):
    pass


class AGVController(Protocol):
    def get_state(self) -> dict[str, object]: ...

    def start_mission(self) -> dict[str, object]: ...

    def pause_mission(self) -> dict[str, object]: ...

    def command(self, action: str) -> dict[str, object]: ...


class AGVState(TypedDict):
    x: int
    y: int
    direction: str
    speed: int
    distance: int
    obstacle: bool
    emergency: bool
    auto_mode: bool
    stage: str
    delivery_status: str
    product_available: bool
    product_loaded: bool
    completed_tasks: int
    message: str


class SimulatedAGVController:
    def __init__(self, clock=time.monotonic):
        self._clock = clock
        self._lock = Lock()
        self._last_tick = clock()
        self._movement_progress = 0.0
        self._phase_elapsed = 0.0
        self._state: AGVState = {
            "x": HOME["x"],
            "y": HOME["y"],
            "direction": "WEST",
            "speed": 0,
            "distance": 0,
            "obstacle": False,
            "emergency": False,
            "auto_mode": False,
            "stage": "IDLE",
            "delivery_status": "READY",
            "product_available": True,
            "product_loaded": False,
            "completed_tasks": 0,
            "message": "System ready",
        }

    def get_state(self) -> dict[str, object]:
        with self._lock:
            self._advance(self._clock())
            return self._snapshot()

    def start_mission(self) -> dict[str, object]:
        with self._lock:
            now = self._clock()
            self._advance(now)

            if self._state["emergency"]:
                raise ControllerError("Reset emergency stop before restarting")
            if self._state["obstacle"]:
                raise ControllerError("Clear the obstacle before starting")
            if self._state["auto_mode"]:
                raise ControllerError("The transport mission is already running")

            if self._state["delivery_status"] == "IN_PROGRESS":
                self._state["auto_mode"] = True
                self._state["speed"] = 40
                self._state["message"] = "Transport mission resumed"
            else:
                if not self._state["product_available"]:
                    raise ControllerError(
                        "No product is available at the Product Loading Station"
                    )

                self._state.update(
                    {
                        "x": HOME["x"],
                        "y": HOME["y"],
                        "direction": "WEST",
                        "speed": 40,
                        "distance": 0,
                        "auto_mode": True,
                        "stage": "TO_PICKUP",
                        "delivery_status": "IN_PROGRESS",
                        "product_loaded": False,
                        "message": "AGV dispatched to Product Loading Station",
                    }
                )
                self._movement_progress = 0.0
                self._phase_elapsed = 0.0

            self._last_tick = now
            return self._snapshot()

    def pause_mission(self) -> dict[str, object]:
        with self._lock:
            self._advance(self._clock())
            self._state["auto_mode"] = False
            self._state["speed"] = 0
            if self._state["delivery_status"] == "IN_PROGRESS":
                self._state["message"] = "Transport mission paused"
            else:
                self._state["message"] = "AGV is idle"
            return self._snapshot()

    def command(self, action: str) -> dict[str, object]:
        with self._lock:
            now = self._clock()
            self._advance(now)

            if action == "emergency":
                self._state["emergency"] = True
                self._state["auto_mode"] = False
                self._state["speed"] = 0
                self._state["message"] = "Emergency stop activated"
            elif action == "reset":
                self._state["emergency"] = False
                self._state["message"] = (
                    "Emergency reset. Inspect the route, then restart the mission."
                )
            elif action == "obstacle_on":
                self._state["obstacle"] = True
                self._state["speed"] = 0
                self._state["message"] = "Obstacle detected. AGV stopped."
            elif action == "obstacle_off":
                self._state["obstacle"] = False
                self._state["message"] = "Obstacle cleared. Mission may resume."
            elif action == "new_product":
                if (
                    self._state["auto_mode"]
                    or self._state["delivery_status"] == "IN_PROGRESS"
                    or self._state["product_loaded"]
                ):
                    raise ControllerError(
                        "Cannot restock while a transport mission is active"
                    )
                self._state["product_available"] = True
                self._state["delivery_status"] = "READY"
                self._state["stage"] = "IDLE"
                self._state["message"] = "Product restocked at the loading station"
            else:
                raise ControllerError("Unknown command")

            self._last_tick = now
            return self._snapshot()

    def _advance(self, now: float) -> None:
        elapsed = max(0.0, now - self._last_tick)
        self._last_tick = now

        if not self._state["auto_mode"] or not self._can_move():
            self._state["speed"] = 0
            return

        stage = self._state["stage"]
        if stage in ("PICKING_UP", "DELIVERING"):
            self._state["speed"] = 0
            self._phase_elapsed += elapsed
            phase_duration = PICKUP_SECONDS if stage == "PICKING_UP" else DELIVERY_SECONDS
            if self._phase_elapsed >= phase_duration:
                self._finish_station_operation(stage)
            return

        self._state["speed"] = 40
        self._movement_progress += (
            elapsed
            * (int(self._state["speed"]) / 100)
            * SIMULATION_SPEED_UNITS_PER_SECOND
        )

        while self._movement_progress >= 1:
            self._movement_progress -= 1
            self._move_one_unit()
            if self._state["stage"] in ("PICKING_UP", "DELIVERING"):
                self._state["speed"] = 0
                self._movement_progress = 0.0
                break

    def _move_one_unit(self) -> None:
        target = PRODUCT_STATION if self._state["stage"] == "TO_PICKUP" else PLANT_STATION
        x = int(self._state["x"])
        y = int(self._state["y"])

        if x != target["x"]:
            direction = "EAST" if x < target["x"] else "WEST"
            x += 1 if direction == "EAST" else -1
        elif y != target["y"]:
            direction = "NORTH" if y < target["y"] else "SOUTH"
            y += 1 if direction == "NORTH" else -1
        else:
            self._arrive_at_station()
            return

        self._state.update(
            {
                "x": x,
                "y": y,
                "direction": direction,
                "distance": int(self._state["distance"]) + 1,
            }
        )

        if x == target["x"] and y == target["y"]:
            self._arrive_at_station()

    def _arrive_at_station(self) -> None:
        if self._state["stage"] == "TO_PICKUP":
            self._state["stage"] = "PICKING_UP"
            self._state["message"] = "At loading station. Product sensor checking load."
        else:
            self._state["stage"] = "DELIVERING"
            self._state["message"] = "At production station. Unloading product."
        self._phase_elapsed = 0.0

    def _finish_station_operation(self, stage: str) -> None:
        self._phase_elapsed = 0.0
        if stage == "PICKING_UP":
            if not self._state["product_available"]:
                self._state.update(
                    {
                        "stage": "IDLE",
                        "delivery_status": "FAILED",
                        "auto_mode": False,
                        "speed": 0,
                        "message": "Product sensor found no product at the loading station",
                    }
                )
                return

            self._state.update(
                {
                    "product_available": False,
                    "product_loaded": True,
                    "stage": "TO_PLANT",
                    "message": "Product collected. Travelling to Plant Production Station.",
                }
            )
        else:
            self._state.update(
                {
                    "product_loaded": False,
                    "stage": "IDLE",
                    "delivery_status": "COMPLETED",
                    "auto_mode": False,
                    "speed": 0,
                    "completed_tasks": int(self._state["completed_tasks"]) + 1,
                    "message": "Product delivered successfully. Mission complete.",
                }
            )

    def _can_move(self) -> bool:
        return not self._state["obstacle"] and not self._state["emergency"]

    def _snapshot(self) -> dict[str, object]:
        state = dict(self._state)
        state.update(
            {
                "status": self._status(),
                "safe": self._can_move(),
                "product_sensor": bool(
                    self._state["product_available"]
                    and self._state["x"] == PRODUCT_STATION["x"]
                    and self._state["y"] == PRODUCT_STATION["y"]
                ),
                "waypoints": [dict(point) for point in ROUTE],
                "current_waypoint": self._current_waypoint(),
            }
        )
        return state

    def _status(self) -> str:
        if self._state["emergency"]:
            return "EMERGENCY STOP"
        if self._state["obstacle"]:
            return "OBSTACLE DETECTED"
        if self._state["delivery_status"] == "COMPLETED":
            return "DELIVERY COMPLETED"
        if self._state["auto_mode"]:
            return "AUTOMATIC RUNNING"
        if self._state["delivery_status"] == "IN_PROGRESS":
            return "MISSION PAUSED"
        return "READY"

    def _current_waypoint(self) -> str:
        stage = self._state["stage"]
        if stage in ("TO_PICKUP", "PICKING_UP"):
            return PRODUCT_STATION["name"]
        if stage in ("TO_PLANT", "DELIVERING"):
            return PLANT_STATION["name"]
        if self._state["delivery_status"] == "COMPLETED":
            return PLANT_STATION["name"]
        return HOME["name"]
