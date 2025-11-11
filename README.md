# ssp_airplane

This is a reference SSP of an aircraft

# System requirements:
- it should be equivalent size and shape of a Boing 737
- it should be using nuclear power for propulsion
- it should be able to fly london to Beijing without refueling
- it should be used to optimize the wing area, motor size and carrying capacity

# Architecture
The architecture is represented in sysml v2
This is the single source of truth regarding system composition and connection

## Components

The system is defined on a high level of abstraction with low fidelity models
It contains models for:
 - fuselage
 - reactor
 - wings
 - motors
 - controlling sw 
 - autopilot
 - electric system

# Build

all sub-systems are to be exported into into Functional mockup units, FMUs. Packaged into a SSP for executing the simulation in the optimization loop.

## Models

All models are build in modelica nd compiled using OpenModelica compiler, omc

These are located under the folder /models

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