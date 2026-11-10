import unittest

from web.app import create_app
from web.controller import ControllerError, SimulatedAGVController


class FakeClock:
    def __init__(self):
        self.now = 0.0

    def __call__(self):
        return self.now

    def advance(self, seconds):
        self.now += seconds


class SimulatedAGVControllerTests(unittest.TestCase):
    def setUp(self):
        self.clock = FakeClock()
        self.controller = SimulatedAGVController(clock=self.clock)

    def advance_until(self, predicate, limit=100):
        for _ in range(limit):
            self.clock.advance(0.5)
            state = self.controller.get_state()
            if predicate(state):
                return state
        self.fail("AGV did not reach the expected mission state")

    def test_completes_pickup_delivery_and_counts_load(self):
        state = self.controller.start_mission()
        self.assertEqual((state["x"], state["y"]), (0, 0))
        self.assertEqual(state["stage"], "TO_PICKUP")

        state = self.advance_until(lambda current: current["stage"] == "PICKING_UP")
        self.assertEqual((state["x"], state["y"]), (-4, 0))
        self.assertTrue(state["product_sensor"])

        state = self.advance_until(lambda current: current["stage"] == "TO_PLANT")
        self.assertTrue(state["product_loaded"])
        self.assertFalse(state["product_available"])

        state = self.advance_until(
            lambda current: current["delivery_status"] == "COMPLETED"
        )
        self.assertEqual((state["x"], state["y"]), (4, 0))
        self.assertFalse(state["product_loaded"])
        self.assertEqual(state["completed_tasks"], 1)
        self.assertEqual(state["stage"], "IDLE")
        self.assertEqual(state["current_waypoint"], "Plant Production Station")

    def test_obstacle_stops_movement_until_cleared(self):
        self.controller.start_mission()
        self.clock.advance(1.5)
        moving = self.controller.get_state()
        self.assertLess(moving["x"], 0)

        stopped = self.controller.command("obstacle_on")
        position = (stopped["x"], stopped["y"])
        self.assertEqual(stopped["speed"], 0)
        self.assertTrue(stopped["auto_mode"])

        self.clock.advance(5)
        stopped = self.controller.get_state()
        self.assertEqual((stopped["x"], stopped["y"]), position)

        self.controller.command("obstacle_off")
        self.clock.advance(1.5)
        resumed = self.controller.get_state()
        self.assertLess(resumed["x"], position[0])

    def test_emergency_requires_reset_and_manual_resume(self):
        self.controller.start_mission()
        self.clock.advance(1.5)
        before_emergency = self.controller.get_state()

        stopped = self.controller.command("emergency")
        self.assertEqual(stopped["speed"], 0)
        self.assertFalse(stopped["auto_mode"])
        self.assertTrue(stopped["emergency"])

        with self.assertRaises(ControllerError):
            self.controller.start_mission()

        self.controller.command("reset")
        resumed = self.controller.start_mission()
        self.assertTrue(resumed["auto_mode"])
        self.assertEqual(
            (resumed["x"], resumed["y"]),
            (before_emergency["x"], before_emergency["y"]),
        )

    def test_flask_api_starts_mission_and_rejects_emergency_start(self):
        app = create_app(self.controller)
        app.config["TESTING"] = True
        client = app.test_client()

        started = client.post("/api/mission/start")
        self.assertEqual(started.status_code, 200)
        self.assertEqual(started.get_json()["stage"], "TO_PICKUP")

        emergency = client.post("/api/command", json={"action": "emergency"})
        self.assertEqual(emergency.status_code, 200)

        rejected = client.post("/api/mission/start")
        self.assertEqual(rejected.status_code, 400)
        self.assertIn("Reset emergency stop", rejected.get_json()["error"])

        invalid = client.post("/api/command", json={"action": "unknown"})
        self.assertEqual(invalid.status_code, 400)


if __name__ == "__main__":
    unittest.main()
