package WingmanDrone {
  port def PilotCommand {
    doc /* HOTAS-style control payload shared across control surfaces and mission computer consumers. */
    attribute stick_pitch_norm: Real;   /* -1..1, aft pull positive */
    attribute stick_roll_norm: Real;    /* -1..1, left deflection positive */
    attribute rudder_norm: Real;        /* -1..1, pedal/twist input */
    attribute throttle_norm: Real;      /* 0..1 primary throttle */
    attribute throttle_aux_norm: Real;  /* 0..1 aux slider or second throttle */
    attribute button_mask: Integer;     /* bitfield: trigger1, trigger2, weapon_release, gear, master_arm, autopilot, comms, countermeasure, flaps_up, flaps_down */
    attribute hat_x: Integer;           /* -1=left,0=center,1=right */
    attribute hat_y: Integer;           /* -1=down,0=center,1=up */
    attribute mode_switch: Integer;     /* 0=Manual,1=Assist,2=RTB,3=Auto */
    attribute reserved: Integer;        /* alignment / future discrete inputs */
  }

  port def OrientationEuler {
    doc /* Air vehicle orientation expressed as body-to-earth Euler angles in degrees. */
    attribute roll_deg: Real;
    attribute pitch_deg: Real;
    attribute yaw_deg: Real;
  }

  port def GeodeticLLA {
    doc /* Geodetic latitude/longitude (degrees) and altitude (meters) above mean sea level. */
    attribute latitude_deg: Real;
    attribute longitude_deg: Real;
    attribute altitude_m: Real;
  }

  port def AirDataInertialState {
    doc /* High-rate pitot-static + INS fused navigation state for control-law inputs. */
    attribute mach_number: Real;
    attribute true_airspeed_mps: Real;
    attribute indicated_airspeed_mps: Real;
    attribute pressure_altitude_m: Real;
    attribute vertical_speed_mps: Real;
    attribute angle_of_attack_deg: Real;
    attribute sideslip_deg: Real;
    attribute roll_rate_degps: Real;
    attribute pitch_rate_degps: Real;
    attribute yaw_rate_degps: Real;
  }

  port def StructuralInterface {
    doc /* Structural mounting loads transferred between assemblies. */
    attribute axial_load_kn: Real;
    attribute shear_load_kn: Real;
    attribute bending_moment_knm: Real;
  }

  port def SurfaceActuationCommand {
    doc /* Commanded surface deflections in degrees for co-simulation with aerodynamic models. */
    attribute left_aileron_deg: Real;
    attribute right_aileron_deg: Real;
    attribute elevator_deg: Real;
    attribute rudder_deg: Real;
    attribute flaperon_deg: Real;
  }

  port def LiftState {
    doc /* Aerodynamic state summary exported from wing solver. */
    attribute lift_kn: Real;
    attribute drag_kn: Real;
    attribute pitching_moment_knm: Real;
  }

  port def ThrottleCommand {
    doc /* Engine throttle and fuel-enable bit for turbofan co-simulation. */
    attribute throttle_norm: Real;
    attribute fuel_enable: Boolean;
    attribute afterburner_enable: Boolean;
  }

  port def ThrustState {
    doc /* Propulsion output shared with performance models. */
    attribute thrust_kn: Real;
    attribute mass_flow_kgps: Real;
    attribute exhaust_velocity_mps: Real;
  }

  port def GenericElectricalBus {
    doc /* Power bus telemetry for avionics, control, and autonomy loads. */
    attribute voltage_kv: Real;
    attribute current_a: Real;
    attribute available_power_kw: Real;
  }

  port def AutonomyGuidance {
    doc /* Autopilot-to-mission-computer guidance cues for co-simulation. */
    attribute waypoint_heading_deg: Real;
    attribute waypoint_altitude_m: Real;
    attribute lateral_accel_mps2: Real;
    attribute aggressiveness_norm: Real;
  }

  port def FlightStatusPacket {
    doc /* Mission computer status feedback consumed by autonomy and analysis models. */
    attribute airspeed_mps: Real;
    attribute energy_state_norm: Real;
    attribute angle_of_attack_deg: Real;
    attribute health_code: Integer;
  }

  port def FuelConsumptionRate {
    doc /* Mass flow request or telemetry for turbofan fuel usage (kg/s). */
    attribute mass_flow_kgps: Real;
  }

  port def FuelLevelState {
    doc /* Remaining fuel mass and normalized level for availability tracking. */
    attribute fuel_remaining_kg: Real;
    attribute fuel_level_norm: Real;
    attribute fuel_starved: Boolean;
  }

  port def StoresCommandBus {
    doc /* Mission-computer command bundle for nine-store management, power, and jettison logic. */
    attribute selected_station: Integer;       /* 1..9 station index */
    attribute release_enable: Boolean;         /* Master arm */
    attribute pickle_command: Boolean;         /* True when release triggered */
    attribute jettison_all: Boolean;           /* Emergency store dump */
    attribute power_mode_mask: Integer;        /* bitmask enabling station power */
    attribute config_checksum: Integer;        /* Validates loadout tables */
  }

  port def StoresStatusBus {
    doc /* Health, weight, and readiness telemetry for all external stores. */
    attribute store_present_mask: Integer;
    attribute weapon_ready_mask: Integer;
    attribute store_mass_total_kg: Real;
    attribute cooling_demand_kw: Real;
    attribute fault_code: Integer;
  }

  port def StructuralPerformanceState {
    doc /* Structural and performance envelope monitoring for g-limit and Mach supervision. */
    attribute load_factor_g: Real;
    attribute mach_estimate: Real;
    attribute structural_margin_norm: Real;
    attribute stores_release_inhibit: Boolean;
    attribute autopilot_limit_code: Integer;
  }
}
