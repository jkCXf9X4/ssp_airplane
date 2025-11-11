within SSPAirplane;
model AutopilotModule
  import Interfaces = SSPAirplane.Interfaces;
  parameter Real updateRateHz = 20;
  parameter Real sensorFidelity = 0.95;
  Interfaces.RealInput missionAggressiveness "0..1 mission intensity";
  Interfaces.RealInput rangeRequestKm;
  Interfaces.RealOutput guidanceCommand;
  Interfaces.RealOutput missionScore;
protected
  Real rangeFactor;
equation
  rangeFactor = min(1.0, rangeRequestKm / 9000);
  guidanceCommand = max(0.3, sensorFidelity * (1 - missionAggressiveness) + 0.1 * rangeFactor);
  missionScore = guidanceCommand * rangeFactor;
end AutopilotModule;
