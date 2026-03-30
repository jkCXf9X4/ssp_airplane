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

inline constexpr size_t Aircraft_AutopilotModule_VrCount = 32;

struct Aircraft_AutopilotModule_Instance {
  Aircraft_VrMapping vr_map[32] = {};
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

inline void Aircraft_AutopilotModule_initialize_vr_map(Aircraft_AutopilotModule_Instance* instance) {
  for (size_t i = 0; i < Aircraft_AutopilotModule_VrCount; ++i) {
    instance->vr_map[i] = {nullptr, AIRCRAFT_DATA_NONE, false};
  }
  instance->vr_map[AIRCRAFT_AUTOPILOTMODULE_VR_COMMENT] = {&instance->comment, AIRCRAFT_DATA_STRING, true};
  instance->vr_map[AIRCRAFT_AUTOPILOTMODULE_VR_WAYPOINTCOUNT] = {&instance->waypointCount, AIRCRAFT_DATA_INTEGER, true};
  instance->vr_map[AIRCRAFT_AUTOPILOTMODULE_VR_WAYPOINTPROXIMITY_KM] = {&instance->waypointProximity_km, AIRCRAFT_DATA_INTEGER, true};
  instance->vr_map[AIRCRAFT_AUTOPILOTMODULE_VR_WAYPOINTX_KM] = {&instance->waypointX_km, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_AUTOPILOTMODULE_VR_WAYPOINTY_KM] = {&instance->waypointY_km, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_AUTOPILOTMODULE_VR_WAYPOINTZ_KM] = {&instance->waypointZ_km, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_AUTOPILOTMODULE_VR_FEEDBACKBUS_AIRSPEED_MPS] = {&instance->feedbackBus.airspeed_mps, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_AUTOPILOTMODULE_VR_FEEDBACKBUS_ENERGY_STATE_NORM] = {&instance->feedbackBus.energy_state_norm, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_AUTOPILOTMODULE_VR_FEEDBACKBUS_ANGLE_OF_ATTACK_DEG] = {&instance->feedbackBus.angle_of_attack_deg, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_AUTOPILOTMODULE_VR_FEEDBACKBUS_CLIMB_RATE] = {&instance->feedbackBus.climb_rate, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_AUTOPILOTMODULE_VR_FEEDBACKBUS_HEALTH_CODE] = {&instance->feedbackBus.health_code, AIRCRAFT_DATA_INTEGER, true};
  instance->vr_map[AIRCRAFT_AUTOPILOTMODULE_VR_CURRENTLOCATION_X_KM] = {&instance->currentLocation.x_km, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_AUTOPILOTMODULE_VR_CURRENTLOCATION_Y_KM] = {&instance->currentLocation.y_km, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_AUTOPILOTMODULE_VR_CURRENTLOCATION_Z_KM] = {&instance->currentLocation.z_km, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_AUTOPILOTMODULE_VR_CURRENTORIENTATION_ROLL_DEG] = {&instance->currentOrientation.roll_deg, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_AUTOPILOTMODULE_VR_CURRENTORIENTATION_PITCH_DEG] = {&instance->currentOrientation.pitch_deg, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_AUTOPILOTMODULE_VR_CURRENTORIENTATION_YAW_DEG] = {&instance->currentOrientation.yaw_deg, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_AUTOPILOTMODULE_VR_AUTOPILOTCMD_STICK_PITCH_NORM] = {&instance->autopilotCmd.stick_pitch_norm, AIRCRAFT_DATA_REAL, false};
  instance->vr_map[AIRCRAFT_AUTOPILOTMODULE_VR_AUTOPILOTCMD_STICK_ROLL_NORM] = {&instance->autopilotCmd.stick_roll_norm, AIRCRAFT_DATA_REAL, false};
  instance->vr_map[AIRCRAFT_AUTOPILOTMODULE_VR_AUTOPILOTCMD_RUDDER_NORM] = {&instance->autopilotCmd.rudder_norm, AIRCRAFT_DATA_REAL, false};
  instance->vr_map[AIRCRAFT_AUTOPILOTMODULE_VR_AUTOPILOTCMD_THROTTLE_NORM] = {&instance->autopilotCmd.throttle_norm, AIRCRAFT_DATA_REAL, false};
  instance->vr_map[AIRCRAFT_AUTOPILOTMODULE_VR_AUTOPILOTCMD_THROTTLE_AUX_NORM] = {&instance->autopilotCmd.throttle_aux_norm, AIRCRAFT_DATA_REAL, false};
  instance->vr_map[AIRCRAFT_AUTOPILOTMODULE_VR_AUTOPILOTCMD_BUTTON_MASK] = {&instance->autopilotCmd.button_mask, AIRCRAFT_DATA_INTEGER, false};
  instance->vr_map[AIRCRAFT_AUTOPILOTMODULE_VR_AUTOPILOTCMD_HAT_X] = {&instance->autopilotCmd.hat_x, AIRCRAFT_DATA_INTEGER, false};
  instance->vr_map[AIRCRAFT_AUTOPILOTMODULE_VR_AUTOPILOTCMD_HAT_Y] = {&instance->autopilotCmd.hat_y, AIRCRAFT_DATA_INTEGER, false};
  instance->vr_map[AIRCRAFT_AUTOPILOTMODULE_VR_AUTOPILOTCMD_MODE_SWITCH] = {&instance->autopilotCmd.mode_switch, AIRCRAFT_DATA_INTEGER, false};
  instance->vr_map[AIRCRAFT_AUTOPILOTMODULE_VR_AUTOPILOTCMD_RESERVED] = {&instance->autopilotCmd.reserved, AIRCRAFT_DATA_INTEGER, false};
  instance->vr_map[AIRCRAFT_AUTOPILOTMODULE_VR_MISSIONSTATUS_WAYPOINT_INDEX] = {&instance->missionStatus.waypoint_index, AIRCRAFT_DATA_INTEGER, false};
  instance->vr_map[AIRCRAFT_AUTOPILOTMODULE_VR_MISSIONSTATUS_TOTAL_WAYPOINTS] = {&instance->missionStatus.total_waypoints, AIRCRAFT_DATA_INTEGER, false};
  instance->vr_map[AIRCRAFT_AUTOPILOTMODULE_VR_MISSIONSTATUS_DISTANCE_TO_WAYPOINT_KM] = {&instance->missionStatus.distance_to_waypoint_km, AIRCRAFT_DATA_REAL, false};
  instance->vr_map[AIRCRAFT_AUTOPILOTMODULE_VR_MISSIONSTATUS_ARRIVED] = {&instance->missionStatus.arrived, AIRCRAFT_DATA_BOOLEAN, false};
  instance->vr_map[AIRCRAFT_AUTOPILOTMODULE_VR_MISSIONSTATUS_COMPLETE] = {&instance->missionStatus.complete, AIRCRAFT_DATA_BOOLEAN, false};
}

#endif  /* __cplusplus */