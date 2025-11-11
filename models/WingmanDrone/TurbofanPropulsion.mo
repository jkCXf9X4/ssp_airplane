within WingmanDrone;
model TurbofanPropulsion
  import Interfaces = WingmanDrone.Interfaces;
  parameter Real maxThrust_kN = 60;
  parameter Real generatorOutputKW = 150;
  parameter Real fuelEfficiency = 0.38;
  Interfaces.RealInput throttleCmd;
  Interfaces.RealOutput thrustOut;
  Interfaces.RealOutput powerBus;
protected
  Real commandedThrust;
equation
  commandedThrust = max(0, throttleCmd) * maxThrust_kN;
  thrustOut = commandedThrust;
  powerBus = generatorOutputKW / 1000 * fuelEfficiency * max(0.2, throttleCmd);
end TurbofanPropulsion;
