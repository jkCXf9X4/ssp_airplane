#pragma once

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/* Generated from architecture package Aircraft. Do not edit manually. */

typedef enum Aircraft_ScalarType {
  AIRCRAFT_SCALAR_REAL = 0,
  AIRCRAFT_SCALAR_INTEGER = 1,
  AIRCRAFT_SCALAR_BOOLEAN = 2,
  AIRCRAFT_SCALAR_STRING = 3,
} Aircraft_ScalarType;

typedef struct Aircraft_FieldBinding {
  int value_reference;
  Aircraft_ScalarType scalar_type;
  size_t offset;
  bool writable;
} Aircraft_FieldBinding;

typedef struct Aircraft_PilotCommand {
  double stick_pitch_norm;
  double stick_roll_norm;
  double rudder_norm;
  double throttle_norm;
  double throttle_aux_norm;
  int button_mask;
  int hat_x;
  int hat_y;
  int mode_switch;
  int reserved;
} Aircraft_PilotCommand;

typedef struct Aircraft_OrientationEuler {
  double roll_deg;
  double pitch_deg;
  double yaw_deg;
} Aircraft_OrientationEuler;

typedef struct Aircraft_PositionXYZ {
  double x_km;
  double y_km;
  double z_km;
} Aircraft_PositionXYZ;

typedef struct Aircraft_SurfaceActuationCommand {
  double left_aileron_deg;
  double right_aileron_deg;
  double elevator_deg;
  double rudder_deg;
  double flaperon_deg;
} Aircraft_SurfaceActuationCommand;

typedef struct Aircraft_LiftState {
  double lift_kn;
  double drag_kn;
  double pitching_moment_knm;
} Aircraft_LiftState;

typedef struct Aircraft_ThrottleCommand {
  double throttle_norm;
  bool fuel_enable;
  bool afterburner_enable;
} Aircraft_ThrottleCommand;

typedef struct Aircraft_ThrustState {
  double thrust_kn;
  double mass_flow_kgps;
  double exhaust_velocity_mps;
} Aircraft_ThrustState;

typedef struct Aircraft_FuelLevelState {
  double fuel_remaining_kg;
  double fuel_level_norm;
  bool fuel_starved;
} Aircraft_FuelLevelState;

typedef struct Aircraft_FuelConsumptionRate {
  double mass_flow_kgps;
} Aircraft_FuelConsumptionRate;

typedef struct Aircraft_FlightStatusPacket {
  double airspeed_mps;
  double energy_state_norm;
  double angle_of_attack_deg;
  double climb_rate;
  int health_code;
} Aircraft_FlightStatusPacket;

typedef struct Aircraft_MissionStatus {
  int waypoint_index;
  int total_waypoints;
  double distance_to_waypoint_km;
  bool arrived;
  bool complete;
} Aircraft_MissionStatus;

typedef enum Aircraft_ControlInterface_ValueReference {
  AIRCRAFT_CONTROLINTERFACE_VR_INPUT_SCHEME = 0,
  AIRCRAFT_CONTROLINTERFACE_VR_TELEMETRY_RATE_HZ = 1,
  AIRCRAFT_CONTROLINTERFACE_VR_USEBRIDGEINPUT = 2,
  AIRCRAFT_CONTROLINTERFACE_VR_BRIDGEINPUT_STICK_PITCH_NORM = 3,
  AIRCRAFT_CONTROLINTERFACE_VR_BRIDGEINPUT_STICK_ROLL_NORM = 4,
  AIRCRAFT_CONTROLINTERFACE_VR_BRIDGEINPUT_RUDDER_NORM = 5,
  AIRCRAFT_CONTROLINTERFACE_VR_BRIDGEINPUT_THROTTLE_NORM = 6,
  AIRCRAFT_CONTROLINTERFACE_VR_BRIDGEINPUT_THROTTLE_AUX_NORM = 7,
  AIRCRAFT_CONTROLINTERFACE_VR_BRIDGEINPUT_BUTTON_MASK = 8,
  AIRCRAFT_CONTROLINTERFACE_VR_BRIDGEINPUT_HAT_X = 9,
  AIRCRAFT_CONTROLINTERFACE_VR_BRIDGEINPUT_HAT_Y = 10,
  AIRCRAFT_CONTROLINTERFACE_VR_BRIDGEINPUT_MODE_SWITCH = 11,
  AIRCRAFT_CONTROLINTERFACE_VR_BRIDGEINPUT_RESERVED = 12,
  AIRCRAFT_CONTROLINTERFACE_VR_PILOTCOMMAND_STICK_PITCH_NORM = 13,
  AIRCRAFT_CONTROLINTERFACE_VR_PILOTCOMMAND_STICK_ROLL_NORM = 14,
  AIRCRAFT_CONTROLINTERFACE_VR_PILOTCOMMAND_RUDDER_NORM = 15,
  AIRCRAFT_CONTROLINTERFACE_VR_PILOTCOMMAND_THROTTLE_NORM = 16,
  AIRCRAFT_CONTROLINTERFACE_VR_PILOTCOMMAND_THROTTLE_AUX_NORM = 17,
  AIRCRAFT_CONTROLINTERFACE_VR_PILOTCOMMAND_BUTTON_MASK = 18,
  AIRCRAFT_CONTROLINTERFACE_VR_PILOTCOMMAND_HAT_X = 19,
  AIRCRAFT_CONTROLINTERFACE_VR_PILOTCOMMAND_HAT_Y = 20,
  AIRCRAFT_CONTROLINTERFACE_VR_PILOTCOMMAND_MODE_SWITCH = 21,
  AIRCRAFT_CONTROLINTERFACE_VR_PILOTCOMMAND_RESERVED = 22,
} Aircraft_ControlInterface_ValueReference;

typedef enum Aircraft_FlightGearBridge_ValueReference {
  AIRCRAFT_FLIGHTGEARBRIDGE_VR_TRANSPORT = 0,
  AIRCRAFT_FLIGHTGEARBRIDGE_VR_REFERENCE_LATITUDE_DEG = 1,
  AIRCRAFT_FLIGHTGEARBRIDGE_VR_REFERENCE_LONGITUDE_DEG = 2,
  AIRCRAFT_FLIGHTGEARBRIDGE_VR_REFERENCE_ALTITUDE_M = 3,
  AIRCRAFT_FLIGHTGEARBRIDGE_VR_REMOTE_HOST = 4,
  AIRCRAFT_FLIGHTGEARBRIDGE_VR_TELEMETRY_PORT = 5,
  AIRCRAFT_FLIGHTGEARBRIDGE_VR_CONTROL_PORT = 6,
  AIRCRAFT_FLIGHTGEARBRIDGE_VR_STATEPOSITION_X_KM = 7,
  AIRCRAFT_FLIGHTGEARBRIDGE_VR_STATEPOSITION_Y_KM = 8,
  AIRCRAFT_FLIGHTGEARBRIDGE_VR_STATEPOSITION_Z_KM = 9,
  AIRCRAFT_FLIGHTGEARBRIDGE_VR_STATEORIENTATION_ROLL_DEG = 10,
  AIRCRAFT_FLIGHTGEARBRIDGE_VR_STATEORIENTATION_PITCH_DEG = 11,
  AIRCRAFT_FLIGHTGEARBRIDGE_VR_STATEORIENTATION_YAW_DEG = 12,
  AIRCRAFT_FLIGHTGEARBRIDGE_VR_FLIGHTSTATUS_AIRSPEED_MPS = 13,
  AIRCRAFT_FLIGHTGEARBRIDGE_VR_FLIGHTSTATUS_ENERGY_STATE_NORM = 14,
  AIRCRAFT_FLIGHTGEARBRIDGE_VR_FLIGHTSTATUS_ANGLE_OF_ATTACK_DEG = 15,
  AIRCRAFT_FLIGHTGEARBRIDGE_VR_FLIGHTSTATUS_CLIMB_RATE = 16,
  AIRCRAFT_FLIGHTGEARBRIDGE_VR_FLIGHTSTATUS_HEALTH_CODE = 17,
  AIRCRAFT_FLIGHTGEARBRIDGE_VR_MISSIONSTATUS_WAYPOINT_INDEX = 18,
  AIRCRAFT_FLIGHTGEARBRIDGE_VR_MISSIONSTATUS_TOTAL_WAYPOINTS = 19,
  AIRCRAFT_FLIGHTGEARBRIDGE_VR_MISSIONSTATUS_DISTANCE_TO_WAYPOINT_KM = 20,
  AIRCRAFT_FLIGHTGEARBRIDGE_VR_MISSIONSTATUS_ARRIVED = 21,
  AIRCRAFT_FLIGHTGEARBRIDGE_VR_MISSIONSTATUS_COMPLETE = 22,
  AIRCRAFT_FLIGHTGEARBRIDGE_VR_PILOTCOMMAND_STICK_PITCH_NORM = 23,
  AIRCRAFT_FLIGHTGEARBRIDGE_VR_PILOTCOMMAND_STICK_ROLL_NORM = 24,
  AIRCRAFT_FLIGHTGEARBRIDGE_VR_PILOTCOMMAND_RUDDER_NORM = 25,
  AIRCRAFT_FLIGHTGEARBRIDGE_VR_PILOTCOMMAND_THROTTLE_NORM = 26,
  AIRCRAFT_FLIGHTGEARBRIDGE_VR_PILOTCOMMAND_THROTTLE_AUX_NORM = 27,
  AIRCRAFT_FLIGHTGEARBRIDGE_VR_PILOTCOMMAND_BUTTON_MASK = 28,
  AIRCRAFT_FLIGHTGEARBRIDGE_VR_PILOTCOMMAND_HAT_X = 29,
  AIRCRAFT_FLIGHTGEARBRIDGE_VR_PILOTCOMMAND_HAT_Y = 30,
  AIRCRAFT_FLIGHTGEARBRIDGE_VR_PILOTCOMMAND_MODE_SWITCH = 31,
  AIRCRAFT_FLIGHTGEARBRIDGE_VR_PILOTCOMMAND_RESERVED = 32,
} Aircraft_FlightGearBridge_ValueReference;

