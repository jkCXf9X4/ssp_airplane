#pragma once

#include "Aircraft_InterfaceCommon.h"

/* Generated interface for Aircraft.FlightGearBridge. Do not edit manually. */

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

#ifdef __cplusplus

struct Aircraft_FlightGearBridge_Instance {
  void* vr_map[33];
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

inline const std::string& Aircraft_FlightGearBridge_TRANSPORT_get(const void* instance) { return static_cast<const Aircraft_FlightGearBridge_Instance*>(instance)->transport; }
inline std::string& Aircraft_FlightGearBridge_TRANSPORT_get_mut(void* instance) { return static_cast<Aircraft_FlightGearBridge_Instance*>(instance)->transport; }
inline const std::string& Aircraft_FlightGearBridge_REMOTE_HOST_get(const void* instance) { return static_cast<const Aircraft_FlightGearBridge_Instance*>(instance)->remote_host; }
inline std::string& Aircraft_FlightGearBridge_REMOTE_HOST_get_mut(void* instance) { return static_cast<Aircraft_FlightGearBridge_Instance*>(instance)->remote_host; }

inline constexpr Aircraft_FieldBinding Aircraft_FlightGearBridge_Bindings[] = {
  {AIRCRAFT_FLIGHTGEARBRIDGE_VR_REFERENCE_LATITUDE_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_FlightGearBridge_Instance, reference_latitude_deg), true},
  {AIRCRAFT_FLIGHTGEARBRIDGE_VR_REFERENCE_LONGITUDE_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_FlightGearBridge_Instance, reference_longitude_deg), true},
  {AIRCRAFT_FLIGHTGEARBRIDGE_VR_REFERENCE_ALTITUDE_M, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_FlightGearBridge_Instance, reference_altitude_m), true},
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

inline constexpr Aircraft_StringFieldBinding Aircraft_FlightGearBridge_StringBindings[] = {
  {AIRCRAFT_FLIGHTGEARBRIDGE_VR_TRANSPORT, &Aircraft_FlightGearBridge_TRANSPORT_get, &Aircraft_FlightGearBridge_TRANSPORT_get_mut, true},
  {AIRCRAFT_FLIGHTGEARBRIDGE_VR_REMOTE_HOST, &Aircraft_FlightGearBridge_REMOTE_HOST_get, &Aircraft_FlightGearBridge_REMOTE_HOST_get_mut, true},
};
inline constexpr size_t Aircraft_FlightGearBridge_StringBindingCount = sizeof(Aircraft_FlightGearBridge_StringBindings) / sizeof(Aircraft_FlightGearBridge_StringBindings[0]);

#endif  /* __cplusplus */