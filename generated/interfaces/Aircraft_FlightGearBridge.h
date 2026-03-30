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

inline constexpr size_t Aircraft_FlightGearBridge_VrCount = 33;

struct Aircraft_FlightGearBridge_Instance {
  Aircraft_VrMapping vr_map[33] = {};
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

inline void Aircraft_FlightGearBridge_initialize_vr_map(Aircraft_FlightGearBridge_Instance* instance) {
  for (size_t i = 0; i < Aircraft_FlightGearBridge_VrCount; ++i) {
    instance->vr_map[i] = {nullptr, AIRCRAFT_DATA_NONE, false};
  }
  instance->vr_map[AIRCRAFT_FLIGHTGEARBRIDGE_VR_TRANSPORT] = {&instance->transport, AIRCRAFT_DATA_STRING, true};
  instance->vr_map[AIRCRAFT_FLIGHTGEARBRIDGE_VR_REFERENCE_LATITUDE_DEG] = {&instance->reference_latitude_deg, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_FLIGHTGEARBRIDGE_VR_REFERENCE_LONGITUDE_DEG] = {&instance->reference_longitude_deg, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_FLIGHTGEARBRIDGE_VR_REFERENCE_ALTITUDE_M] = {&instance->reference_altitude_m, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_FLIGHTGEARBRIDGE_VR_REMOTE_HOST] = {&instance->remote_host, AIRCRAFT_DATA_STRING, true};
  instance->vr_map[AIRCRAFT_FLIGHTGEARBRIDGE_VR_TELEMETRY_PORT] = {&instance->telemetry_port, AIRCRAFT_DATA_INTEGER, true};
  instance->vr_map[AIRCRAFT_FLIGHTGEARBRIDGE_VR_CONTROL_PORT] = {&instance->control_port, AIRCRAFT_DATA_INTEGER, true};
  instance->vr_map[AIRCRAFT_FLIGHTGEARBRIDGE_VR_STATEPOSITION_X_KM] = {&instance->statePosition.x_km, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_FLIGHTGEARBRIDGE_VR_STATEPOSITION_Y_KM] = {&instance->statePosition.y_km, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_FLIGHTGEARBRIDGE_VR_STATEPOSITION_Z_KM] = {&instance->statePosition.z_km, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_FLIGHTGEARBRIDGE_VR_STATEORIENTATION_ROLL_DEG] = {&instance->stateOrientation.roll_deg, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_FLIGHTGEARBRIDGE_VR_STATEORIENTATION_PITCH_DEG] = {&instance->stateOrientation.pitch_deg, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_FLIGHTGEARBRIDGE_VR_STATEORIENTATION_YAW_DEG] = {&instance->stateOrientation.yaw_deg, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_FLIGHTGEARBRIDGE_VR_FLIGHTSTATUS_AIRSPEED_MPS] = {&instance->flightStatus.airspeed_mps, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_FLIGHTGEARBRIDGE_VR_FLIGHTSTATUS_ENERGY_STATE_NORM] = {&instance->flightStatus.energy_state_norm, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_FLIGHTGEARBRIDGE_VR_FLIGHTSTATUS_ANGLE_OF_ATTACK_DEG] = {&instance->flightStatus.angle_of_attack_deg, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_FLIGHTGEARBRIDGE_VR_FLIGHTSTATUS_CLIMB_RATE] = {&instance->flightStatus.climb_rate, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_FLIGHTGEARBRIDGE_VR_FLIGHTSTATUS_HEALTH_CODE] = {&instance->flightStatus.health_code, AIRCRAFT_DATA_INTEGER, true};
  instance->vr_map[AIRCRAFT_FLIGHTGEARBRIDGE_VR_MISSIONSTATUS_WAYPOINT_INDEX] = {&instance->missionStatus.waypoint_index, AIRCRAFT_DATA_INTEGER, true};
  instance->vr_map[AIRCRAFT_FLIGHTGEARBRIDGE_VR_MISSIONSTATUS_TOTAL_WAYPOINTS] = {&instance->missionStatus.total_waypoints, AIRCRAFT_DATA_INTEGER, true};
  instance->vr_map[AIRCRAFT_FLIGHTGEARBRIDGE_VR_MISSIONSTATUS_DISTANCE_TO_WAYPOINT_KM] = {&instance->missionStatus.distance_to_waypoint_km, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_FLIGHTGEARBRIDGE_VR_MISSIONSTATUS_ARRIVED] = {&instance->missionStatus.arrived, AIRCRAFT_DATA_BOOLEAN, true};
  instance->vr_map[AIRCRAFT_FLIGHTGEARBRIDGE_VR_MISSIONSTATUS_COMPLETE] = {&instance->missionStatus.complete, AIRCRAFT_DATA_BOOLEAN, true};
  instance->vr_map[AIRCRAFT_FLIGHTGEARBRIDGE_VR_PILOTCOMMAND_STICK_PITCH_NORM] = {&instance->pilotCommand.stick_pitch_norm, AIRCRAFT_DATA_REAL, false};
  instance->vr_map[AIRCRAFT_FLIGHTGEARBRIDGE_VR_PILOTCOMMAND_STICK_ROLL_NORM] = {&instance->pilotCommand.stick_roll_norm, AIRCRAFT_DATA_REAL, false};
  instance->vr_map[AIRCRAFT_FLIGHTGEARBRIDGE_VR_PILOTCOMMAND_RUDDER_NORM] = {&instance->pilotCommand.rudder_norm, AIRCRAFT_DATA_REAL, false};
  instance->vr_map[AIRCRAFT_FLIGHTGEARBRIDGE_VR_PILOTCOMMAND_THROTTLE_NORM] = {&instance->pilotCommand.throttle_norm, AIRCRAFT_DATA_REAL, false};
  instance->vr_map[AIRCRAFT_FLIGHTGEARBRIDGE_VR_PILOTCOMMAND_THROTTLE_AUX_NORM] = {&instance->pilotCommand.throttle_aux_norm, AIRCRAFT_DATA_REAL, false};
  instance->vr_map[AIRCRAFT_FLIGHTGEARBRIDGE_VR_PILOTCOMMAND_BUTTON_MASK] = {&instance->pilotCommand.button_mask, AIRCRAFT_DATA_INTEGER, false};
  instance->vr_map[AIRCRAFT_FLIGHTGEARBRIDGE_VR_PILOTCOMMAND_HAT_X] = {&instance->pilotCommand.hat_x, AIRCRAFT_DATA_INTEGER, false};
  instance->vr_map[AIRCRAFT_FLIGHTGEARBRIDGE_VR_PILOTCOMMAND_HAT_Y] = {&instance->pilotCommand.hat_y, AIRCRAFT_DATA_INTEGER, false};
  instance->vr_map[AIRCRAFT_FLIGHTGEARBRIDGE_VR_PILOTCOMMAND_MODE_SWITCH] = {&instance->pilotCommand.mode_switch, AIRCRAFT_DATA_INTEGER, false};
  instance->vr_map[AIRCRAFT_FLIGHTGEARBRIDGE_VR_PILOTCOMMAND_RESERVED] = {&instance->pilotCommand.reserved, AIRCRAFT_DATA_INTEGER, false};
}

#endif  /* __cplusplus */