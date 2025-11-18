within Aircraft;
model Environment
  import GI = Aircraft.GeneratedInterfaces;
  parameter Real initX_km = 0;
  parameter Real initY_km = 0;
  parameter Real initZ_km = 1.0 "Initial altitude in km";
  input GI.SurfaceActuationCommand actuation_command;
  input GI.LiftState lift;
  input GI.ThrustState thrust_in;
  output GI.OrientationEuler orientation;
  output GI.PositionXYZ location;
  output GI.FlightStatusPacket flight_status;
protected
  Real heading_deg(start=0);
  Real heading_rad;
  Real ground_speed;
  Real climb_rate;
  Real geoScale = 1; // km base frame
equation
  heading_rad = heading_deg * 3.14159265358979 / 180;
  heading_deg = actuation_command.rudder_deg;
  ground_speed = max(50, 0.5 * thrust_in.thrust_kn + 150);
  climb_rate = lift.lift_kn; // simplistic climb proxy

  // Orientation/telemetry outputs
  orientation.roll_deg = actuation_command.left_aileron_deg - actuation_command.right_aileron_deg;
  orientation.pitch_deg = actuation_command.elevator_deg / 2;
  orientation.yaw_deg = heading_deg + actuation_command.rudder_deg;

  location.x_km = initX_km + (ground_speed * cos(heading_rad) * time) / 1000.0;
  location.y_km = initY_km + (ground_speed * sin(heading_rad) * time) / 1000.0;
  location.z_km = initZ_km + (climb_rate * time) / 1000.0;

  flight_status.airspeed_mps = ground_speed;
  flight_status.energy_state_norm = max(0, min(1, thrust_in.thrust_kn / 130));
  flight_status.angle_of_attack_deg = orientation.pitch_deg;
  flight_status.health_code = 0;
initial equation
  location.x_km = initX_km;
  location.y_km = initY_km;
  location.z_km = initZ_km;
end Environment;
