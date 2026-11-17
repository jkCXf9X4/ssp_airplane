#ifndef AIRCRAFT_ROS2UDPBRIDGE_HOOKS_H
#define AIRCRAFT_ROS2UDPBRIDGE_HOOKS_H

#include "Aircraft_Ros2UdpBridge.h"
#include "fmi2/fmi2Functions.h"

/* Model hooks for Aircraft.Ros2UdpBridge. Implemented in Aircraft_Ros2UdpBridge_model.cpp. */

#ifdef __cplusplus
extern "C" {
#endif

fmi2Status Aircraft_Ros2UdpBridge_model_initialize(Aircraft_Ros2UdpBridge_Instance* instance);

fmi2Status Aircraft_Ros2UdpBridge_model_do_step(
    Aircraft_Ros2UdpBridge_Instance* instance, fmi2Real current_communication_point,
    fmi2Real communication_step_size);

fmi2Status Aircraft_Ros2UdpBridge_model_terminate(Aircraft_Ros2UdpBridge_Instance* instance);

/* Called before fmi2Reset clears the instance. The returned status is
   propagated; the user_data pointer survives the reset. */
fmi2Status Aircraft_Ros2UdpBridge_model_reset(Aircraft_Ros2UdpBridge_Instance* instance);

/* Called from fmi2FreeInstance, before the instance is deleted. The
   status is ignored: the FMI interface cannot report a free failure. */
fmi2Status Aircraft_Ros2UdpBridge_model_free(Aircraft_Ros2UdpBridge_Instance* instance);

#ifdef __cplusplus
}
#endif

#endif  /* AIRCRAFT_ROS2UDPBRIDGE_HOOKS_H */