typedef enum Aircraft_AutopilotModule_ValueReference {
  AIRCRAFT_AUTOPILOTMODULE_VR_COMMENT = 0,
  AIRCRAFT_AUTOPILOTMODULE_VR_WAYPOINTCOUNT = 1,
  AIRCRAFT_AUTOPILOTMODULE_VR_WAYPOINTPROXIMITY_KM = 2,
  AIRCRAFT_AUTOPILOTMODULE_VR_WAYPOINTX_KM = 3,
  AIRCRAFT_AUTOPILOTMODULE_VR_WAYPOINTY_KM = 4,
  AIRCRAFT_AUTOPILOTMODULE_VR_WAYPOINTZ_KM = 5,
  AIRCRAFT_AUTOPILOTMODULE_VR_FEEDBACKBUS_AIRSPEED_MPS = 6,
  AIRCRAFT_AUTOPILOTMODULE_VR_FEEDBACKBUS_ENERGY_STATE_NORM = 7,
  AIRCRAFT_AUTOPILOTMODULE_VR_FEEDBACKBUS_ANGLE_OF_ATTACK_DEG = 8,
  AIRCRAFT_AUTOPILOTMODULE_VR_FEEDBACKBUS_CLIMB_RATE = 9,
  AIRCRAFT_AUTOPILOTMODULE_VR_FEEDBACKBUS_HEALTH_CODE = 10,
  AIRCRAFT_AUTOPILOTMODULE_VR_CURRENTLOCATION_X_KM = 11,
  AIRCRAFT_AUTOPILOTMODULE_VR_CURRENTLOCATION_Y_KM = 12,
  AIRCRAFT_AUTOPILOTMODULE_VR_CURRENTLOCATION_Z_KM = 13,
  AIRCRAFT_AUTOPILOTMODULE_VR_CURRENTORIENTATION_ROLL_DEG = 14,
  AIRCRAFT_AUTOPILOTMODULE_VR_CURRENTORIENTATION_PITCH_DEG = 15,
  AIRCRAFT_AUTOPILOTMODULE_VR_CURRENTORIENTATION_YAW_DEG = 16,
  AIRCRAFT_AUTOPILOTMODULE_VR_AUTOPILOTCMD_STICK_PITCH_NORM = 17,
  AIRCRAFT_AUTOPILOTMODULE_VR_AUTOPILOTCMD_STICK_ROLL_NORM = 18,
  AIRCRAFT_AUTOPILOTMODULE_VR_AUTOPILOTCMD_RUDDER_NORM = 19,
  AIRCRAFT_AUTOPILOTMODULE_VR_AUTOPILOTCMD_THROTTLE_NORM = 20,
  AIRCRAFT_AUTOPILOTMODULE_VR_AUTOPILOTCMD_THROTTLE_AUX_NORM = 21,
  AIRCRAFT_AUTOPILOTMODULE_VR_AUTOPILOTCMD_BUTTON_MASK = 22,
  AIRCRAFT_AUTOPILOTMODULE_VR_AUTOPILOTCMD_HAT_X = 23,
  AIRCRAFT_AUTOPILOTMODULE_VR_AUTOPILOTCMD_HAT_Y = 24,
  AIRCRAFT_AUTOPILOTMODULE_VR_AUTOPILOTCMD_MODE_SWITCH = 25,
  AIRCRAFT_AUTOPILOTMODULE_VR_AUTOPILOTCMD_RESERVED = 26,
  AIRCRAFT_AUTOPILOTMODULE_VR_MISSIONSTATUS_WAYPOINT_INDEX = 27,
  AIRCRAFT_AUTOPILOTMODULE_VR_MISSIONSTATUS_TOTAL_WAYPOINTS = 28,
  AIRCRAFT_AUTOPILOTMODULE_VR_MISSIONSTATUS_DISTANCE_TO_WAYPOINT_KM = 29,
  AIRCRAFT_AUTOPILOTMODULE_VR_MISSIONSTATUS_ARRIVED = 30,
  AIRCRAFT_AUTOPILOTMODULE_VR_MISSIONSTATUS_COMPLETE = 31,
} Aircraft_AutopilotModule_ValueReference;

typedef enum Aircraft_CompositeAirframe_ValueReference {
  AIRCRAFT_COMPOSITEAIRFRAME_VR_LENGTH_M = 0,
  AIRCRAFT_COMPOSITEAIRFRAME_VR_FUSELAGE_WIDTH_M = 1,
  AIRCRAFT_COMPOSITEAIRFRAME_VR_WINGSPAN_M = 2,
  AIRCRAFT_COMPOSITEAIRFRAME_VR_EMPTY_WEIGHT_KG = 3,
  AIRCRAFT_COMPOSITEAIRFRAME_VR_PAYLOAD_CAPACITY_KG = 4,
  AIRCRAFT_COMPOSITEAIRFRAME_VR_HARDPOINT_COUNT = 5,
} Aircraft_CompositeAirframe_ValueReference;

typedef enum Aircraft_TurbofanPropulsion_ValueReference {
  AIRCRAFT_TURBOFANPROPULSION_VR_MAX_THRUST_KN = 0,
  AIRCRAFT_TURBOFANPROPULSION_VR_DRY_THRUST_KN = 1,
  AIRCRAFT_TURBOFANPROPULSION_VR_SPECIFIC_FUEL_CONSUMPTION = 2,
  AIRCRAFT_TURBOFANPROPULSION_VR_FUEL_CAPACITY_KG = 3,
  AIRCRAFT_TURBOFANPROPULSION_VR_GENERATOR_OUTPUT_KW = 4,
  AIRCRAFT_TURBOFANPROPULSION_VR_THROTTLECMD_THROTTLE_NORM = 5,
  AIRCRAFT_TURBOFANPROPULSION_VR_THROTTLECMD_FUEL_ENABLE = 6,
  AIRCRAFT_TURBOFANPROPULSION_VR_THROTTLECMD_AFTERBURNER_ENABLE = 7,
  AIRCRAFT_TURBOFANPROPULSION_VR_THRUSTOUT_THRUST_KN = 8,
  AIRCRAFT_TURBOFANPROPULSION_VR_THRUSTOUT_MASS_FLOW_KGPS = 9,
  AIRCRAFT_TURBOFANPROPULSION_VR_THRUSTOUT_EXHAUST_VELOCITY_MPS = 10,
  AIRCRAFT_TURBOFANPROPULSION_VR_FUEL_CONSUMPTION_MASS_FLOW_KGPS = 11,
} Aircraft_TurbofanPropulsion_ValueReference;

typedef enum Aircraft_MissionComputer_ValueReference {
  AIRCRAFT_MISSIONCOMPUTER_VR_MANUALINPUT_STICK_PITCH_NORM = 0,
  AIRCRAFT_MISSIONCOMPUTER_VR_MANUALINPUT_STICK_ROLL_NORM = 1,
  AIRCRAFT_MISSIONCOMPUTER_VR_MANUALINPUT_RUDDER_NORM = 2,
  AIRCRAFT_MISSIONCOMPUTER_VR_MANUALINPUT_THROTTLE_NORM = 3,
  AIRCRAFT_MISSIONCOMPUTER_VR_MANUALINPUT_THROTTLE_AUX_NORM = 4,
  AIRCRAFT_MISSIONCOMPUTER_VR_MANUALINPUT_BUTTON_MASK = 5,
  AIRCRAFT_MISSIONCOMPUTER_VR_MANUALINPUT_HAT_X = 6,
  AIRCRAFT_MISSIONCOMPUTER_VR_MANUALINPUT_HAT_Y = 7,
  AIRCRAFT_MISSIONCOMPUTER_VR_MANUALINPUT_MODE_SWITCH = 8,
  AIRCRAFT_MISSIONCOMPUTER_VR_MANUALINPUT_RESERVED = 9,
  AIRCRAFT_MISSIONCOMPUTER_VR_AUTOPILOTINPUT_STICK_PITCH_NORM = 10,
  AIRCRAFT_MISSIONCOMPUTER_VR_AUTOPILOTINPUT_STICK_ROLL_NORM = 11,
  AIRCRAFT_MISSIONCOMPUTER_VR_AUTOPILOTINPUT_RUDDER_NORM = 12,
  AIRCRAFT_MISSIONCOMPUTER_VR_AUTOPILOTINPUT_THROTTLE_NORM = 13,
  AIRCRAFT_MISSIONCOMPUTER_VR_AUTOPILOTINPUT_THROTTLE_AUX_NORM = 14,
  AIRCRAFT_MISSIONCOMPUTER_VR_AUTOPILOTINPUT_BUTTON_MASK = 15,
  AIRCRAFT_MISSIONCOMPUTER_VR_AUTOPILOTINPUT_HAT_X = 16,
  AIRCRAFT_MISSIONCOMPUTER_VR_AUTOPILOTINPUT_HAT_Y = 17,
  AIRCRAFT_MISSIONCOMPUTER_VR_AUTOPILOTINPUT_MODE_SWITCH = 18,
  AIRCRAFT_MISSIONCOMPUTER_VR_AUTOPILOTINPUT_RESERVED = 19,
  AIRCRAFT_MISSIONCOMPUTER_VR_FUELSTATUS_FUEL_REMAINING_KG = 20,
  AIRCRAFT_MISSIONCOMPUTER_VR_FUELSTATUS_FUEL_LEVEL_NORM = 21,
  AIRCRAFT_MISSIONCOMPUTER_VR_FUELSTATUS_FUEL_STARVED = 22,
  AIRCRAFT_MISSIONCOMPUTER_VR_ENGINETHROTTLE_THROTTLE_NORM = 23,
  AIRCRAFT_MISSIONCOMPUTER_VR_ENGINETHROTTLE_FUEL_ENABLE = 24,
  AIRCRAFT_MISSIONCOMPUTER_VR_ENGINETHROTTLE_AFTERBURNER_ENABLE = 25,
  AIRCRAFT_MISSIONCOMPUTER_VR_DIRECTION_COMMAND_ROLL_DEG = 26,
  AIRCRAFT_MISSIONCOMPUTER_VR_DIRECTION_COMMAND_PITCH_DEG = 27,
  AIRCRAFT_MISSIONCOMPUTER_VR_DIRECTION_COMMAND_YAW_DEG = 28,
} Aircraft_MissionComputer_ValueReference;

typedef enum Aircraft_FuelSystem_ValueReference {
  AIRCRAFT_FUELSYSTEM_VR_FUEL_CAPACITY_KG = 0,
  AIRCRAFT_FUELSYSTEM_VR_RESERVE_FRACTION = 1,
  AIRCRAFT_FUELSYSTEM_VR_FUEL_CONSUMPTION_RATE_MASS_FLOW_KGPS = 2,
  AIRCRAFT_FUELSYSTEM_VR_FUELSTATE_FUEL_REMAINING_KG = 3,
  AIRCRAFT_FUELSYSTEM_VR_FUELSTATE_FUEL_LEVEL_NORM = 4,
  AIRCRAFT_FUELSYSTEM_VR_FUELSTATE_FUEL_STARVED = 5,
} Aircraft_FuelSystem_ValueReference;

