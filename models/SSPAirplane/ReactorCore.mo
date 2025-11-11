within SSPAirplane;
model ReactorCore
  import Modelica.SIunits;
  parameter Real thermalPowerMW = 80 "Thermal power (MW)";
  parameter Real electricalEfficiency(min=0, max=1) = 0.42;
  parameter SI.Mass shieldingMass = 12000;
  parameter SI.Time enduranceHours = 20;
  Modelica.Blocks.Interfaces.RealOutput electricPowerMW "Net electrical output";
  Modelica.Blocks.Interfaces.RealOutput wasteHeatMW "Residual waste heat";
equation
  electricPowerMW = thermalPowerMW * electricalEfficiency;
  wasteHeatMW = thermalPowerMW - electricPowerMW;
end ReactorCore;
