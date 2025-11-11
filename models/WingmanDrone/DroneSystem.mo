within WingmanDrone;
model DroneSystem
  import Interfaces = WingmanDrone.Interfaces;
  parameter Real wingAreaScale = 1.0;
  parameter Real engineThrustScale = 1.0;
  parameter Real payloadScale = 1.0;
  PowerSystem power;
  TurbofanPropulsion engine(maxThrust_kN = 60 * engineThrustScale);
  CompositeAirframe airframe(payloadScale = payloadScale);
  AdaptiveWingSystem wings(wingAreaScale = wingAreaScale);
  MissionComputer missionComputer;
  AutopilotModule autopilot;
  ControlInterface controls;
  Interfaces.RealInput manualCommand;
  Interfaces.RealOutput thrust_kN;
  Interfaces.RealOutput liftInterface;
  Interfaces.RealOutput payloadCapacityKg;
  Interfaces.RealOutput rangeEstimateKm;
protected
  Real thrustToWeight;
  constant Real g_n = 9.80665;
equation
  connect(engine.powerBus, power.generatorInput);
  connect(power.avionicsFeed, missionComputer.powerIn);
  connect(power.controlFeed, controls.powerIn);
  connect(power.autonomyFeed, autopilot.powerIn);
  connect(controls.pilotCommandOut, missionComputer.manualInput);
  connect(autopilot.guidanceCmd, missionComputer.autonomyPort);
  connect(missionComputer.engineThrottle, engine.throttleCmd);
  connect(missionComputer.surfaceBus, wings.controlSurfaces);
  connect(missionComputer.flightStatus, autopilot.feedbackBus);
  connect(manualCommand, controls.pilotCommand);
  connect(engine.thrustOut, thrust_kN);
  connect(wings.liftInterface, liftInterface);
  connect(airframe.payloadCapacity, payloadCapacityKg);
  thrustToWeight = (engine.thrustOut * 1000) / max(1.0, g_n * (airframe.emptyMass + airframe.payloadCapacity));
  rangeEstimateKm = 3000 * thrustToWeight * wingAreaScale;
end DroneSystem;
