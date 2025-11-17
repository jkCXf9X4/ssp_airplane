package Aircraft {
  doc /* Reconfigured to model an F-16 Fighting Falcon multirole fighter with single-engine propulsion and manned cockpit. */

  part def CompositeAirframe {
    doc /* F-16 aluminum/composite fuselage sized for high-supersonic operations with dorsal spine for avionics. */
    attribute length_m = 15.0;
    attribute fuselage_width_m = 3.0;
    attribute wingspan_m = 10.0;
    attribute empty_weight_kg = 8573;
    attribute payload_capacity_kg = 7700;
    attribute hardpoint_count = 9;

    doc /* Structural attachment interface feeding stores racks and pylons. */
    out port storesMounts : StructuralInterface;
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

    doc /* Autopilot command bundle using same HOTAS signal structure. */
    in port autopilotInput : PilotCommand;

    doc /* Mission status feedback from autopilot waypoint driver. */
    in port autopilotStatus : MissionStatus;

    doc /* Autopilot/autonomy guidance cue input. */
    in port autonomyPort : AutonomyGuidance;

    doc /* Pitot-static/INS fused air-data ingress for flight-control laws. */
    in port airDataIn : AirDataInertialState;

    doc /* Fuel telemetry used for command blending and power limiting. */
    in port fuelStatus : FuelLevelState;

    doc /* Electrical inlet powering the mission computer. */
    in port powerIn : GenericElectricalBus;

    doc /* Redundant emergency-bus feed for backup avionics power. */
    in port backupPower : GenericElectricalBus;

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

    doc /* Mission-computer stores control broadcast to SMS. */
    out port storesCommand : StoresCommandBus;

    doc /* Stores health/status feedback for fire-control logic. */
    in port storesStatus : StoresStatusBus;

    doc /* Structural envelope monitoring input to gate commands. */
    in port performanceStatus : StructuralPerformanceState;
  }

  part def AutopilotModule {
    doc /* F-16 autopilot providing hold modes (attitude, altitude, heading) with auto-throttle coordination. */
    attribute autonomy_mode_default = "altitude-hold";
    attribute guidance_modes = "att_hold+hdg_hold+auto_throttle";
    attribute update_rate_hz = 40;

    doc /* Mission-computer flight status back into autopilot. */
    in port feedbackBus : FlightStatusPacket;

    doc /* Current geodetic position from mission computer. */
    in port currentLocation : GeodeticLLA;

    doc /* Current attitude from mission computer. */
    in port currentOrientation : OrientationEuler;

    doc /* Air-data/INS feed for hold modes and envelope limits. */
    in port airDataIn : AirDataInertialState;

    doc /* Structural envelope monitoring input to gate holds. */
    in port performanceStatus : StructuralPerformanceState;

    doc /* Electrical supply for autopilot electronics. */
    in port powerIn : GenericElectricalBus;

    doc /* Backup/emergency electrical bus input. */
    in port backupPower : GenericElectricalBus;

    doc /* Autopilot guidance directives to mission computer. */
    out port guidanceCmd : AutonomyGuidance;

    doc /* HOTAS-equivalent command stream for mission computer blending. */
    out port autopilotCmd : PilotCommand;

    doc /* Tracking of waypoint progress for mission supervision. */
    out port missionStatus : MissionStatus;

  }

  part def PowerSystem {
    doc /* F-16 270 VDC / 115 VAC hybrid electrical system for avionics, flight control, and weapon systems. */
    attribute bus_voltage_kv = 0.27;
    attribute battery_capacity_mj = 650;
    attribute generator_efficiency = 0.95;
    attribute ac_bus_voltage_kv = 0.115;
    attribute converter_rating_kw = 40;
    attribute epu_type = "hydrazine-turbine";

    doc /* Generator output feed captured as structured electrical telemetry. */
    in port generatorInput : GenericElectricalBus;

    doc /* Conditioned electrical feed powering avionics and mission computer. */
    out port avionicsFeed : GenericElectricalBus;

    doc /* 270 VDC main distribution bus for avionics and flight controls. */
    out port dcBus270 : GenericElectricalBus;

    doc /* 115 VAC transformer bus for legacy/control loads. */
    out port acBus115 : GenericElectricalBus;

    doc /* Regulated bus powering control interface and actuator electronics. */
    out port controlFeed : GenericElectricalBus;

    doc /* Dedicated supply for autonomy/autopilot compute payloads. */
    out port autonomyFeed : GenericElectricalBus;

    doc /* Isolated distribution path for stores management electronics and pylons. */
    out port storesFeed : GenericElectricalBus;

    doc /* Emergency-power-unit backfeed input. */
    in port emergencyInput : GenericElectricalBus;

    doc /* Routed emergency bus for redundant avionics/autopilot feeds. */
    out port emergencyBus : GenericElectricalBus;

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

  part def FlyByWireController {
    doc /* Triple-redundant fly-by-wire computers that stabilize the relaxed-static-stability F-16 airframe. */
    attribute redundant_channels = 3;
    attribute control_law = "CCV+gain-scheduled";
    attribute update_rate_hz = 200;
    attribute stability_margin_deg = 15;

    doc /* Mission-computer command bus input. */
    in port commandBus : SurfaceActuationCommand;

    doc /* High-rate flight status feedback for gain scheduling. */
    in port flightFeedback : FlightStatusPacket;

    doc /* Direct aerodynamic feedback from wing solver for structural damping. */
    in port aeroFeedback : LiftState;

    doc /* Conditioned electrical feed for actuator drive computers. */
    in port powerIn : GenericElectricalBus;

    doc /* Filtered actuator drive outputs dispatched to wing/tail surfaces. */
    out port actuatorDrive : SurfaceActuationCommand;
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

  part def AirDataAndInertialSuite {
    doc /* Triple redundant ADC, INS, and GPS sensors providing Mach/attitude states. */
    attribute pitot_count = 3;
    attribute ins_grade = "ring-laser";
    attribute update_rate_hz = 200;

    doc /* Avionics-bus power input for sensors and air-data computers. */
    in port powerIn : GenericElectricalBus;

    doc /* Air-data and inertial solution output shared with consumers. */
    out port airDataOut : AirDataInertialState;
  }

  part def EmergencyPowerUnit {
    doc /* Hydrazine-driven emergency power unit sustaining avionics/control loads after generator loss. */
    attribute duration_minutes = 10;
    attribute generator_output_kw = 25;
    attribute fuel_type = "hydrazine";

    doc /* Shared fuel telemetry for EPU reactant state tracking. */
    in port fuelState : FuelLevelState;

    doc /* Emergency electrical bus output. */
    out port emergencyOutput : GenericElectricalBus;
  }

  part def StructuralLoadsAndPerformanceMonitor {
    doc /* Calculates Mach/g loads to enforce structural and store-release envelopes. */
    attribute max_load_factor_g = 9;
    attribute max_mach = 2.0;
    attribute release_inhibit_g = 5.5;

    doc /* Aerodynamic loads from wing solver. */
    in port liftIn : LiftState;

    doc /* Propulsion thrust telemetry for acceleration estimation. */
    in port thrustIn : ThrustState;

    doc /* Air-data/INS solution for Mach and attitude context. */
    in port airDataIn : AirDataInertialState;

    doc /* Structural/performance envelope telemetry exported to consumers. */
    out port performanceStatus : StructuralPerformanceState;
  }

  part def StoresManagementSystem {
    doc /* Nine-station stores management system coordinating pylons, weapon power, and release logic. */
    attribute total_station_count = 9;
    attribute data_bus_type = "MIL-STD-1553/1760 hybrid";
    attribute cooling_capacity_kw = 12;
    attribute emergency_release_mode = "Selective+Jettison";

    doc /* Mission-computer command ingress for weapon selection, master arm, and payload profiles. */
    in port storesBusIn : StoresCommandBus;

    doc /* Stores readiness, mass properties, and fault codes exported to mission computer. */
    out port storesTelemetry : StoresStatusBus;

    doc /* Primary power feed for ejector racks, weapon heaters, and bus controllers. */
    in port powerIn : GenericElectricalBus;

    doc /* Structural interface tying the rack to the fuselage/wing airframe. */
    in port airframeMount : StructuralInterface;

    doc /* Structural envelope status to inhibit unsafe releases. */
    in port performanceStatus : StructuralPerformanceState;

  }

}
