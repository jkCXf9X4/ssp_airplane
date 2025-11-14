within WingmanDrone;
model CompositeAirframe
  import Interfaces = WingmanDrone.Interfaces;
  parameter Real length = 15.0 "Fuselage length (m)";
  parameter Real fuselageWidth = 3.0 "Average fuselage width (m)";
  parameter Real wingspan = 10.0 "Wing span (m)";
  parameter Real payloadScale(min=0.4, max=1.4) = 1.0;
  parameter Real maxPayload = 7700 "kg";
  parameter Real emptyMass = 8573 "kg";
  output Real payloadCapacity "Usable payload in kg";
  output Real referenceArea "Estimated wetted area proxy";
  output Real wingLoading "Wing loading proxy (kg/m2)";
protected
  parameter Real wettedAreaFactor = 2.2;
equation
  referenceArea = wettedAreaFactor * length * fuselageWidth;
  payloadCapacity = maxPayload * payloadScale;
  wingLoading = (emptyMass + payloadCapacity) / max(1, wingspan * 0.3 * length);
end CompositeAirframe;
