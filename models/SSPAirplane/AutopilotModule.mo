within SSPAirplane;
model AutopilotModule
  parameter Real updateRateHz = 20;
  parameter Real sensorFidelity = 0.95;
  Modelica.Blocks.Interfaces.RealInput missionAggressiveness "0..1 mission intensity";
  Modelica.Blocks.Interfaces.RealInput rangeRequestKm;
  Modelica.Blocks.Interfaces.RealOutput guidanceCommand;
  Modelica.Blocks.Interfaces.RealOutput missionScore;
protected
  Real rangeFactor;
equation
  rangeFactor = min(1.0, rangeRequestKm / 9000);
  guidanceCommand = max(0.3, sensorFidelity * (1 - missionAggressiveness) + 0.1 * rangeFactor);
  missionScore = guidanceCommand * rangeFactor;
end AutopilotModule;
