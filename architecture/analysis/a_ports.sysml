package Aircraft::Analysis {

  port def LiftState {
    doc /* Aerodynamic state summary exported from wing solver. */
    attribute lift_kn: Real;
    attribute drag_kn: Real;
    attribute pitching_moment_knm: Real;
  }

  port def ThrustState {
    doc /* Propulsion output shared with performance models. */
    attribute thrust_kn: Real;
    attribute mass_flow_kgps: Real;
    attribute exhaust_velocity_mps: Real;
  }

  port def FlightStatusPacket {
    doc /* Mission computer status feedback consumed by autonomy and analysis models. */
    attribute airspeed_mps: Real;
    attribute energy_state_norm: Real;
    attribute angle_of_attack_deg: Real;
    attribute health_code: Integer;
  }

}
