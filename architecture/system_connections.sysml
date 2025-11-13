package WingmanDrone {
  connect AdaptiveWingSystem.structuralMount to CompositeAirframe.structuralMount;
  connect TurbofanPropulsion.mountingHardpoint to CompositeAirframe.engineMount;
  connect TurbofanPropulsion.powerBus to PowerSystem.generatorInput;
  connect PowerSystem.avionicsFeed to MissionComputer.powerIn;
  connect PowerSystem.controlFeed to ControlInterface.powerIn;
  connect PowerSystem.autonomyFeed to AutopilotModule.powerIn;
  connect MissionComputer.surfaceBus to AdaptiveWingSystem.controlSurfaces;
  connect MissionComputer.engineThrottle to TurbofanPropulsion.throttleCmd;
  connect TurbofanPropulsion.fuelFlow to FuelSystem.fuelFlowIn;
  connect FuelSystem.fuelState to TurbofanPropulsion.fuelStatus;
  connect FuelSystem.fuelState to MissionComputer.fuelStatus;
  connect AutopilotModule.guidanceCmd to MissionComputer.autonomyPort;
  connect MissionComputer.flightStatus to AutopilotModule.feedbackBus;
  connect ControlInterface.pilotCommandOut to MissionComputer.manualInput;
}