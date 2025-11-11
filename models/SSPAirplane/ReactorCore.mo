within SSPAirplane;
model ReactorCore
  import Interfaces = SSPAirplane.Interfaces;
  parameter Real thermalPowerMW = 80 "Thermal power (MW)";
  parameter Real electricalEfficiency(min=0, max=1) = 0.42;
  parameter Real shieldingMass = 12000 "kg";
  parameter Real enduranceHours = 20 "h";
  Interfaces.RealOutput electricPowerMW "Net electrical output";
  Interfaces.RealOutput wasteHeatMW "Residual waste heat";
equation
  electricPowerMW = thermalPowerMW * electricalEfficiency;
  wasteHeatMW = thermalPowerMW - electricPowerMW;
end ReactorCore;
