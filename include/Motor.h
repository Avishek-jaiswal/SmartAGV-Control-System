#pragma once

class Motor {
private:
    int speed;

public:
    Motor();

    void setSpeed(int newSpeed);
    void stop();
    int getSpeed() const;
};