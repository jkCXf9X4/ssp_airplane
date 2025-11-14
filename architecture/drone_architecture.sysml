package WingmanDrone {
  doc /* Reconfigured to model an F-16 Fighting Falcon multirole fighter with single-engine propulsion and manned cockpit. */

  part def CompositeAirframe {
    doc /* F-16 aluminum/composite fuselage sized for high-supersonic operations with dorsal spine for avionics. */
    attribute length_m = 15.0;
    attribute fuselage_width_m = 3.0;
    attribute wingspan_m = 10.0;
    attribute empty_weight_kg = 8573;
    attribute payload_capacity_kg = 7700;
    attribute hardpoint_count = 9;
  }

  part def AdaptiveWingSystem {
    doc /* Leading-edge strake and cropped-delta wing sized to F-16 Block 50 geometry with 9g capability. */
    attribute reference_area_m2 = 28.0;
    attribute span_m = 10.0;
    attribute aspect_ratio = 3.6;
    attribute control_authority_deg = 25;
    attribute load_factor_limit_g = 9;

    doc /* Flight-control computer commands for elevator, tailerons, and rudder. */
    in port controlSurfaces : SurfaceActuationCommand;

    doc /* Aerodynamic loads + moments returned to flight-control computers. */
    out port liftInterface : LiftState;
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

    doc /* Fuel availability feedback for power scheduling and afterburner inhibit. */
    in port fuelStatus : FuelLevelState;


    doc /* Propulsion thrust telemetry exported to airframe. */
    out port thrustOut : ThrustState;

    doc /* Requested fuel mass-flow shared with storage system. */
    out port fuelFlow : FuelConsumptionRate;

    doc /* Electrical bus output feeding vehicle power distribution. */
    out port powerBus : GenericElectricalBus;
  }

  part def MissionComputer {
    doc /* F-16C/D mission computer blending pilot HOTAS inputs with fly-by-wire control laws and stores management. */
    attribute compute_budget_tops = 35;
    attribute digital_fly_by_wire_channels = 3;
    attribute stores_management_buses = 2;

    doc /* Manual HOTAS command bundle from cockpit controls. */
    in port manualInput : PilotCommand;

    doc /* Autopilot/autonomy guidance cue input. */
    in port autonomyPort : AutonomyGuidance;

    doc /* Fuel telemetry used for command blending and power limiting. */
    in port fuelStatus : FuelLevelState;

    doc /* Electrical inlet powering the mission computer. */
    in port powerIn : GenericElectricalBus;


    doc /* Structured throttle/fuel enable command to propulsion. */
    out port engineThrottle : ThrottleCommand;

    doc /* Control-surface commands broadcast toward actuators. */
    out port surfaceBus : SurfaceActuationCommand;

    doc /* Summary of vehicle energy/health for upstream consumers. */
    out port flightStatus : FlightStatusPacket;

    doc /* Body attitude exported as roll/pitch/yaw Euler angles in degrees. */
    out port orientationEuler : OrientationEuler;

    doc /* Geodetic latitude/longitude/altitude update for mission/autonomy. */
    out port locationLLA : GeodeticLLA;

  }

  part def AutopilotModule {
    doc /* F-16 autopilot providing hold modes (attitude, altitude, heading) with auto-throttle coordination. */
    attribute autonomy_mode_default = "altitude-hold";
    attribute guidance_modes = "att_hold+hdg_hold+auto_throttle";
    attribute update_rate_hz = 40;

    doc /* Mission-computer flight status back into autopilot. */
    in port feedbackBus : FlightStatusPacket;

    doc /* Electrical supply for autopilot electronics. */
    in port powerIn : GenericElectricalBus;


    doc /* Autopilot guidance directives to mission computer. */
    out port guidanceCmd : AutonomyGuidance;

  }

  part def PowerSystem {
    doc /* F-16 270 VDC / 115 VAC hybrid electrical system for avionics, flight control, and weapon systems. */
    attribute bus_voltage_kv = 0.27;
    attribute battery_capacity_mj = 650;
    attribute generator_efficiency = 0.95;

    doc /* Generator output feed captured as structured electrical telemetry. */
    in port generatorInput : GenericElectricalBus;

    doc /* Conditioned electrical feed powering avionics and mission computer. */
    out port avionicsFeed : GenericElectricalBus;

    doc /* Regulated bus powering control interface and actuator electronics. */
    out port controlFeed : GenericElectricalBus;

    doc /* Dedicated supply for autonomy/autopilot compute payloads. */
    out port autonomyFeed : GenericElectricalBus;

  }

  part def FuelSystem {
    doc /* Internal + conformal fuel storage management with transfer pumps feeding engine feed tanks. */
    attribute fuel_capacity_kg = 3160;
    attribute reserve_fraction = 0.08;

    doc /* Propulsion-requested fuel mass flow entering storage manager. */
    in port fuelFlowIn : FuelConsumptionRate;

    doc /* Telemetry describing remaining fuel mass/normalized level. */
    out port fuelState : FuelLevelState;
  }

  part def ControlInterface {
    doc /* F-16 HOTAS + side-stick interface for pilot inputs and trim switches. */
    attribute input_scheme = "HOTAS";
    attribute telemetry_rate_hz = 120;

    doc /* General power */
    in port powerIn : GenericElectricalBus;

    doc /* HOTAS-control bundle forwarded for mission computer sensor fusion. */
    out port pilotCommand : PilotCommand;

  }

}
