within RprStateSourceFMU;
model RprStateSource
  extends AircraftCommon.RprStateSource_Interface;

protected
  constant Real wgs84_a = 6378137.0;
  constant Real wgs84_f = 1.0 / 298.257223563;
  constant Real wgs84_e2 = wgs84_f * (2.0 - wgs84_f);
  constant Real deg_to_rad = Modelica.Constants.pi / 180.0;

  // WGS84 reference origin in ECEF and the ENU basis it defines.
  Real sin_ref_lat;
  Real cos_ref_lat;
  Real sin_ref_lon;
  Real cos_ref_lon;
  Real ref_radius;
  Real ref_x;
  Real ref_y;
  Real ref_z;

  // Local ENU offset in metres.
  Real north_m;
  Real east_m;
  Real up_m;

  Real aoa_rad;

equation
  // ---- identity, type, marking and force come from the instance parameters ----
  entityState.entity_identifier_site = entity_site;
  entityState.entity_identifier_application = entity_application;
  entityState.entity_identifier_entity = entity_entity;
  entityState.entity_type_kind = entity_type_kind;
  entityState.entity_type_domain = entity_type_domain;
  entityState.entity_type_country = entity_type_country;
  entityState.entity_type_category = entity_type_category;
  entityState.entity_type_subcategory = entity_type_subcategory;
  entityState.entity_type_specific = entity_type_specific;
  entityState.entity_type_extra = entity_type_extra;
  entityState.marking_character_set = marking_character_set;
  entityState.marking_characters = marking_characters;
  entityState.force = force;

  // ---- WGS84 geodetic origin (degrees, metres) to ECEF (metres) ----
  sin_ref_lat = sin(reference_latitude_deg * deg_to_rad);
  cos_ref_lat = cos(reference_latitude_deg * deg_to_rad);
  sin_ref_lon = sin(reference_longitude_deg * deg_to_rad);
  cos_ref_lon = cos(reference_longitude_deg * deg_to_rad);

  ref_radius = wgs84_a / sqrt(1.0 - wgs84_e2 * sin_ref_lat * sin_ref_lat);
  ref_x = (ref_radius + reference_altitude_m) * cos_ref_lat * cos_ref_lon;
  ref_y = (ref_radius + reference_altitude_m) * cos_ref_lat * sin_ref_lon;
  ref_z = (ref_radius * (1.0 - wgs84_e2) + reference_altitude_m) * sin_ref_lat;

  // ---- local ENU offset (x north, y east, z up; kilometres to metres) ----
  north_m = position.x_km * 1000.0;
  east_m = position.y_km * 1000.0;
  up_m = position.z_km * 1000.0;

  entityState.spatial_world_location_x = ref_x
    - sin_ref_lon * east_m
    - sin_ref_lat * cos_ref_lon * north_m
    + cos_ref_lat * cos_ref_lon * up_m;
  entityState.spatial_world_location_y = ref_y
    + cos_ref_lon * east_m
    - sin_ref_lat * sin_ref_lon * north_m
    + cos_ref_lat * sin_ref_lon * up_m;
  entityState.spatial_world_location_z = ref_z
    + cos_ref_lat * north_m
    + sin_ref_lat * up_m;

  // ---- attitude: Euler degrees to Z-Y-X (psi, theta, phi) radians ----
  entityState.spatial_orientation_psi = orientation.yaw_deg * deg_to_rad;
  entityState.spatial_orientation_theta = orientation.pitch_deg * deg_to_rad;
  entityState.spatial_orientation_phi = orientation.roll_deg * deg_to_rad;

  // ---- body-frame velocity, x forward and z down-positive ----
  // Approximation: level-flight airspeed and angle of attack only; climb rate
  // and side-slip are not represented in this first broadcast.
  aoa_rad = flightStatus.angle_of_attack_deg * deg_to_rad;
  entityState.spatial_velocity_x = flightStatus.airspeed_mps * cos(aoa_rad);
  entityState.spatial_velocity_y = 0.0;
  entityState.spatial_velocity_z = flightStatus.airspeed_mps * sin(aoa_rad);

  // Gap: the aircraft model exposes no body-frame accelerations yet.
  entityState.spatial_acceleration_x = 0.0;
  entityState.spatial_acceleration_y = 0.0;
  entityState.spatial_acceleration_z = 0.0;

  // Gap: the aircraft model exposes no body-frame angular rates yet.
  entityState.spatial_angular_velocity_x = 0.0;
  entityState.spatial_angular_velocity_y = 0.0;
  entityState.spatial_angular_velocity_z = 0.0;

  entityState.spatial_dead_reckoning_algorithm = 0;
  entityState.spatial_is_frozen = false;
end RprStateSource;
