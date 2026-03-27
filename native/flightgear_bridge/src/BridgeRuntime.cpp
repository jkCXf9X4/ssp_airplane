#include "BridgeRuntime.hpp"

#include <arpa/inet.h>
#include <fcntl.h>
#include <unistd.h>

#include <cerrno>
#include <cmath>
#include <cstdlib>
#include <cstring>
#include <sstream>
#include <string>
#include <vector>

namespace fgbridge {
namespace {

constexpr double kPi = 3.14159265358979323846;

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

    parse_double(fields[0], instance->pilotCommand.stick_pitch_norm);
    parse_double(fields[1], instance->pilotCommand.stick_roll_norm);
    parse_double(fields[2], instance->pilotCommand.rudder_norm);
    parse_double(fields[3], instance->pilotCommand.throttle_norm);
    instance->pilotCommand.throttle_aux_norm = instance->pilotCommand.throttle_norm;

    if (fields.size() >= 5) {
      parse_double(fields[4], instance->pilotCommand.throttle_aux_norm);
    }
    if (fields.size() >= 6) {
      parse_int(fields[5], instance->pilotCommand.button_mask);
    }
    if (fields.size() >= 7) {
      parse_int(fields[6], instance->pilotCommand.hat_x);
    }
    if (fields.size() >= 8) {
      parse_int(fields[7], instance->pilotCommand.hat_y);
    }
    if (fields.size() >= 9) {
      parse_int(fields[8], instance->pilotCommand.mode_switch);
    }
    if (fields.size() >= 10) {
      parse_int(fields[9], instance->pilotCommand.reserved);
    }
  }
}

std::string telemetry_packet(const ModelInstance* instance) {
  constexpr double km_per_degree = 111.0;
  const double lat_rad = instance->reference_latitude_deg * kPi / 180.0;
  const double latitude_deg = instance->reference_latitude_deg + (instance->statePosition.x_km / km_per_degree);
  const double longitude_scale = km_per_degree * (std::abs(std::cos(lat_rad)) < 1e-9 ? 1.0 : std::cos(lat_rad));
  const double longitude_deg = instance->reference_longitude_deg + (instance->statePosition.y_km / longitude_scale);
  const double altitude_m = instance->reference_altitude_m + (instance->statePosition.z_km * 1000.0);
  const double altitude_ft = altitude_m * 3.28083989501312;
  const double airspeed_kt = instance->flightStatus.airspeed_mps * 1.9438444924406;
  const double climb_rate_fps = instance->flightStatus.climb_rate * 3.28083989501312;

  std::ostringstream stream;
  stream.setf(std::ios::fixed);
  stream.precision(6);
  stream
      << latitude_deg << ','
      << longitude_deg << ','
      << altitude_ft << ','
      << instance->stateOrientation.roll_deg << ','
      << instance->stateOrientation.pitch_deg << ','
      << instance->stateOrientation.yaw_deg << ','
      << airspeed_kt << ','
      << instance->flightStatus.energy_state_norm << ','
      << instance->flightStatus.angle_of_attack_deg << ','
      << climb_rate_fps << ','
      << instance->flightStatus.health_code << ','
      << instance->missionStatus.waypoint_index << ','
      << instance->missionStatus.total_waypoints << ','
      << instance->missionStatus.distance_to_waypoint_km << ','
      << instance->missionStatus.arrived << ','
      << instance->missionStatus.complete
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

}  // namespace

ModelInstance* create_instance() {
  return new ModelInstance();
}

void destroy_instance(ModelInstance* instance) {
  if (instance == nullptr) {
    return;
  }
  reset_sockets(instance);
  delete instance;
}

fmi2Status enter_initialization(ModelInstance* instance) {
  return ensure_sockets(instance) ? fmi2OK : fmi2Warning;
}

fmi2Status reset_instance(ModelInstance* instance) {
  reset_sockets(instance);
  instance->pilotCommand = {};
  instance->pilotCommand.throttle_norm = 0.6;
  instance->pilotCommand.throttle_aux_norm = 0.6;
  return fmi2OK;
}

fmi2Status do_step(ModelInstance* instance) {
  receive_control_packet(instance);
  send_telemetry_packet(instance);
  return fmi2OK;
}

