within Aircraft;
model AirDataAndInertialSuite
  import GI = Aircraft.GeneratedInterfaces;
  parameter Real updateRateHz = 200;
  parameter Real baselineAltitude_m = 6000;
  input GI.GenericElectricalBus powerIn;
  output GI.AirDataInertialState airDataOut;
protected
  Real sensorQuality;
  Real speedProfile;
  Real altitudeProfile;
equation
  sensorQuality = min(1.0, max(0.3, powerIn.available_power_kw / 20.0));
  speedProfile = (220 + 40 * sin(time / 30)) * sensorQuality;
  altitudeProfile = baselineAltitude_m + 200 * sin(time / 50);

  airDataOut.true_airspeed_mps = speedProfile;
  airDataOut.indicated_airspeed_mps = speedProfile * 0.95;
  airDataOut.mach_number = speedProfile / 340;
  airDataOut.pressure_altitude_m = altitudeProfile;
  airDataOut.vertical_speed_mps = 4 * cos(time / 50);
  airDataOut.angle_of_attack_deg = 5 + 2 * sin(time / 20);
  airDataOut.sideslip_deg = 1.5 * sin(time / 25);
  airDataOut.roll_rate_degps = 2 * sin(time / 15);
  airDataOut.pitch_rate_degps = 1.5 * cos(time / 18);
  airDataOut.yaw_rate_degps = 1.2 * sin(time / 22);
end AirDataAndInertialSuite;
