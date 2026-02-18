package Aircraft {

  part def AircraftComposition {
    doc /* Top-level composition containing all subsystem instances and signal routing. */
    part control_interface : ControlInterface;
    part autopilot_module : AutopilotModule;
    part composite_airframe : CompositeAirframe;
    part turbofan_propulsion : TurbofanPropulsion;
    part mission_computer : MissionComputer;
    part fuel_system : FuelSystem;
    part adaptive_wing_system : AdaptiveWingSystem;
    part environment : Environment;
    part input_output : InputOutput;

  doc /* ControlInterface */
  connect control_interface.pilotCommand to mission_computer.manualInput;

  doc /* AutopilotModule */
  connect autopilot_module.autopilotCmd to mission_computer.autopilotInput;

  doc /* TurbofanPropulsion */
  connect turbofan_propulsion.thrustOut to environment.thrust_in;
  connect turbofan_propulsion.fuel_consumption to fuel_system.fuel_consumption_rate;

  doc /* MissionComputer */
  connect mission_computer.engineThrottle to turbofan_propulsion.throttleCmd;
  connect mission_computer.direction_command to adaptive_wing_system.direction_command;
  connect mission_computer.direction_command to environment.direction_command;

  doc /* FuelSystem */
  connect fuel_system.fuelState to mission_computer.fuelStatus;

  doc /* AdaptiveWingSystem */
  connect adaptive_wing_system.actuation_command to environment.actuation_command;
  connect adaptive_wing_system.liftInterface to environment.lift;

  doc /* Environment */
  connect environment.orientation to autopilot_module.currentOrientation;
  connect environment.location to autopilot_module.currentLocation;
  connect environment.flight_status to autopilot_module.feedbackBus;
  connect environment.flight_status to adaptive_wing_system.flight_speed;

  doc /* InputOutput telemetry taps */
  connect environment.location to input_output.locationXYZ;
  connect environment.orientation to input_output.orientation;
  connect autopilot_module.autopilotCmd to input_output.autopilotCmd;
  connect environment.flight_status to input_output.flightStatus;
  connect autopilot_module.missionStatus to input_output.missionStatus;
  }

}
