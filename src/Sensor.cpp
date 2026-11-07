
#include "Sensor.h"

Sensor::Sensor() {
    obstacleDetected = false;
}

void Sensor::setObstacle(bool detected) {
    obstacleDetected = detected;
}

bool Sensor::isObstacleDetected() const {
    return obstacleDetected;
}
