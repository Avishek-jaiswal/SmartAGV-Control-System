
#pragma once 

#include "Motor.h"
#include "Sensor.h"
#include "SafetySystem.h"

class AGV {
private:
    Motor motor;
    Sensor sensor;
    SafetySystem safetySystem;

public:
    AGV();

    void start(int speed);
    void stop();

    void detectObstacle(bool detected);

    void emergencyStop();
    void resetEmergencyStop();

    int getSpeed() const;
    bool canMove() const;
};
