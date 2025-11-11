within SSPAirplane;
model Fuselage
  import Interfaces = SSPAirplane.Interfaces;
  parameter Real length = 39.5 "Fuselage length (m)";
  parameter Real cabinDiameter = 3.76;
  parameter Real payloadScale(min=0.5, max=1.2) = 1.0;
  parameter Real maxPayload = 20000 "kg";
  parameter Real emptyMass = 22000 "kg";
  Interfaces.RealOutput payloadCapacity "Usable payload in kg";
  Interfaces.RealOutput referenceArea "Estimated wetted area proxy";
protected
  parameter Real wettedAreaFactor = 3.2;
equation
  referenceArea = wettedAreaFactor * length * cabinDiameter;
  payloadCapacity = maxPayload * payloadScale;
end Fuselage;
