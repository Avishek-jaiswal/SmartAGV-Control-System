
#include "AGV.h"
#include <iostream>

AGV::AGV() {
    motor.stop();
}

void AGV::start(int speed) {

    if (safetySystem.canMove(sensor)) {
        motor.setSpeed(speed);

        std::cout << "AGV started successfully."
                  << std::endl;
    }
    else {
        motor.stop();

        std::cout << "Movement blocked! Safety condition triggered."
                  << std::endl;
    }
}

void AGV::stop() {
    motor.stop();

    std::cout << "AGV stopped." << std::endl;
}

void AGV::detectObstacle(bool detected) {
    sensor.setObstacle(detected);

    if (detected) {
        motor.stop();
        std::cout << "Obstacle detected! AGV stopped."
                  << std::endl;
    }
}

void AGV::emergencyStop() {
    safetySystem.activateEmergencyStop();
    motor.stop();

    std::cout << "EMERGENCY STOP ACTIVATED!"
              << std::endl;
}

void AGV::resetEmergencyStop() {
    safetySystem.resetEmergencyStop();

    std::cout << "Emergency stop reset."
              << std::endl;
}

int AGV::getSpeed() const {
    return motor.getSpeed();
}

bool AGV::canMove() const {
    return safetySystem.canMove(sensor);
}