typedef enum Aircraft_AdaptiveWingSystem_ValueReference {
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_REFERENCE_AREA_M2 = 0,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_SPAN_M = 1,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_ASPECT_RATIO = 2,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_CONTROL_AUTHORITY_DEG = 3,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_LOAD_FACTOR_LIMIT_G = 4,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_DIRECTION_COMMAND_ROLL_DEG = 5,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_DIRECTION_COMMAND_PITCH_DEG = 6,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_DIRECTION_COMMAND_YAW_DEG = 7,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_FLIGHT_SPEED_AIRSPEED_MPS = 8,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_FLIGHT_SPEED_ENERGY_STATE_NORM = 9,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_FLIGHT_SPEED_ANGLE_OF_ATTACK_DEG = 10,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_FLIGHT_SPEED_CLIMB_RATE = 11,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_FLIGHT_SPEED_HEALTH_CODE = 12,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_ACTUATION_COMMAND_LEFT_AILERON_DEG = 13,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_ACTUATION_COMMAND_RIGHT_AILERON_DEG = 14,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_ACTUATION_COMMAND_ELEVATOR_DEG = 15,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_ACTUATION_COMMAND_RUDDER_DEG = 16,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_ACTUATION_COMMAND_FLAPERON_DEG = 17,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_LIFTINTERFACE_LIFT_KN = 18,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_LIFTINTERFACE_DRAG_KN = 19,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_LIFTINTERFACE_PITCHING_MOMENT_KNM = 20,
} Aircraft_AdaptiveWingSystem_ValueReference;

typedef enum Aircraft_Environment_ValueReference {
  AIRCRAFT_ENVIRONMENT_VR_ACTUATION_COMMAND_LEFT_AILERON_DEG = 0,
  AIRCRAFT_ENVIRONMENT_VR_ACTUATION_COMMAND_RIGHT_AILERON_DEG = 1,
  AIRCRAFT_ENVIRONMENT_VR_ACTUATION_COMMAND_ELEVATOR_DEG = 2,
  AIRCRAFT_ENVIRONMENT_VR_ACTUATION_COMMAND_RUDDER_DEG = 3,
  AIRCRAFT_ENVIRONMENT_VR_ACTUATION_COMMAND_FLAPERON_DEG = 4,
  AIRCRAFT_ENVIRONMENT_VR_DIRECTION_COMMAND_ROLL_DEG = 5,
  AIRCRAFT_ENVIRONMENT_VR_DIRECTION_COMMAND_PITCH_DEG = 6,
  AIRCRAFT_ENVIRONMENT_VR_DIRECTION_COMMAND_YAW_DEG = 7,
  AIRCRAFT_ENVIRONMENT_VR_LIFT_LIFT_KN = 8,
  AIRCRAFT_ENVIRONMENT_VR_LIFT_DRAG_KN = 9,
  AIRCRAFT_ENVIRONMENT_VR_LIFT_PITCHING_MOMENT_KNM = 10,
  AIRCRAFT_ENVIRONMENT_VR_THRUST_IN_THRUST_KN = 11,
  AIRCRAFT_ENVIRONMENT_VR_THRUST_IN_MASS_FLOW_KGPS = 12,
  AIRCRAFT_ENVIRONMENT_VR_THRUST_IN_EXHAUST_VELOCITY_MPS = 13,
  AIRCRAFT_ENVIRONMENT_VR_ORIENTATION_ROLL_DEG = 14,
  AIRCRAFT_ENVIRONMENT_VR_ORIENTATION_PITCH_DEG = 15,
  AIRCRAFT_ENVIRONMENT_VR_ORIENTATION_YAW_DEG = 16,
  AIRCRAFT_ENVIRONMENT_VR_LOCATION_X_KM = 17,
  AIRCRAFT_ENVIRONMENT_VR_LOCATION_Y_KM = 18,
  AIRCRAFT_ENVIRONMENT_VR_LOCATION_Z_KM = 19,
  AIRCRAFT_ENVIRONMENT_VR_FLIGHT_STATUS_AIRSPEED_MPS = 20,
  AIRCRAFT_ENVIRONMENT_VR_FLIGHT_STATUS_ENERGY_STATE_NORM = 21,
  AIRCRAFT_ENVIRONMENT_VR_FLIGHT_STATUS_ANGLE_OF_ATTACK_DEG = 22,
  AIRCRAFT_ENVIRONMENT_VR_FLIGHT_STATUS_CLIMB_RATE = 23,
  AIRCRAFT_ENVIRONMENT_VR_FLIGHT_STATUS_HEALTH_CODE = 24,
} Aircraft_Environment_ValueReference;

typedef enum Aircraft_InputOutput_ValueReference {
  AIRCRAFT_INPUTOUTPUT_VR_LOCATIONXYZ_X_KM = 0,
  AIRCRAFT_INPUTOUTPUT_VR_LOCATIONXYZ_Y_KM = 1,
  AIRCRAFT_INPUTOUTPUT_VR_LOCATIONXYZ_Z_KM = 2,
  AIRCRAFT_INPUTOUTPUT_VR_ORIENTATION_ROLL_DEG = 3,
  AIRCRAFT_INPUTOUTPUT_VR_ORIENTATION_PITCH_DEG = 4,
  AIRCRAFT_INPUTOUTPUT_VR_ORIENTATION_YAW_DEG = 5,
  AIRCRAFT_INPUTOUTPUT_VR_AUTOPILOTCMD_STICK_PITCH_NORM = 6,
  AIRCRAFT_INPUTOUTPUT_VR_AUTOPILOTCMD_STICK_ROLL_NORM = 7,
  AIRCRAFT_INPUTOUTPUT_VR_AUTOPILOTCMD_RUDDER_NORM = 8,
  AIRCRAFT_INPUTOUTPUT_VR_AUTOPILOTCMD_THROTTLE_NORM = 9,
  AIRCRAFT_INPUTOUTPUT_VR_AUTOPILOTCMD_THROTTLE_AUX_NORM = 10,
  AIRCRAFT_INPUTOUTPUT_VR_AUTOPILOTCMD_BUTTON_MASK = 11,
  AIRCRAFT_INPUTOUTPUT_VR_AUTOPILOTCMD_HAT_X = 12,
  AIRCRAFT_INPUTOUTPUT_VR_AUTOPILOTCMD_HAT_Y = 13,
  AIRCRAFT_INPUTOUTPUT_VR_AUTOPILOTCMD_MODE_SWITCH = 14,
  AIRCRAFT_INPUTOUTPUT_VR_AUTOPILOTCMD_RESERVED = 15,
  AIRCRAFT_INPUTOUTPUT_VR_FLIGHTSTATUS_AIRSPEED_MPS = 16,
  AIRCRAFT_INPUTOUTPUT_VR_FLIGHTSTATUS_ENERGY_STATE_NORM = 17,
  AIRCRAFT_INPUTOUTPUT_VR_FLIGHTSTATUS_ANGLE_OF_ATTACK_DEG = 18,
  AIRCRAFT_INPUTOUTPUT_VR_FLIGHTSTATUS_CLIMB_RATE = 19,
  AIRCRAFT_INPUTOUTPUT_VR_FLIGHTSTATUS_HEALTH_CODE = 20,
  AIRCRAFT_INPUTOUTPUT_VR_MISSIONSTATUS_WAYPOINT_INDEX = 21,
  AIRCRAFT_INPUTOUTPUT_VR_MISSIONSTATUS_TOTAL_WAYPOINTS = 22,
  AIRCRAFT_INPUTOUTPUT_VR_MISSIONSTATUS_DISTANCE_TO_WAYPOINT_KM = 23,
  AIRCRAFT_INPUTOUTPUT_VR_MISSIONSTATUS_ARRIVED = 24,
  AIRCRAFT_INPUTOUTPUT_VR_MISSIONSTATUS_COMPLETE = 25,
} Aircraft_InputOutput_ValueReference;

#ifdef __cplusplus
#include <string>

struct Aircraft_ControlInterface_Instance {
  std::string input_scheme = "HOTAS";
  int telemetry_rate_hz = 120;
  bool useBridgeInput = false;
  Aircraft_PilotCommand bridgeInput = {};
  Aircraft_PilotCommand pilotCommand = {};
};

