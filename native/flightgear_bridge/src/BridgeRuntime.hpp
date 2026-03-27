#pragma once

#include <netinet/in.h>

#include <string>

#include "fmi2Functions.h"
#include "architecture_interface.h"

namespace fgbridge {

constexpr const char* kGuid = "{2d7d0b06-4525-4e59-b188-2a9b0b8cb5bb}";
constexpr const char* kTypesPlatform = fmi2TypesPlatform;
constexpr const char* kVersion = fmi2Version;

struct ModelInstance {
  std::string transport = "FlightGearGeneric";
  double reference_latitude_deg = 0.0;
  double reference_longitude_deg = 0.0;
  double reference_altitude_m = 0.0;
  std::string remote_host = "127.0.0.1";
  int telemetry_port = 5501;
  int control_port = 5502;

  Aircraft_PositionXYZ statePosition {};
  Aircraft_OrientationEuler stateOrientation {};
  Aircraft_FlightStatusPacket flightStatus {};
  Aircraft_MissionStatus missionStatus {};
  Aircraft_PilotCommand pilotCommand {};

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
