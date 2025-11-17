within Aircraft;
package GeneratedInterfaces
  connector FlightStatusPacket
    Real airspeed_mps;
    Real energy_state_norm;
    Real angle_of_attack_deg;
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

  connector GeodeticLLA
    Real latitude_deg;
    Real longitude_deg;
    Real altitude_m;
  end GeodeticLLA;

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