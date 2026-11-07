
#pragma once

#include "Sensor.h"

class SafetySystem {
private:
    bool emergencyStopActive;

public:
    SafetySystem();

    void activateEmergencyStop();
    void resetEmergencyStop();

    bool isEmergencyStopActive() const;

    bool canMove(const Sensor& sensor) const;
};

