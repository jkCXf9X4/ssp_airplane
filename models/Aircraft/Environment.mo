within Aircraft;
model Environment
  import GI = Aircraft.GeneratedInterfaces;
  parameter Real initLatitude_deg = 0;
  parameter Real initLongitude_deg = 0;
  input GI.SurfaceActuationCommand actuation_command;
  input GI.LiftState lift;
  input GI.ThrustState thrust_in;
  output GI.OrientationEuler orientation;
  output GI.GeodeticLLA location;
  output GI.FlightStatusPacket flight_status;
protected
  Real heading_deg(start=0);
  Real heading_rad;
  Real ground_speed;
  Real climb_rate;
  Real geoScale = 111000;
equation
  heading_rad = heading_deg * 3.14159265358979 / 180;
  heading_deg = actuation_command.rudder_deg;
  ground_speed = max(50, 0.5 * thrust_in.thrust_kn + 150);
  climb_rate = lift.lift_kn; // simplistic climb proxy

  // Orientation/telemetry outputs
  orientation.roll_deg = actuation_command.left_aileron_deg - actuation_command.right_aileron_deg;
  orientation.pitch_deg = actuation_command.elevator_deg / 2;
  orientation.yaw_deg = heading_deg + actuation_command.rudder_deg;

  location.latitude_deg = initLatitude_deg + (ground_speed * cos(heading_rad) * time) / geoScale;
  location.longitude_deg = initLongitude_deg + (ground_speed * sin(heading_rad) * time) / (geoScale * max(1e-3, cos(initLatitude_deg * 3.14159265358979 / 180)));
  location.altitude_m = 1000 + climb_rate * time;

  flight_status.airspeed_mps = ground_speed;
  flight_status.energy_state_norm = max(0, min(1, thrust_in.thrust_kn / 130));
  flight_status.angle_of_attack_deg = orientation.pitch_deg;
  flight_status.health_code = 0;
initial equation
  location.latitude_deg = initLatitude_deg;
  location.longitude_deg = initLongitude_deg;
  location.altitude_m = 1000;
end Environment;
