
#include "SafetySystem.h"

SafetySystem::SafetySystem() {
    emergencyStopActive = false;
}

void SafetySystem::activateEmergencyStop() {
    emergencyStopActive = true;
}

void SafetySystem::resetEmergencyStop() {
    emergencyStopActive = false;
}

bool SafetySystem::isEmergencyStopActive() const {
    return emergencyStopActive;
}

bool SafetySystem::canMove(const Sensor& sensor) const {

    if (emergencyStopActive) {
        return false;
    }

    if (sensor.isObstacleDetected()) {
        return false;
    }

    return true;
}
