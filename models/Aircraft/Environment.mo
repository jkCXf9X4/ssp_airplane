within Aircraft;
model Environment
  import GI = Aircraft.GeneratedInterfaces;

  parameter Real initX_km = 0;
  parameter Real initY_km = 0;
  parameter Real initZ_km = 1.0 "Initial altitude in km";
  parameter Real tauDirection_s = 2.0 "s, first-order response to direction commands";
  parameter Real thrustToSpeedGain = 4.0 "m/s per kN of thrust converted to forward speed";
  parameter Real climbBleedFraction = 0.35 "Fractional speed loss at straight-up climb";
  parameter Real minAirspeed_mps = 50 "Lower bound on indicated airspeed";
  parameter Real referenceEnergySpeed_mps = 300 "Speed used to normalize energy_state_norm";

  input GI.SurfaceActuationCommand actuation_command "Unused at the moment, verify function before implementing";
  input GI.OrientationEuler direction_command "Direct steering command from mission computer";
  input GI.LiftState lift;
  input GI.ThrustState thrust_in;

  output GI.OrientationEuler orientation;
  output GI.PositionXYZ location;
  output GI.FlightStatusPacket flight_status;

protected 

  // Target absolute Euler angles
  Real target_roll_deg(start=0);
  Real target_pitch_deg(start=0);
  Real target_yaw_deg(start=0);

  // Actual aircraft (continuous states)
  Real roll_deg(start=0);
  Real pitch_deg(start=0);
  Real yaw_deg(start=0);

  Real heading_rad;
  Real pitch_heading_rad;
  Real climb_rate;
  Real ground_speed_ms;
  Real base_speed_ms;
  Real ground_speed_unclamped_ms;

equation

  // Copy current offsets into discrete vars
  target_roll_deg  = roll_deg + direction_command.roll_deg;
  target_pitch_deg = pitch_deg + direction_command.pitch_deg;
  target_yaw_deg   = yaw_deg + direction_command.yaw_deg;

  // First-order response toward the target attitude
  der(roll_deg)  = (target_roll_deg  - roll_deg)  / tauDirection_s;
  der(pitch_deg) = (target_pitch_deg - pitch_deg) / tauDirection_s;
  der(yaw_deg)   = (target_yaw_deg   - yaw_deg)   / tauDirection_s;

  // Orientation/telemetry outputs follow the current attitude
  orientation.roll_deg  = roll_deg;
  orientation.pitch_deg = pitch_deg;
  orientation.yaw_deg   = yaw_deg;

  // Simple kinematics
  heading_rad  = yaw_deg * Modelica.Constants.pi / 180;
  pitch_heading_rad = pitch_deg * Modelica.Constants.pi / 180;

  base_speed_ms = max(minAirspeed_mps,
                      thrust_in.thrust_kn * thrustToSpeedGain);
  ground_speed_unclamped_ms = base_speed_ms *
                              max(0.5,
                                  1 - climbBleedFraction * max(0, sin(pitch_heading_rad)));
  ground_speed_ms = max(minAirspeed_mps, ground_speed_unclamped_ms);

  climb_rate = ground_speed_ms * sin(pitch_heading_rad);

  der(location.x_km) = (ground_speed_ms * cos(heading_rad)) / 1000.0;
  der(location.y_km) = (ground_speed_ms * sin(heading_rad)) / 1000.0;
  der(location.z_km) = climb_rate / 1000.0;

  // Flight status
  flight_status.airspeed_mps        = ground_speed_ms;
  flight_status.energy_state_norm   = max(0,
                                          min(1,
                                              0.5 * (thrust_in.thrust_kn / 130)
                                              + 0.5 * (ground_speed_ms / referenceEnergySpeed_mps)));
  flight_status.angle_of_attack_deg = orientation.pitch_deg;
  flight_status.health_code         = 0;
  flight_status.climb_rate         = climb_rate;


initial equation
  location.x_km = initX_km;
  location.y_km = initY_km;
  location.z_km = initZ_km;
end Environment;
