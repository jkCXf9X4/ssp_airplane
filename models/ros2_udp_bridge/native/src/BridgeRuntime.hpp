#pragma once

#include <netinet/in.h>

#include <chrono>
#include <string>

#include "fmi2Functions.h"
#include "Aircraft_Ros2UdpBridge.h"

namespace ros2udpbridge {

constexpr const char* kGuid = AIRCRAFT_ROS2UDPBRIDGE_GUID;
constexpr const char* kTypesPlatform = fmi2TypesPlatform;
constexpr const char* kVersion = fmi2Version;

struct ModelInstance : public Aircraft_Ros2UdpBridge_Instance {
  int tx_socket = -1;
  int rx_socket = -1;
  sockaddr_in tx_address {};
  bool sockets_ready = false;
  std::chrono::steady_clock::time_point last_control_update {};
  bool control_active = false;
};

ModelInstance* create_instance();
void destroy_instance(ModelInstance* instance);

fmi2Status enter_initialization(ModelInstance* instance);
fmi2Status reset_instance(ModelInstance* instance);
void invalidate_network(ModelInstance* instance);
fmi2Status do_step(ModelInstance* instance);

}  // namespace ros2udpbridge
