#include "BridgeRuntime.hpp"

#include <arpa/inet.h>
#include <fcntl.h>
#include <unistd.h>

#include <cerrno>
#include <new>
#include <chrono>
#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>

namespace ros2udpbridge {
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

void set_inactive_command(BridgeState* state) {
  state->control_active = false;
  state->instance->pilotCommand.stick_pitch_norm = 0.0;
  state->instance->pilotCommand.stick_roll_norm = 0.0;
  state->instance->pilotCommand.rudder_norm = 0.0;
  state->instance->pilotCommand.throttle_norm = 0.6;
  state->instance->pilotCommand.throttle_aux_norm = 0.6;
  state->instance->pilotCommand.button_mask = 0;
  state->instance->pilotCommand.hat_x = 0;
  state->instance->pilotCommand.hat_y = 0;
  state->instance->pilotCommand.mode_switch = -1;
  state->instance->pilotCommand.reserved = 0;
}

bool ensure_sockets(BridgeState* state) {
  if (state->sockets_ready) {
    return true;
  }

  state->tx_socket = socket(AF_INET, SOCK_DGRAM, 0);
  if (state->tx_socket < 0) {
    return false;
  }

  state->rx_socket = socket(AF_INET, SOCK_DGRAM, 0);
  if (state->rx_socket < 0) {
    close_socket_if_open(state->tx_socket);
    return false;
  }

  const int flags = fcntl(state->rx_socket, F_GETFL, 0);
  if (flags < 0 || fcntl(state->rx_socket, F_SETFL, flags | O_NONBLOCK) < 0) {
    close_socket_if_open(state->tx_socket);
    close_socket_if_open(state->rx_socket);
    return false;
  }

  sockaddr_in rx_address {};
  rx_address.sin_family = AF_INET;
  rx_address.sin_port = htons(static_cast<uint16_t>(state->instance->control_port));
  rx_address.sin_addr.s_addr = htonl(INADDR_ANY);

  constexpr int reuse = 1;
  setsockopt(state->rx_socket, SOL_SOCKET, SO_REUSEADDR, &reuse, sizeof(reuse));
  if (bind(state->rx_socket, reinterpret_cast<sockaddr*>(&rx_address), sizeof(rx_address)) < 0) {
    close_socket_if_open(state->tx_socket);
    close_socket_if_open(state->rx_socket);
    return false;
  }

  state->tx_address = {};
  state->tx_address.sin_family = AF_INET;
  state->tx_address.sin_port = htons(static_cast<uint16_t>(state->instance->telemetry_port));
  if (inet_pton(AF_INET, state->instance->remote_host.c_str(), &state->tx_address.sin_addr) != 1) {
    close_socket_if_open(state->tx_socket);
    close_socket_if_open(state->rx_socket);
    return false;
  }

  state->sockets_ready = true;
  return true;
}

void reset_sockets(BridgeState* state) {
  state->sockets_ready = false;
  close_socket_if_open(state->tx_socket);
  close_socket_if_open(state->rx_socket);
}

void apply_control_json(BridgeState* state, const std::string& payload) {
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

  state->instance->pilotCommand = next;
  state->control_active = true;
  state->last_control_update = std::chrono::steady_clock::now();
}

void receive_control_packet(BridgeState* state) {
  if (!ensure_sockets(state)) {
    return;
  }

  char buffer[2048];
  bool received_valid_packet = false;
  for (;;) {
    ssize_t received = recv(state->rx_socket, buffer, sizeof(buffer) - 1, 0);
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
    apply_control_json(state, payload);
    received_valid_packet = true;
  }

  if (received_valid_packet) {
    return;
  }

  if (!state->control_active) {
    return;
  }

  const auto age =
      std::chrono::duration_cast<std::chrono::duration<double>>(std::chrono::steady_clock::now() - state->last_control_update)
          .count();
  if (age > kControlTimeoutSec) {
    set_inactive_command(state);
  }
}

std::string telemetry_packet(const BridgeState* state) {
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
      state->instance->transport.c_str(),
      state->instance->reference_latitude_deg,
      state->instance->reference_longitude_deg,
      state->instance->reference_altitude_m,
      state->instance->statePosition.x_km,
      state->instance->statePosition.y_km,
      state->instance->statePosition.z_km,
      state->instance->stateOrientation.roll_deg,
      state->instance->stateOrientation.pitch_deg,
      state->instance->stateOrientation.yaw_deg,
      state->instance->flightStatus.airspeed_mps,
      state->instance->flightStatus.energy_state_norm,
      state->instance->flightStatus.angle_of_attack_deg,
      state->instance->flightStatus.climb_rate,
      state->instance->flightStatus.health_code,
      state->instance->missionStatus.waypoint_index,
      state->instance->missionStatus.total_waypoints,
      state->instance->missionStatus.distance_to_waypoint_km,
      state->instance->missionStatus.arrived ? "true" : "false",
      state->instance->missionStatus.complete ? "true" : "false");
  if (written <= 0) {
    return {};
  }
  const size_t size = static_cast<size_t>(written) < sizeof(buffer) ? static_cast<size_t>(written) : sizeof(buffer) - 1;
  return std::string(buffer, size);
}

void send_telemetry_packet(BridgeState* state) {
  if (!ensure_sockets(state)) {
    return;
  }
  const std::string payload = telemetry_packet(state);
  sendto(
      state->tx_socket,
      payload.c_str(),
      payload.size(),
      0,
      reinterpret_cast<const sockaddr*>(&state->tx_address),
      sizeof(state->tx_address));
}

}  // namespace

BridgeState* create_state(Aircraft_Ros2UdpBridge_Instance* instance) {
  auto* state = new (std::nothrow) BridgeState();
  if (state == nullptr) {
    return nullptr;
  }
  state->instance = instance;
  set_inactive_command(state);
  return state;
}

void destroy_state(BridgeState* state) {
  if (state == nullptr) {
    return;
  }
  reset_sockets(state);
  set_inactive_command(state);
  delete state;
}

fmi2Status enter_initialization(BridgeState* state) {
  if (!state->instance->transport.empty() && state->instance->transport != "Ros2UdpBridge") {
    state->instance->transport = "Ros2UdpBridge";
  }
  set_inactive_command(state);
  return ensure_sockets(state) ? fmi2OK : fmi2Warning;
}

fmi2Status reset_instance(BridgeState* state) {
  reset_sockets(state);
  set_inactive_command(state);
  return fmi2OK;
}

fmi2Status do_step(BridgeState* state) {
  receive_control_packet(state);
  send_telemetry_packet(state);
  return fmi2OK;
}

}  // namespace ros2udpbridge