inline constexpr Aircraft_FieldBinding Aircraft_ControlInterface_Bindings[] = {
  {AIRCRAFT_CONTROLINTERFACE_VR_INPUT_SCHEME, AIRCRAFT_SCALAR_STRING, offsetof(Aircraft_ControlInterface_Instance, input_scheme), true},
  {AIRCRAFT_CONTROLINTERFACE_VR_TELEMETRY_RATE_HZ, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_ControlInterface_Instance, telemetry_rate_hz), true},
  {AIRCRAFT_CONTROLINTERFACE_VR_USEBRIDGEINPUT, AIRCRAFT_SCALAR_BOOLEAN, offsetof(Aircraft_ControlInterface_Instance, useBridgeInput), true},
  {AIRCRAFT_CONTROLINTERFACE_VR_BRIDGEINPUT_STICK_PITCH_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_ControlInterface_Instance, bridgeInput) + offsetof(Aircraft_PilotCommand, stick_pitch_norm), true},
  {AIRCRAFT_CONTROLINTERFACE_VR_BRIDGEINPUT_STICK_ROLL_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_ControlInterface_Instance, bridgeInput) + offsetof(Aircraft_PilotCommand, stick_roll_norm), true},
  {AIRCRAFT_CONTROLINTERFACE_VR_BRIDGEINPUT_RUDDER_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_ControlInterface_Instance, bridgeInput) + offsetof(Aircraft_PilotCommand, rudder_norm), true},
  {AIRCRAFT_CONTROLINTERFACE_VR_BRIDGEINPUT_THROTTLE_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_ControlInterface_Instance, bridgeInput) + offsetof(Aircraft_PilotCommand, throttle_norm), true},
  {AIRCRAFT_CONTROLINTERFACE_VR_BRIDGEINPUT_THROTTLE_AUX_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_ControlInterface_Instance, bridgeInput) + offsetof(Aircraft_PilotCommand, throttle_aux_norm), true},
  {AIRCRAFT_CONTROLINTERFACE_VR_BRIDGEINPUT_BUTTON_MASK, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_ControlInterface_Instance, bridgeInput) + offsetof(Aircraft_PilotCommand, button_mask), true},
  {AIRCRAFT_CONTROLINTERFACE_VR_BRIDGEINPUT_HAT_X, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_ControlInterface_Instance, bridgeInput) + offsetof(Aircraft_PilotCommand, hat_x), true},
  {AIRCRAFT_CONTROLINTERFACE_VR_BRIDGEINPUT_HAT_Y, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_ControlInterface_Instance, bridgeInput) + offsetof(Aircraft_PilotCommand, hat_y), true},
  {AIRCRAFT_CONTROLINTERFACE_VR_BRIDGEINPUT_MODE_SWITCH, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_ControlInterface_Instance, bridgeInput) + offsetof(Aircraft_PilotCommand, mode_switch), true},
  {AIRCRAFT_CONTROLINTERFACE_VR_BRIDGEINPUT_RESERVED, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_ControlInterface_Instance, bridgeInput) + offsetof(Aircraft_PilotCommand, reserved), true},
  {AIRCRAFT_CONTROLINTERFACE_VR_PILOTCOMMAND_STICK_PITCH_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_ControlInterface_Instance, pilotCommand) + offsetof(Aircraft_PilotCommand, stick_pitch_norm), false},
  {AIRCRAFT_CONTROLINTERFACE_VR_PILOTCOMMAND_STICK_ROLL_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_ControlInterface_Instance, pilotCommand) + offsetof(Aircraft_PilotCommand, stick_roll_norm), false},
  {AIRCRAFT_CONTROLINTERFACE_VR_PILOTCOMMAND_RUDDER_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_ControlInterface_Instance, pilotCommand) + offsetof(Aircraft_PilotCommand, rudder_norm), false},
  {AIRCRAFT_CONTROLINTERFACE_VR_PILOTCOMMAND_THROTTLE_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_ControlInterface_Instance, pilotCommand) + offsetof(Aircraft_PilotCommand, throttle_norm), false},
  {AIRCRAFT_CONTROLINTERFACE_VR_PILOTCOMMAND_THROTTLE_AUX_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_ControlInterface_Instance, pilotCommand) + offsetof(Aircraft_PilotCommand, throttle_aux_norm), false},
  {AIRCRAFT_CONTROLINTERFACE_VR_PILOTCOMMAND_BUTTON_MASK, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_ControlInterface_Instance, pilotCommand) + offsetof(Aircraft_PilotCommand, button_mask), false},
  {AIRCRAFT_CONTROLINTERFACE_VR_PILOTCOMMAND_HAT_X, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_ControlInterface_Instance, pilotCommand) + offsetof(Aircraft_PilotCommand, hat_x), false},
  {AIRCRAFT_CONTROLINTERFACE_VR_PILOTCOMMAND_HAT_Y, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_ControlInterface_Instance, pilotCommand) + offsetof(Aircraft_PilotCommand, hat_y), false},
  {AIRCRAFT_CONTROLINTERFACE_VR_PILOTCOMMAND_MODE_SWITCH, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_ControlInterface_Instance, pilotCommand) + offsetof(Aircraft_PilotCommand, mode_switch), false},
  {AIRCRAFT_CONTROLINTERFACE_VR_PILOTCOMMAND_RESERVED, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_ControlInterface_Instance, pilotCommand) + offsetof(Aircraft_PilotCommand, reserved), false},
};
inline constexpr size_t Aircraft_ControlInterface_BindingCount = sizeof(Aircraft_ControlInterface_Bindings) / sizeof(Aircraft_ControlInterface_Bindings[0]);

struct Aircraft_FlightGearBridge_Instance {
  std::string transport = "FlightGearGeneric";
  double reference_latitude_deg = 0.0;
  double reference_longitude_deg = 0.0;
  double reference_altitude_m = 0.0;
  std::string remote_host = "127.0.0.1";
  int telemetry_port = 5501;
  int control_port = 5502;
  Aircraft_PositionXYZ statePosition = {};
  Aircraft_OrientationEuler stateOrientation = {};
  Aircraft_FlightStatusPacket flightStatus = {};
  Aircraft_MissionStatus missionStatus = {};
  Aircraft_PilotCommand pilotCommand = {};
};

inline constexpr Aircraft_FieldBinding Aircraft_FlightGearBridge_Bindings[] = {
  {AIRCRAFT_FLIGHTGEARBRIDGE_VR_TRANSPORT, AIRCRAFT_SCALAR_STRING, offsetof(Aircraft_FlightGearBridge_Instance, transport), true},
  {AIRCRAFT_FLIGHTGEARBRIDGE_VR_REFERENCE_LATITUDE_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_FlightGearBridge_Instance, reference_latitude_deg), true},
  {AIRCRAFT_FLIGHTGEARBRIDGE_VR_REFERENCE_LONGITUDE_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_FlightGearBridge_Instance, reference_longitude_deg), true},
  {AIRCRAFT_FLIGHTGEARBRIDGE_VR_REFERENCE_ALTITUDE_M, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_FlightGearBridge_Instance, reference_altitude_m), true},
  {AIRCRAFT_FLIGHTGEARBRIDGE_VR_REMOTE_HOST, AIRCRAFT_SCALAR_STRING, offsetof(Aircraft_FlightGearBridge_Instance, remote_host), true},
  {AIRCRAFT_FLIGHTGEARBRIDGE_VR_TELEMETRY_PORT, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_FlightGearBridge_Instance, telemetry_port), true},
  {AIRCRAFT_FLIGHTGEARBRIDGE_VR_CONTROL_PORT, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_FlightGearBridge_Instance, control_port), true},
  {AIRCRAFT_FLIGHTGEARBRIDGE_VR_STATEPOSITION_X_KM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_FlightGearBridge_Instance, statePosition) + offsetof(Aircraft_PositionXYZ, x_km), true},
  {AIRCRAFT_FLIGHTGEARBRIDGE_VR_STATEPOSITION_Y_KM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_FlightGearBridge_Instance, statePosition) + offsetof(Aircraft_PositionXYZ, y_km), true},
  {AIRCRAFT_FLIGHTGEARBRIDGE_VR_STATEPOSITION_Z_KM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_FlightGearBridge_Instance, statePosition) + offsetof(Aircraft_PositionXYZ, z_km), true},
  {AIRCRAFT_FLIGHTGEARBRIDGE_VR_STATEORIENTATION_ROLL_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_FlightGearBridge_Instance, stateOrientation) + offsetof(Aircraft_OrientationEuler, roll_deg), true},
  {AIRCRAFT_FLIGHTGEARBRIDGE_VR_STATEORIENTATION_PITCH_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_FlightGearBridge_Instance, stateOrientation) + offsetof(Aircraft_OrientationEuler, pitch_deg), true},
  {AIRCRAFT_FLIGHTGEARBRIDGE_VR_STATEORIENTATION_YAW_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_FlightGearBridge_Instance, stateOrientation) + offsetof(Aircraft_OrientationEuler, yaw_deg), true},
  {AIRCRAFT_FLIGHTGEARBRIDGE_VR_FLIGHTSTATUS_AIRSPEED_MPS, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_FlightGearBridge_Instance, flightStatus) + offsetof(Aircraft_FlightStatusPacket, airspeed_mps), true},
  {AIRCRAFT_FLIGHTGEARBRIDGE_VR_FLIGHTSTATUS_ENERGY_STATE_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_FlightGearBridge_Instance, flightStatus) + offsetof(Aircraft_FlightStatusPacket, energy_state_norm), true},
  {AIRCRAFT_FLIGHTGEARBRIDGE_VR_FLIGHTSTATUS_ANGLE_OF_ATTACK_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_FlightGearBridge_Instance, flightStatus) + offsetof(Aircraft_FlightStatusPacket, angle_of_attack_deg), true},
  {AIRCRAFT_FLIGHTGEARBRIDGE_VR_FLIGHTSTATUS_CLIMB_RATE, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_FlightGearBridge_Instance, flightStatus) + offsetof(Aircraft_FlightStatusPacket, climb_rate), true},
  {AIRCRAFT_FLIGHTGEARBRIDGE_VR_FLIGHTSTATUS_HEALTH_CODE, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_FlightGearBridge_Instance, flightStatus) + offsetof(Aircraft_FlightStatusPacket, health_code), true},
  {AIRCRAFT_FLIGHTGEARBRIDGE_VR_MISSIONSTATUS_WAYPOINT_INDEX, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_FlightGearBridge_Instance, missionStatus) + offsetof(Aircraft_MissionStatus, waypoint_index), true},
  {AIRCRAFT_FLIGHTGEARBRIDGE_VR_MISSIONSTATUS_TOTAL_WAYPOINTS, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_FlightGearBridge_Instance, missionStatus) + offsetof(Aircraft_MissionStatus, total_waypoints), true},
  {AIRCRAFT_FLIGHTGEARBRIDGE_VR_MISSIONSTATUS_DISTANCE_TO_WAYPOINT_KM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_FlightGearBridge_Instance, missionStatus) + offsetof(Aircraft_MissionStatus, distance_to_waypoint_km), true},
  {AIRCRAFT_FLIGHTGEARBRIDGE_VR_MISSIONSTATUS_ARRIVED, AIRCRAFT_SCALAR_BOOLEAN, offsetof(Aircraft_FlightGearBridge_Instance, missionStatus) + offsetof(Aircraft_MissionStatus, arrived), true},
  {AIRCRAFT_FLIGHTGEARBRIDGE_VR_MISSIONSTATUS_COMPLETE, AIRCRAFT_SCALAR_BOOLEAN, offsetof(Aircraft_FlightGearBridge_Instance, missionStatus) + offsetof(Aircraft_MissionStatus, complete), true},
  {AIRCRAFT_FLIGHTGEARBRIDGE_VR_PILOTCOMMAND_STICK_PITCH_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_FlightGearBridge_Instance, pilotCommand) + offsetof(Aircraft_PilotCommand, stick_pitch_norm), false},
  {AIRCRAFT_FLIGHTGEARBRIDGE_VR_PILOTCOMMAND_STICK_ROLL_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_FlightGearBridge_Instance, pilotCommand) + offsetof(Aircraft_PilotCommand, stick_roll_norm), false},
  {AIRCRAFT_FLIGHTGEARBRIDGE_VR_PILOTCOMMAND_RUDDER_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_FlightGearBridge_Instance, pilotCommand) + offsetof(Aircraft_PilotCommand, rudder_norm), false},
  {AIRCRAFT_FLIGHTGEARBRIDGE_VR_PILOTCOMMAND_THROTTLE_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_FlightGearBridge_Instance, pilotCommand) + offsetof(Aircraft_PilotCommand, throttle_norm), false},
  {AIRCRAFT_FLIGHTGEARBRIDGE_VR_PILOTCOMMAND_THROTTLE_AUX_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_FlightGearBridge_Instance, pilotCommand) + offsetof(Aircraft_PilotCommand, throttle_aux_norm), false},
  {AIRCRAFT_FLIGHTGEARBRIDGE_VR_PILOTCOMMAND_BUTTON_MASK, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_FlightGearBridge_Instance, pilotCommand) + offsetof(Aircraft_PilotCommand, button_mask), false},
  {AIRCRAFT_FLIGHTGEARBRIDGE_VR_PILOTCOMMAND_HAT_X, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_FlightGearBridge_Instance, pilotCommand) + offsetof(Aircraft_PilotCommand, hat_x), false},
  {AIRCRAFT_FLIGHTGEARBRIDGE_VR_PILOTCOMMAND_HAT_Y, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_FlightGearBridge_Instance, pilotCommand) + offsetof(Aircraft_PilotCommand, hat_y), false},
  {AIRCRAFT_FLIGHTGEARBRIDGE_VR_PILOTCOMMAND_MODE_SWITCH, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_FlightGearBridge_Instance, pilotCommand) + offsetof(Aircraft_PilotCommand, mode_switch), false},
  {AIRCRAFT_FLIGHTGEARBRIDGE_VR_PILOTCOMMAND_RESERVED, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_FlightGearBridge_Instance, pilotCommand) + offsetof(Aircraft_PilotCommand, reserved), false},
};
inline constexpr size_t Aircraft_FlightGearBridge_BindingCount = sizeof(Aircraft_FlightGearBridge_Bindings) / sizeof(Aircraft_FlightGearBridge_Bindings[0]);

