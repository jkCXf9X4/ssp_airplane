// Workshop aircraft: high-level, ROS-free aircraft system in SysML v2 textual
// notation. The composition at the bottom defines the workshop day.
// Every leaf part points at a prebuilt FMI 2.0 CoSimulation FMU from the
// airplane reference build; no source FMU is authored here.

package AircraftWorkshop {

  // ---- dialect markers (declared locally: this file has no imports) ----

  part def SspModel;
  part def Analysis;
  part def FmuModel;

  port def ParameterInterface;
  attribute def ParameterSet;

  attribute def Experiment {
    attribute startTime : Real;
    attribute stopTime : Real;
    attribute stepSize : Real;
  }

  attribute def BaselineExperiment :> Experiment {
    attribute startTime = 0.0;
    attribute stopTime = 120.0;
    attribute stepSize = 0.1;
  }

  // ---- FMU build metadata ----
  // fmu_meta.source is resolved against --fmu-root. implementation must match
  // the FMU interface; all prebuilt airplane FMUs are CoSimulation.

  attribute def FmuMetadata {
    attribute source : String;
    attribute implementation : String;
  }

  attribute def EnvironmentFmu :> FmuMetadata {
    attribute source = "build/fmus/Environment.fmu";
    attribute implementation = "CoSimulation";
  }

  attribute def CompositeAirframeFmu :> FmuMetadata {
    attribute source = "build/fmus/CompositeAirframe.fmu";
    attribute implementation = "CoSimulation";
  }

  attribute def TurbofanPropulsionFmu :> FmuMetadata {
    attribute source = "build/fmus/TurbofanPropulsion.fmu";
    attribute implementation = "CoSimulation";
  }

  attribute def FuelSystemFmu :> FmuMetadata {
    attribute source = "build/fmus/FuelSystem.fmu";
    attribute implementation = "CoSimulation";
  }

  attribute def MissionComputerFmu :> FmuMetadata {
    attribute source = "build/fmus/MissionComputer.fmu";
    attribute implementation = "CoSimulation";
  }

  attribute def AutopilotModuleFmu :> FmuMetadata {
    attribute source = "build/fmus/AutopilotModule.fmu";
    attribute implementation = "CoSimulation";
  }

  attribute def AdaptiveWingSystemFmu :> FmuMetadata {
    attribute source = "build/fmus/AdaptiveWingSystem.fmu";
    attribute implementation = "CoSimulation";
  }

  attribute def InputOutputFmu :> FmuMetadata {
    attribute source = "build/fmus/InputOutput.fmu";
    attribute implementation = "CoSimulation";
  }

  // ---- parameter interfaces (the FMU parameter surface) ----

  port def AutopilotParameters :> ParameterInterface {
    attribute updateRateHz : Real = 40.0;
    attribute defaultThrottle : Real = 0.5;
    attribute targetAirspeed_mps : Real = 200.0;
    attribute airspeedToThrottleGain : Real = 0.003;
    attribute climbRateToThrottleGain : Real = 0.001;
    attribute minThrottleCommand : Real = 0.2;
    attribute headingGain : Real = 0.016666666666666666;
    attribute altitudeToPitchGain : Real = 10.0;
    attribute pitchAngleGain : Real = 0.05;
    attribute maxPitchCommand_deg : Real = 20.0;
    attribute waypointX_km : Real[10] = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0);
    attribute waypointY_km : Real[10] = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0);
    attribute waypointZ_km : Real[10] = (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0);
    attribute waypointProximity_km : Real = 10.0;
    attribute waypointAltitudeProximity_km : Real = 1.0;
    attribute tauCmd : Real = 1.0;
  }

  port def AirframeParameters :> ParameterInterface {
    attribute length : Real = 15.0;
    attribute fuselageWidth : Real = 3.0;
    attribute wingspan : Real = 10.0;
    attribute emptyMass : Real = 8573.0;
    attribute maxPayload : Real = 7700.0;
    attribute payloadScale : Real = 1.0;
  }

  port def PropulsionParameters :> ParameterInterface {
    attribute maxThrust_kN : Real = 129.7;
    attribute dryThrust_kN : Real = 79.0;
    attribute fuelEfficiency : Real = 0.33;
    attribute fuelFlowAtFull_kgps : Real = 1.15;
    attribute generatorOutputKW : Real = 80.0;
  }

  port def MissionComputerParameters :> ParameterInterface {
    attribute flyByWireChannels : Integer = 3;
    attribute rollAuthority_deg : Real = 25.0;
    attribute pitchAuthority_deg : Real = 20.0;
    attribute yawAuthority_deg : Real = 10.0;
  }

  port def FuelSystemParameters :> ParameterInterface {
    attribute fuelCapacityKg : Real = 3160.0;
    attribute reserveFraction : Real = 0.08;
  }

  port def WingParameters :> ParameterInterface {
    attribute referenceArea : Real = 28.0;
    attribute span : Real = 10.0;
    attribute aspectRatio : Real = 3.6;
    attribute wingAreaScale : Real = 1.0;
    attribute liftCoeffBase : Real = 0.75;
    attribute rollAuthority_deg : Real = 25.0;
    attribute pitchAuthority_deg : Real = 20.0;
  }

  port def EnvironmentParameters :> ParameterInterface {
    attribute initX_km : Real = 0.0;
    attribute initY_km : Real = 0.0;
    attribute initZ_km : Real = 1.0;
    attribute tauDirection_s : Real = 2.0;
    attribute thrustToSpeedGain : Real = 4.0;
    attribute climbBleedFraction : Real = 0.35;
    attribute minAirspeed_mps : Real = 50.0;
    attribute referenceEnergySpeed_mps : Real = 300.0;
  }

  // ---- scenario parameter set (analysis-side names) ----

  attribute def NominalMission :> ParameterSet {
    doc /* Default workshop mission. Units are carried in the names. */
    attribute targetAirspeed_mps : Real = 200.0;
    attribute initZ_km : Real = 1.0;
    attribute wingspan_m : Real = 10.0;
    attribute empty_weight_kg : Real = 8573.0;
    attribute waypointX_km : Real[10] = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0);
    attribute waypointY_km : Real[10] = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0);
    attribute waypointZ_km : Real[10] = (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0);
    attribute waypointProximity_km : Real = 10.0;
  }

  // ---- port definitions ----
  // Structured ports keep the prebuilt FMU variable names (port.attribute).
  // RealSignal is the flat single-value variant for participant additions.

  port def RealSignal {
    attribute pyssp_flat_connector : Boolean = true;
    attribute value : Real;
  }

  port def PilotCommand {
    doc /* Abstract pilot/autopilot command bundle (normalized stick and throttle). */
    attribute stick_pitch_norm : Real;
    attribute stick_roll_norm : Real;
    attribute rudder_norm : Real;
    attribute throttle_norm : Real;
    attribute throttle_aux_norm : Real;
    attribute button_mask : Integer;
    attribute hat_x : Integer;
    attribute hat_y : Integer;
    attribute mode_switch : Integer;
    attribute reserved : Integer;
  }

  port def OrientationEuler {
    doc /* Air vehicle orientation as Euler angles in degrees. */
    attribute roll_deg : Real;
    attribute pitch_deg : Real;
    attribute yaw_deg : Real;
  }

  port def PositionXYZ {
    doc /* Local navigation frame in kilometers (x=North, y=East, z=Up). */
    attribute x_km : Real;
    attribute y_km : Real;
    attribute z_km : Real;
  }

  port def SurfaceActuationCommand {
    doc /* Commanded control-surface deflections in degrees. */
    attribute left_aileron_deg : Real;
    attribute right_aileron_deg : Real;
    attribute elevator_deg : Real;
    attribute rudder_deg : Real;
    attribute flaperon_deg : Real;
  }

  port def LiftState {
    doc /* Aerodynamic state summary from the wing solver. */
    attribute lift_kn : Real;
    attribute drag_kn : Real;
    attribute pitching_moment_knm : Real;
  }

  port def ThrottleCommand {
    doc /* Engine throttle and fuel-enable bits. */
    attribute throttle_norm : Real;
    attribute fuel_enable : Boolean;
    attribute afterburner_enable : Boolean;
  }

  port def ThrustState {
    doc /* Propulsion output shared with the environment. */
    attribute thrust_kn : Real;
    attribute mass_flow_kgps : Real;
    attribute exhaust_velocity_mps : Real;
  }

  port def FuelLevelState {
    doc /* Remaining fuel mass and normalized level. */
    attribute fuel_remaining_kg : Real;
    attribute fuel_level_norm : Real;
    attribute fuel_starved : Boolean;
  }

  port def FuelConsumptionRate {
    doc /* Fuel mass-flow request/telemetry in kg/s. */
    attribute mass_flow_kgps : Real;
  }

  port def FlightStatusPacket {
    doc /* Consolidated air-data and health feedback. */
    attribute airspeed_mps : Real;
    attribute energy_state_norm : Real;
    attribute angle_of_attack_deg : Real;
    attribute climb_rate : Real;
    attribute health_code : Integer;
  }

  port def MissionStatus {
    doc /* Waypoint-tracking status for logging and verification. */
    attribute waypoint_index : Integer;
    attribute total_waypoints : Integer;
    attribute distance_to_waypoint_km : Real;
    attribute arrived : Boolean;
    attribute complete : Boolean;
  }

  // ---- leaf part definitions (one FMU each) ----

  part def Environment {
    doc /* Atmosphere, navigation frame, and aircraft state propagation. */
    attribute fmu_meta : EnvironmentFmu;
    in port parameters : EnvironmentParameters;
    in port actuation_command : SurfaceActuationCommand;
    in port direction_command : OrientationEuler;
    in port lift : LiftState;
    in port thrust_in : ThrustState;
    out port orientation : OrientationEuler;
    out port location : PositionXYZ;
    out port flight_status : FlightStatusPacket;
  }

  part def CompositeAirframe {
    doc /* Abstract airframe: geometry, mass, payload, and hardpoints. */
    attribute fmu_meta : CompositeAirframeFmu;
    in port parameters : AirframeParameters;
  }

  part def TurbofanPropulsion {
    doc /* Abstract augmented turbofan with fuel flow and thrust output. */
    attribute fmu_meta : TurbofanPropulsionFmu;
    in port parameters : PropulsionParameters;
    in port throttleCmd : ThrottleCommand;
    out port thrustOut : ThrustState;
    out port fuel_consumption : FuelConsumptionRate;
  }

  part def FuelSystem {
    doc /* Fuel storage, reserve management, and engine feed. */
    attribute fmu_meta : FuelSystemFmu;
    in port parameters : FuelSystemParameters;
    in port fuel_consumption_rate : FuelConsumptionRate;
    out port fuelState : FuelLevelState;
  }

  part def MissionComputer {
    doc /* Fly-by-wire blending and stores/engine command generation. */
    attribute fmu_meta : MissionComputerFmu;
    in port parameters : MissionComputerParameters;
    in port manualInput : PilotCommand;
    in port autopilotInput : PilotCommand;
    in port fuelStatus : FuelLevelState;
    out port engineThrottle : ThrottleCommand;
    out port direction_command : OrientationEuler;
  }

  part def AutopilotModule {
    doc /* Waypoint tracking and airspeed/altitude hold. */
    attribute fmu_meta : AutopilotModuleFmu;
    in port parameters : AutopilotParameters;
    in port feedbackBus : FlightStatusPacket;
    in port currentLocation : PositionXYZ;
    in port currentOrientation : OrientationEuler;
    out port autopilotCmd : PilotCommand;
    out port missionStatus : MissionStatus;
  }

  part def AdaptiveWingSystem {
    doc /* Wing aerodynamics and control-surface actuation. */
    attribute fmu_meta : AdaptiveWingSystemFmu;
    in port parameters : WingParameters;
    in port direction_command : OrientationEuler;
    in port flight_speed : FlightStatusPacket;
    out port actuation_command : SurfaceActuationCommand;
    out port liftInterface : LiftState;
  }

  part def InputOutput {
    doc /* Simulation sink: position, attitude, command, and status recording. */
    attribute fmu_meta : InputOutputFmu;
    in port locationXYZ : PositionXYZ;
    in port orientation : OrientationEuler;
    in port autopilotCmd : PilotCommand;
    in port flightStatus : FlightStatusPacket;
    in port missionStatus : MissionStatus;
  }

  // ---- composition ----

  // The one-day workshop composition: 8 parts, full closed loop.
  part def WorkshopAircraft :> SspModel {
    part environment : Environment;
    part composite_airframe : CompositeAirframe;
    part turbofan_propulsion : TurbofanPropulsion;
    part fuel_system : FuelSystem;
    part mission_computer : MissionComputer;
    part autopilot_module : AutopilotModule;
    part adaptive_wing_system : AdaptiveWingSystem;
    part input_output : InputOutput;

    connect turbofan_propulsion.thrustOut to environment.thrust_in;
    connect turbofan_propulsion.fuel_consumption to fuel_system.fuel_consumption_rate;
    connect mission_computer.engineThrottle to turbofan_propulsion.throttleCmd;
    connect mission_computer.direction_command to adaptive_wing_system.direction_command;
    connect mission_computer.direction_command to environment.direction_command;
    connect fuel_system.fuelState to mission_computer.fuelStatus;
    connect adaptive_wing_system.actuation_command to environment.actuation_command;
    connect adaptive_wing_system.liftInterface to environment.lift;
    connect environment.orientation to autopilot_module.currentOrientation;
    connect environment.location to autopilot_module.currentLocation;
    connect environment.flight_status to autopilot_module.feedbackBus;
    connect environment.flight_status to adaptive_wing_system.flight_speed;
    connect autopilot_module.autopilotCmd to mission_computer.autopilotInput;
    // No pilot interface in the 8-part model: use the autopilot command for the
    // manual blend input so every MissionComputer input is driven.
    connect autopilot_module.autopilotCmd to mission_computer.manualInput;
    connect environment.location to input_output.locationXYZ;
    connect environment.orientation to input_output.orientation;
    connect autopilot_module.autopilotCmd to input_output.autopilotCmd;
    connect environment.flight_status to input_output.flightStatus;
    connect autopilot_module.missionStatus to input_output.missionStatus;
  }

  // ---- analysis: a scenario connected to an experiment ----

  part def WorkshopMission :> Analysis {
    doc /* Experiment-only analysis: the scenario set drives every parameter binding. */
    attribute experiment_baseline : BaselineExperiment;
    attribute scenario : NominalMission;
    part sut : WorkshopAircraft;

    bind sut.autopilot_module.parameters.targetAirspeed_mps = scenario.targetAirspeed_mps;
    bind sut.autopilot_module.parameters.waypointX_km = scenario.waypointX_km;
    bind sut.autopilot_module.parameters.waypointY_km = scenario.waypointY_km;
    bind sut.autopilot_module.parameters.waypointZ_km = scenario.waypointZ_km;
    bind sut.autopilot_module.parameters.waypointProximity_km = scenario.waypointProximity_km;
    bind sut.environment.parameters.initZ_km = scenario.initZ_km;
    bind sut.composite_airframe.parameters.wingspan = scenario.wingspan_m;
    bind sut.composite_airframe.parameters.emptyMass = scenario.empty_weight_kg;
  }

  // ==== Ex1: YOUR PART HERE =================================================
  //
  // Exercise: add one leaf part, give it a port, and wire it into a
  // composition without breaking SSD generation.
  //
  // 1. Uncomment the part definition and metadata below (or copy them).
  // 2. Add the part usage inside WorkshopAircraft.
  // 3. Add the connect line. The Environment output already exists.
  // 4. Regenerate the SSD (see README) and confirm the new component appears.
  //
  // Keep fmu_meta.source pointing at a built FMU so SSP packaging also works.
  // This example reuses the InputOutput FMU and one of its input variables.
  //
  // attribute def ParticipantProbeFmu :> FmuMetadata {
  //   attribute source = "build/fmus/InputOutput.fmu";
  //   attribute implementation = "CoSimulation";
  // }
  //
  // part def ParticipantProbe {
  //   attribute fmu_meta : ParticipantProbeFmu;
  //   in port flightStatus : FlightStatusPacket;
  // }
  //
  // Inside WorkshopAircraft:
  //   part participant_probe : ParticipantProbe;
  //   connect environment.flight_status to participant_probe.flightStatus;
  //
  // ==== end Ex1 =============================================================

}
