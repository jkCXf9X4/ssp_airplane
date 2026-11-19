#pragma once

#include <netinet/in.h>

#include <chrono>
#include <string>

#include "fmi2/fmi2Functions.h"
#include "Aircraft_UdpBridge.h"

namespace udpbridge {

struct BridgeState {
  Aircraft_UdpBridge_Instance* instance = nullptr;
  int tx_socket = -1;
  int rx_socket = -1;
  sockaddr_in tx_address {};
  bool sockets_ready = false;
  std::chrono::steady_clock::time_point last_control_update {};
  bool control_active = false;
  bool telemetry_started = false;
};

BridgeState* create_state(Aircraft_UdpBridge_Instance* instance);
void destroy_state(BridgeState* state);

fmi2Status enter_initialization(BridgeState* state);
fmi2Status reset_instance(BridgeState* state);
fmi2Status do_step(BridgeState* state);

}  // namespace udpbridge
