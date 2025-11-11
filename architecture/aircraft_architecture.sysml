package SSP_Airplane {
  doc /* Nuclear-powered Boeing 737-class aircraft optimized for long range missions. */
  attribute system_name = "SSP_Airplane";
  attribute author = "Codex Agent";
  attribute language = "SysML v2";

  comment Requirement_REQ_Size /* Overall geometry equivalent to Boeing 737-800 (39.5 m length, 35.8 m wingspan). */
  comment Requirement_REQ_Propulsion /* Primary propulsion provided by nuclear reactor powered electric motors. */
  comment Requirement_REQ_Range /* Must fly London to Beijing (~8140 km) without refueling. */
  comment Requirement_REQ_Optimization /* Wing area, motor size, and carrying capacity must be tunable for optimization. */

  part def SSP_Airframe {
    doc /* Top-level aircraft aggregating fuselage, propulsion, control, and electrical subsystems. */
    attribute crew_capacity = 8;
    attribute passenger_capacity = 180;
    attribute design_range_km = 8500;

    part fuselage: Fuselage;
    part reactor: ReactorCore;
    part wings: WingSystem;
    part motors: MotorArray;
    part control_sw: ControlSoftware;
    part autopilot: AutopilotModule;
    part electrical: ElectricalSystem;
  }

  part def Fuselage {
    doc /* Pressurized cabin and payload bay sized for Boeing 737 class missions. */
    attribute length_m = 39.5;
    attribute cabin_diameter_m = 3.76;
    attribute max_payload_kg = 20000;
    attribute empty_mass_kg = 22000;

    port structuralMount {
      attribute kind = "structural";
      attribute direction = "bi";
    }
    port avionicsBus {
      attribute kind = "data";
      attribute direction = "bi";
    }
  }

  part def ReactorCore {
    doc /* Compact molten-salt nuclear reactor driving closed-loop Brayton cycle generator. */
    attribute thermal_power_mw = 80;
    attribute electrical_efficiency = 0.42;
    attribute shielding_mass_kg = 12000;
    attribute fuel_endurance_hr = 20;

    port thermalOutput {
      attribute kind = "thermal";
      attribute direction = "out";
    }
    port powerBus {
      attribute kind = "electrical";
      attribute direction = "out";
    }
    port coolantLoop {
      attribute kind = "fluid";
      attribute direction = "bi";
    }
  }

  part def WingSystem {
    doc /* High aspect ratio wings providing lift and fuel pod integration. */
    attribute reference_area_m2 = 134;
    attribute span_m = 35.8;
    attribute aspect_ratio = 9.6;
    attribute structural_mass_kg = 12000;

    port liftInterface {
      attribute kind = "aerodynamic";
      attribute direction = "out";
    }
    port structuralMount {
      attribute kind = "structural";
      attribute direction = "bi";
    }
    port controlSurfaces {
      attribute kind = "data";
      attribute direction = "in";
    }
  }

  part def MotorArray {
    doc /* Electrically driven ducted fans translating electrical power into thrust. */
    attribute count = 4;
    attribute thrust_per_motor_kn = 120;
    attribute motor_efficiency = 0.9;
    attribute specific_mass_kg_per_kw = 0.8;

    in port electricalInput {
      attribute kind = "electrical";
      attribute direction = "in";
    }
    out port thrustOut {
      attribute kind = "mechanical";
      attribute direction = "out";
    }
    in port throttleCmd {
      attribute kind = "data";
      attribute direction = "in";
    }
  }

  part def ControlSoftware {
    doc /* Flight control computers managing actuators and propulsion. */
    attribute compute_budget_tops = 30;
    attribute redundancy_level = 3;

    out port actuatorBus {
      attribute kind = "data";
      attribute direction = "out";
    }
    in port telemetryIn {
      attribute kind = "data";
      attribute direction = "in";
    }
    out port throttleOut {
      attribute kind = "data";
      attribute direction = "out";
    }
    port autopilotLink {
      attribute kind = "data";
      attribute direction = "bi";
    }
  }

  part def AutopilotModule {
    doc /* Mission-level guidance autopilot optimizing for range and safety. */
    attribute sensor_suite = "INS+GNSS+WeatherRadar";
    attribute update_rate_hz = 20;

    out port guidanceCmd {
      attribute kind = "data";
      attribute direction = "out";
    }
    port controlBus {
      attribute kind = "data";
      attribute direction = "bi";
    }
  }

  part def ElectricalSystem {
    doc /* Power conditioning, storage, and distribution network. */
    attribute bus_voltage_kv = 5;
    attribute buffer_capacity_mj = 800;
    attribute distribution_efficiency = 0.96;

    port primaryBus {
      attribute kind = "electrical";
      attribute direction = "bi";
    }
    out port avionicsFeed {
      attribute kind = "electrical";
      attribute direction = "out";
    }
    in port reactorInput {
      attribute kind = "electrical";
      attribute direction = "in";
    }
    out port motorFeed {
      attribute kind = "electrical";
      attribute direction = "out";
    }
    out port controlFeed {
      attribute kind = "electrical";
      attribute direction = "out";
    }
  }

  part def AnalysisParameters {
    doc /* Design targets and optimization bounds used for high-level analysis. */
    attribute cruise_speed_mps = 230;
    attribute design_payload_kg = 20000;
    attribute target_range_km = 8500;

    part optimization: OptimizationSettings;
  }

  part def OptimizationSettings {
    doc /* Tunable variables for range optimization. */
    part wing_area_scale: VariableRange {
      attribute min = 0.8;
      attribute max = 1.2;
    }
    part motor_power_scale: VariableRange {
      attribute min = 0.7;
      attribute max = 1.3;
    }
    part payload_scale: VariableRange {
      attribute min = 0.6;
      attribute max = 1.1;
    }
  }

  part def VariableRange {
    attribute min = 0.0;
    attribute max = 0.0;
  }

  connect ReactorCore.powerBus to ElectricalSystem.reactorInput;
  connect ElectricalSystem.motorFeed to MotorArray.electricalInput;
  connect WingSystem.structuralMount to Fuselage.structuralMount;
  connect ControlSoftware.throttleOut to MotorArray.throttleCmd;
  connect ControlSoftware.actuatorBus to WingSystem.controlSurfaces;
  connect AutopilotModule.guidanceCmd to ControlSoftware.autopilotLink;
  connect ElectricalSystem.controlFeed to ControlSoftware.telemetryIn;
  connect ElectricalSystem.avionicsFeed to Fuselage.avionicsBus;
}