fmi2Status get_real(ModelInstance* instance, const fmi2ValueReference vr[], size_t nvr, fmi2Real value[]) {
  for (size_t i = 0; i < nvr; ++i) {
    switch (vr[i]) {
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_REFERENCE_LATITUDE_DEG: value[i] = instance->reference_latitude_deg; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_REFERENCE_LONGITUDE_DEG: value[i] = instance->reference_longitude_deg; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_REFERENCE_ALTITUDE_M: value[i] = instance->reference_altitude_m; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_STATEPOSITION_X_KM: value[i] = instance->statePosition.x_km; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_STATEPOSITION_Y_KM: value[i] = instance->statePosition.y_km; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_STATEPOSITION_Z_KM: value[i] = instance->statePosition.z_km; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_STATEORIENTATION_ROLL_DEG: value[i] = instance->stateOrientation.roll_deg; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_STATEORIENTATION_PITCH_DEG: value[i] = instance->stateOrientation.pitch_deg; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_STATEORIENTATION_YAW_DEG: value[i] = instance->stateOrientation.yaw_deg; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_FLIGHTSTATUS_AIRSPEED_MPS: value[i] = instance->flightStatus.airspeed_mps; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_FLIGHTSTATUS_ENERGY_STATE_NORM: value[i] = instance->flightStatus.energy_state_norm; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_FLIGHTSTATUS_ANGLE_OF_ATTACK_DEG: value[i] = instance->flightStatus.angle_of_attack_deg; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_FLIGHTSTATUS_CLIMB_RATE: value[i] = instance->flightStatus.climb_rate; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_MISSIONSTATUS_DISTANCE_TO_WAYPOINT_KM: value[i] = instance->missionStatus.distance_to_waypoint_km; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_PILOTCOMMAND_STICK_PITCH_NORM: value[i] = instance->pilotCommand.stick_pitch_norm; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_PILOTCOMMAND_STICK_ROLL_NORM: value[i] = instance->pilotCommand.stick_roll_norm; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_PILOTCOMMAND_RUDDER_NORM: value[i] = instance->pilotCommand.rudder_norm; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_PILOTCOMMAND_THROTTLE_NORM: value[i] = instance->pilotCommand.throttle_norm; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_PILOTCOMMAND_THROTTLE_AUX_NORM: value[i] = instance->pilotCommand.throttle_aux_norm; break;
      default: return fmi2Error;
    }
  }
  return fmi2OK;
}

fmi2Status get_integer(ModelInstance* instance, const fmi2ValueReference vr[], size_t nvr, fmi2Integer value[]) {
  for (size_t i = 0; i < nvr; ++i) {
    switch (vr[i]) {
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_TELEMETRY_PORT: value[i] = instance->telemetry_port; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_CONTROL_PORT: value[i] = instance->control_port; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_FLIGHTSTATUS_HEALTH_CODE: value[i] = instance->flightStatus.health_code; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_MISSIONSTATUS_WAYPOINT_INDEX: value[i] = instance->missionStatus.waypoint_index; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_MISSIONSTATUS_TOTAL_WAYPOINTS: value[i] = instance->missionStatus.total_waypoints; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_PILOTCOMMAND_BUTTON_MASK: value[i] = instance->pilotCommand.button_mask; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_PILOTCOMMAND_HAT_X: value[i] = instance->pilotCommand.hat_x; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_PILOTCOMMAND_HAT_Y: value[i] = instance->pilotCommand.hat_y; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_PILOTCOMMAND_MODE_SWITCH: value[i] = instance->pilotCommand.mode_switch; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_PILOTCOMMAND_RESERVED: value[i] = instance->pilotCommand.reserved; break;
      default: return fmi2Error;
    }
  }
  return fmi2OK;
}

fmi2Status get_boolean(ModelInstance* instance, const fmi2ValueReference vr[], size_t nvr, fmi2Boolean value[]) {
  for (size_t i = 0; i < nvr; ++i) {
    switch (vr[i]) {
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_MISSIONSTATUS_ARRIVED: value[i] = static_cast<fmi2Boolean>(instance->missionStatus.arrived); break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_MISSIONSTATUS_COMPLETE: value[i] = static_cast<fmi2Boolean>(instance->missionStatus.complete); break;
      default: return fmi2Error;
    }
  }
  return fmi2OK;
}

fmi2Status get_string(ModelInstance* instance, const fmi2ValueReference vr[], size_t nvr, fmi2String value[]) {
  for (size_t i = 0; i < nvr; ++i) {
    switch (vr[i]) {
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_TRANSPORT: value[i] = instance->transport.c_str(); break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_REMOTE_HOST: value[i] = instance->remote_host.c_str(); break;
      default: return fmi2Error;
    }
  }
  return fmi2OK;
}

