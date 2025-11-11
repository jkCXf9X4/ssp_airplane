within SSPAirplane;
model Fuselage
  import Modelica.SIunits;
  parameter SI.Length length = 39.5 "Fuselage length (m)";
  parameter SI.Length cabinDiameter = 3.76;
  parameter Real payloadScale(min=0.5, max=1.2) = 1.0;
  parameter SI.Mass maxPayload = 20000;
  parameter SI.Mass emptyMass = 22000;
  Modelica.Blocks.Interfaces.RealOutput payloadCapacity "Usable payload in kg";
  Modelica.Blocks.Interfaces.RealOutput referenceArea "Estimated wetted area proxy";
protected
  parameter Real wettedAreaFactor = 3.2;
initial equation
  referenceArea = wettedAreaFactor * length * cabinDiameter;
equation
  payloadCapacity = maxPayload * payloadScale;
end Fuselage;
