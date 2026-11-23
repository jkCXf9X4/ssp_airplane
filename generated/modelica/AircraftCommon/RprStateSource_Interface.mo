within AircraftCommon;

partial model RprStateSource_Interface
  parameter Real reference_latitude_deg = 0;
  parameter Real reference_longitude_deg = 0;
  parameter Real reference_altitude_m = 0;
  parameter Integer entity_site = 0;
  parameter Integer entity_application = 0;
  parameter Integer entity_entity = 0;
  parameter Integer entity_type_kind = 0;
  parameter Integer entity_type_domain = 0;
  parameter Integer entity_type_country = 0;
  parameter Integer entity_type_category = 0;
  parameter Integer entity_type_subcategory = 0;
  parameter Integer entity_type_specific = 0;
  parameter Integer entity_type_extra = 0;
  parameter Integer force = 0;
  parameter Integer marking_character_set = 0;
  parameter String marking_characters = "";
  input GeneratedInterfaces.PositionXYZ position;
  input GeneratedInterfaces.OrientationEuler orientation;
  input GeneratedInterfaces.FlightStatusPacket flightStatus;
  output GeneratedInterfaces.EntityState entityState;
end RprStateSource_Interface;
