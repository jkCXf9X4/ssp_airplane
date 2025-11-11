package WingmanDrone {
  doc /* Loyal-wingman autonomous drone modeled after MQ-28 and Hellsing CA-1 Europa with conventional aviation propulsion. */
  attribute system_name = "WingmanDrone";
  attribute author = "Codex Agent";
  attribute language = "SysML v2";

  comment Requirement_REQ_Profile /* Maintain MQ-28 class geometry (~11.7 m length, 7.3 m wingspan) for loyal wingman compatibility. */
  comment Requirement_REQ_Propulsion /* Use conventional turbofan propulsion with aviation fuel. */
  comment Requirement_REQ_Control /* Expose pilot-style inputs (stick, throttle, mode select) while keeping autopilot authority in the loop. */
  comment Requirement_REQ_Mission /* Support range, loiter, and escort scenario optimization for collaborative missions. */

  data def PilotCommandOut {
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

  data def OrientationEuler {
    doc /* Air vehicle orientation expressed as body-to-earth Euler angles in degrees. */
    attribute roll_deg: Real;
    attribute pitch_deg: Real;
    attribute yaw_deg: Real;
  }

  data def GeodeticLLA {
    doc /* Geodetic latitude/longitude (degrees) and altitude (meters) above mean sea level. */
    attribute latitude_deg: Real;
    attribute longitude_deg: Real;
    attribute altitude_m: Real;
  }

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
    part controls: ControlInterface;
  }

  part def CompositeAirframe {
    doc /* Composite fuselage and payload bay sized to MQ-28 proportions. */
    attribute length_m = 11.7;
    attribute fuselage_width_m = 1.9;
    attribute payload_capacity_kg = 1500;
    attribute hardpoint_count = 4;

    port structuralMount {
      attribute kind = "structural";
      attribute direction = "bi";
    }
    port engineMount {
      attribute kind = "structural";
      attribute direction = "bi";
    }
    port avionicsBay {
      attribute kind = "data";
      attribute direction = "bi";
    }
  }

  part def AdaptiveWingSystem {
    doc /* High-efficiency wing with control surfaces for agile escort missions. */
    attribute reference_area_m2 = 28;
    attribute span_m = 7.3;
    attribute aspect_ratio = 5.5;
    attribute control_authority_deg = 35;

    port structuralMount {
      attribute kind = "structural";
      attribute direction = "bi";
    }
    port controlSurfaces {
      attribute kind = "data";
      attribute direction = "in";
    }
    port liftInterface {
      attribute kind = "aerodynamic";
      attribute direction = "out";
    }
  }

  part def TurbofanPropulsion {
    doc /* Conventional turbofan sized for MQ-28-class thrust with onboard generator. */
    attribute max_thrust_kn = 60;
    attribute specific_fuel_consumption = 0.8;
    attribute fuel_capacity_kg = 2000;
    attribute generator_output_kw = 150;

    in port throttleCmd {
      attribute kind = "data";
      attribute direction = "in";
    }
    out port thrustOut {
      attribute kind = "mechanical";
      attribute direction = "out";
    }
    out port powerBus {
      attribute kind = "electrical";
      attribute direction = "out";
    }
    port mountingHardpoint {
      attribute kind = "structural";
      attribute direction = "bi";
    }
  }

  part def MissionComputer {
    doc /* Tactical mission computer blending pilot-style inputs with autonomy services. */
    attribute compute_budget_tops = 20;
    attribute tactical_ai_level = 4;
    attribute networked_control_buses = 3;

    in port manualInput {
      attribute type = PilotCommandOut;
      attribute kind = "data";
      attribute direction = "in";
    }
    in port autonomyPort {
      attribute kind = "data";
      attribute direction = "in";
    }
    out port engineThrottle {
      attribute kind = "data";
      attribute direction = "out";
    }
    out port surfaceBus {
      attribute kind = "data";
      attribute direction = "out";
    }
    out port flightStatus {
      attribute kind = "data";
      attribute direction = "out";
    }
    out port orientationEuler {
      doc /* Body attitude exported as roll/pitch/yaw Euler angles in degrees. */
      attribute type = OrientationEuler;
      attribute kind = "data";
      attribute direction = "out";
    }
    out port locationLLA {
      doc /* Geodetic latitude, longitude (deg) and altitude (m) for navigation consumers. */
      attribute type = GeodeticLLA;
      attribute kind = "data";
      attribute direction = "out";
    }
    in port powerIn {
      attribute kind = "electrical";
      attribute direction = "in";
    }
  }

  part def AutopilotModule {
    doc /* Guidance core to execute escort, loiter, and waypoint scripts. */
    attribute guidance_modes = "escort+loiter+return";
    attribute update_rate_hz = 25;

    out port guidanceCmd {
      attribute kind = "data";
      attribute direction = "out";
    }
    in port feedbackBus {
      attribute kind = "data";
      attribute direction = "in";
    }
    in port powerIn {
      attribute kind = "electrical";
      attribute direction = "in";
    }
  }

  part def PowerSystem {
    doc /* Hybrid battery and generator bus distributing electrical power to avionics and control interfaces. */
    attribute bus_voltage_kv = 1.2;
    attribute battery_capacity_mj = 500;
    attribute generator_efficiency = 0.92;

    in port generatorInput {
      attribute kind = "electrical";
      attribute direction = "in";
    }
    out port avionicsFeed {
      attribute kind = "electrical";
      attribute direction = "out";
    }
    out port controlFeed {
      attribute kind = "electrical";
      attribute direction = "out";
    }
    out port autonomyFeed {
      attribute kind = "electrical";
      attribute direction = "out";
    }
  }

  part def ControlInterface {
    doc /* HOTAS or gamepad style interface for remote pilots or simulator inputs. */
    attribute input_scheme = "HOTAS/Gamepad";
    attribute telemetry_rate_hz = 60;

    out port pilotCommandOut {
      doc /* HOTAS-style control bundle typed as PilotCommandOut for downstream consumers. */
      attribute type = PilotCommandOut;
      attribute kind = "data";
      attribute direction = "out";
    }
    in port powerIn {
      attribute kind = "electrical";
      attribute direction = "in";
    }
  }

  part def AnalysisParameters {
    doc /* Scenario planning targets and optimization bounds. */
    attribute cruise_speed_mps = 250;
    attribute design_payload_kg = 1200;
    attribute target_range_km = 3700;
    attribute loiter_time_minutes = 80;

    part optimization: OptimizationSettings;
  }

  part def OptimizationSettings {
    doc /* Tunable variables for range and scenario trade studies. */
    part wing_area_scale: VariableRange {
      attribute min = 0.85;
      attribute max = 1.15;
    }
    part engine_thrust_scale: VariableRange {
      attribute min = 0.8;
      attribute max = 1.2;
    }
    part payload_scale: VariableRange {
      attribute min = 0.5;
      attribute max = 1.3;
    }
  }

  part def VariableRange {
    attribute min = 0.0;
    attribute max = 0.0;
  }

  connect AdaptiveWingSystem.structuralMount to CompositeAirframe.structuralMount;
  connect TurbofanPropulsion.mountingHardpoint to CompositeAirframe.engineMount;
  connect TurbofanPropulsion.powerBus to PowerSystem.generatorInput;
  connect PowerSystem.avionicsFeed to MissionComputer.powerIn;
  connect PowerSystem.controlFeed to ControlInterface.powerIn;
  connect PowerSystem.autonomyFeed to AutopilotModule.powerIn;
  connect MissionComputer.surfaceBus to AdaptiveWingSystem.controlSurfaces;
  connect MissionComputer.engineThrottle to TurbofanPropulsion.throttleCmd;
  connect AutopilotModule.guidanceCmd to MissionComputer.autonomyPort;
  connect MissionComputer.flightStatus to AutopilotModule.feedbackBus;
  connect ControlInterface.pilotCommandOut to MissionComputer.manualInput;
}
