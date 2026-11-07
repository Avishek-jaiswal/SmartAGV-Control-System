#pragma once

#include <string>

class Navigation {
private:
    int currentX;
    int currentY;
    std::string direction;

    bool obstacleAhead;

public:
    Navigation();

    void moveForward();
    void moveBackward();

    void turnLeft();
    void turnRight();

    void setObstacle(bool detected);

    void displayPosition() const;
};