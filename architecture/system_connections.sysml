package Aircraft {
  doc /* ControlInterface */
  connect ControlInterface.pilotCommand to MissionComputer.manualInput;

  doc /* AutopilotModule */
  connect AutopilotModule.autopilotCmd to MissionComputer.autopilotInput;

  doc /* TurbofanPropulsion */
  connect TurbofanPropulsion.thrustOut to Environment.thrust_in;
  connect TurbofanPropulsion.fuel_consumption to FuelSystem.fuel_consumption_rate;

  doc /* MissionComputer */
  connect MissionComputer.engineThrottle to TurbofanPropulsion.throttleCmd;
  connect MissionComputer.speed_vector_change to AdaptiveWingSystem.velocity_vector_alteration;

  doc /* FuelSystem */
  connect FuelSystem.fuelState to MissionComputer.fuelStatus;

  doc /* AdaptiveWingSystem */
  connect AdaptiveWingSystem.actuation_command to Environment.actuation_command;
  connect AdaptiveWingSystem.lift_state to Environment.lift_state;

  doc /* Environment */
  connect Environment.orientation to AutopilotModule.currentOrientation;
  connect Environment.location to AutopilotModule.currentLocation;
  connect Environment.flight_status to AutopilotModule.feedbackBus;
  connect Environment.flight_status to AdaptiveWingSystem.flight_speed;
}



