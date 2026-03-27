#include <arpa/inet.h>
#include <fcntl.h>
#include <math.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <unistd.h>

#include <cerrno>
#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <sstream>
#include <string>
#include <utility>
#include <vector>

#include "fmi2Functions.h"

namespace {

constexpr const char* kGuid = "{2d7d0b06-4525-4e59-b188-2a9b0b8cb5bb}";
constexpr const char* kTypesPlatform = fmi2TypesPlatform;
constexpr const char* kVersion = fmi2Version;
constexpr double kPi = 3.14159265358979323846;

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

void close_socket_if_open(int& fd) {
  if (fd >= 0) {
    close(fd);
    fd = -1;
  }
}

std::vector<std::string> split_csv(const std::string& payload) {
  std::vector<std::string> parts;
  std::stringstream stream(payload);
  std::string item;
  while (std::getline(stream, item, ',')) {
    while (!item.empty() && (item.back() == '\n' || item.back() == '\r' || item.back() == ' ' || item.back() == '\t')) {
      item.pop_back();
    }
    std::size_t start = 0;
    while (start < item.size() && (item[start] == ' ' || item[start] == '\t')) {
      ++start;
    }
    parts.emplace_back(item.substr(start));
  }
  return parts;
}

bool parse_double(const std::string& text, double& value) {
  char* end = nullptr;
  const double parsed = std::strtod(text.c_str(), &end);
  if (end == text.c_str() || (end && *end != '\0')) {
    return false;
  }
  value = parsed;
  return true;
}

bool parse_int(const std::string& text, int& value) {
  char* end = nullptr;
  const long parsed = std::strtol(text.c_str(), &end, 10);
  if (end == text.c_str() || (end && *end != '\0')) {
    return false;
  }
  value = static_cast<int>(parsed);
  return true;
}

bool ensure_sockets(ModelInstance* instance) {
  if (instance->sockets_ready) {
    return true;
  }

  instance->tx_socket = socket(AF_INET, SOCK_DGRAM, 0);
  if (instance->tx_socket < 0) {
    return false;
  }

  instance->rx_socket = socket(AF_INET, SOCK_DGRAM, 0);
  if (instance->rx_socket < 0) {
    close_socket_if_open(instance->tx_socket);
    return false;
  }

  const int flags = fcntl(instance->rx_socket, F_GETFL, 0);
  if (flags < 0 || fcntl(instance->rx_socket, F_SETFL, flags | O_NONBLOCK) < 0) {
    close_socket_if_open(instance->tx_socket);
    close_socket_if_open(instance->rx_socket);
    return false;
  }

  sockaddr_in rx_address {};
  rx_address.sin_family = AF_INET;
  rx_address.sin_port = htons(static_cast<uint16_t>(instance->control_port));
  rx_address.sin_addr.s_addr = htonl(INADDR_ANY);

  constexpr int reuse = 1;
  setsockopt(instance->rx_socket, SOL_SOCKET, SO_REUSEADDR, &reuse, sizeof(reuse));
  if (bind(instance->rx_socket, reinterpret_cast<sockaddr*>(&rx_address), sizeof(rx_address)) < 0) {
    close_socket_if_open(instance->tx_socket);
    close_socket_if_open(instance->rx_socket);
    return false;
  }

  instance->tx_address = {};
  instance->tx_address.sin_family = AF_INET;
  instance->tx_address.sin_port = htons(static_cast<uint16_t>(instance->telemetry_port));
  if (inet_pton(AF_INET, instance->remote_host.c_str(), &instance->tx_address.sin_addr) != 1) {
    close_socket_if_open(instance->tx_socket);
    close_socket_if_open(instance->rx_socket);
    return false;
  }

  instance->sockets_ready = true;
  return true;
}

void reset_sockets(ModelInstance* instance) {
  instance->sockets_ready = false;
  close_socket_if_open(instance->tx_socket);
  close_socket_if_open(instance->rx_socket);
}

void receive_control_packet(ModelInstance* instance) {
  if (!ensure_sockets(instance)) {
    return;
  }

  char buffer[1024];
  for (;;) {
    ssize_t received = recv(instance->rx_socket, buffer, sizeof(buffer) - 1, 0);
    if (received < 0) {
      if (errno == EAGAIN || errno == EWOULDBLOCK) {
        break;
      }
      return;
    }
    if (received == 0) {
      break;
    }

    buffer[received] = '\0';
    const auto fields = split_csv(buffer);
    if (fields.size() < 4) {
      continue;
    }

    parse_double(fields[0], instance->pilot_command_stick_pitch_norm);
    parse_double(fields[1], instance->pilot_command_stick_roll_norm);
    parse_double(fields[2], instance->pilot_command_rudder_norm);
    parse_double(fields[3], instance->pilot_command_throttle_norm);
    instance->pilot_command_throttle_aux_norm = instance->pilot_command_throttle_norm;

    if (fields.size() >= 5) {
      parse_double(fields[4], instance->pilot_command_throttle_aux_norm);
    }
    if (fields.size() >= 6) {
      parse_int(fields[5], instance->pilot_command_button_mask);
    }
    if (fields.size() >= 7) {
      parse_int(fields[6], instance->pilot_command_hat_x);
    }
    if (fields.size() >= 8) {
      parse_int(fields[7], instance->pilot_command_hat_y);
    }
    if (fields.size() >= 9) {
      parse_int(fields[8], instance->pilot_command_mode_switch);
    }
    if (fields.size() >= 10) {
      parse_int(fields[9], instance->pilot_command_reserved);
    }
  }
}

std::string telemetry_packet(const ModelInstance* instance) {
  constexpr double km_per_degree = 111.0;
  const double lat_rad = instance->reference_latitude_deg * kPi / 180.0;
  const double latitude_deg = instance->reference_latitude_deg + (instance->state_position_x_km / km_per_degree);
  const double longitude_scale = km_per_degree * (std::abs(std::cos(lat_rad)) < 1e-9 ? 1.0 : std::cos(lat_rad));
  const double longitude_deg = instance->reference_longitude_deg + (instance->state_position_y_km / longitude_scale);
  const double altitude_m = instance->reference_altitude_m + (instance->state_position_z_km * 1000.0);
  const double altitude_ft = altitude_m * 3.28083989501312;
  const double airspeed_kt = instance->flight_status_airspeed_mps * 1.9438444924406;
  const double climb_rate_fps = instance->flight_status_climb_rate * 3.28083989501312;

  std::ostringstream stream;
  stream.setf(std::ios::fixed);
  stream.precision(6);
  stream
      << latitude_deg << ','
      << longitude_deg << ','
      << altitude_ft << ','
      << instance->state_orientation_roll_deg << ','
      << instance->state_orientation_pitch_deg << ','
      << instance->state_orientation_yaw_deg << ','
      << airspeed_kt << ','
      << instance->flight_status_energy_state_norm << ','
      << instance->flight_status_angle_of_attack_deg << ','
      << climb_rate_fps << ','
      << instance->flight_status_health_code << ','
      << instance->mission_status_waypoint_index << ','
      << instance->mission_status_total_waypoints << ','
      << instance->mission_status_distance_to_waypoint_km << ','
      << instance->mission_status_arrived << ','
      << instance->mission_status_complete
      << '\n';
  return stream.str();
}

void send_telemetry_packet(ModelInstance* instance) {
  if (!ensure_sockets(instance)) {
    return;
  }
  const std::string payload = telemetry_packet(instance);
  sendto(
      instance->tx_socket,
      payload.c_str(),
      payload.size(),
      0,
      reinterpret_cast<const sockaddr*>(&instance->tx_address),
      sizeof(instance->tx_address));
}

ModelInstance* as_instance(fmi2Component component) {
  return reinterpret_cast<ModelInstance*>(component);
}

}  // namespace

