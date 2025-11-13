within WingmanDrone;
model DroneSystem
  import Interfaces = WingmanDrone.Interfaces;
  import GI = WingmanDrone.GeneratedInterfaces;
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
  FuelSystem fuel;
  Interfaces.RealOutput thrust_kN;
  Interfaces.RealOutput liftInterface;
  Interfaces.RealOutput payloadCapacityKg;
  Interfaces.RealOutput rangeEstimateKm;
  Interfaces.RealOutput orientationEuler;
  Interfaces.RealOutput locationLLA;
protected
  Real thrustToWeight;
  constant Real g_n = 9.80665;
equation
  power.generatorInput = engine.powerBus;
  missionComputer.powerIn = power.avionicsFeed;
  controls.powerIn = power.controlFeed;
  autopilot.powerIn = power.autonomyFeed;

  fuel.fuelFlowIn = engine.fuelFlow;
  engine.fuelStatus = fuel.fuelState;
  missionComputer.fuelStatus = fuel.fuelState;

  missionComputer.manualInput = controls.pilotCommandOut;
  missionComputer.autonomyPort = autopilot.guidanceCmd;
  engine.throttleCmd = missionComputer.engineThrottle;
  wings.controlSurfaces = missionComputer.surfaceBus;
  autopilot.feedbackBus = missionComputer.flightStatus;

  thrust_kN = engine.thrustOut.thrust_kn;
  liftInterface = wings.liftInterface.lift_kn;
  payloadCapacityKg = airframe.payloadCapacity;
  orientationEuler = missionComputer.orientationEuler.yaw_deg;
  locationLLA = missionComputer.locationLLA.latitude_deg;

  thrustToWeight = (engine.thrustOut.thrust_kn * 1000) / max(1.0, g_n * (airframe.emptyMass + airframe.payloadCapacity));
  rangeEstimateKm = 3000 * thrustToWeight * wingAreaScale;
end DroneSystem;
