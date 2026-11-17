within CompositeAirframeFMU;
model CompositeAirframe
  extends AircraftCommon.CompositeAirframe_Interface;
protected
  Real payloadCapacity "Usable payload in kg";
  Real referenceArea "Estimated wetted area proxy";
  Real wingLoading "Wing loading proxy (kg/m2)";
equation
  referenceArea = wettedAreaFactor * length * fuselageWidth;
  payloadCapacity = maxPayload * payloadScale;
  wingLoading = (emptyMass + payloadCapacity) / max(1, wingspan * 0.3 * length);
end CompositeAirframe;
