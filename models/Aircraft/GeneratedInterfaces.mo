within Aircraft;
package GeneratedInterfaces
  connector AirDataInertialState
    Real mach_number;
    Real true_airspeed_mps;
    Real indicated_airspeed_mps;
    Real pressure_altitude_m;
    Real vertical_speed_mps;
    Real angle_of_attack_deg;
    Real sideslip_deg;
    Real roll_rate_degps;
    Real pitch_rate_degps;
    Real yaw_rate_degps;
  end AirDataInertialState;

  connector AutonomyGuidance
    Real waypoint_heading_deg;
    Real waypoint_altitude_m;
    Real lateral_accel_mps2;
    Real aggressiveness_norm;
  end AutonomyGuidance;

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

  connector GenericElectricalBus
    Real voltage_kv;
    Real current_a;
    Real available_power_kw;
  end GenericElectricalBus;

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

  connector StoresCommandBus
    Integer selected_station;
    Boolean release_enable;
    Boolean pickle_command;
    Boolean jettison_all;
    Integer power_mode_mask;
    Integer config_checksum;
  end StoresCommandBus;

  connector StoresStatusBus
    Integer store_present_mask;
    Integer weapon_ready_mask;
    Real store_mass_total_kg;
    Real cooling_demand_kw;
    Integer fault_code;
  end StoresStatusBus;

  connector StructuralInterface
    Real axial_load_kn;
    Real shear_load_kn;
    Real bending_moment_knm;
  end StructuralInterface;

  connector StructuralPerformanceState
    Real load_factor_g;
    Real mach_estimate;
    Real structural_margin_norm;
    Boolean stores_release_inhibit;
    Integer autopilot_limit_code;
  end StructuralPerformanceState;

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