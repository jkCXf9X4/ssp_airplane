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

struct Aircraft_ControlInterface_Instance {
  std::string input_scheme = "HOTAS";
  int telemetry_rate_hz = 120;
  bool useBridgeInput = false;
  Aircraft_PilotCommand bridgeInput = {};
  Aircraft_PilotCommand pilotCommand = {};
};

inline const std::string& Aircraft_ControlInterface_INPUT_SCHEME_get(const void* instance) { return static_cast<const Aircraft_ControlInterface_Instance*>(instance)->input_scheme; }
inline std::string& Aircraft_ControlInterface_INPUT_SCHEME_get_mut(void* instance) { return static_cast<Aircraft_ControlInterface_Instance*>(instance)->input_scheme; }

inline constexpr Aircraft_FieldBinding Aircraft_ControlInterface_Bindings[] = {
  {AIRCRAFT_CONTROLINTERFACE_VR_TELEMETRY_RATE_HZ, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_ControlInterface_Instance, telemetry_rate_hz), true},
  {AIRCRAFT_CONTROLINTERFACE_VR_USEBRIDGEINPUT, AIRCRAFT_SCALAR_BOOLEAN, offsetof(Aircraft_ControlInterface_Instance, useBridgeInput), true},
  {AIRCRAFT_CONTROLINTERFACE_VR_BRIDGEINPUT_STICK_PITCH_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_ControlInterface_Instance, bridgeInput) + offsetof(Aircraft_PilotCommand, stick_pitch_norm), true},
  {AIRCRAFT_CONTROLINTERFACE_VR_BRIDGEINPUT_STICK_ROLL_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_ControlInterface_Instance, bridgeInput) + offsetof(Aircraft_PilotCommand, stick_roll_norm), true},
  {AIRCRAFT_CONTROLINTERFACE_VR_BRIDGEINPUT_RUDDER_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_ControlInterface_Instance, bridgeInput) + offsetof(Aircraft_PilotCommand, rudder_norm), true},
  {AIRCRAFT_CONTROLINTERFACE_VR_BRIDGEINPUT_THROTTLE_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_ControlInterface_Instance, bridgeInput) + offsetof(Aircraft_PilotCommand, throttle_norm), true},
  {AIRCRAFT_CONTROLINTERFACE_VR_BRIDGEINPUT_THROTTLE_AUX_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_ControlInterface_Instance, bridgeInput) + offsetof(Aircraft_PilotCommand, throttle_aux_norm), true},
  {AIRCRAFT_CONTROLINTERFACE_VR_BRIDGEINPUT_BUTTON_MASK, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_ControlInterface_Instance, bridgeInput) + offsetof(Aircraft_PilotCommand, button_mask), true},
  {AIRCRAFT_CONTROLINTERFACE_VR_BRIDGEINPUT_HAT_X, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_ControlInterface_Instance, bridgeInput) + offsetof(Aircraft_PilotCommand, hat_x), true},
  {AIRCRAFT_CONTROLINTERFACE_VR_BRIDGEINPUT_HAT_Y, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_ControlInterface_Instance, bridgeInput) + offsetof(Aircraft_PilotCommand, hat_y), true},
  {AIRCRAFT_CONTROLINTERFACE_VR_BRIDGEINPUT_MODE_SWITCH, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_ControlInterface_Instance, bridgeInput) + offsetof(Aircraft_PilotCommand, mode_switch), true},
  {AIRCRAFT_CONTROLINTERFACE_VR_BRIDGEINPUT_RESERVED, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_ControlInterface_Instance, bridgeInput) + offsetof(Aircraft_PilotCommand, reserved), true},
  {AIRCRAFT_CONTROLINTERFACE_VR_PILOTCOMMAND_STICK_PITCH_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_ControlInterface_Instance, pilotCommand) + offsetof(Aircraft_PilotCommand, stick_pitch_norm), false},
  {AIRCRAFT_CONTROLINTERFACE_VR_PILOTCOMMAND_STICK_ROLL_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_ControlInterface_Instance, pilotCommand) + offsetof(Aircraft_PilotCommand, stick_roll_norm), false},
  {AIRCRAFT_CONTROLINTERFACE_VR_PILOTCOMMAND_RUDDER_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_ControlInterface_Instance, pilotCommand) + offsetof(Aircraft_PilotCommand, rudder_norm), false},
  {AIRCRAFT_CONTROLINTERFACE_VR_PILOTCOMMAND_THROTTLE_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_ControlInterface_Instance, pilotCommand) + offsetof(Aircraft_PilotCommand, throttle_norm), false},
  {AIRCRAFT_CONTROLINTERFACE_VR_PILOTCOMMAND_THROTTLE_AUX_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_ControlInterface_Instance, pilotCommand) + offsetof(Aircraft_PilotCommand, throttle_aux_norm), false},
  {AIRCRAFT_CONTROLINTERFACE_VR_PILOTCOMMAND_BUTTON_MASK, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_ControlInterface_Instance, pilotCommand) + offsetof(Aircraft_PilotCommand, button_mask), false},
  {AIRCRAFT_CONTROLINTERFACE_VR_PILOTCOMMAND_HAT_X, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_ControlInterface_Instance, pilotCommand) + offsetof(Aircraft_PilotCommand, hat_x), false},
  {AIRCRAFT_CONTROLINTERFACE_VR_PILOTCOMMAND_HAT_Y, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_ControlInterface_Instance, pilotCommand) + offsetof(Aircraft_PilotCommand, hat_y), false},
  {AIRCRAFT_CONTROLINTERFACE_VR_PILOTCOMMAND_MODE_SWITCH, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_ControlInterface_Instance, pilotCommand) + offsetof(Aircraft_PilotCommand, mode_switch), false},
  {AIRCRAFT_CONTROLINTERFACE_VR_PILOTCOMMAND_RESERVED, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_ControlInterface_Instance, pilotCommand) + offsetof(Aircraft_PilotCommand, reserved), false},
};
inline constexpr size_t Aircraft_ControlInterface_BindingCount = sizeof(Aircraft_ControlInterface_Bindings) / sizeof(Aircraft_ControlInterface_Bindings[0]);

inline constexpr Aircraft_StringFieldBinding Aircraft_ControlInterface_StringBindings[] = {
  {AIRCRAFT_CONTROLINTERFACE_VR_INPUT_SCHEME, &Aircraft_ControlInterface_INPUT_SCHEME_get, &Aircraft_ControlInterface_INPUT_SCHEME_get_mut, true},
};
inline constexpr size_t Aircraft_ControlInterface_StringBindingCount = sizeof(Aircraft_ControlInterface_StringBindings) / sizeof(Aircraft_ControlInterface_StringBindings[0]);

#endif  /* __cplusplus */