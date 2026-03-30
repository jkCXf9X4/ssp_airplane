#pragma once

#include "Aircraft_InterfaceCommon.h"

/* Generated interface for Aircraft.ControlInterface. Do not edit manually. */

typedef enum Aircraft_ControlInterface_ValueReference {
  AIRCRAFT_CONTROLINTERFACE_VR_INPUT_SCHEME = 0,
  AIRCRAFT_CONTROLINTERFACE_VR_TELEMETRY_RATE_HZ = 1,
  AIRCRAFT_CONTROLINTERFACE_VR_USEBRIDGEINPUT = 2,
  AIRCRAFT_CONTROLINTERFACE_VR_BRIDGEINPUT_STICK_PITCH_NORM = 3,
  AIRCRAFT_CONTROLINTERFACE_VR_BRIDGEINPUT_STICK_ROLL_NORM = 4,
  AIRCRAFT_CONTROLINTERFACE_VR_BRIDGEINPUT_RUDDER_NORM = 5,
  AIRCRAFT_CONTROLINTERFACE_VR_BRIDGEINPUT_THROTTLE_NORM = 6,
  AIRCRAFT_CONTROLINTERFACE_VR_BRIDGEINPUT_THROTTLE_AUX_NORM = 7,
  AIRCRAFT_CONTROLINTERFACE_VR_BRIDGEINPUT_BUTTON_MASK = 8,
  AIRCRAFT_CONTROLINTERFACE_VR_BRIDGEINPUT_HAT_X = 9,
  AIRCRAFT_CONTROLINTERFACE_VR_BRIDGEINPUT_HAT_Y = 10,
  AIRCRAFT_CONTROLINTERFACE_VR_BRIDGEINPUT_MODE_SWITCH = 11,
  AIRCRAFT_CONTROLINTERFACE_VR_BRIDGEINPUT_RESERVED = 12,
  AIRCRAFT_CONTROLINTERFACE_VR_PILOTCOMMAND_STICK_PITCH_NORM = 13,
  AIRCRAFT_CONTROLINTERFACE_VR_PILOTCOMMAND_STICK_ROLL_NORM = 14,
  AIRCRAFT_CONTROLINTERFACE_VR_PILOTCOMMAND_RUDDER_NORM = 15,
  AIRCRAFT_CONTROLINTERFACE_VR_PILOTCOMMAND_THROTTLE_NORM = 16,
  AIRCRAFT_CONTROLINTERFACE_VR_PILOTCOMMAND_THROTTLE_AUX_NORM = 17,
  AIRCRAFT_CONTROLINTERFACE_VR_PILOTCOMMAND_BUTTON_MASK = 18,
  AIRCRAFT_CONTROLINTERFACE_VR_PILOTCOMMAND_HAT_X = 19,
  AIRCRAFT_CONTROLINTERFACE_VR_PILOTCOMMAND_HAT_Y = 20,
  AIRCRAFT_CONTROLINTERFACE_VR_PILOTCOMMAND_MODE_SWITCH = 21,
  AIRCRAFT_CONTROLINTERFACE_VR_PILOTCOMMAND_RESERVED = 22,
} Aircraft_ControlInterface_ValueReference;

#ifdef __cplusplus

inline constexpr size_t Aircraft_ControlInterface_VrCount = 23;

struct Aircraft_ControlInterface_Instance {
  Aircraft_VrMapping vr_map[23] = {};
  std::string input_scheme = "HOTAS";
  int telemetry_rate_hz = 120;
  bool useBridgeInput = false;
  Aircraft_PilotCommand bridgeInput = {};
  Aircraft_PilotCommand pilotCommand = {};
};

