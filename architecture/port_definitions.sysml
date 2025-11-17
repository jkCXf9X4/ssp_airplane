package Aircraft {
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

  port def FuelLevelState {
    doc /* Remaining fuel mass and normalized level for availability tracking. */
    attribute fuel_remaining_kg: Real;
    attribute fuel_level_norm: Real;
    attribute fuel_starved: Boolean;
  }

  port def FlightStatusPacket {
    doc /* Mission computer status feedback consumed by autonomy and analysis models. */
    attribute airspeed_mps: Real;
  }



}