struct Aircraft_AutopilotModule_Instance {
  std::string comment = "uses waypoint tracking";
  int waypointCount = 10;
  int waypointProximity_km = 10;
  double waypointX_km = {};
  double waypointY_km = {};
  double waypointZ_km = {};
  Aircraft_FlightStatusPacket feedbackBus = {};
  Aircraft_PositionXYZ currentLocation = {};
  Aircraft_OrientationEuler currentOrientation = {};
  Aircraft_PilotCommand autopilotCmd = {};
  Aircraft_MissionStatus missionStatus = {};
};

inline constexpr Aircraft_FieldBinding Aircraft_AutopilotModule_Bindings[] = {
  {AIRCRAFT_AUTOPILOTMODULE_VR_COMMENT, AIRCRAFT_SCALAR_STRING, offsetof(Aircraft_AutopilotModule_Instance, comment), true},
  {AIRCRAFT_AUTOPILOTMODULE_VR_WAYPOINTCOUNT, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_AutopilotModule_Instance, waypointCount), true},
  {AIRCRAFT_AUTOPILOTMODULE_VR_WAYPOINTPROXIMITY_KM, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_AutopilotModule_Instance, waypointProximity_km), true},
  {AIRCRAFT_AUTOPILOTMODULE_VR_WAYPOINTX_KM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_AutopilotModule_Instance, waypointX_km), true},
  {AIRCRAFT_AUTOPILOTMODULE_VR_WAYPOINTY_KM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_AutopilotModule_Instance, waypointY_km), true},
  {AIRCRAFT_AUTOPILOTMODULE_VR_WAYPOINTZ_KM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_AutopilotModule_Instance, waypointZ_km), true},
  {AIRCRAFT_AUTOPILOTMODULE_VR_FEEDBACKBUS_AIRSPEED_MPS, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_AutopilotModule_Instance, feedbackBus) + offsetof(Aircraft_FlightStatusPacket, airspeed_mps), true},
  {AIRCRAFT_AUTOPILOTMODULE_VR_FEEDBACKBUS_ENERGY_STATE_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_AutopilotModule_Instance, feedbackBus) + offsetof(Aircraft_FlightStatusPacket, energy_state_norm), true},
  {AIRCRAFT_AUTOPILOTMODULE_VR_FEEDBACKBUS_ANGLE_OF_ATTACK_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_AutopilotModule_Instance, feedbackBus) + offsetof(Aircraft_FlightStatusPacket, angle_of_attack_deg), true},
  {AIRCRAFT_AUTOPILOTMODULE_VR_FEEDBACKBUS_CLIMB_RATE, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_AutopilotModule_Instance, feedbackBus) + offsetof(Aircraft_FlightStatusPacket, climb_rate), true},
  {AIRCRAFT_AUTOPILOTMODULE_VR_FEEDBACKBUS_HEALTH_CODE, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_AutopilotModule_Instance, feedbackBus) + offsetof(Aircraft_FlightStatusPacket, health_code), true},
  {AIRCRAFT_AUTOPILOTMODULE_VR_CURRENTLOCATION_X_KM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_AutopilotModule_Instance, currentLocation) + offsetof(Aircraft_PositionXYZ, x_km), true},
  {AIRCRAFT_AUTOPILOTMODULE_VR_CURRENTLOCATION_Y_KM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_AutopilotModule_Instance, currentLocation) + offsetof(Aircraft_PositionXYZ, y_km), true},
  {AIRCRAFT_AUTOPILOTMODULE_VR_CURRENTLOCATION_Z_KM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_AutopilotModule_Instance, currentLocation) + offsetof(Aircraft_PositionXYZ, z_km), true},
  {AIRCRAFT_AUTOPILOTMODULE_VR_CURRENTORIENTATION_ROLL_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_AutopilotModule_Instance, currentOrientation) + offsetof(Aircraft_OrientationEuler, roll_deg), true},
  {AIRCRAFT_AUTOPILOTMODULE_VR_CURRENTORIENTATION_PITCH_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_AutopilotModule_Instance, currentOrientation) + offsetof(Aircraft_OrientationEuler, pitch_deg), true},
  {AIRCRAFT_AUTOPILOTMODULE_VR_CURRENTORIENTATION_YAW_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_AutopilotModule_Instance, currentOrientation) + offsetof(Aircraft_OrientationEuler, yaw_deg), true},
  {AIRCRAFT_AUTOPILOTMODULE_VR_AUTOPILOTCMD_STICK_PITCH_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_AutopilotModule_Instance, autopilotCmd) + offsetof(Aircraft_PilotCommand, stick_pitch_norm), false},
  {AIRCRAFT_AUTOPILOTMODULE_VR_AUTOPILOTCMD_STICK_ROLL_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_AutopilotModule_Instance, autopilotCmd) + offsetof(Aircraft_PilotCommand, stick_roll_norm), false},
  {AIRCRAFT_AUTOPILOTMODULE_VR_AUTOPILOTCMD_RUDDER_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_AutopilotModule_Instance, autopilotCmd) + offsetof(Aircraft_PilotCommand, rudder_norm), false},
  {AIRCRAFT_AUTOPILOTMODULE_VR_AUTOPILOTCMD_THROTTLE_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_AutopilotModule_Instance, autopilotCmd) + offsetof(Aircraft_PilotCommand, throttle_norm), false},
  {AIRCRAFT_AUTOPILOTMODULE_VR_AUTOPILOTCMD_THROTTLE_AUX_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_AutopilotModule_Instance, autopilotCmd) + offsetof(Aircraft_PilotCommand, throttle_aux_norm), false},
  {AIRCRAFT_AUTOPILOTMODULE_VR_AUTOPILOTCMD_BUTTON_MASK, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_AutopilotModule_Instance, autopilotCmd) + offsetof(Aircraft_PilotCommand, button_mask), false},
  {AIRCRAFT_AUTOPILOTMODULE_VR_AUTOPILOTCMD_HAT_X, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_AutopilotModule_Instance, autopilotCmd) + offsetof(Aircraft_PilotCommand, hat_x), false},
  {AIRCRAFT_AUTOPILOTMODULE_VR_AUTOPILOTCMD_HAT_Y, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_AutopilotModule_Instance, autopilotCmd) + offsetof(Aircraft_PilotCommand, hat_y), false},
  {AIRCRAFT_AUTOPILOTMODULE_VR_AUTOPILOTCMD_MODE_SWITCH, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_AutopilotModule_Instance, autopilotCmd) + offsetof(Aircraft_PilotCommand, mode_switch), false},
  {AIRCRAFT_AUTOPILOTMODULE_VR_AUTOPILOTCMD_RESERVED, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_AutopilotModule_Instance, autopilotCmd) + offsetof(Aircraft_PilotCommand, reserved), false},
  {AIRCRAFT_AUTOPILOTMODULE_VR_MISSIONSTATUS_WAYPOINT_INDEX, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_AutopilotModule_Instance, missionStatus) + offsetof(Aircraft_MissionStatus, waypoint_index), false},
  {AIRCRAFT_AUTOPILOTMODULE_VR_MISSIONSTATUS_TOTAL_WAYPOINTS, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_AutopilotModule_Instance, missionStatus) + offsetof(Aircraft_MissionStatus, total_waypoints), false},
  {AIRCRAFT_AUTOPILOTMODULE_VR_MISSIONSTATUS_DISTANCE_TO_WAYPOINT_KM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_AutopilotModule_Instance, missionStatus) + offsetof(Aircraft_MissionStatus, distance_to_waypoint_km), false},
  {AIRCRAFT_AUTOPILOTMODULE_VR_MISSIONSTATUS_ARRIVED, AIRCRAFT_SCALAR_BOOLEAN, offsetof(Aircraft_AutopilotModule_Instance, missionStatus) + offsetof(Aircraft_MissionStatus, arrived), false},
  {AIRCRAFT_AUTOPILOTMODULE_VR_MISSIONSTATUS_COMPLETE, AIRCRAFT_SCALAR_BOOLEAN, offsetof(Aircraft_AutopilotModule_Instance, missionStatus) + offsetof(Aircraft_MissionStatus, complete), false},
};
inline constexpr size_t Aircraft_AutopilotModule_BindingCount = sizeof(Aircraft_AutopilotModule_Bindings) / sizeof(Aircraft_AutopilotModule_Bindings[0]);

struct Aircraft_CompositeAirframe_Instance {
  double length_m = 15.0;
  double fuselage_width_m = 3.0;
  double wingspan_m = 10.0;
  int empty_weight_kg = 8573;
  int payload_capacity_kg = 7700;
  int hardpoint_count = 9;
};

