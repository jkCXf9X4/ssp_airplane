#include "BridgeRuntime.hpp"

#include <arpa/inet.h>
#include <fcntl.h>
#include <unistd.h>

#include <cerrno>
#include <chrono>
#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>

namespace fgbridge {
namespace {

constexpr double kControlTimeoutSec = 1.0;

void close_socket_if_open(int& fd) {
  if (fd >= 0) {
    close(fd);
    fd = -1;
  }
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

bool extract_json_value(const std::string& payload, const char* key, std::string& value) {
  const std::string quoted_key = std::string("\"") + key + "\"";
  const std::size_t key_pos = payload.find(quoted_key);
  if (key_pos == std::string::npos) {
    return false;
  }
  const std::size_t colon = payload.find(':', key_pos + quoted_key.size());
  if (colon == std::string::npos) {
    return false;
  }

  std::size_t start = colon + 1;
  while (start < payload.size() && (payload[start] == ' ' || payload[start] == '\t')) {
    ++start;
  }
  std::size_t end = start;
  if (start < payload.size() && payload[start] == '"') {
    ++start;
    end = start;
    while (end < payload.size() && payload[end] != '"') {
      ++end;
    }
    if (end >= payload.size()) {
      return false;
    }
    value = payload.substr(start, end - start);
    return true;
  }

  while (end < payload.size() && payload[end] != ',' && payload[end] != '}' && payload[end] != '\n' &&
         payload[end] != '\r') {
    ++end;
  }
  while (end > start && (payload[end - 1] == ' ' || payload[end - 1] == '\t')) {
    --end;
  }
  if (end <= start) {
    return false;
  }
  value = payload.substr(start, end - start);
  return true;
}

bool extract_json_double(const std::string& payload, const char* key, double& value) {
  std::string raw;
  return extract_json_value(payload, key, raw) && parse_double(raw, value);
}

bool extract_json_int(const std::string& payload, const char* key, int& value) {
  std::string raw;
  return extract_json_value(payload, key, raw) && parse_int(raw, value);
}

void set_inactive_command(ModelInstance* instance) {
  instance->control_active = false;
  instance->pilotCommand.stick_pitch_norm = 0.0;
  instance->pilotCommand.stick_roll_norm = 0.0;
  instance->pilotCommand.rudder_norm = 0.0;
  instance->pilotCommand.throttle_norm = 0.6;
  instance->pilotCommand.throttle_aux_norm = 0.6;
  instance->pilotCommand.button_mask = 0;
  instance->pilotCommand.hat_x = 0;
  instance->pilotCommand.hat_y = 0;
  instance->pilotCommand.mode_switch = -1;
  instance->pilotCommand.reserved = 0;
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

void apply_control_json(ModelInstance* instance, const std::string& payload) {
  Aircraft_PilotCommand next = {};
  next.throttle_norm = 0.6;
  next.throttle_aux_norm = 0.6;
  next.mode_switch = 0;

  extract_json_double(payload, "stick_pitch_norm", next.stick_pitch_norm);
  extract_json_double(payload, "stick_roll_norm", next.stick_roll_norm);
  extract_json_double(payload, "rudder_norm", next.rudder_norm);
  extract_json_double(payload, "throttle_norm", next.throttle_norm);
  next.throttle_aux_norm = next.throttle_norm;
  extract_json_double(payload, "throttle_aux_norm", next.throttle_aux_norm);
  extract_json_int(payload, "button_mask", next.button_mask);
  extract_json_int(payload, "hat_x", next.hat_x);
  extract_json_int(payload, "hat_y", next.hat_y);
  extract_json_int(payload, "mode_switch", next.mode_switch);
  extract_json_int(payload, "reserved", next.reserved);

  instance->pilotCommand = next;
  instance->control_active = true;
  instance->last_control_update = std::chrono::steady_clock::now();
}

void receive_control_packet(ModelInstance* instance) {
  if (!ensure_sockets(instance)) {
    return;
  }

  char buffer[2048];
  bool received_valid_packet = false;
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
    const std::string payload(buffer);
    if (payload.find('{') == std::string::npos) {
      continue;
    }
    apply_control_json(instance, payload);
    received_valid_packet = true;
  }

  if (received_valid_packet) {
    return;
  }

  if (!instance->control_active) {
    return;
  }

  const auto age =
      std::chrono::duration_cast<std::chrono::duration<double>>(std::chrono::steady_clock::now() - instance->last_control_update)
          .count();
  if (age > kControlTimeoutSec) {
    set_inactive_command(instance);
  }
}

std::string telemetry_packet(const ModelInstance* instance) {
  char buffer[1024];
  const int written = std::snprintf(
      buffer,
      sizeof(buffer),
      "{"
      "\"transport\":\"%s\","
      "\"reference_latitude_deg\":%.6f,"
      "\"reference_longitude_deg\":%.6f,"
      "\"reference_altitude_m\":%.6f,"
      "\"state\":{\"x_km\":%.6f,\"y_km\":%.6f,\"z_km\":%.6f},"
      "\"orientation\":{\"roll_deg\":%.6f,\"pitch_deg\":%.6f,\"yaw_deg\":%.6f},"
      "\"flight_status\":{\"airspeed_mps\":%.6f,\"energy_state_norm\":%.6f,\"angle_of_attack_deg\":%.6f,\"climb_rate\":%.6f,"
      "\"health_code\":%d},"
      "\"mission_status\":{\"waypoint_index\":%d,\"total_waypoints\":%d,\"distance_to_waypoint_km\":%.6f,\"arrived\":%s,"
      "\"complete\":%s}"
      "}\n",
      instance->transport.c_str(),
      instance->reference_latitude_deg,
      instance->reference_longitude_deg,
      instance->reference_altitude_m,
      instance->statePosition.x_km,
      instance->statePosition.y_km,
      instance->statePosition.z_km,
      instance->stateOrientation.roll_deg,
      instance->stateOrientation.pitch_deg,
      instance->stateOrientation.yaw_deg,
      instance->flightStatus.airspeed_mps,
      instance->flightStatus.energy_state_norm,
      instance->flightStatus.angle_of_attack_deg,
      instance->flightStatus.climb_rate,
      instance->flightStatus.health_code,
      instance->missionStatus.waypoint_index,
      instance->missionStatus.total_waypoints,
      instance->missionStatus.distance_to_waypoint_km,
      instance->missionStatus.arrived ? "true" : "false",
      instance->missionStatus.complete ? "true" : "false");
  if (written <= 0) {
    return {};
  }
  const size_t size = static_cast<size_t>(written) < sizeof(buffer) ? static_cast<size_t>(written) : sizeof(buffer) - 1;
  return std::string(buffer, size);
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
  auto* instance = new ModelInstance();
  set_inactive_command(instance);
  return instance;
}

void destroy_instance(ModelInstance* instance) {
  if (instance == nullptr) {
    return;
  }
  reset_sockets(instance);
  delete instance;
}

fmi2Status enter_initialization(ModelInstance* instance) {
  if (!instance->transport.empty() && instance->transport != "Ros2UdpBridge") {
    instance->transport = "Ros2UdpBridge";
  }
  set_inactive_command(instance);
  return ensure_sockets(instance) ? fmi2OK : fmi2Warning;
}

fmi2Status reset_instance(ModelInstance* instance) {
  reset_sockets(instance);
  set_inactive_command(instance);
  return fmi2OK;
}

void invalidate_network(ModelInstance* instance) {
  reset_sockets(instance);
}

fmi2Status do_step(ModelInstance* instance) {
  receive_control_packet(instance);
  send_telemetry_packet(instance);
  return fmi2OK;
}

}  // namespace fgbridge
