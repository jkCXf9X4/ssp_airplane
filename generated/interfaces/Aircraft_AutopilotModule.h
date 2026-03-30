#pragma once

#include "Aircraft_InterfaceCommon.h"

/* Generated interface for Aircraft.AutopilotModule. Do not edit manually. */

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

#ifdef __cplusplus

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

inline const std::string& Aircraft_AutopilotModule_COMMENT_get(const void* instance) { return static_cast<const Aircraft_AutopilotModule_Instance*>(instance)->comment; }
inline std::string& Aircraft_AutopilotModule_COMMENT_get_mut(void* instance) { return static_cast<Aircraft_AutopilotModule_Instance*>(instance)->comment; }

inline constexpr Aircraft_FieldBinding Aircraft_AutopilotModule_Bindings[] = {
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

inline constexpr Aircraft_StringFieldBinding Aircraft_AutopilotModule_StringBindings[] = {
  {AIRCRAFT_AUTOPILOTMODULE_VR_COMMENT, &Aircraft_AutopilotModule_COMMENT_get, &Aircraft_AutopilotModule_COMMENT_get_mut, true},
};
inline constexpr size_t Aircraft_AutopilotModule_StringBindingCount = sizeof(Aircraft_AutopilotModule_StringBindings) / sizeof(Aircraft_AutopilotModule_StringBindings[0]);

#endif  /* __cplusplus */