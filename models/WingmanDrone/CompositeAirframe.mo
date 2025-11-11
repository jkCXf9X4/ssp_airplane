within WingmanDrone;
model CompositeAirframe
  import Interfaces = WingmanDrone.Interfaces;
  parameter Real length = 11.7 "Fuselage length (m)";
  parameter Real fuselageWidth = 1.9 "Average fuselage width (m)";
  parameter Real payloadScale(min=0.4, max=1.4) = 1.0;
  parameter Real maxPayload = 1500 "kg";
  parameter Real emptyMass = 2800 "kg";
  Interfaces.RealOutput payloadCapacity "Usable payload in kg";
  Interfaces.RealOutput referenceArea "Estimated wetted area proxy";
protected
  parameter Real wettedAreaFactor = 2.4;
equation
  referenceArea = wettedAreaFactor * length * fuselageWidth;
  payloadCapacity = maxPayload * payloadScale;
end CompositeAirframe;
