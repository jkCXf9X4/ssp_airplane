#pragma once

#include "Aircraft_InterfaceCommon.h"

/* Generated interface for Aircraft.InputOutput. Do not edit manually. */

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

inline constexpr const Aircraft_StringFieldBinding* Aircraft_InputOutput_StringBindings = nullptr;
inline constexpr size_t Aircraft_InputOutput_StringBindingCount = 0;

#endif  /* __cplusplus */