extern "C" {

const char* fmi2GetTypesPlatform() {
  return kTypesPlatform;
}

const char* fmi2GetVersion() {
  return kVersion;
}

fmi2Status fmi2SetDebugLogging(fmi2Component, fmi2Boolean, size_t, const fmi2String[]) {
  return fmi2OK;
}

fmi2Component fmi2Instantiate(
    fmi2String,
    fmi2Type fmuType,
    fmi2String fmuGUID,
    fmi2String,
    const fmi2CallbackFunctions*,
    fmi2Boolean,
    fmi2Boolean) {
  if (fmuType != fmi2CoSimulation) {
    return nullptr;
  }
  if (fmuGUID == nullptr || std::strcmp(fmuGUID, kGuid) != 0) {
    return nullptr;
  }
  return reinterpret_cast<fmi2Component>(new ModelInstance());
}

void fmi2FreeInstance(fmi2Component component) {
  if (component == nullptr) {
    return;
  }
  auto* instance = as_instance(component);
  reset_sockets(instance);
  delete instance;
}

fmi2Status fmi2SetupExperiment(
    fmi2Component,
    fmi2Boolean,
    fmi2Real,
    fmi2Real,
    fmi2Boolean,
    fmi2Real) {
  return fmi2OK;
}

fmi2Status fmi2EnterInitializationMode(fmi2Component) {
  return fmi2OK;
}

fmi2Status fmi2ExitInitializationMode(fmi2Component component) {
  auto* instance = as_instance(component);
  return ensure_sockets(instance) ? fmi2OK : fmi2Warning;
}

fmi2Status fmi2Terminate(fmi2Component component) {
  auto* instance = as_instance(component);
  reset_sockets(instance);
  return fmi2OK;
}

fmi2Status fmi2Reset(fmi2Component component) {
  auto* instance = as_instance(component);
  reset_sockets(instance);
  instance->pilot_command_stick_pitch_norm = 0.0;
  instance->pilot_command_stick_roll_norm = 0.0;
  instance->pilot_command_rudder_norm = 0.0;
  instance->pilot_command_throttle_norm = 0.6;
  instance->pilot_command_throttle_aux_norm = 0.6;
  instance->pilot_command_button_mask = 0;
  instance->pilot_command_hat_x = 0;
  instance->pilot_command_hat_y = 0;
  instance->pilot_command_mode_switch = 0;
  instance->pilot_command_reserved = 0;
  return fmi2OK;
}

fmi2Status fmi2GetReal(fmi2Component component, const fmi2ValueReference vr[], size_t nvr, fmi2Real value[]) {
  auto* instance = as_instance(component);
  for (size_t i = 0; i < nvr; ++i) {
    switch (vr[i]) {
      case VR_REFERENCE_LATITUDE_DEG: value[i] = instance->reference_latitude_deg; break;
      case VR_REFERENCE_LONGITUDE_DEG: value[i] = instance->reference_longitude_deg; break;
      case VR_REFERENCE_ALTITUDE_M: value[i] = instance->reference_altitude_m; break;
      case VR_STATE_POSITION_X_KM: value[i] = instance->state_position_x_km; break;
      case VR_STATE_POSITION_Y_KM: value[i] = instance->state_position_y_km; break;
      case VR_STATE_POSITION_Z_KM: value[i] = instance->state_position_z_km; break;
      case VR_STATE_ORIENTATION_ROLL_DEG: value[i] = instance->state_orientation_roll_deg; break;
      case VR_STATE_ORIENTATION_PITCH_DEG: value[i] = instance->state_orientation_pitch_deg; break;
      case VR_STATE_ORIENTATION_YAW_DEG: value[i] = instance->state_orientation_yaw_deg; break;
      case VR_FLIGHT_STATUS_AIRSPEED_MPS: value[i] = instance->flight_status_airspeed_mps; break;
      case VR_FLIGHT_STATUS_ENERGY_STATE_NORM: value[i] = instance->flight_status_energy_state_norm; break;
      case VR_FLIGHT_STATUS_ANGLE_OF_ATTACK_DEG: value[i] = instance->flight_status_angle_of_attack_deg; break;
      case VR_FLIGHT_STATUS_CLIMB_RATE: value[i] = instance->flight_status_climb_rate; break;
      case VR_MISSION_STATUS_DISTANCE_TO_WAYPOINT_KM: value[i] = instance->mission_status_distance_to_waypoint_km; break;
      case VR_PILOT_COMMAND_STICK_PITCH_NORM: value[i] = instance->pilot_command_stick_pitch_norm; break;
      case VR_PILOT_COMMAND_STICK_ROLL_NORM: value[i] = instance->pilot_command_stick_roll_norm; break;
      case VR_PILOT_COMMAND_RUDDER_NORM: value[i] = instance->pilot_command_rudder_norm; break;
      case VR_PILOT_COMMAND_THROTTLE_NORM: value[i] = instance->pilot_command_throttle_norm; break;
      case VR_PILOT_COMMAND_THROTTLE_AUX_NORM: value[i] = instance->pilot_command_throttle_aux_norm; break;
      default: return fmi2Error;
    }
  }
  return fmi2OK;
}

fmi2Status fmi2GetInteger(fmi2Component component, const fmi2ValueReference vr[], size_t nvr, fmi2Integer value[]) {
  auto* instance = as_instance(component);
  for (size_t i = 0; i < nvr; ++i) {
    switch (vr[i]) {
      case VR_TELEMETRY_PORT: value[i] = instance->telemetry_port; break;
      case VR_CONTROL_PORT: value[i] = instance->control_port; break;
      case VR_FLIGHT_STATUS_HEALTH_CODE: value[i] = instance->flight_status_health_code; break;
      case VR_MISSION_STATUS_WAYPOINT_INDEX: value[i] = instance->mission_status_waypoint_index; break;
      case VR_MISSION_STATUS_TOTAL_WAYPOINTS: value[i] = instance->mission_status_total_waypoints; break;
      case VR_PILOT_COMMAND_BUTTON_MASK: value[i] = instance->pilot_command_button_mask; break;
      case VR_PILOT_COMMAND_HAT_X: value[i] = instance->pilot_command_hat_x; break;
      case VR_PILOT_COMMAND_HAT_Y: value[i] = instance->pilot_command_hat_y; break;
      case VR_PILOT_COMMAND_MODE_SWITCH: value[i] = instance->pilot_command_mode_switch; break;
      case VR_PILOT_COMMAND_RESERVED: value[i] = instance->pilot_command_reserved; break;
      default: return fmi2Error;
    }
  }
  return fmi2OK;
}

fmi2Status fmi2GetBoolean(fmi2Component component, const fmi2ValueReference vr[], size_t nvr, fmi2Boolean value[]) {
  auto* instance = as_instance(component);
  for (size_t i = 0; i < nvr; ++i) {
    switch (vr[i]) {
      case VR_MISSION_STATUS_ARRIVED: value[i] = static_cast<fmi2Boolean>(instance->mission_status_arrived); break;
      case VR_MISSION_STATUS_COMPLETE: value[i] = static_cast<fmi2Boolean>(instance->mission_status_complete); break;
      default: return fmi2Error;
    }
  }
  return fmi2OK;
}

fmi2Status fmi2GetString(fmi2Component component, const fmi2ValueReference vr[], size_t nvr, fmi2String value[]) {
  auto* instance = as_instance(component);
  for (size_t i = 0; i < nvr; ++i) {
    switch (vr[i]) {
      case VR_TRANSPORT: value[i] = instance->transport.c_str(); break;
      case VR_REMOTE_HOST: value[i] = instance->remote_host.c_str(); break;
      default: return fmi2Error;
    }
  }
  return fmi2OK;
}

fmi2Status fmi2SetReal(fmi2Component component, const fmi2ValueReference vr[], size_t nvr, const fmi2Real value[]) {
  auto* instance = as_instance(component);
  for (size_t i = 0; i < nvr; ++i) {
    switch (vr[i]) {
      case VR_REFERENCE_LATITUDE_DEG: instance->reference_latitude_deg = value[i]; break;
      case VR_REFERENCE_LONGITUDE_DEG: instance->reference_longitude_deg = value[i]; break;
      case VR_REFERENCE_ALTITUDE_M: instance->reference_altitude_m = value[i]; break;
      case VR_STATE_POSITION_X_KM: instance->state_position_x_km = value[i]; break;
      case VR_STATE_POSITION_Y_KM: instance->state_position_y_km = value[i]; break;
      case VR_STATE_POSITION_Z_KM: instance->state_position_z_km = value[i]; break;
      case VR_STATE_ORIENTATION_ROLL_DEG: instance->state_orientation_roll_deg = value[i]; break;
      case VR_STATE_ORIENTATION_PITCH_DEG: instance->state_orientation_pitch_deg = value[i]; break;
      case VR_STATE_ORIENTATION_YAW_DEG: instance->state_orientation_yaw_deg = value[i]; break;
      case VR_FLIGHT_STATUS_AIRSPEED_MPS: instance->flight_status_airspeed_mps = value[i]; break;
      case VR_FLIGHT_STATUS_ENERGY_STATE_NORM: instance->flight_status_energy_state_norm = value[i]; break;
      case VR_FLIGHT_STATUS_ANGLE_OF_ATTACK_DEG: instance->flight_status_angle_of_attack_deg = value[i]; break;
      case VR_FLIGHT_STATUS_CLIMB_RATE: instance->flight_status_climb_rate = value[i]; break;
      case VR_MISSION_STATUS_DISTANCE_TO_WAYPOINT_KM: instance->mission_status_distance_to_waypoint_km = value[i]; break;
      default: return fmi2Error;
    }
  }
  return fmi2OK;
}

fmi2Status fmi2SetInteger(fmi2Component component, const fmi2ValueReference vr[], size_t nvr, const fmi2Integer value[]) {
  auto* instance = as_instance(component);
  bool network_param_changed = false;
  for (size_t i = 0; i < nvr; ++i) {
    switch (vr[i]) {
      case VR_TELEMETRY_PORT: instance->telemetry_port = value[i]; network_param_changed = true; break;
      case VR_CONTROL_PORT: instance->control_port = value[i]; network_param_changed = true; break;
      case VR_FLIGHT_STATUS_HEALTH_CODE: instance->flight_status_health_code = value[i]; break;
      case VR_MISSION_STATUS_WAYPOINT_INDEX: instance->mission_status_waypoint_index = value[i]; break;
      case VR_MISSION_STATUS_TOTAL_WAYPOINTS: instance->mission_status_total_waypoints = value[i]; break;
      case VR_PILOT_COMMAND_BUTTON_MASK: instance->pilot_command_button_mask = value[i]; break;
      case VR_PILOT_COMMAND_HAT_X: instance->pilot_command_hat_x = value[i]; break;
      case VR_PILOT_COMMAND_HAT_Y: instance->pilot_command_hat_y = value[i]; break;
      case VR_PILOT_COMMAND_MODE_SWITCH: instance->pilot_command_mode_switch = value[i]; break;
      case VR_PILOT_COMMAND_RESERVED: instance->pilot_command_reserved = value[i]; break;
      default: return fmi2Error;
    }
  }
  if (network_param_changed) {
    reset_sockets(instance);
  }
  return fmi2OK;
}

fmi2Status fmi2SetBoolean(fmi2Component component, const fmi2ValueReference vr[], size_t nvr, const fmi2Boolean value[]) {
  auto* instance = as_instance(component);
  for (size_t i = 0; i < nvr; ++i) {
    switch (vr[i]) {
      case VR_MISSION_STATUS_ARRIVED: instance->mission_status_arrived = value[i]; break;
      case VR_MISSION_STATUS_COMPLETE: instance->mission_status_complete = value[i]; break;
      default: return fmi2Error;
    }
  }
  return fmi2OK;
}

fmi2Status fmi2SetString(fmi2Component component, const fmi2ValueReference vr[], size_t nvr, const fmi2String value[]) {
  auto* instance = as_instance(component);
  bool network_param_changed = false;
  for (size_t i = 0; i < nvr; ++i) {
    switch (vr[i]) {
      case VR_TRANSPORT: instance->transport = value[i] ? value[i] : ""; break;
      case VR_REMOTE_HOST: instance->remote_host = value[i] ? value[i] : ""; network_param_changed = true; break;
      default: return fmi2Error;
    }
  }
  if (network_param_changed) {
    reset_sockets(instance);
  }
  return fmi2OK;
}

fmi2Status fmi2DoStep(fmi2Component component, fmi2Real, fmi2Real, fmi2Boolean) {
  auto* instance = as_instance(component);
  receive_control_packet(instance);
  send_telemetry_packet(instance);
  return fmi2OK;
}

fmi2Status fmi2CancelStep(fmi2Component) {
  return fmi2OK;
}

fmi2Status fmi2GetStatus(fmi2Component, const fmi2StatusKind, fmi2Status* value) {
  if (value != nullptr) {
    *value = fmi2OK;
  }
  return fmi2OK;
}

fmi2Status fmi2GetRealStatus(fmi2Component, const fmi2StatusKind, fmi2Real* value) {
  if (value != nullptr) {
    *value = 0.0;
  }
  return fmi2OK;
}

fmi2Status fmi2GetIntegerStatus(fmi2Component, const fmi2StatusKind, fmi2Integer* value) {
  if (value != nullptr) {
    *value = 0;
  }
  return fmi2OK;
}

fmi2Status fmi2GetBooleanStatus(fmi2Component, const fmi2StatusKind, fmi2Boolean* value) {
  if (value != nullptr) {
    *value = fmi2False;
  }
  return fmi2OK;
}

fmi2Status fmi2GetStringStatus(fmi2Component, const fmi2StatusKind, fmi2String* value) {
  if (value != nullptr) {
    *value = "";
  }
  return fmi2OK;
}

fmi2Status fmi2SetRealInputDerivatives(fmi2Component, const fmi2ValueReference[], size_t, const fmi2Integer[], const fmi2Real[]) {
  return fmi2Error;
}

fmi2Status fmi2GetRealOutputDerivatives(fmi2Component, const fmi2ValueReference[], size_t, const fmi2Integer[], fmi2Real[]) {
  return fmi2Error;
}

fmi2Status fmi2GetDirectionalDerivative(fmi2Component, const fmi2ValueReference[], size_t, const fmi2ValueReference[], size_t, const fmi2Real[], fmi2Real[]) {
  return fmi2Error;
}

fmi2Status fmi2GetFMUstate(fmi2Component, fmi2FMUstate*) {
  return fmi2Error;
}

fmi2Status fmi2SetFMUstate(fmi2Component, fmi2FMUstate) {
  return fmi2Error;
}

fmi2Status fmi2FreeFMUstate(fmi2Component, fmi2FMUstate*) {
  return fmi2Error;
}

fmi2Status fmi2SerializedFMUstateSize(fmi2Component, fmi2FMUstate, size_t*) {
  return fmi2Error;
}

fmi2Status fmi2SerializeFMUstate(fmi2Component, fmi2FMUstate, fmi2Byte[], size_t) {
  return fmi2Error;
}

fmi2Status fmi2DeSerializeFMUstate(fmi2Component, const fmi2Byte[], size_t, fmi2FMUstate*) {
  return fmi2Error;
}

}  // extern "C"
