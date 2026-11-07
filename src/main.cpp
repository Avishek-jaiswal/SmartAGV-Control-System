
#include <iostream>
#include "AGV.h"
#include "Navigation.h"

using namespace std;

int main() {

    // Create AGV object
    AGV agv;

    cout << "=================================" << endl;
    cout << "     SMART AGV CONTROL SYSTEM    " << endl;
    cout << "=================================" << endl;


    // Scenario 1: Normal Movement
    cout << "\nScenario 1: Normal Movement" << endl;

    agv.start(60);

    cout << "Current Speed: "
         << agv.getSpeed() << "%" << endl;


    // Scenario 2: Obstacle Detection
    cout << "\nScenario 2: Obstacle Detection" << endl;

    agv.detectObstacle(true);

    cout << "Current Speed: "
         << agv.getSpeed() << "%" << endl;


    // Scenario 3: Path Cleared
    cout << "\nScenario 3: Path Cleared" << endl;

    agv.detectObstacle(false);

    agv.start(40);

    cout << "Current Speed: "
         << agv.getSpeed() << "%" << endl;


    // Scenario 4: Emergency Stop
    cout << "\nScenario 4: Emergency Stop" << endl;

    agv.emergencyStop();

    cout << "Current Speed: "
         << agv.getSpeed() << "%" << endl;


    // Scenario 5: Emergency Reset
    cout << "\nScenario 5: Emergency Reset" << endl;

    agv.resetEmergencyStop();

    agv.start(30);

    cout << "Current Speed: "
         << agv.getSpeed() << "%" << endl;

    agv.stop();


    // Scenario 6: Obstacle-Aware Navigation
    cout << "\nScenario 6: Obstacle-Aware Navigation" << endl;

    Navigation navigation;

    navigation.displayPosition();


    // Test 1: Normal Movement
    cout << "\nTest 1: Normal Movement" << endl;

    navigation.moveForward();

    navigation.displayPosition();


    // Test 2: Obstacle Detection
    cout << "\nTest 2: Obstacle Detected" << endl;

    navigation.setObstacle(true);

    navigation.moveForward();

    navigation.displayPosition();


    // Test 3: Obstacle Removed
    cout << "\nTest 3: Obstacle Removed" << endl;

    navigation.setObstacle(false);

    navigation.moveForward();

    navigation.displayPosition();


    // Finish Simulation
    cout << "\nSimulation Completed!" << endl;

    return 0;
}