inline constexpr Aircraft_FieldBinding Aircraft_CompositeAirframe_Bindings[] = {
  {AIRCRAFT_COMPOSITEAIRFRAME_VR_LENGTH_M, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_CompositeAirframe_Instance, length_m), true},
  {AIRCRAFT_COMPOSITEAIRFRAME_VR_FUSELAGE_WIDTH_M, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_CompositeAirframe_Instance, fuselage_width_m), true},
  {AIRCRAFT_COMPOSITEAIRFRAME_VR_WINGSPAN_M, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_CompositeAirframe_Instance, wingspan_m), true},
  {AIRCRAFT_COMPOSITEAIRFRAME_VR_EMPTY_WEIGHT_KG, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_CompositeAirframe_Instance, empty_weight_kg), true},
  {AIRCRAFT_COMPOSITEAIRFRAME_VR_PAYLOAD_CAPACITY_KG, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_CompositeAirframe_Instance, payload_capacity_kg), true},
  {AIRCRAFT_COMPOSITEAIRFRAME_VR_HARDPOINT_COUNT, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_CompositeAirframe_Instance, hardpoint_count), true},
};
inline constexpr size_t Aircraft_CompositeAirframe_BindingCount = sizeof(Aircraft_CompositeAirframe_Bindings) / sizeof(Aircraft_CompositeAirframe_Bindings[0]);

struct Aircraft_TurbofanPropulsion_Instance {
  double max_thrust_kn = 129.7;
  double dry_thrust_kn = 79.0;
  double specific_fuel_consumption = 0.76;
  int fuel_capacity_kg = 3160;
  int generator_output_kw = 80;
  Aircraft_ThrottleCommand throttleCmd = {};
  Aircraft_ThrustState thrustOut = {};
  Aircraft_FuelConsumptionRate fuel_consumption = {};
};

inline constexpr Aircraft_FieldBinding Aircraft_TurbofanPropulsion_Bindings[] = {
  {AIRCRAFT_TURBOFANPROPULSION_VR_MAX_THRUST_KN, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_TurbofanPropulsion_Instance, max_thrust_kn), true},
  {AIRCRAFT_TURBOFANPROPULSION_VR_DRY_THRUST_KN, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_TurbofanPropulsion_Instance, dry_thrust_kn), true},
  {AIRCRAFT_TURBOFANPROPULSION_VR_SPECIFIC_FUEL_CONSUMPTION, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_TurbofanPropulsion_Instance, specific_fuel_consumption), true},
  {AIRCRAFT_TURBOFANPROPULSION_VR_FUEL_CAPACITY_KG, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_TurbofanPropulsion_Instance, fuel_capacity_kg), true},
  {AIRCRAFT_TURBOFANPROPULSION_VR_GENERATOR_OUTPUT_KW, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_TurbofanPropulsion_Instance, generator_output_kw), true},
  {AIRCRAFT_TURBOFANPROPULSION_VR_THROTTLECMD_THROTTLE_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_TurbofanPropulsion_Instance, throttleCmd) + offsetof(Aircraft_ThrottleCommand, throttle_norm), true},
  {AIRCRAFT_TURBOFANPROPULSION_VR_THROTTLECMD_FUEL_ENABLE, AIRCRAFT_SCALAR_BOOLEAN, offsetof(Aircraft_TurbofanPropulsion_Instance, throttleCmd) + offsetof(Aircraft_ThrottleCommand, fuel_enable), true},
  {AIRCRAFT_TURBOFANPROPULSION_VR_THROTTLECMD_AFTERBURNER_ENABLE, AIRCRAFT_SCALAR_BOOLEAN, offsetof(Aircraft_TurbofanPropulsion_Instance, throttleCmd) + offsetof(Aircraft_ThrottleCommand, afterburner_enable), true},
  {AIRCRAFT_TURBOFANPROPULSION_VR_THRUSTOUT_THRUST_KN, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_TurbofanPropulsion_Instance, thrustOut) + offsetof(Aircraft_ThrustState, thrust_kn), false},
  {AIRCRAFT_TURBOFANPROPULSION_VR_THRUSTOUT_MASS_FLOW_KGPS, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_TurbofanPropulsion_Instance, thrustOut) + offsetof(Aircraft_ThrustState, mass_flow_kgps), false},
  {AIRCRAFT_TURBOFANPROPULSION_VR_THRUSTOUT_EXHAUST_VELOCITY_MPS, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_TurbofanPropulsion_Instance, thrustOut) + offsetof(Aircraft_ThrustState, exhaust_velocity_mps), false},
  {AIRCRAFT_TURBOFANPROPULSION_VR_FUEL_CONSUMPTION_MASS_FLOW_KGPS, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_TurbofanPropulsion_Instance, fuel_consumption) + offsetof(Aircraft_FuelConsumptionRate, mass_flow_kgps), false},
};
inline constexpr size_t Aircraft_TurbofanPropulsion_BindingCount = sizeof(Aircraft_TurbofanPropulsion_Bindings) / sizeof(Aircraft_TurbofanPropulsion_Bindings[0]);

struct Aircraft_MissionComputer_Instance {
  Aircraft_PilotCommand manualInput = {};
  Aircraft_PilotCommand autopilotInput = {};
  Aircraft_FuelLevelState fuelStatus = {};
  Aircraft_ThrottleCommand engineThrottle = {};
  Aircraft_OrientationEuler direction_command = {};
};

inline constexpr Aircraft_FieldBinding Aircraft_MissionComputer_Bindings[] = {
  {AIRCRAFT_MISSIONCOMPUTER_VR_MANUALINPUT_STICK_PITCH_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_MissionComputer_Instance, manualInput) + offsetof(Aircraft_PilotCommand, stick_pitch_norm), true},
  {AIRCRAFT_MISSIONCOMPUTER_VR_MANUALINPUT_STICK_ROLL_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_MissionComputer_Instance, manualInput) + offsetof(Aircraft_PilotCommand, stick_roll_norm), true},
  {AIRCRAFT_MISSIONCOMPUTER_VR_MANUALINPUT_RUDDER_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_MissionComputer_Instance, manualInput) + offsetof(Aircraft_PilotCommand, rudder_norm), true},
  {AIRCRAFT_MISSIONCOMPUTER_VR_MANUALINPUT_THROTTLE_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_MissionComputer_Instance, manualInput) + offsetof(Aircraft_PilotCommand, throttle_norm), true},
  {AIRCRAFT_MISSIONCOMPUTER_VR_MANUALINPUT_THROTTLE_AUX_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_MissionComputer_Instance, manualInput) + offsetof(Aircraft_PilotCommand, throttle_aux_norm), true},
  {AIRCRAFT_MISSIONCOMPUTER_VR_MANUALINPUT_BUTTON_MASK, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_MissionComputer_Instance, manualInput) + offsetof(Aircraft_PilotCommand, button_mask), true},
  {AIRCRAFT_MISSIONCOMPUTER_VR_MANUALINPUT_HAT_X, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_MissionComputer_Instance, manualInput) + offsetof(Aircraft_PilotCommand, hat_x), true},
  {AIRCRAFT_MISSIONCOMPUTER_VR_MANUALINPUT_HAT_Y, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_MissionComputer_Instance, manualInput) + offsetof(Aircraft_PilotCommand, hat_y), true},
  {AIRCRAFT_MISSIONCOMPUTER_VR_MANUALINPUT_MODE_SWITCH, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_MissionComputer_Instance, manualInput) + offsetof(Aircraft_PilotCommand, mode_switch), true},
  {AIRCRAFT_MISSIONCOMPUTER_VR_MANUALINPUT_RESERVED, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_MissionComputer_Instance, manualInput) + offsetof(Aircraft_PilotCommand, reserved), true},
  {AIRCRAFT_MISSIONCOMPUTER_VR_AUTOPILOTINPUT_STICK_PITCH_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_MissionComputer_Instance, autopilotInput) + offsetof(Aircraft_PilotCommand, stick_pitch_norm), true},
  {AIRCRAFT_MISSIONCOMPUTER_VR_AUTOPILOTINPUT_STICK_ROLL_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_MissionComputer_Instance, autopilotInput) + offsetof(Aircraft_PilotCommand, stick_roll_norm), true},
  {AIRCRAFT_MISSIONCOMPUTER_VR_AUTOPILOTINPUT_RUDDER_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_MissionComputer_Instance, autopilotInput) + offsetof(Aircraft_PilotCommand, rudder_norm), true},
  {AIRCRAFT_MISSIONCOMPUTER_VR_AUTOPILOTINPUT_THROTTLE_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_MissionComputer_Instance, autopilotInput) + offsetof(Aircraft_PilotCommand, throttle_norm), true},
  {AIRCRAFT_MISSIONCOMPUTER_VR_AUTOPILOTINPUT_THROTTLE_AUX_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_MissionComputer_Instance, autopilotInput) + offsetof(Aircraft_PilotCommand, throttle_aux_norm), true},
  {AIRCRAFT_MISSIONCOMPUTER_VR_AUTOPILOTINPUT_BUTTON_MASK, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_MissionComputer_Instance, autopilotInput) + offsetof(Aircraft_PilotCommand, button_mask), true},
  {AIRCRAFT_MISSIONCOMPUTER_VR_AUTOPILOTINPUT_HAT_X, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_MissionComputer_Instance, autopilotInput) + offsetof(Aircraft_PilotCommand, hat_x), true},
  {AIRCRAFT_MISSIONCOMPUTER_VR_AUTOPILOTINPUT_HAT_Y, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_MissionComputer_Instance, autopilotInput) + offsetof(Aircraft_PilotCommand, hat_y), true},
  {AIRCRAFT_MISSIONCOMPUTER_VR_AUTOPILOTINPUT_MODE_SWITCH, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_MissionComputer_Instance, autopilotInput) + offsetof(Aircraft_PilotCommand, mode_switch), true},
  {AIRCRAFT_MISSIONCOMPUTER_VR_AUTOPILOTINPUT_RESERVED, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_MissionComputer_Instance, autopilotInput) + offsetof(Aircraft_PilotCommand, reserved), true},
  {AIRCRAFT_MISSIONCOMPUTER_VR_FUELSTATUS_FUEL_REMAINING_KG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_MissionComputer_Instance, fuelStatus) + offsetof(Aircraft_FuelLevelState, fuel_remaining_kg), true},
  {AIRCRAFT_MISSIONCOMPUTER_VR_FUELSTATUS_FUEL_LEVEL_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_MissionComputer_Instance, fuelStatus) + offsetof(Aircraft_FuelLevelState, fuel_level_norm), true},
  {AIRCRAFT_MISSIONCOMPUTER_VR_FUELSTATUS_FUEL_STARVED, AIRCRAFT_SCALAR_BOOLEAN, offsetof(Aircraft_MissionComputer_Instance, fuelStatus) + offsetof(Aircraft_FuelLevelState, fuel_starved), true},
  {AIRCRAFT_MISSIONCOMPUTER_VR_ENGINETHROTTLE_THROTTLE_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_MissionComputer_Instance, engineThrottle) + offsetof(Aircraft_ThrottleCommand, throttle_norm), false},
  {AIRCRAFT_MISSIONCOMPUTER_VR_ENGINETHROTTLE_FUEL_ENABLE, AIRCRAFT_SCALAR_BOOLEAN, offsetof(Aircraft_MissionComputer_Instance, engineThrottle) + offsetof(Aircraft_ThrottleCommand, fuel_enable), false},
  {AIRCRAFT_MISSIONCOMPUTER_VR_ENGINETHROTTLE_AFTERBURNER_ENABLE, AIRCRAFT_SCALAR_BOOLEAN, offsetof(Aircraft_MissionComputer_Instance, engineThrottle) + offsetof(Aircraft_ThrottleCommand, afterburner_enable), false},
  {AIRCRAFT_MISSIONCOMPUTER_VR_DIRECTION_COMMAND_ROLL_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_MissionComputer_Instance, direction_command) + offsetof(Aircraft_OrientationEuler, roll_deg), false},
  {AIRCRAFT_MISSIONCOMPUTER_VR_DIRECTION_COMMAND_PITCH_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_MissionComputer_Instance, direction_command) + offsetof(Aircraft_OrientationEuler, pitch_deg), false},
  {AIRCRAFT_MISSIONCOMPUTER_VR_DIRECTION_COMMAND_YAW_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_MissionComputer_Instance, direction_command) + offsetof(Aircraft_OrientationEuler, yaw_deg), false},
};
inline constexpr size_t Aircraft_MissionComputer_BindingCount = sizeof(Aircraft_MissionComputer_Bindings) / sizeof(Aircraft_MissionComputer_Bindings[0]);

