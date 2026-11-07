#pragma once

class Sensor {
private:
    bool obstacleDetected;

public:
    Sensor();

    void setObstacle(bool detected);
    bool isObstacleDetected() const;
};