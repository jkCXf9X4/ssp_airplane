package Aircraft {

  part def AircraftComposition {
    doc /* Top-level composition containing all subsystem instances and signal routing. */
    part ControlInterface : ControlInterface;
    part AutopilotModule : AutopilotModule;
    part CompositeAirframe : CompositeAirframe;
    part TurbofanPropulsion : TurbofanPropulsion;
    part MissionComputer : MissionComputer;
    part FuelSystem : FuelSystem;
    part AdaptiveWingSystem : AdaptiveWingSystem;
    part Environment : Environment;
    part InputOutput : InputOutput;

  doc /* ControlInterface */
  connect ControlInterface.pilotCommand to MissionComputer.manualInput;

  doc /* AutopilotModule */
  connect AutopilotModule.autopilotCmd to MissionComputer.autopilotInput;

  doc /* TurbofanPropulsion */
  connect TurbofanPropulsion.thrustOut to Environment.thrust_in;
  connect TurbofanPropulsion.fuel_consumption to FuelSystem.fuel_consumption_rate;

  doc /* MissionComputer */
  connect MissionComputer.engineThrottle to TurbofanPropulsion.throttleCmd;
  connect MissionComputer.direction_command to AdaptiveWingSystem.direction_command;
  connect MissionComputer.direction_command to Environment.direction_command;

  doc /* FuelSystem */
  connect FuelSystem.fuelState to MissionComputer.fuelStatus;

  doc /* AdaptiveWingSystem */
  connect AdaptiveWingSystem.actuation_command to Environment.actuation_command;
  connect AdaptiveWingSystem.liftInterface to Environment.lift;

  doc /* Environment */
  connect Environment.orientation to AutopilotModule.currentOrientation;
  connect Environment.location to AutopilotModule.currentLocation;
  connect Environment.flight_status to AutopilotModule.feedbackBus;
  connect Environment.flight_status to AdaptiveWingSystem.flight_speed;

  doc /* InputOutput telemetry taps */
  connect Environment.location to InputOutput.locationXYZ;
  connect Environment.orientation to InputOutput.orientation;
  connect AutopilotModule.autopilotCmd to InputOutput.autopilotCmd;
  connect Environment.flight_status to InputOutput.flightStatus;
  connect AutopilotModule.missionStatus to InputOutput.missionStatus;
  }

}