struct Aircraft_FuelSystem_Instance {
  int fuel_capacity_kg = 3160;
  double reserve_fraction = 0.08;
  Aircraft_FuelConsumptionRate fuel_consumption_rate = {};
  Aircraft_FuelLevelState fuelState = {};
};

inline constexpr Aircraft_FieldBinding Aircraft_FuelSystem_Bindings[] = {
  {AIRCRAFT_FUELSYSTEM_VR_FUEL_CAPACITY_KG, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_FuelSystem_Instance, fuel_capacity_kg), true},
  {AIRCRAFT_FUELSYSTEM_VR_RESERVE_FRACTION, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_FuelSystem_Instance, reserve_fraction), true},
  {AIRCRAFT_FUELSYSTEM_VR_FUEL_CONSUMPTION_RATE_MASS_FLOW_KGPS, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_FuelSystem_Instance, fuel_consumption_rate) + offsetof(Aircraft_FuelConsumptionRate, mass_flow_kgps), true},
  {AIRCRAFT_FUELSYSTEM_VR_FUELSTATE_FUEL_REMAINING_KG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_FuelSystem_Instance, fuelState) + offsetof(Aircraft_FuelLevelState, fuel_remaining_kg), false},
  {AIRCRAFT_FUELSYSTEM_VR_FUELSTATE_FUEL_LEVEL_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_FuelSystem_Instance, fuelState) + offsetof(Aircraft_FuelLevelState, fuel_level_norm), false},
  {AIRCRAFT_FUELSYSTEM_VR_FUELSTATE_FUEL_STARVED, AIRCRAFT_SCALAR_BOOLEAN, offsetof(Aircraft_FuelSystem_Instance, fuelState) + offsetof(Aircraft_FuelLevelState, fuel_starved), false},
};
inline constexpr size_t Aircraft_FuelSystem_BindingCount = sizeof(Aircraft_FuelSystem_Bindings) / sizeof(Aircraft_FuelSystem_Bindings[0]);

struct Aircraft_AdaptiveWingSystem_Instance {
  double reference_area_m2 = 28.0;
  double span_m = 10.0;
  double aspect_ratio = 3.6;
  int control_authority_deg = 25;
  int load_factor_limit_g = 9;
  Aircraft_OrientationEuler direction_command = {};
  Aircraft_FlightStatusPacket flight_speed = {};
  Aircraft_SurfaceActuationCommand actuation_command = {};
  Aircraft_LiftState liftInterface = {};
};

inline constexpr Aircraft_FieldBinding Aircraft_AdaptiveWingSystem_Bindings[] = {
  {AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_REFERENCE_AREA_M2, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_AdaptiveWingSystem_Instance, reference_area_m2), true},
  {AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_SPAN_M, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_AdaptiveWingSystem_Instance, span_m), true},
  {AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_ASPECT_RATIO, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_AdaptiveWingSystem_Instance, aspect_ratio), true},
  {AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_CONTROL_AUTHORITY_DEG, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_AdaptiveWingSystem_Instance, control_authority_deg), true},
  {AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_LOAD_FACTOR_LIMIT_G, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_AdaptiveWingSystem_Instance, load_factor_limit_g), true},
  {AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_DIRECTION_COMMAND_ROLL_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_AdaptiveWingSystem_Instance, direction_command) + offsetof(Aircraft_OrientationEuler, roll_deg), true},
  {AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_DIRECTION_COMMAND_PITCH_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_AdaptiveWingSystem_Instance, direction_command) + offsetof(Aircraft_OrientationEuler, pitch_deg), true},
  {AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_DIRECTION_COMMAND_YAW_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_AdaptiveWingSystem_Instance, direction_command) + offsetof(Aircraft_OrientationEuler, yaw_deg), true},
  {AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_FLIGHT_SPEED_AIRSPEED_MPS, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_AdaptiveWingSystem_Instance, flight_speed) + offsetof(Aircraft_FlightStatusPacket, airspeed_mps), true},
  {AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_FLIGHT_SPEED_ENERGY_STATE_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_AdaptiveWingSystem_Instance, flight_speed) + offsetof(Aircraft_FlightStatusPacket, energy_state_norm), true},
  {AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_FLIGHT_SPEED_ANGLE_OF_ATTACK_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_AdaptiveWingSystem_Instance, flight_speed) + offsetof(Aircraft_FlightStatusPacket, angle_of_attack_deg), true},
  {AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_FLIGHT_SPEED_CLIMB_RATE, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_AdaptiveWingSystem_Instance, flight_speed) + offsetof(Aircraft_FlightStatusPacket, climb_rate), true},
  {AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_FLIGHT_SPEED_HEALTH_CODE, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_AdaptiveWingSystem_Instance, flight_speed) + offsetof(Aircraft_FlightStatusPacket, health_code), true},
  {AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_ACTUATION_COMMAND_LEFT_AILERON_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_AdaptiveWingSystem_Instance, actuation_command) + offsetof(Aircraft_SurfaceActuationCommand, left_aileron_deg), false},
  {AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_ACTUATION_COMMAND_RIGHT_AILERON_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_AdaptiveWingSystem_Instance, actuation_command) + offsetof(Aircraft_SurfaceActuationCommand, right_aileron_deg), false},
  {AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_ACTUATION_COMMAND_ELEVATOR_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_AdaptiveWingSystem_Instance, actuation_command) + offsetof(Aircraft_SurfaceActuationCommand, elevator_deg), false},
  {AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_ACTUATION_COMMAND_RUDDER_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_AdaptiveWingSystem_Instance, actuation_command) + offsetof(Aircraft_SurfaceActuationCommand, rudder_deg), false},
  {AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_ACTUATION_COMMAND_FLAPERON_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_AdaptiveWingSystem_Instance, actuation_command) + offsetof(Aircraft_SurfaceActuationCommand, flaperon_deg), false},
  {AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_LIFTINTERFACE_LIFT_KN, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_AdaptiveWingSystem_Instance, liftInterface) + offsetof(Aircraft_LiftState, lift_kn), false},
  {AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_LIFTINTERFACE_DRAG_KN, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_AdaptiveWingSystem_Instance, liftInterface) + offsetof(Aircraft_LiftState, drag_kn), false},
  {AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_LIFTINTERFACE_PITCHING_MOMENT_KNM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_AdaptiveWingSystem_Instance, liftInterface) + offsetof(Aircraft_LiftState, pitching_moment_knm), false},
};
inline constexpr size_t Aircraft_AdaptiveWingSystem_BindingCount = sizeof(Aircraft_AdaptiveWingSystem_Bindings) / sizeof(Aircraft_AdaptiveWingSystem_Bindings[0]);

struct Aircraft_Environment_Instance {
  Aircraft_SurfaceActuationCommand actuation_command = {};
  Aircraft_OrientationEuler direction_command = {};
  Aircraft_LiftState lift = {};
  Aircraft_ThrustState thrust_in = {};
  Aircraft_OrientationEuler orientation = {};
  Aircraft_PositionXYZ location = {};
  Aircraft_FlightStatusPacket flight_status = {};
};

