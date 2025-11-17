
[x] Enable handling scenario data to the simulation
 - [x] Review how the scenario data is structured, evaluate plausibility (scenario validation added in simulate_scenario.py)
 - [x] The scenario data should be a string parameter to enable utilizing different parameter sets as basis for switching scenario, preferably a comma separated string, there is a modelica function "stringToRealVector" to help parse the string into usable values (waypoint string writer + AutopilotModule.scenarioData driven by stringToRealVector)
 - [x] Track the mission status under the AutopilotModule (new MissionStatus connector and missionStatus output)
 - [x] The AutopilotModule should interface with the MissionComputer using the same PilotCommand used by the manual input to enable seamless switching. (autopilotCmd to MissionComputer.autopilotInput)
 - [x] Implement a simple control loop to steer the aircraft towards the next location point, when close enough switch to the next point. (heading/altitude loop in AutopilotModule)
 - [x] after the simulation, enable plotting the aircraft position during flight to verify that the aircraft has passed all the points (plotting flag in simulate_scenario.py outputs path PNG)
 - [x] add metric that you can understand to the simulation to verify that the aircraft is doing what it is supposed to do (waypoint miss/hit metrics in simulation summaries)
 - [x] add this aspect to the verification flight to enable verifying that the aircraft is following the waypoints (summaries and CLI JSON include waypoint metrics; plotting available via `--plot`)
 - [x] iterate until the aircraft is flying as it should, if you need additional information from within the simulation to evaluate or debug usage, add these as debug ports and create a InputOutput sub-system that acts as a sink for simulation input/output (MissionStatus wiring + InputOutput sink added; scenario strings exported for autopilot)
