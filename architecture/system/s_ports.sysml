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
    doc /* Air vehicle orientation expressed as Euler angles in degrees. */
    attribute roll_deg: Real;
    attribute pitch_deg: Real;
    attribute yaw_deg: Real;
  }

  port def PositionXYZ {
    doc /* Local navigation frame expressed in kilometers (x=North, y=East, z=Up). */
    attribute x_km: Real;
    attribute y_km: Real;
    attribute z_km: Real;
  }

  port def SurfaceActuationCommand {
    doc /* Commanded surface deflections in degrees for co-simulation with aerodynamic models. */
    attribute left_aileron_deg: Real;
    attribute right_aileron_deg: Real;
    attribute elevator_deg: Real;
    attribute rudder_deg: Real;
    attribute flaperon_deg: Real;
  }

  port def ThrottleCommand {
    doc /* Engine throttle and fuel-enable bit for turbofan co-simulation. */
    attribute throttle_norm: Real;
    attribute fuel_enable: Boolean;
    attribute afterburner_enable: Boolean;
  }

  port def FuelLevelState {
    doc /* Remaining fuel mass and normalized level for availability tracking. */
    attribute fuel_remaining_kg: Real;
    attribute fuel_level_norm: Real;
    attribute fuel_starved: Boolean;
  }

  port def FuelConsumptionRate {
    doc /* Mass flow request or telemetry for turbofan fuel usage (kg/s). */
    attribute mass_flow_kgps: Real;
  }

  port def MissionStatus {
    doc /* Waypoint-tracking status produced by the autopilot for logging and requirement evaluation. */
    attribute waypoint_index: Integer;
    attribute total_waypoints: Integer;
    attribute distance_to_waypoint_km: Real;
    attribute arrived: Boolean;
    attribute complete: Boolean;
  }

  port def FlightStatusPacket {
    doc /* Mission computer status feedback consumed by autonomy and analysis models. */
    attribute airspeed_mps: Real;
    attribute energy_state_norm: Real;
    attribute angle_of_attack_deg: Real;
    attribute health_code: Integer;
  }


}
