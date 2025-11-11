within SSPAirplane;
model AircraftSystem
  import Modelica.Constants;
  parameter Real wingAreaScale = 1.0;
  parameter Real motorPowerScale = 1.0;
  parameter Real payloadScale = 1.0;
  ReactorCore reactor;
  ElectricalSystem electrical;
  MotorArray motors(motorPowerScale = motorPowerScale);
  Fuselage fuselage(payloadScale = payloadScale);
  WingSystem wings(wingAreaScale = wingAreaScale);
  ControlSoftware control;
  AutopilotModule autopilot;
  Modelica.Blocks.Interfaces.RealInput missionAggressiveness;
  Modelica.Blocks.Interfaces.RealInput rangeRequestKm;
  Modelica.Blocks.Interfaces.RealOutput thrust_kN;
  Modelica.Blocks.Interfaces.RealOutput liftCoefficient;
  Modelica.Blocks.Interfaces.RealOutput payloadCapacityKg;
  Modelica.Blocks.Interfaces.RealOutput rangeEstimateKm;
protected
  Real reserveFactor;
  Real thrustToWeight;
equation
  connect(reactor.electricPowerMW, electrical.reactorPowerMW);
  connect(electrical.motorPowerMW, motors.electricalPowerMW);
  connect(control.throttleCmd, motors.throttleCmd);
  connect(control.liftCommand, wings.liftCommand);
  connect(fuselage.payloadCapacity, control.payloadCapacityKg);
  connect(electrical.controlPowerMW, control.avionicsPowerMW);
  connect(autopilot.guidanceCommand, control.guidanceCommand);
  connect(motors.thrust_kN, thrust_kN);
  connect(wings.liftCoefficient, liftCoefficient);
  connect(fuselage.payloadCapacity, payloadCapacityKg);
  connect(missionAggressiveness, autopilot.missionAggressiveness);
  connect(rangeRequestKm, autopilot.rangeRequestKm);
  reserveFactor = max(0.2, 1.0 - missionAggressiveness);
  thrustToWeight = (motors.thrust_kN * 1000) / max(1.0, Constants.g_n * (fuselage.emptyMass + fuselage.payloadCapacity));
  rangeEstimateKm = (8500 * thrustToWeight * reserveFactor) + 1000 * autopilot.missionScore;
end AircraftSystem;
