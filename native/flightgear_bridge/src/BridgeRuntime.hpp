#pragma once

#include <netinet/in.h>

#include <string>

#include "fmi2Functions.h"

namespace fgbridge {

constexpr const char* kGuid = "{2d7d0b06-4525-4e59-b188-2a9b0b8cb5bb}";
constexpr const char* kTypesPlatform = fmi2TypesPlatform;
constexpr const char* kVersion = fmi2Version;

enum ValueReference : fmi2ValueReference {
  VR_TRANSPORT = 0,
  VR_REFERENCE_LATITUDE_DEG = 1,
  VR_REFERENCE_LONGITUDE_DEG = 2,
  VR_REFERENCE_ALTITUDE_M = 3,
  VR_REMOTE_HOST = 4,
  VR_TELEMETRY_PORT = 5,
  VR_CONTROL_PORT = 6,

  VR_STATE_POSITION_X_KM = 10,
  VR_STATE_POSITION_Y_KM = 11,
  VR_STATE_POSITION_Z_KM = 12,
  VR_STATE_ORIENTATION_ROLL_DEG = 13,
  VR_STATE_ORIENTATION_PITCH_DEG = 14,
  VR_STATE_ORIENTATION_YAW_DEG = 15,
  VR_FLIGHT_STATUS_AIRSPEED_MPS = 16,
  VR_FLIGHT_STATUS_ENERGY_STATE_NORM = 17,
  VR_FLIGHT_STATUS_ANGLE_OF_ATTACK_DEG = 18,
  VR_FLIGHT_STATUS_CLIMB_RATE = 19,
  VR_FLIGHT_STATUS_HEALTH_CODE = 20,
  VR_MISSION_STATUS_WAYPOINT_INDEX = 21,
  VR_MISSION_STATUS_TOTAL_WAYPOINTS = 22,
  VR_MISSION_STATUS_DISTANCE_TO_WAYPOINT_KM = 23,
  VR_MISSION_STATUS_ARRIVED = 24,
  VR_MISSION_STATUS_COMPLETE = 25,

  VR_PILOT_COMMAND_STICK_PITCH_NORM = 40,
  VR_PILOT_COMMAND_STICK_ROLL_NORM = 41,
  VR_PILOT_COMMAND_RUDDER_NORM = 42,
  VR_PILOT_COMMAND_THROTTLE_NORM = 43,
  VR_PILOT_COMMAND_THROTTLE_AUX_NORM = 44,
  VR_PILOT_COMMAND_BUTTON_MASK = 45,
  VR_PILOT_COMMAND_HAT_X = 46,
  VR_PILOT_COMMAND_HAT_Y = 47,
  VR_PILOT_COMMAND_MODE_SWITCH = 48,
  VR_PILOT_COMMAND_RESERVED = 49,
};

struct ModelInstance {
  std::string transport = "FlightGearGeneric";
  double reference_latitude_deg = 0.0;
  double reference_longitude_deg = 0.0;
  double reference_altitude_m = 0.0;
  std::string remote_host = "127.0.0.1";
  int telemetry_port = 5501;
  int control_port = 5502;

  double state_position_x_km = 0.0;
  double state_position_y_km = 0.0;
  double state_position_z_km = 0.0;
  double state_orientation_roll_deg = 0.0;
  double state_orientation_pitch_deg = 0.0;
  double state_orientation_yaw_deg = 0.0;
  double flight_status_airspeed_mps = 0.0;
  double flight_status_energy_state_norm = 0.0;
  double flight_status_angle_of_attack_deg = 0.0;
  double flight_status_climb_rate = 0.0;
  int flight_status_health_code = 0;
  int mission_status_waypoint_index = 0;
  int mission_status_total_waypoints = 0;
  double mission_status_distance_to_waypoint_km = 0.0;
  int mission_status_arrived = fmi2False;
  int mission_status_complete = fmi2False;

  double pilot_command_stick_pitch_norm = 0.0;
  double pilot_command_stick_roll_norm = 0.0;
  double pilot_command_rudder_norm = 0.0;
  double pilot_command_throttle_norm = 0.6;
  double pilot_command_throttle_aux_norm = 0.6;
  int pilot_command_button_mask = 0;
  int pilot_command_hat_x = 0;
  int pilot_command_hat_y = 0;
  int pilot_command_mode_switch = 0;
  int pilot_command_reserved = 0;

  int tx_socket = -1;
  int rx_socket = -1;
  sockaddr_in tx_address {};
  bool sockets_ready = false;
};

ModelInstance* create_instance();
void destroy_instance(ModelInstance* instance);

fmi2Status enter_initialization(ModelInstance* instance);
fmi2Status reset_instance(ModelInstance* instance);
fmi2Status do_step(ModelInstance* instance);

fmi2Status get_real(ModelInstance* instance, const fmi2ValueReference vr[], size_t nvr, fmi2Real value[]);
fmi2Status get_integer(ModelInstance* instance, const fmi2ValueReference vr[], size_t nvr, fmi2Integer value[]);
fmi2Status get_boolean(ModelInstance* instance, const fmi2ValueReference vr[], size_t nvr, fmi2Boolean value[]);
fmi2Status get_string(ModelInstance* instance, const fmi2ValueReference vr[], size_t nvr, fmi2String value[]);

fmi2Status set_real(ModelInstance* instance, const fmi2ValueReference vr[], size_t nvr, const fmi2Real value[]);
fmi2Status set_integer(ModelInstance* instance, const fmi2ValueReference vr[], size_t nvr, const fmi2Integer value[]);
fmi2Status set_boolean(ModelInstance* instance, const fmi2ValueReference vr[], size_t nvr, const fmi2Boolean value[]);
fmi2Status set_string(ModelInstance* instance, const fmi2ValueReference vr[], size_t nvr, const fmi2String value[]);

}  // namespace fgbridge
