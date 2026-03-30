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

inline constexpr size_t Aircraft_InputOutput_VrCount = 26;

struct Aircraft_InputOutput_Instance {
  Aircraft_VrMapping vr_map[26] = {};
  Aircraft_PositionXYZ locationXYZ = {};
  Aircraft_OrientationEuler orientation = {};
  Aircraft_PilotCommand autopilotCmd = {};
  Aircraft_FlightStatusPacket flightStatus = {};
  Aircraft_MissionStatus missionStatus = {};
};

inline void Aircraft_InputOutput_initialize_vr_map(Aircraft_InputOutput_Instance* instance) {
  for (size_t i = 0; i < Aircraft_InputOutput_VrCount; ++i) {
    instance->vr_map[i] = {nullptr, AIRCRAFT_DATA_NONE, false};
  }
  instance->vr_map[AIRCRAFT_INPUTOUTPUT_VR_LOCATIONXYZ_X_KM] = {&instance->locationXYZ.x_km, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_INPUTOUTPUT_VR_LOCATIONXYZ_Y_KM] = {&instance->locationXYZ.y_km, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_INPUTOUTPUT_VR_LOCATIONXYZ_Z_KM] = {&instance->locationXYZ.z_km, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_INPUTOUTPUT_VR_ORIENTATION_ROLL_DEG] = {&instance->orientation.roll_deg, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_INPUTOUTPUT_VR_ORIENTATION_PITCH_DEG] = {&instance->orientation.pitch_deg, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_INPUTOUTPUT_VR_ORIENTATION_YAW_DEG] = {&instance->orientation.yaw_deg, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_INPUTOUTPUT_VR_AUTOPILOTCMD_STICK_PITCH_NORM] = {&instance->autopilotCmd.stick_pitch_norm, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_INPUTOUTPUT_VR_AUTOPILOTCMD_STICK_ROLL_NORM] = {&instance->autopilotCmd.stick_roll_norm, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_INPUTOUTPUT_VR_AUTOPILOTCMD_RUDDER_NORM] = {&instance->autopilotCmd.rudder_norm, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_INPUTOUTPUT_VR_AUTOPILOTCMD_THROTTLE_NORM] = {&instance->autopilotCmd.throttle_norm, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_INPUTOUTPUT_VR_AUTOPILOTCMD_THROTTLE_AUX_NORM] = {&instance->autopilotCmd.throttle_aux_norm, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_INPUTOUTPUT_VR_AUTOPILOTCMD_BUTTON_MASK] = {&instance->autopilotCmd.button_mask, AIRCRAFT_DATA_INTEGER, true};
  instance->vr_map[AIRCRAFT_INPUTOUTPUT_VR_AUTOPILOTCMD_HAT_X] = {&instance->autopilotCmd.hat_x, AIRCRAFT_DATA_INTEGER, true};
  instance->vr_map[AIRCRAFT_INPUTOUTPUT_VR_AUTOPILOTCMD_HAT_Y] = {&instance->autopilotCmd.hat_y, AIRCRAFT_DATA_INTEGER, true};
  instance->vr_map[AIRCRAFT_INPUTOUTPUT_VR_AUTOPILOTCMD_MODE_SWITCH] = {&instance->autopilotCmd.mode_switch, AIRCRAFT_DATA_INTEGER, true};
  instance->vr_map[AIRCRAFT_INPUTOUTPUT_VR_AUTOPILOTCMD_RESERVED] = {&instance->autopilotCmd.reserved, AIRCRAFT_DATA_INTEGER, true};
  instance->vr_map[AIRCRAFT_INPUTOUTPUT_VR_FLIGHTSTATUS_AIRSPEED_MPS] = {&instance->flightStatus.airspeed_mps, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_INPUTOUTPUT_VR_FLIGHTSTATUS_ENERGY_STATE_NORM] = {&instance->flightStatus.energy_state_norm, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_INPUTOUTPUT_VR_FLIGHTSTATUS_ANGLE_OF_ATTACK_DEG] = {&instance->flightStatus.angle_of_attack_deg, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_INPUTOUTPUT_VR_FLIGHTSTATUS_CLIMB_RATE] = {&instance->flightStatus.climb_rate, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_INPUTOUTPUT_VR_FLIGHTSTATUS_HEALTH_CODE] = {&instance->flightStatus.health_code, AIRCRAFT_DATA_INTEGER, true};
  instance->vr_map[AIRCRAFT_INPUTOUTPUT_VR_MISSIONSTATUS_WAYPOINT_INDEX] = {&instance->missionStatus.waypoint_index, AIRCRAFT_DATA_INTEGER, true};
  instance->vr_map[AIRCRAFT_INPUTOUTPUT_VR_MISSIONSTATUS_TOTAL_WAYPOINTS] = {&instance->missionStatus.total_waypoints, AIRCRAFT_DATA_INTEGER, true};
  instance->vr_map[AIRCRAFT_INPUTOUTPUT_VR_MISSIONSTATUS_DISTANCE_TO_WAYPOINT_KM] = {&instance->missionStatus.distance_to_waypoint_km, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_INPUTOUTPUT_VR_MISSIONSTATUS_ARRIVED] = {&instance->missionStatus.arrived, AIRCRAFT_DATA_BOOLEAN, true};
  instance->vr_map[AIRCRAFT_INPUTOUTPUT_VR_MISSIONSTATUS_COMPLETE] = {&instance->missionStatus.complete, AIRCRAFT_DATA_BOOLEAN, true};
}

#endif  /* __cplusplus */