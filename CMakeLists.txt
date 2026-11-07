
cmake_minimum_required(VERSION 3.16)

project(SmartAGV_Control_System)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include_directories(include)

add_executable(SmartAGV
    src/main.cpp
    src/AGV.cpp
    src/Motor.cpp
    src/Sensor.cpp
    src/SafetySystem.cpp
    src/Navigation.cpp
)
