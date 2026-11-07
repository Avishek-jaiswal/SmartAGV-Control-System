#include "Motor.h"

Motor::Motor() {
    speed = 0;
}

void Motor::setSpeed(int newSpeed) {
    if (newSpeed < 0) {
        newSpeed = 0;
    }

    if (newSpeed > 100) {
        newSpeed = 100;
    }

    speed = newSpeed;
}

void Motor::stop() {
    speed = 0;
}

int Motor::getSpeed() const {
    return speed;
}