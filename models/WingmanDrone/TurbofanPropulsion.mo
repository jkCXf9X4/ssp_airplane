within WingmanDrone;
model TurbofanPropulsion
  import Interfaces = WingmanDrone.Interfaces;
  parameter Real maxThrust_kN = 60;
  parameter Real generatorOutputKW = 150;
  parameter Real fuelEfficiency = 0.38;
  parameter Real fuelFlowAtFull_kgps = 0.75;
  Interfaces.RealInput throttleCmd;
  Interfaces.RealInput fuelStatus;
  Interfaces.RealOutput thrustOut;
  Interfaces.RealOutput fuelFlow;
  Interfaces.RealOutput powerBus;
protected
  Real commandedThrust;
  Real throttle;
  Real fuelAvailability;
equation
  throttle = max(0, min(1, throttleCmd));
  fuelAvailability = max(0, min(1, fuelStatus));
  commandedThrust = throttle * fuelAvailability * maxThrust_kN;
  thrustOut = commandedThrust;
  fuelFlow = throttle * fuelAvailability * fuelFlowAtFull_kgps;
  powerBus = generatorOutputKW / 1000 * fuelEfficiency * max(0.2, throttle) * fuelAvailability;
end TurbofanPropulsion;
