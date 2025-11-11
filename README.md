# ssp_airplane

This repository tracks an SSP for a loyal-wingman style autonomous drone modeled after MQ-28 / Hellsing CA-1 concepts.

# System requirements:
- MQ-28 class geometry (≈11.7 m length, 7.3 m span) to operate as a loyal wingman
- Conventional turbofan propulsion with generator support for avionics
- Accepts pilot-style (game/simulator) control inputs while still supporting an onboard autopilot
- Optimization focuses on range, loiter/escort scenarios, and payload configuration

# Architecture
The architecture is captured as SysML v2 textual notation in `architecture/aircraft_architecture.sysml`.  
This file is parsed with [PySysML2](https://github.com/DAF-Digital-Transformation-Office/PySysML2) and serves as the single source of truth for the drone's composition (airframe, wings, turbofan propulsion, mission computer, control interface, power system, autopilot), connections, and scenario-planning parameters.

## Components

The system is defined on a high level of abstraction with low fidelity models
It contains models for:
 - composite airframe
 - adaptive wing system
 - turbofan propulsion module
 - mission computer with manual + autonomy inputs
 - optional autopilot module
 - power distribution system
 - control interface for HOTAS / gamepad style inputs

# Build

all sub-systems are to be exported into into Functional mockup units, FMUs. Packaged into a SSP for executing the simulation in the optimization loop.

## Models

All subsystem FMUs are generated from the `models/WingmanDrone` Modelica package using the OpenModelica compiler (`omc`).

## The SSD

The ssd is build by a script that parses the architecture and creates a system structure definition (SSD)

## SSP 

FMUs and SSD are packaged into a zip file, renamed *.ssp


# Simulation 

Utilize OMSimulator as simulation engine, via python


# File disposition

architecture/ - the system architecture 
models/ - all models are located here
scripts/ - all scripts used to build this setup is located here

# Development

The tracking of tasks for this project is defined in the file todo.md