inline constexpr Aircraft_FieldBinding Aircraft_Environment_Bindings[] = {
  {AIRCRAFT_ENVIRONMENT_VR_ACTUATION_COMMAND_LEFT_AILERON_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_Environment_Instance, actuation_command) + offsetof(Aircraft_SurfaceActuationCommand, left_aileron_deg), true},
  {AIRCRAFT_ENVIRONMENT_VR_ACTUATION_COMMAND_RIGHT_AILERON_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_Environment_Instance, actuation_command) + offsetof(Aircraft_SurfaceActuationCommand, right_aileron_deg), true},
  {AIRCRAFT_ENVIRONMENT_VR_ACTUATION_COMMAND_ELEVATOR_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_Environment_Instance, actuation_command) + offsetof(Aircraft_SurfaceActuationCommand, elevator_deg), true},
  {AIRCRAFT_ENVIRONMENT_VR_ACTUATION_COMMAND_RUDDER_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_Environment_Instance, actuation_command) + offsetof(Aircraft_SurfaceActuationCommand, rudder_deg), true},
  {AIRCRAFT_ENVIRONMENT_VR_ACTUATION_COMMAND_FLAPERON_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_Environment_Instance, actuation_command) + offsetof(Aircraft_SurfaceActuationCommand, flaperon_deg), true},
  {AIRCRAFT_ENVIRONMENT_VR_DIRECTION_COMMAND_ROLL_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_Environment_Instance, direction_command) + offsetof(Aircraft_OrientationEuler, roll_deg), true},
  {AIRCRAFT_ENVIRONMENT_VR_DIRECTION_COMMAND_PITCH_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_Environment_Instance, direction_command) + offsetof(Aircraft_OrientationEuler, pitch_deg), true},
  {AIRCRAFT_ENVIRONMENT_VR_DIRECTION_COMMAND_YAW_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_Environment_Instance, direction_command) + offsetof(Aircraft_OrientationEuler, yaw_deg), true},
  {AIRCRAFT_ENVIRONMENT_VR_LIFT_LIFT_KN, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_Environment_Instance, lift) + offsetof(Aircraft_LiftState, lift_kn), true},
  {AIRCRAFT_ENVIRONMENT_VR_LIFT_DRAG_KN, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_Environment_Instance, lift) + offsetof(Aircraft_LiftState, drag_kn), true},
  {AIRCRAFT_ENVIRONMENT_VR_LIFT_PITCHING_MOMENT_KNM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_Environment_Instance, lift) + offsetof(Aircraft_LiftState, pitching_moment_knm), true},
  {AIRCRAFT_ENVIRONMENT_VR_THRUST_IN_THRUST_KN, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_Environment_Instance, thrust_in) + offsetof(Aircraft_ThrustState, thrust_kn), true},
  {AIRCRAFT_ENVIRONMENT_VR_THRUST_IN_MASS_FLOW_KGPS, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_Environment_Instance, thrust_in) + offsetof(Aircraft_ThrustState, mass_flow_kgps), true},
  {AIRCRAFT_ENVIRONMENT_VR_THRUST_IN_EXHAUST_VELOCITY_MPS, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_Environment_Instance, thrust_in) + offsetof(Aircraft_ThrustState, exhaust_velocity_mps), true},
  {AIRCRAFT_ENVIRONMENT_VR_ORIENTATION_ROLL_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_Environment_Instance, orientation) + offsetof(Aircraft_OrientationEuler, roll_deg), false},
  {AIRCRAFT_ENVIRONMENT_VR_ORIENTATION_PITCH_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_Environment_Instance, orientation) + offsetof(Aircraft_OrientationEuler, pitch_deg), false},
  {AIRCRAFT_ENVIRONMENT_VR_ORIENTATION_YAW_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_Environment_Instance, orientation) + offsetof(Aircraft_OrientationEuler, yaw_deg), false},
  {AIRCRAFT_ENVIRONMENT_VR_LOCATION_X_KM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_Environment_Instance, location) + offsetof(Aircraft_PositionXYZ, x_km), false},
  {AIRCRAFT_ENVIRONMENT_VR_LOCATION_Y_KM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_Environment_Instance, location) + offsetof(Aircraft_PositionXYZ, y_km), false},
  {AIRCRAFT_ENVIRONMENT_VR_LOCATION_Z_KM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_Environment_Instance, location) + offsetof(Aircraft_PositionXYZ, z_km), false},
  {AIRCRAFT_ENVIRONMENT_VR_FLIGHT_STATUS_AIRSPEED_MPS, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_Environment_Instance, flight_status) + offsetof(Aircraft_FlightStatusPacket, airspeed_mps), false},
  {AIRCRAFT_ENVIRONMENT_VR_FLIGHT_STATUS_ENERGY_STATE_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_Environment_Instance, flight_status) + offsetof(Aircraft_FlightStatusPacket, energy_state_norm), false},
  {AIRCRAFT_ENVIRONMENT_VR_FLIGHT_STATUS_ANGLE_OF_ATTACK_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_Environment_Instance, flight_status) + offsetof(Aircraft_FlightStatusPacket, angle_of_attack_deg), false},
  {AIRCRAFT_ENVIRONMENT_VR_FLIGHT_STATUS_CLIMB_RATE, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_Environment_Instance, flight_status) + offsetof(Aircraft_FlightStatusPacket, climb_rate), false},
  {AIRCRAFT_ENVIRONMENT_VR_FLIGHT_STATUS_HEALTH_CODE, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_Environment_Instance, flight_status) + offsetof(Aircraft_FlightStatusPacket, health_code), false},
};
inline constexpr size_t Aircraft_Environment_BindingCount = sizeof(Aircraft_Environment_Bindings) / sizeof(Aircraft_Environment_Bindings[0]);

struct Aircraft_InputOutput_Instance {
  Aircraft_PositionXYZ locationXYZ = {};
  Aircraft_OrientationEuler orientation = {};
  Aircraft_PilotCommand autopilotCmd = {};
  Aircraft_FlightStatusPacket flightStatus = {};
  Aircraft_MissionStatus missionStatus = {};
};

inline constexpr Aircraft_FieldBinding Aircraft_InputOutput_Bindings[] = {
  {AIRCRAFT_INPUTOUTPUT_VR_LOCATIONXYZ_X_KM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_InputOutput_Instance, locationXYZ) + offsetof(Aircraft_PositionXYZ, x_km), true},
  {AIRCRAFT_INPUTOUTPUT_VR_LOCATIONXYZ_Y_KM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_InputOutput_Instance, locationXYZ) + offsetof(Aircraft_PositionXYZ, y_km), true},
  {AIRCRAFT_INPUTOUTPUT_VR_LOCATIONXYZ_Z_KM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_InputOutput_Instance, locationXYZ) + offsetof(Aircraft_PositionXYZ, z_km), true},
  {AIRCRAFT_INPUTOUTPUT_VR_ORIENTATION_ROLL_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_InputOutput_Instance, orientation) + offsetof(Aircraft_OrientationEuler, roll_deg), true},
  {AIRCRAFT_INPUTOUTPUT_VR_ORIENTATION_PITCH_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_InputOutput_Instance, orientation) + offsetof(Aircraft_OrientationEuler, pitch_deg), true},
  {AIRCRAFT_INPUTOUTPUT_VR_ORIENTATION_YAW_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_InputOutput_Instance, orientation) + offsetof(Aircraft_OrientationEuler, yaw_deg), true},
  {AIRCRAFT_INPUTOUTPUT_VR_AUTOPILOTCMD_STICK_PITCH_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_InputOutput_Instance, autopilotCmd) + offsetof(Aircraft_PilotCommand, stick_pitch_norm), true},
  {AIRCRAFT_INPUTOUTPUT_VR_AUTOPILOTCMD_STICK_ROLL_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_InputOutput_Instance, autopilotCmd) + offsetof(Aircraft_PilotCommand, stick_roll_norm), true},
  {AIRCRAFT_INPUTOUTPUT_VR_AUTOPILOTCMD_RUDDER_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_InputOutput_Instance, autopilotCmd) + offsetof(Aircraft_PilotCommand, rudder_norm), true},
  {AIRCRAFT_INPUTOUTPUT_VR_AUTOPILOTCMD_THROTTLE_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_InputOutput_Instance, autopilotCmd) + offsetof(Aircraft_PilotCommand, throttle_norm), true},
  {AIRCRAFT_INPUTOUTPUT_VR_AUTOPILOTCMD_THROTTLE_AUX_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_InputOutput_Instance, autopilotCmd) + offsetof(Aircraft_PilotCommand, throttle_aux_norm), true},
  {AIRCRAFT_INPUTOUTPUT_VR_AUTOPILOTCMD_BUTTON_MASK, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_InputOutput_Instance, autopilotCmd) + offsetof(Aircraft_PilotCommand, button_mask), true},
  {AIRCRAFT_INPUTOUTPUT_VR_AUTOPILOTCMD_HAT_X, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_InputOutput_Instance, autopilotCmd) + offsetof(Aircraft_PilotCommand, hat_x), true},
  {AIRCRAFT_INPUTOUTPUT_VR_AUTOPILOTCMD_HAT_Y, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_InputOutput_Instance, autopilotCmd) + offsetof(Aircraft_PilotCommand, hat_y), true},
  {AIRCRAFT_INPUTOUTPUT_VR_AUTOPILOTCMD_MODE_SWITCH, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_InputOutput_Instance, autopilotCmd) + offsetof(Aircraft_PilotCommand, mode_switch), true},
  {AIRCRAFT_INPUTOUTPUT_VR_AUTOPILOTCMD_RESERVED, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_InputOutput_Instance, autopilotCmd) + offsetof(Aircraft_PilotCommand, reserved), true},
  {AIRCRAFT_INPUTOUTPUT_VR_FLIGHTSTATUS_AIRSPEED_MPS, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_InputOutput_Instance, flightStatus) + offsetof(Aircraft_FlightStatusPacket, airspeed_mps), true},
  {AIRCRAFT_INPUTOUTPUT_VR_FLIGHTSTATUS_ENERGY_STATE_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_InputOutput_Instance, flightStatus) + offsetof(Aircraft_FlightStatusPacket, energy_state_norm), true},
  {AIRCRAFT_INPUTOUTPUT_VR_FLIGHTSTATUS_ANGLE_OF_ATTACK_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_InputOutput_Instance, flightStatus) + offsetof(Aircraft_FlightStatusPacket, angle_of_attack_deg), true},
  {AIRCRAFT_INPUTOUTPUT_VR_FLIGHTSTATUS_CLIMB_RATE, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_InputOutput_Instance, flightStatus) + offsetof(Aircraft_FlightStatusPacket, climb_rate), true},
  {AIRCRAFT_INPUTOUTPUT_VR_FLIGHTSTATUS_HEALTH_CODE, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_InputOutput_Instance, flightStatus) + offsetof(Aircraft_FlightStatusPacket, health_code), true},
  {AIRCRAFT_INPUTOUTPUT_VR_MISSIONSTATUS_WAYPOINT_INDEX, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_InputOutput_Instance, missionStatus) + offsetof(Aircraft_MissionStatus, waypoint_index), true},
  {AIRCRAFT_INPUTOUTPUT_VR_MISSIONSTATUS_TOTAL_WAYPOINTS, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_InputOutput_Instance, missionStatus) + offsetof(Aircraft_MissionStatus, total_waypoints), true},
  {AIRCRAFT_INPUTOUTPUT_VR_MISSIONSTATUS_DISTANCE_TO_WAYPOINT_KM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_InputOutput_Instance, missionStatus) + offsetof(Aircraft_MissionStatus, distance_to_waypoint_km), true},
  {AIRCRAFT_INPUTOUTPUT_VR_MISSIONSTATUS_ARRIVED, AIRCRAFT_SCALAR_BOOLEAN, offsetof(Aircraft_InputOutput_Instance, missionStatus) + offsetof(Aircraft_MissionStatus, arrived), true},
  {AIRCRAFT_INPUTOUTPUT_VR_MISSIONSTATUS_COMPLETE, AIRCRAFT_SCALAR_BOOLEAN, offsetof(Aircraft_InputOutput_Instance, missionStatus) + offsetof(Aircraft_MissionStatus, complete), true},
};
inline constexpr size_t Aircraft_InputOutput_BindingCount = sizeof(Aircraft_InputOutput_Bindings) / sizeof(Aircraft_InputOutput_Bindings[0]);

#endif  /* __cplusplus */