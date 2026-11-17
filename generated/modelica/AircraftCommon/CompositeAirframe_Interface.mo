within AircraftCommon;

partial model CompositeAirframe_Interface
  parameter Real length_m = 15;
  parameter Real fuselage_width_m = 3;
  parameter Real wingspan_m = 10;
  parameter Real empty_weight_kg = 8573;
  parameter Real payload_capacity_kg = 7700;
  parameter Integer hardpoint_count = 9;
  parameter Real length = 15;
  parameter Real fuselageWidth = 3;
  parameter Real wingspan = 10;
  parameter Real payloadScale = 1;
  parameter Real maxPayload = 7700;
  parameter Real emptyMass = 8573;
  parameter Real wettedAreaFactor = 2.2;
end CompositeAirframe_Interface;
