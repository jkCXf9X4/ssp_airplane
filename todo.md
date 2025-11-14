
[x] rework the architecture to fit the F-16 Fighting Falcon, in the file f16_specs.md is summary of the general specifications of the F-16 Fighting Falcon

[x] Extend with new requirements that could fit an aircraft of this size and capability

[x] rework the models to fit the new scope and architecture

[x] build and run simulation to verify that the conversion is correct 

[x] Do a critical overview of the architecture, list the most tangible improvements to better reflect the 16 specification and the requirements. extend this todo list with the possible improvements (2024-05-14)

[x] Add a dedicated StoresManagementSystem part (with nine Hardpoint subparts and munition/pylon metadata) and connect it to MissionComputer stores interfaces, PowerSystem, and CompositeAirframe structures. (2024-05-14)

[x] Introduce a FlyByWireController/StabilityAugmentation subsystem that models the triplex FBW channels required for an unstable F-16 platform and mediates MissionComputer commands to AdaptiveWingSystem actuators. (2024-05-14)

[x] Model an AirDataAndInertialSuite (pitot-static, INS/GPS, rate gyros) that feeds MissionComputer, AutopilotModule, and Performance monitoring ports so autopilot hold modes and dash performance are driven by sensed states. (2024-05-14)

[x] Extend PowerSystem to capture the dual 270 VDC / 115 VAC buses with converter/transformer ports plus an emergency power unit so avionics/autopilot loads remain powered under generator loss. (2024-05-14)

[x] Add a StructuralLoadsAndPerformanceMonitor part that ingests LiftState and ThrustState to validate 9 g and Mach 2 requirements and to gate stores release / autopilot envelopes. (2024-05-14)

---

Not is scope for now:

[] outline a few use case scenarios that connect to the requirements
[] extend simulation test scenarios to fulfill the use cases 

[] create simulation unit tests to verify requirement fulfillment of use-case simulations towards requirements
