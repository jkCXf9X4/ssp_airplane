within WingmanDrone;
package GeneratedInterfaces
  record AutonomyGuidance
    Real waypoint_heading_deg;
    Real waypoint_altitude_m;
    Real lateral_accel_mps2;
    Real aggressiveness_norm;
  end AutonomyGuidance;

  record FlightStatusPacket
    Real airspeed_mps;
    Real energy_state_norm;
    Real angle_of_attack_deg;
    Integer health_code;
  end FlightStatusPacket;

  record FuelConsumptionRate
    Real mass_flow_kgps;
  end FuelConsumptionRate;

  record FuelLevelState
    Real fuel_remaining_kg;
    Real fuel_level_norm;
    Boolean fuel_starved;
  end FuelLevelState;

  record GenericElectricalBus
    Real voltage_kv;
    Real current_a;
    Real available_power_kw;
  end GenericElectricalBus;

  record GeodeticLLA
    Real latitude_deg;
    Real longitude_deg;
    Real altitude_m;
  end GeodeticLLA;

  record LiftState
    Real lift_kn;
    Real drag_kn;
    Real pitching_moment_knm;
  end LiftState;

  record OrientationEuler
    Real roll_deg;
    Real pitch_deg;
    Real yaw_deg;
  end OrientationEuler;

  record PilotCommand
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

  record StructuralInterface
    Real axial_load_kn;
    Real shear_load_kn;
    Real bending_moment_knm;
  end StructuralInterface;

  record SurfaceActuationCommand
    Real left_aileron_deg;
    Real right_aileron_deg;
    Real elevator_deg;
    Real rudder_deg;
    Real flaperon_deg;
  end SurfaceActuationCommand;

  record ThrottleCommand
    Real throttle_norm;
    Boolean fuel_enable;
    Boolean afterburner_enable;
  end ThrottleCommand;

  record ThrustState
    Real thrust_kn;
    Real mass_flow_kgps;
    Real exhaust_velocity_mps;
  end ThrustState;

end GeneratedInterfaces;