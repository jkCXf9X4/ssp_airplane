#include "BridgeRuntime.hpp"

#include <arpa/inet.h>
#include <fcntl.h>
#include <unistd.h>

#include <cerrno>
#include <cmath>
#include <cstdio>
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

  char buffer[512];
  const int written = std::snprintf(
      buffer,
      sizeof(buffer),
      "%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%d,%d,%d,%.6f,%d,%d\n",
      latitude_deg,
      longitude_deg,
      altitude_ft,
      instance->stateOrientation.roll_deg,
      instance->stateOrientation.pitch_deg,
      instance->stateOrientation.yaw_deg,
      airspeed_kt,
      instance->flightStatus.energy_state_norm,
      instance->flightStatus.angle_of_attack_deg,
      climb_rate_fps,
      instance->flightStatus.health_code,
      instance->missionStatus.waypoint_index,
      instance->missionStatus.total_waypoints,
      instance->missionStatus.distance_to_waypoint_km,
      instance->missionStatus.arrived ? 1 : 0,
      instance->missionStatus.complete ? 1 : 0);
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

void invalidate_network(ModelInstance* instance) {
  reset_sockets(instance);
}

fmi2Status do_step(ModelInstance* instance) {
  receive_control_packet(instance);
  send_telemetry_packet(instance);
  return fmi2OK;
}

}  // namespace fgbridge
