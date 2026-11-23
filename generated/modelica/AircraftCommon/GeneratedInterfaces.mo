within AircraftCommon;
package GeneratedInterfaces
  connector EntityState
    Integer entity_identifier_site;
    Integer entity_identifier_application;
    Integer entity_identifier_entity;
    Integer entity_type_kind;
    Integer entity_type_domain;
    Integer entity_type_country;
    Integer entity_type_category;
    Integer entity_type_subcategory;
    Integer entity_type_specific;
    Integer entity_type_extra;
    Integer marking_character_set;
    String marking_characters;
    Integer force;
    Real spatial_world_location_x;
    Real spatial_world_location_y;
    Real spatial_world_location_z;
    Real spatial_orientation_psi;
    Real spatial_orientation_theta;
    Real spatial_orientation_phi;
    Real spatial_velocity_x;
    Real spatial_velocity_y;
    Real spatial_velocity_z;
    Real spatial_acceleration_x;
    Real spatial_acceleration_y;
    Real spatial_acceleration_z;
    Real spatial_angular_velocity_x;
    Real spatial_angular_velocity_y;
    Real spatial_angular_velocity_z;
    Integer spatial_dead_reckoning_algorithm;
    Boolean spatial_is_frozen;
  end EntityState;

  connector FlightStatusPacket
    Real airspeed_mps;
    Real energy_state_norm;
    Real angle_of_attack_deg;
    Real climb_rate;
    Integer health_code;
  end FlightStatusPacket;

  connector FuelConsumptionRate
    Real mass_flow_kgps;
  end FuelConsumptionRate;

  connector FuelLevelState
    Real fuel_remaining_kg;
    Real fuel_level_norm;
    Boolean fuel_starved;
  end FuelLevelState;

  connector LiftState
    Real lift_kn;
    Real drag_kn;
    Real pitching_moment_knm;
  end LiftState;

  connector MissionStatus
    Integer waypoint_index;
    Integer total_waypoints;
    Real distance_to_waypoint_km;
    Boolean arrived;
    Boolean complete;
  end MissionStatus;

  connector OrientationEuler
    Real roll_deg;
    Real pitch_deg;
    Real yaw_deg;
  end OrientationEuler;

  connector PilotCommand
    Real stick_pitch_norm;
    Real stick_roll_norm;
    Real rudder_norm;
    Real throttle_norm;
    Real throttle_aux_norm;
    Integer button_mask;
    Integer hat_x;
    Integer hat_y;
    Integer mode_switch;
    Integer reserved;
  end PilotCommand;

  connector PositionXYZ
    Real x_km;
    Real y_km;
    Real z_km;
  end PositionXYZ;

  connector SurfaceActuationCommand
    Real left_aileron_deg;
    Real right_aileron_deg;
    Real elevator_deg;
    Real rudder_deg;
    Real flaperon_deg;
  end SurfaceActuationCommand;

  connector ThrottleCommand
    Real throttle_norm;
    Boolean fuel_enable;
    Boolean afterburner_enable;
  end ThrottleCommand;

  connector ThrustState
    Real thrust_kn;
    Real mass_flow_kgps;
    Real exhaust_velocity_mps;
  end ThrustState;

end GeneratedInterfaces;