inline void Aircraft_ControlInterface_initialize_vr_map(Aircraft_ControlInterface_Instance* instance) {
  for (size_t i = 0; i < Aircraft_ControlInterface_VrCount; ++i) {
    instance->vr_map[i] = {nullptr, AIRCRAFT_DATA_NONE, false};
  }
  instance->vr_map[AIRCRAFT_CONTROLINTERFACE_VR_INPUT_SCHEME] = {&instance->input_scheme, AIRCRAFT_DATA_STRING, true};
  instance->vr_map[AIRCRAFT_CONTROLINTERFACE_VR_TELEMETRY_RATE_HZ] = {&instance->telemetry_rate_hz, AIRCRAFT_DATA_INTEGER, true};
  instance->vr_map[AIRCRAFT_CONTROLINTERFACE_VR_USEBRIDGEINPUT] = {&instance->useBridgeInput, AIRCRAFT_DATA_BOOLEAN, true};
  instance->vr_map[AIRCRAFT_CONTROLINTERFACE_VR_BRIDGEINPUT_STICK_PITCH_NORM] = {&instance->bridgeInput.stick_pitch_norm, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_CONTROLINTERFACE_VR_BRIDGEINPUT_STICK_ROLL_NORM] = {&instance->bridgeInput.stick_roll_norm, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_CONTROLINTERFACE_VR_BRIDGEINPUT_RUDDER_NORM] = {&instance->bridgeInput.rudder_norm, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_CONTROLINTERFACE_VR_BRIDGEINPUT_THROTTLE_NORM] = {&instance->bridgeInput.throttle_norm, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_CONTROLINTERFACE_VR_BRIDGEINPUT_THROTTLE_AUX_NORM] = {&instance->bridgeInput.throttle_aux_norm, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_CONTROLINTERFACE_VR_BRIDGEINPUT_BUTTON_MASK] = {&instance->bridgeInput.button_mask, AIRCRAFT_DATA_INTEGER, true};
  instance->vr_map[AIRCRAFT_CONTROLINTERFACE_VR_BRIDGEINPUT_HAT_X] = {&instance->bridgeInput.hat_x, AIRCRAFT_DATA_INTEGER, true};
  instance->vr_map[AIRCRAFT_CONTROLINTERFACE_VR_BRIDGEINPUT_HAT_Y] = {&instance->bridgeInput.hat_y, AIRCRAFT_DATA_INTEGER, true};
  instance->vr_map[AIRCRAFT_CONTROLINTERFACE_VR_BRIDGEINPUT_MODE_SWITCH] = {&instance->bridgeInput.mode_switch, AIRCRAFT_DATA_INTEGER, true};
  instance->vr_map[AIRCRAFT_CONTROLINTERFACE_VR_BRIDGEINPUT_RESERVED] = {&instance->bridgeInput.reserved, AIRCRAFT_DATA_INTEGER, true};
  instance->vr_map[AIRCRAFT_CONTROLINTERFACE_VR_PILOTCOMMAND_STICK_PITCH_NORM] = {&instance->pilotCommand.stick_pitch_norm, AIRCRAFT_DATA_REAL, false};
  instance->vr_map[AIRCRAFT_CONTROLINTERFACE_VR_PILOTCOMMAND_STICK_ROLL_NORM] = {&instance->pilotCommand.stick_roll_norm, AIRCRAFT_DATA_REAL, false};
  instance->vr_map[AIRCRAFT_CONTROLINTERFACE_VR_PILOTCOMMAND_RUDDER_NORM] = {&instance->pilotCommand.rudder_norm, AIRCRAFT_DATA_REAL, false};
  instance->vr_map[AIRCRAFT_CONTROLINTERFACE_VR_PILOTCOMMAND_THROTTLE_NORM] = {&instance->pilotCommand.throttle_norm, AIRCRAFT_DATA_REAL, false};
  instance->vr_map[AIRCRAFT_CONTROLINTERFACE_VR_PILOTCOMMAND_THROTTLE_AUX_NORM] = {&instance->pilotCommand.throttle_aux_norm, AIRCRAFT_DATA_REAL, false};
  instance->vr_map[AIRCRAFT_CONTROLINTERFACE_VR_PILOTCOMMAND_BUTTON_MASK] = {&instance->pilotCommand.button_mask, AIRCRAFT_DATA_INTEGER, false};
  instance->vr_map[AIRCRAFT_CONTROLINTERFACE_VR_PILOTCOMMAND_HAT_X] = {&instance->pilotCommand.hat_x, AIRCRAFT_DATA_INTEGER, false};
  instance->vr_map[AIRCRAFT_CONTROLINTERFACE_VR_PILOTCOMMAND_HAT_Y] = {&instance->pilotCommand.hat_y, AIRCRAFT_DATA_INTEGER, false};
  instance->vr_map[AIRCRAFT_CONTROLINTERFACE_VR_PILOTCOMMAND_MODE_SWITCH] = {&instance->pilotCommand.mode_switch, AIRCRAFT_DATA_INTEGER, false};
  instance->vr_map[AIRCRAFT_CONTROLINTERFACE_VR_PILOTCOMMAND_RESERVED] = {&instance->pilotCommand.reserved, AIRCRAFT_DATA_INTEGER, false};
}

#endif  /* __cplusplus */