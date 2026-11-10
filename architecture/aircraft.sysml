package Aircraft {

  // ---- SSP/FMI dialect markers (pyssp ecosystem: pycps_sysml2 core) ----

  part def SspModel;
  part def Analysis;
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

  // ---- FMU build metadata (SSD component sources are derived from part names) ----

  attribute def FmuMetadata {
    attribute source : String;
    attribute implementation : String;
  }

  attribute def ControlInterfaceFmu :> FmuMetadata {
    attribute source = "build/fmus/ControlInterface.fmu";
  }

  attribute def Ros2UdpBridgeFmu :> FmuMetadata {
    attribute source = "build/fmus/Ros2UdpBridge.fmu";
  }

  attribute def AutopilotModuleFmu :> FmuMetadata {
    attribute source = "build/fmus/AutopilotModule.fmu";
  }

  attribute def CompositeAirframeFmu :> FmuMetadata {
    attribute source = "build/fmus/CompositeAirframe.fmu";
  }

  attribute def TurbofanPropulsionFmu :> FmuMetadata {
    attribute source = "build/fmus/TurbofanPropulsion.fmu";
  }

  attribute def MissionComputerFmu :> FmuMetadata {
    attribute source = "build/fmus/MissionComputer.fmu";
  }

  attribute def FuelSystemFmu :> FmuMetadata {
    attribute source = "build/fmus/FuelSystem.fmu";
  }

  attribute def AdaptiveWingSystemFmu :> FmuMetadata {
    attribute source = "build/fmus/AdaptiveWingSystem.fmu";
  }

  attribute def EnvironmentFmu :> FmuMetadata {
    attribute source = "build/fmus/Environment.fmu";
  }

  attribute def InputOutputFmu :> FmuMetadata {
    attribute source = "build/fmus/InputOutput.fmu";
  }

  // ---- parameter interfaces (the FMU parameter surface) ----

  port def ControlParameters :> ParameterInterface {
    attribute input_scheme : String = "HOTAS";
    attribute telemetry_rate_hz : Integer = 120;
    attribute useBridgeInput : Boolean = false;
    attribute inputLag : Real = 0.05;
    attribute manualCommandDefault : Real = 0.6;
  }

  port def Ros2UdpParameters :> ParameterInterface {
    attribute transport : String = "Ros2UdpBridge";
    attribute reference_latitude_deg : Real = 0.0;
    attribute reference_longitude_deg : Real = 0.0;
    attribute reference_altitude_m : Real = 0.0;
    attribute remote_host : String = "127.0.0.1";
    attribute telemetry_port : Integer = 5501;
    attribute control_port : Integer = 5502;
  }

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
    attribute waypointCount : Integer = 10;
    attribute waypointX_km : Real[10] = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0);
    attribute waypointY_km : Real[10] = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0);
    attribute waypointZ_km : Real[10] = (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0);
    attribute waypointProximity_km : Real = 10.0;
    attribute waypointAltitudeProximity_km : Real = 1.0;
    attribute tauCmd : Real = 1.0;
  }

  port def AirframeParameters :> ParameterInterface {
    attribute length_m : Real = 15.0;
    attribute fuselage_width_m : Real = 3.0;
    attribute wingspan_m : Real = 10.0;
    attribute empty_weight_kg : Real = 8573.0;
    attribute payload_capacity_kg : Real = 7700.0;
    attribute hardpoint_count : Integer = 9;
    attribute length : Real = 15.0;
    attribute fuselageWidth : Real = 3.0;
    attribute wingspan : Real = 10.0;
    attribute payloadScale : Real = 1.0;
    attribute maxPayload : Real = 7700.0;
    attribute emptyMass : Real = 8573.0;
    attribute wettedAreaFactor : Real = 2.2;
  }

  port def PropulsionParameters :> ParameterInterface {
    attribute max_thrust_kn : Real = 129.7;
    attribute dry_thrust_kn : Real = 79.0;
    attribute specific_fuel_consumption : Real = 0.76;
    attribute fuel_capacity_kg : Real = 3160.0;
    attribute generator_output_kw : Real = 80.0;
    attribute maxThrust_kN : Real = 129.7;
    attribute dryThrust_kN : Real = 79.0;
    attribute generatorOutputKW : Real = 80.0;
    attribute fuelEfficiency : Real = 0.33;
    attribute fuelFlowAtFull_kgps : Real = 1.15;
  }

  port def MissionComputerParameters :> ParameterInterface {
    attribute flyByWireChannels : Integer = 3;
    attribute rollAuthority_deg : Real = 25.0;
    attribute pitchAuthority_deg : Real = 20.0;
    attribute yawAuthority_deg : Real = 10.0;
  }

  port def FuelSystemParameters :> ParameterInterface {
    attribute fuel_capacity_kg : Real = 3160.0;
    attribute reserve_fraction : Real = 0.08;
    attribute fuelCapacityKg : Real = 3160.0;
    attribute reserveFraction : Real = 0.08;
  }

  port def WingParameters :> ParameterInterface {
    attribute reference_area_m2 : Real = 28.0;
    attribute span_m : Real = 10.0;
    attribute aspect_ratio : Real = 3.6;
    attribute control_authority_deg : Real = 25.0;
    attribute load_factor_limit_g : Integer = 9;
    attribute referenceArea : Real = 28.0;
    attribute span : Real = 10.0;
    attribute wingAreaScale : Real = 1.0;
    attribute aspectRatio : Real = 3.6;
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

  // ---- scenario parameter set (the scenario's tunable surface) ----

  attribute def MissionScenario :> ParameterSet {
    attribute useBridgeInput : Boolean = false;
    attribute initX_km : Real = 0.0;
    attribute initY_km : Real = 0.0;
    attribute initZ_km : Real = 0.0;
    attribute waypointProximity_km : Real = 10.0;
    attribute targetAirspeed_mps : Real = 200.0;
    attribute waypointX_km : Real[10] = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0);
    attribute waypointY_km : Real[10] = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0);
    attribute waypointZ_km : Real[10] = (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0);
  }

  // ---- data (port) definitions ----

  port def PilotCommand {
    doc /* HOTAS-style control payload shared across control surfaces and mission computer consumers. */
    attribute stick_pitch_norm: Real;
    attribute stick_roll_norm: Real;
    attribute rudder_norm: Real;
    attribute throttle_norm: Real;
    attribute throttle_aux_norm: Real;
    attribute button_mask: Integer;
    attribute hat_x: Integer;
    attribute hat_y: Integer;
    attribute mode_switch: Integer;
    attribute reserved: Integer;
  }

  port def OrientationEuler {
    doc /* Air vehicle orientation expressed as Euler angles in degrees. */
    attribute roll_deg: Real;
    attribute pitch_deg: Real;
    attribute yaw_deg: Real;
  }

  port def PositionXYZ {
    doc /* Local navigation frame expressed in kilometers (x=North, y=East, z=Up). */
    attribute x_km: Real;
    attribute y_km: Real;
    attribute z_km: Real;
  }

  port def SurfaceActuationCommand {
    doc /* Commanded surface deflections in degrees for co-simulation with aerodynamic models. */
    attribute left_aileron_deg: Real;
    attribute right_aileron_deg: Real;
    attribute elevator_deg: Real;
    attribute rudder_deg: Real;
    attribute flaperon_deg: Real;
  }

  port def LiftState {
    doc /* Aerodynamic state summary exported from wing solver. */
    attribute lift_kn: Real;
    attribute drag_kn: Real;
    attribute pitching_moment_knm: Real;
  }

  port def ThrottleCommand {
    doc /* Engine throttle and fuel-enable bit for turbofan co-simulation. */
    attribute throttle_norm: Real;
    attribute fuel_enable: Boolean;
    attribute afterburner_enable: Boolean;
  }

  port def ThrustState {
    doc /* Propulsion output shared with performance models. */
    attribute thrust_kn: Real;
    attribute mass_flow_kgps: Real;
    attribute exhaust_velocity_mps: Real;
  }

  port def FuelLevelState {
    doc /* Remaining fuel mass and normalized level for availability tracking. */
    attribute fuel_remaining_kg: Real;
    attribute fuel_level_norm: Real;
    attribute fuel_starved: Boolean;
  }

  port def FuelConsumptionRate {
    doc /* Mass flow request or telemetry for turbofan fuel usage (kg/s). */
    attribute mass_flow_kgps: Real;
  }

  port def FlightStatusPacket {
    doc /* Mission computer status feedback consumed by autonomy and analysis models. */
    attribute airspeed_mps: Real;
    attribute energy_state_norm: Real;
    attribute angle_of_attack_deg: Real;
    attribute climb_rate: Real;
    attribute health_code: Integer;
  }

  port def MissionStatus {
    doc /* Waypoint-tracking status produced by the autopilot for logging and requirement evaluation. */
    attribute waypoint_index: Integer;
    attribute total_waypoints: Integer;
    attribute distance_to_waypoint_km: Real;
    attribute arrived: Boolean;
    attribute complete: Boolean;
  }

  // ---- part definitions ----

  part def ControlInterface {
    doc /* F-16 HOTAS + side-stick interface for pilot inputs and trim switches. */
    attribute fmu_meta : ControlInterfaceFmu;
    in port parameters : ControlParameters;
    in port bridgeInput : PilotCommand;
    out port pilotCommand : PilotCommand;
  }

  part def Ros2UdpBridge {
    doc /* Adapter component for ROS 2 visualization/control coupling via a UDP companion runtime. */
    attribute fmu_meta : Ros2UdpBridgeFmu;
    in port parameters : Ros2UdpParameters;
    in port statePosition : PositionXYZ;
    in port stateOrientation : OrientationEuler;
    in port flightStatus : FlightStatusPacket;
    in port missionStatus : MissionStatus;
    out port pilotCommand : PilotCommand;
  }

  part def AutopilotModule {
    doc /* F-16 autopilot, takes in sensor data and translates it into a equivalent hotas command. */
    attribute fmu_meta : AutopilotModuleFmu;
    in port parameters : AutopilotParameters;
    in port feedbackBus : FlightStatusPacket;
    in port currentLocation : PositionXYZ;
    in port currentOrientation : OrientationEuler;
    out port autopilotCmd : PilotCommand;
    out port missionStatus : MissionStatus;
  }

  part def CompositeAirframe {
    doc /* F-16 aluminum/composite fuselage sized for high-supersonic operations with dorsal spine for avionics. */
    attribute fmu_meta : CompositeAirframeFmu;
    in port parameters : AirframeParameters;
  }

  part def TurbofanPropulsion {
    doc /* Pratt & Whitney F100 / GE F110 class augmented turbofan powering the F-16. */
    attribute fmu_meta : TurbofanPropulsionFmu;
    in port parameters : PropulsionParameters;
    in port throttleCmd : ThrottleCommand;
    out port thrustOut : ThrustState;
    out port fuel_consumption : FuelConsumptionRate;
  }

  part def MissionComputer {
    doc /* F-16C/D mission computer blending pilot HOTAS inputs with fly-by-wire control laws and stores management. */
    attribute fmu_meta : MissionComputerFmu;
    in port parameters : MissionComputerParameters;
    in port manualInput : PilotCommand;
    in port autopilotInput : PilotCommand;
    in port fuelStatus : FuelLevelState;
    out port engineThrottle : ThrottleCommand;
    out port direction_command : OrientationEuler;
  }

  part def FuelSystem {
    doc /* Internal + conformal fuel storage management with transfer pumps feeding engine feed tanks. */
    attribute fmu_meta : FuelSystemFmu;
    in port parameters : FuelSystemParameters;
    in port fuel_consumption_rate : FuelConsumptionRate;
    out port fuelState : FuelLevelState;
  }

  part def AdaptiveWingSystem {
    doc /* Leading-edge strake and cropped-delta wing sized to F-16 Block 50 geometry with 9g capability. This model includes the control system. */
    attribute fmu_meta : AdaptiveWingSystemFmu;
    in port parameters : WingParameters;
    in port direction_command : OrientationEuler;
    in port flight_speed : FlightStatusPacket;
    out port actuation_command : SurfaceActuationCommand;
    out port liftInterface : LiftState;
  }

  part def Environment {
    doc /* Tracking position and velocities of the aircraft and feeds the sensors. */
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

  part def InputOutput {
    doc /* Simulation sink for debugging and recording mission/autopilot telemetry. */
    attribute fmu_meta : InputOutputFmu;
    in port locationXYZ : PositionXYZ;
    in port orientation : OrientationEuler;
    in port autopilotCmd : PilotCommand;
    in port flightStatus : FlightStatusPacket;
    in port missionStatus : MissionStatus;
  }

  // ---- the simulation model (SSP target) ----

  part def AircraftModel :> SspModel {
    part control_interface : ControlInterface;
    part ros2_udp_bridge : Ros2UdpBridge;
    part autopilot_module : AutopilotModule;
    part composite_airframe : CompositeAirframe;
    part turbofan_propulsion : TurbofanPropulsion;
    part mission_computer : MissionComputer;
    part fuel_system : FuelSystem;
    part adaptive_wing_system : AdaptiveWingSystem;
    part environment : Environment;
    part input_output : InputOutput;

    connect ros2_udp_bridge.pilotCommand to control_interface.bridgeInput;
    connect control_interface.pilotCommand to mission_computer.manualInput;
    connect autopilot_module.autopilotCmd to mission_computer.autopilotInput;
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
    connect environment.location to ros2_udp_bridge.statePosition;
    connect environment.orientation to ros2_udp_bridge.stateOrientation;
    connect environment.flight_status to ros2_udp_bridge.flightStatus;
    connect autopilot_module.missionStatus to ros2_udp_bridge.missionStatus;
    connect environment.location to input_output.locationXYZ;
    connect environment.orientation to input_output.orientation;
    connect autopilot_module.autopilotCmd to input_output.autopilotCmd;
    connect environment.flight_status to input_output.flightStatus;
    connect autopilot_module.missionStatus to input_output.missionStatus;
  }

  // ---- analysis: a scenario connected to an experiment ----

  part def HighAltitudeIntercept :> Analysis {
    attribute experiment_baseline : BaselineExperiment;
    attribute scenario : MissionScenario;
    part sut : AircraftModel;

    bind sut.control_interface.parameters.useBridgeInput = scenario.useBridgeInput;
    bind sut.environment.parameters.initX_km = scenario.initX_km;
    bind sut.environment.parameters.initY_km = scenario.initY_km;
    bind sut.environment.parameters.initZ_km = scenario.initZ_km;
    bind sut.autopilot_module.parameters.waypointProximity_km = scenario.waypointProximity_km;
    bind sut.autopilot_module.parameters.targetAirspeed_mps = scenario.targetAirspeed_mps;
    bind sut.autopilot_module.parameters.waypointX_km = scenario.waypointX_km;
    bind sut.autopilot_module.parameters.waypointY_km = scenario.waypointY_km;
    bind sut.autopilot_module.parameters.waypointZ_km = scenario.waypointZ_km;
  }
}