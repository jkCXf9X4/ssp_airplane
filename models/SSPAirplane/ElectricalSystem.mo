within SSPAirplane;
model ElectricalSystem
  import Interfaces = SSPAirplane.Interfaces;
  parameter Real busVoltageKV = 5;
  parameter Real bufferCapacityMJ = 800;
  parameter Real distributionEfficiency = 0.96;
  Interfaces.RealInput reactorPowerMW;
  Interfaces.RealOutput motorPowerMW;
  Interfaces.RealOutput controlPowerMW;
  Interfaces.RealOutput lossesMW;
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
