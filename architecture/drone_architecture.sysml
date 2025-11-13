package WingmanDrone {
  doc /* Loyal-wingman autonomous drone modeled after MQ-28 and Hellsing CA-1 Europa with conventional aviation propulsion. */
  attribute system_name = "DroneSystem";

  part def WingmanDrone {
    doc /* Mission-configurable air vehicle coordinating with crewed fighters or remote operators. */
    attribute autonomy_mode_default = "loyal-wingman";
    attribute design_range_km = 3700;
    attribute crew_capacity = 0;

    part airframe: CompositeAirframe;
    part wings: AdaptiveWingSystem;
    part propulsion: TurbofanPropulsion;
    part missionComputer: MissionComputer;
    part autopilot: AutopilotModule;
    part power: PowerSystem;
    part fuel: FuelSystem;
    part controls: ControlInterface;
  }

  part def CompositeAirframe {
    doc /* Composite fuselage and payload bay sized to MQ-28 proportions. */
    attribute length_m = 11.7;
    attribute fuselage_width_m = 1.9;
    attribute payload_capacity_kg = 1500;
    attribute hardpoint_count = 4;

  }

  part def AdaptiveWingSystem {
    doc /* High-efficiency wing with control surfaces for agile escort missions. */
    attribute reference_area_m2 = 28;
    attribute span_m = 7.3;
    attribute aspect_ratio = 5.5;
    attribute control_authority_deg = 35;

    doc /* Mission computer bus commanding surface deflections per axis. */
    in controlSurfaces : SurfaceActuationCommand;


    doc /* Aerodynamic load feedback returned to mission computer/autopilot. */
    out liftInterface : LiftState;
  }

  part def TurbofanPropulsion {
    doc /* Conventional turbofan sized for MQ-28-class thrust with onboard generator. */
    attribute max_thrust_kn = 60;
    attribute specific_fuel_consumption = 0.8;
    attribute fuel_capacity_kg = 2000;
    attribute generator_output_kw = 150;

    doc /* Mission computer throttle command input. */
    in throttleCmd : ThrottleCommand;

    doc /* Fuel availability feedback for derating logic. */
    in fuelStatus : FuelLevelState;


    doc /* Propulsion thrust telemetry exported to airframe. */
    out thrustOut : ThrustState;

    doc /* Requested fuel mass-flow shared with storage system. */
    out fuelFlow : FuelConsumptionRate;

    doc /* Electrical bus output feeding vehicle power distribution. */
    out powerBus : GenericElectricalBus;
  }

  part def MissionComputer {
    doc /* Tactical mission computer blending pilot-style inputs with autonomy services. */
    attribute compute_budget_tops = 20;
    attribute tactical_ai_level = 4;
    attribute networked_control_buses = 3;

    doc /* Manual HOTAS command bundle from control interface. */
    in manualInput : PilotCommand;

    doc /* Autopilot/autonomy guidance cue input. */
    in autonomyPort : AutonomyGuidance;

    doc /* Fuel telemetry used for command blending and power limiting. */
    in fuelStatus : FuelLevelState;

    doc /* Electrical inlet powering the mission computer. */
    in powerIn : GenericElectricalBus;


    doc /* Structured throttle/fuel enable command to propulsion. */
    out engineThrottle : ThrottleCommand;

    doc /* Control-surface commands broadcast toward actuators. */
    out surfaceBus : SurfaceActuationCommand;

    doc /* Summary of vehicle energy/health for upstream consumers. */
    out flightStatus : FlightStatusPacket;

    doc /* Body attitude exported as roll/pitch/yaw Euler angles in degrees. */
    out orientationEuler : OrientationEuler;

    doc /* Geodetic latitude/longitude/altitude update for mission/autonomy. */
    out locationLLA : GeodeticLLA;

  }

  part def AutopilotModule {
    doc /* Guidance core to execute escort, loiter, and waypoint scripts. */
    attribute guidance_modes = "escort+loiter+return";
    attribute update_rate_hz = 25;

    doc /* Mission-computer flight status back into autopilot. */
    in feedbackBus : FlightStatusPacket;

    doc /* Electrical supply for autopilot electronics. */
    in powerIn : GenericElectricalBus;


    doc /* Autopilot guidance directives to mission computer. */
    out guidanceCmd : AutonomyGuidance;

  }

  part def PowerSystem {
    doc /* Hybrid battery and generator bus distributing electrical power to avionics and control interfaces. */
    attribute bus_voltage_kv = 1.2;
    attribute battery_capacity_mj = 500;
    attribute generator_efficiency = 0.92;

    doc /* Generator output feed captured as structured electrical telemetry. */
    in generatorInput : GenericElectricalBus;

    doc /* Conditioned electrical feed powering avionics and mission computer. */
    out avionicsFeed : GenericElectricalBus;

    doc /* Regulated bus powering control interface and actuator electronics. */
    out controlFeed : GenericElectricalBus;

    doc /* Dedicated supply for autonomy/autopilot compute payloads. */
    out autonomyFeed : GenericElectricalBus;

  }

  part def FuelSystem {
    doc /* Fuel storage and management subsystem feeding the turbofan and publishing remaining range. */
    attribute fuel_capacity_kg = 2000;
    attribute reserve_fraction = 0.05;

    doc /* Propulsion-requested fuel mass flow entering storage manager. */
    in fuelFlowIn : FuelConsumptionRate;

    doc /* Telemetry describing remaining fuel mass/normalized level. */
    out fuelState : FuelLevelState;
  }

  part def ControlInterface {
    doc /* HOTAS or gamepad style interface for remote pilots or simulator inputs. */
    attribute input_scheme = "HOTAS/Gamepad";
    attribute telemetry_rate_hz = 60;

    doc /* General power */
    in powerIn : GenericElectricalBus;

    doc /* HOTAS-control bundle forwarded for mission computer sensor fusion. */
    out PilotCommand : PilotCommand;

  }

}
