package Aircraft {
  doc /* Reconfigured to model an F-16 Fighting Falcon multirole fighter with single-engine propulsion and manned cockpit. *


  part def ControlInterface {
    doc /* F-16 HOTAS + side-stick interface for pilot inputs and trim switches. */
    attribute input_scheme = "HOTAS";
    attribute telemetry_rate_hz = 120;
  
    doc /* HOTAS-control bundle forwarded for mission computer sensor fusion. */
    out port pilotCommand : PilotCommand;

  }

  part def AutopilotModule {
    doc /* F-16 autopilot, takes in sensor data and translates it into a equivalent hotas command. */
    attribute comment = "uses waypoint tracking";

    doc /* Mission-computer flight status back into autopilot. */
    in port feedbackBus : FlightStatusPacket;

    doc /* Current local position from sensors */
    in port currentLocation : PositionXYZ;

    doc /* Current attitude from sensors. */
    in port currentOrientation : OrientationEuler;

    doc /* HOTAS-equivalent command stream for mission computer blending. */
    out port autopilotCmd : PilotCommand;

    doc /* Waypoint progression for logging and verification. */
    out port missionStatus : MissionStatus;
  }

  part def CompositeAirframe {
    doc /* F-16 aluminum/composite fuselage sized for high-supersonic operations with dorsal spine for avionics. */
    attribute length_m = 15.0;
    attribute fuselage_width_m = 3.0;
    attribute wingspan_m = 10.0;
    attribute empty_weight_kg = 8573;
    attribute payload_capacity_kg = 7700;
    attribute hardpoint_count = 9;

  }


  part def TurbofanPropulsion {
    doc /* Pratt & Whitney F100 / GE F110 class augmented turbofan powering the F-16. */
    attribute max_thrust_kn = 129.7;
    attribute dry_thrust_kn = 79.0;
    attribute specific_fuel_consumption = 0.76;
    attribute fuel_capacity_kg = 3160;
    attribute generator_output_kw = 80;

    doc /* Mission computer throttle + afterburner command input. */
    in port throttleCmd : ThrottleCommand;

    doc /* Propulsion thrust telemetry exported to airframe. */
    out port thrustOut : ThrustState;

    doc /* Mass flow telemetry  */
    out port fuel_consumption : FuelConsumptionRate;
  }

  part def MissionComputer {
    doc /* F-16C/D mission computer blending pilot HOTAS inputs with fly-by-wire control laws and stores management. */

    doc /* Manual HOTAS command bundle from cockpit controls. */
    in port manualInput : PilotCommand;

    doc /* Autopilot command bundle using same HOTAS signal structure. */
    in port autopilotInput : PilotCommand;

    doc /* Fuel telemetry used for command blending and power limiting. */
    in port fuelStatus : FuelLevelState;

    doc /* Structured throttle/fuel enable command to propulsion. */
    out port engineThrottle : ThrottleCommand;

    doc /* Command how to alter the current velocity vector, pith, yaw, roll  */
    out port direction_command : OrientationEuler;
  }


  part def FuelSystem {
    doc /* Internal + conformal fuel storage management with transfer pumps feeding engine feed tanks. */
    attribute fuel_capacity_kg = 3160;
    attribute reserve_fraction = 0.08;

    doc /* Propulsion-requested fuel mass flow entering storage manager. */
    in port fuel_consumption_rate : FuelConsumptionRate;

    doc /* Telemetry describing remaining fuel mass/normalized level. */
    out port fuelState : FuelLevelState;
  }

  part def AdaptiveWingSystem {
    doc /* Leading-edge strake and cropped-delta wing sized to F-16 Block 50 geometry with 9g capability. This model includes the control system */
    attribute reference_area_m2 = 28.0;
    attribute span_m = 10.0;
    attribute aspect_ratio = 3.6;
    attribute control_authority_deg = 25;
    attribute load_factor_limit_g = 9;

    doc /* Mission-computer command bus input. Desired change in speed vector */
    in port direction_command : OrientationEuler;

    in port flight_speed : FlightStatusPacket;

    doc /* Actuation commands, sent to environment to track and calculate new position */
    out port actuation_command : SurfaceActuationCommand;

    doc /* Tracking of lift, drag */
    out port liftInterface : LiftState;
  }

  part def Environment {
    doc /* Tracking position and velocities of the aircraft and feeds the sensors */

    doc /* Reads the actuation and thrust commands to calculate the position, rotation and velocities */

    in port actuation_command : SurfaceActuationCommand;
    in port direction_command : OrientationEuler;
    in port lift : LiftState;
    in port thrust_in : ThrustState;

    doc /* Feedback for simulated sensors */
    out port orientation : OrientationEuler;
    out port location : PositionXYZ;
    out port flight_status : FlightStatusPacket;

  }

  part def InputOutput {
    doc /* Simulation sink for debugging and recording mission/autopilot telemetry. */
    in port locationXYZ : PositionXYZ;
    in port orientation : OrientationEuler;
    in port autopilotCmd : PilotCommand;
    in port flightStatus : FlightStatusPacket;
    in port missionStatus : MissionStatus;
  }

}
