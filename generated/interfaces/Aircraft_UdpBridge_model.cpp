/* Hand-written model behaviour for Aircraft.UdpBridge.
   The generator creates this file only when it is absent and never rewrites it. */
#include "Aircraft_UdpBridge_hooks.h"

#include "BridgeRuntime.hpp"

fmi2Status Aircraft_UdpBridge_model_initialize(Aircraft_UdpBridge_Instance* instance) {
  if (instance->user_data == nullptr) {
    auto* state = udpbridge::create_state(instance);
    if (state == nullptr) {
      return fmi2Error;
    }
    instance->user_data = state;
  }
  auto* state = static_cast<udpbridge::BridgeState*>(instance->user_data);
  return udpbridge::enter_initialization(state);
}

fmi2Status Aircraft_UdpBridge_model_do_step(
    Aircraft_UdpBridge_Instance* instance, fmi2Real current_communication_point,
    fmi2Real communication_step_size) {
  (void)current_communication_point;
  (void)communication_step_size;
  auto* state = static_cast<udpbridge::BridgeState*>(instance->user_data);
  if (state == nullptr) {
    return fmi2Error;
  }
  return udpbridge::do_step(state);
}

fmi2Status Aircraft_UdpBridge_model_terminate(Aircraft_UdpBridge_Instance* instance) {
  auto* state = static_cast<udpbridge::BridgeState*>(instance->user_data);
  if (state == nullptr) {
    return fmi2OK;
  }
  return udpbridge::reset_instance(state);
}

fmi2Status Aircraft_UdpBridge_model_reset(Aircraft_UdpBridge_Instance* instance) {
  auto* state = static_cast<udpbridge::BridgeState*>(instance->user_data);
  if (state == nullptr) {
    return fmi2OK;
  }
  return udpbridge::reset_instance(state);
}

fmi2Status Aircraft_UdpBridge_model_free(Aircraft_UdpBridge_Instance* instance) {
  auto* state = static_cast<udpbridge::BridgeState*>(instance->user_data);
  udpbridge::destroy_state(state);
  instance->user_data = nullptr;
  return fmi2OK;
}