fmi2Status set_real(ModelInstance* instance, const fmi2ValueReference vr[], size_t nvr, const fmi2Real value[]) {
  for (size_t i = 0; i < nvr; ++i) {
    switch (vr[i]) {
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_REFERENCE_LATITUDE_DEG: instance->reference_latitude_deg = value[i]; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_REFERENCE_LONGITUDE_DEG: instance->reference_longitude_deg = value[i]; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_REFERENCE_ALTITUDE_M: instance->reference_altitude_m = value[i]; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_STATEPOSITION_X_KM: instance->statePosition.x_km = value[i]; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_STATEPOSITION_Y_KM: instance->statePosition.y_km = value[i]; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_STATEPOSITION_Z_KM: instance->statePosition.z_km = value[i]; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_STATEORIENTATION_ROLL_DEG: instance->stateOrientation.roll_deg = value[i]; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_STATEORIENTATION_PITCH_DEG: instance->stateOrientation.pitch_deg = value[i]; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_STATEORIENTATION_YAW_DEG: instance->stateOrientation.yaw_deg = value[i]; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_FLIGHTSTATUS_AIRSPEED_MPS: instance->flightStatus.airspeed_mps = value[i]; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_FLIGHTSTATUS_ENERGY_STATE_NORM: instance->flightStatus.energy_state_norm = value[i]; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_FLIGHTSTATUS_ANGLE_OF_ATTACK_DEG: instance->flightStatus.angle_of_attack_deg = value[i]; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_FLIGHTSTATUS_CLIMB_RATE: instance->flightStatus.climb_rate = value[i]; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_MISSIONSTATUS_DISTANCE_TO_WAYPOINT_KM: instance->missionStatus.distance_to_waypoint_km = value[i]; break;
      default: return fmi2Error;
    }
  }
  return fmi2OK;
}

fmi2Status set_integer(ModelInstance* instance, const fmi2ValueReference vr[], size_t nvr, const fmi2Integer value[]) {
  bool network_param_changed = false;
  for (size_t i = 0; i < nvr; ++i) {
    switch (vr[i]) {
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_TELEMETRY_PORT: instance->telemetry_port = value[i]; network_param_changed = true; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_CONTROL_PORT: instance->control_port = value[i]; network_param_changed = true; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_FLIGHTSTATUS_HEALTH_CODE: instance->flightStatus.health_code = value[i]; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_MISSIONSTATUS_WAYPOINT_INDEX: instance->missionStatus.waypoint_index = value[i]; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_MISSIONSTATUS_TOTAL_WAYPOINTS: instance->missionStatus.total_waypoints = value[i]; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_PILOTCOMMAND_BUTTON_MASK: instance->pilotCommand.button_mask = value[i]; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_PILOTCOMMAND_HAT_X: instance->pilotCommand.hat_x = value[i]; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_PILOTCOMMAND_HAT_Y: instance->pilotCommand.hat_y = value[i]; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_PILOTCOMMAND_MODE_SWITCH: instance->pilotCommand.mode_switch = value[i]; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_PILOTCOMMAND_RESERVED: instance->pilotCommand.reserved = value[i]; break;
      default: return fmi2Error;
    }
  }
  if (network_param_changed) {
    reset_sockets(instance);
  }
  return fmi2OK;
}

fmi2Status set_boolean(ModelInstance* instance, const fmi2ValueReference vr[], size_t nvr, const fmi2Boolean value[]) {
  for (size_t i = 0; i < nvr; ++i) {
    switch (vr[i]) {
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_MISSIONSTATUS_ARRIVED: instance->missionStatus.arrived = value[i]; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_MISSIONSTATUS_COMPLETE: instance->missionStatus.complete = value[i]; break;
      default: return fmi2Error;
    }
  }
  return fmi2OK;
}

fmi2Status set_string(ModelInstance* instance, const fmi2ValueReference vr[], size_t nvr, const fmi2String value[]) {
  bool network_param_changed = false;
  for (size_t i = 0; i < nvr; ++i) {
    switch (vr[i]) {
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_TRANSPORT: instance->transport = value[i] ? value[i] : ""; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_REMOTE_HOST: instance->remote_host = value[i] ? value[i] : ""; network_param_changed = true; break;
      default: return fmi2Error;
    }
  }
  if (network_param_changed) {
    reset_sockets(instance);
  }
  return fmi2OK;
}

}  // namespace fgbridge
