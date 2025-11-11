within SSPAirplane;
model ElectricalSystem
  parameter Real busVoltageKV = 5;
  parameter Real bufferCapacityMJ = 800;
  parameter Real distributionEfficiency = 0.96;
  Modelica.Blocks.Interfaces.RealInput reactorPowerMW;
  Modelica.Blocks.Interfaces.RealOutput motorPowerMW;
  Modelica.Blocks.Interfaces.RealOutput controlPowerMW;
  Modelica.Blocks.Interfaces.RealOutput lossesMW;
protected
  parameter Real controlShare = 0.08;
  Real availableMW;
  Real bufferedMW;
equation
  availableMW = reactorPowerMW * distributionEfficiency;
  bufferedMW = min(bufferCapacityMJ / 3.6, reactorPowerMW - availableMW);
  controlPowerMW = availableMW * controlShare;
  motorPowerMW = max(0, availableMW - controlPowerMW);
  lossesMW = reactorPowerMW - availableMW + bufferedMW;
end ElectricalSystem;
