
#include "Navigation.h"
#include <iostream>

Navigation::Navigation() {
    currentX = 0;
    currentY = 0;
    direction = "NORTH";
    obstacleAhead = false;
}

void Navigation::setObstacle(bool detected) {
    obstacleAhead = detected;

    if (detected) {
        std::cout << "Obstacle detected ahead!" << std::endl;
    } else {
        std::cout << "Path is clear." << std::endl;
    }
}

void Navigation::moveForward() {
    if (obstacleAhead) {
        std::cout << "Movement blocked! Obstacle ahead."
                  << std::endl;
        return;
    }

    if (direction == "NORTH") currentY++;
    else if (direction == "SOUTH") currentY--;
    else if (direction == "EAST") currentX++;
    else if (direction == "WEST") currentX--;

    std::cout << "Moving forward." << std::endl;
}

void Navigation::moveBackward() {
    if (direction == "NORTH") currentY--;
    else if (direction == "SOUTH") currentY++;
    else if (direction == "EAST") currentX--;
    else if (direction == "WEST") currentX++;

    std::cout << "Moving backward." << std::endl;
}

void Navigation::turnLeft() {
    if (direction == "NORTH") direction = "WEST";
    else if (direction == "WEST") direction = "SOUTH";
    else if (direction == "SOUTH") direction = "EAST";
    else if (direction == "EAST") direction = "NORTH";

    std::cout << "Turned left." << std::endl;
}

void Navigation::turnRight() {
    if (direction == "NORTH") direction = "EAST";
    else if (direction == "EAST") direction = "SOUTH";
    else if (direction == "SOUTH") direction = "WEST";
    else if (direction == "WEST") direction = "NORTH";

    std::cout << "Turned right." << std::endl;
}

void Navigation::displayPosition() const {
    std::cout << "Current Position: ("
              << currentX << ", "
              << currentY << ")" << std::endl;

    std::cout << "Direction: "
              << direction << std::endl;
}
