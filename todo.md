
[x] Review the models and how they map towards the architecture, create todo items for differentiating items
[x] Update CompositeAirframe.mo to expose the `StructuralInterface storesMounts` port defined in the SysML architecture.
[x] Extend MissionComputer.mo to include `airDataIn`, `storesStatus`, `performanceStatus`, `backupPower`, and the `storesCommand` output.
[x] Extend AutopilotModule.mo to support the `airDataIn`, `performanceStatus`, and `backupPower` ports described in SysML.
[x] Expand PowerSystem.mo to provide the `dcBus270`, `acBus115`, `storesFeed`, `emergencyBus`, and `emergencyInput` interfaces.
[x] Implement FlyByWireController.mo so surface commands, aero feedback, and actuator outputs match the architecture.
[x] Implement AirDataAndInertialSuite.mo to supply the `AirDataInertialState` output with proper power input handling.
[x] Implement EmergencyPowerUnit.mo to ingest `FuelLevelState` and provide an emergency electrical bus output.
[x] Implement StructuralLoadsAndPerformanceMonitor.mo to consume lift/thrust/air-data and emit `StructuralPerformanceState`.
[x] Implement StoresManagementSystem.mo covering command/telemetry buses plus power and structural interfaces.

---

Not is scope for now:

[] outline a few use case scenarios that connect to the requirements
[] extend simulation test scenarios to fulfill the use cases 

[] create simulation unit tests to verify requirement fulfillment of use-case simulations towards requirements
