#pragma once

#include "Aircraft_InterfaceCommon.h"

/* Generated interface for Aircraft.MissionComputer. Do not edit manually. */

typedef enum Aircraft_MissionComputer_ValueReference {
  AIRCRAFT_MISSIONCOMPUTER_VR_MANUALINPUT_STICK_PITCH_NORM = 0,
  AIRCRAFT_MISSIONCOMPUTER_VR_MANUALINPUT_STICK_ROLL_NORM = 1,
  AIRCRAFT_MISSIONCOMPUTER_VR_MANUALINPUT_RUDDER_NORM = 2,
  AIRCRAFT_MISSIONCOMPUTER_VR_MANUALINPUT_THROTTLE_NORM = 3,
  AIRCRAFT_MISSIONCOMPUTER_VR_MANUALINPUT_THROTTLE_AUX_NORM = 4,
  AIRCRAFT_MISSIONCOMPUTER_VR_MANUALINPUT_BUTTON_MASK = 5,
  AIRCRAFT_MISSIONCOMPUTER_VR_MANUALINPUT_HAT_X = 6,
  AIRCRAFT_MISSIONCOMPUTER_VR_MANUALINPUT_HAT_Y = 7,
  AIRCRAFT_MISSIONCOMPUTER_VR_MANUALINPUT_MODE_SWITCH = 8,
  AIRCRAFT_MISSIONCOMPUTER_VR_MANUALINPUT_RESERVED = 9,
  AIRCRAFT_MISSIONCOMPUTER_VR_AUTOPILOTINPUT_STICK_PITCH_NORM = 10,
  AIRCRAFT_MISSIONCOMPUTER_VR_AUTOPILOTINPUT_STICK_ROLL_NORM = 11,
  AIRCRAFT_MISSIONCOMPUTER_VR_AUTOPILOTINPUT_RUDDER_NORM = 12,
  AIRCRAFT_MISSIONCOMPUTER_VR_AUTOPILOTINPUT_THROTTLE_NORM = 13,
  AIRCRAFT_MISSIONCOMPUTER_VR_AUTOPILOTINPUT_THROTTLE_AUX_NORM = 14,
  AIRCRAFT_MISSIONCOMPUTER_VR_AUTOPILOTINPUT_BUTTON_MASK = 15,
  AIRCRAFT_MISSIONCOMPUTER_VR_AUTOPILOTINPUT_HAT_X = 16,
  AIRCRAFT_MISSIONCOMPUTER_VR_AUTOPILOTINPUT_HAT_Y = 17,
  AIRCRAFT_MISSIONCOMPUTER_VR_AUTOPILOTINPUT_MODE_SWITCH = 18,
  AIRCRAFT_MISSIONCOMPUTER_VR_AUTOPILOTINPUT_RESERVED = 19,
  AIRCRAFT_MISSIONCOMPUTER_VR_FUELSTATUS_FUEL_REMAINING_KG = 20,
  AIRCRAFT_MISSIONCOMPUTER_VR_FUELSTATUS_FUEL_LEVEL_NORM = 21,
  AIRCRAFT_MISSIONCOMPUTER_VR_FUELSTATUS_FUEL_STARVED = 22,
  AIRCRAFT_MISSIONCOMPUTER_VR_ENGINETHROTTLE_THROTTLE_NORM = 23,
  AIRCRAFT_MISSIONCOMPUTER_VR_ENGINETHROTTLE_FUEL_ENABLE = 24,
  AIRCRAFT_MISSIONCOMPUTER_VR_ENGINETHROTTLE_AFTERBURNER_ENABLE = 25,
  AIRCRAFT_MISSIONCOMPUTER_VR_DIRECTION_COMMAND_ROLL_DEG = 26,
  AIRCRAFT_MISSIONCOMPUTER_VR_DIRECTION_COMMAND_PITCH_DEG = 27,
  AIRCRAFT_MISSIONCOMPUTER_VR_DIRECTION_COMMAND_YAW_DEG = 28,
} Aircraft_MissionComputer_ValueReference;

#ifdef __cplusplus

struct Aircraft_MissionComputer_Instance {
  Aircraft_PilotCommand manualInput = {};
  Aircraft_PilotCommand autopilotInput = {};
  Aircraft_FuelLevelState fuelStatus = {};
  Aircraft_ThrottleCommand engineThrottle = {};
  Aircraft_OrientationEuler direction_command = {};
};

inline constexpr Aircraft_FieldBinding Aircraft_MissionComputer_Bindings[] = {
  {AIRCRAFT_MISSIONCOMPUTER_VR_MANUALINPUT_STICK_PITCH_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_MissionComputer_Instance, manualInput) + offsetof(Aircraft_PilotCommand, stick_pitch_norm), true},
  {AIRCRAFT_MISSIONCOMPUTER_VR_MANUALINPUT_STICK_ROLL_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_MissionComputer_Instance, manualInput) + offsetof(Aircraft_PilotCommand, stick_roll_norm), true},
  {AIRCRAFT_MISSIONCOMPUTER_VR_MANUALINPUT_RUDDER_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_MissionComputer_Instance, manualInput) + offsetof(Aircraft_PilotCommand, rudder_norm), true},
  {AIRCRAFT_MISSIONCOMPUTER_VR_MANUALINPUT_THROTTLE_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_MissionComputer_Instance, manualInput) + offsetof(Aircraft_PilotCommand, throttle_norm), true},
  {AIRCRAFT_MISSIONCOMPUTER_VR_MANUALINPUT_THROTTLE_AUX_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_MissionComputer_Instance, manualInput) + offsetof(Aircraft_PilotCommand, throttle_aux_norm), true},
  {AIRCRAFT_MISSIONCOMPUTER_VR_MANUALINPUT_BUTTON_MASK, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_MissionComputer_Instance, manualInput) + offsetof(Aircraft_PilotCommand, button_mask), true},
  {AIRCRAFT_MISSIONCOMPUTER_VR_MANUALINPUT_HAT_X, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_MissionComputer_Instance, manualInput) + offsetof(Aircraft_PilotCommand, hat_x), true},
  {AIRCRAFT_MISSIONCOMPUTER_VR_MANUALINPUT_HAT_Y, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_MissionComputer_Instance, manualInput) + offsetof(Aircraft_PilotCommand, hat_y), true},
  {AIRCRAFT_MISSIONCOMPUTER_VR_MANUALINPUT_MODE_SWITCH, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_MissionComputer_Instance, manualInput) + offsetof(Aircraft_PilotCommand, mode_switch), true},
  {AIRCRAFT_MISSIONCOMPUTER_VR_MANUALINPUT_RESERVED, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_MissionComputer_Instance, manualInput) + offsetof(Aircraft_PilotCommand, reserved), true},
  {AIRCRAFT_MISSIONCOMPUTER_VR_AUTOPILOTINPUT_STICK_PITCH_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_MissionComputer_Instance, autopilotInput) + offsetof(Aircraft_PilotCommand, stick_pitch_norm), true},
  {AIRCRAFT_MISSIONCOMPUTER_VR_AUTOPILOTINPUT_STICK_ROLL_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_MissionComputer_Instance, autopilotInput) + offsetof(Aircraft_PilotCommand, stick_roll_norm), true},
  {AIRCRAFT_MISSIONCOMPUTER_VR_AUTOPILOTINPUT_RUDDER_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_MissionComputer_Instance, autopilotInput) + offsetof(Aircraft_PilotCommand, rudder_norm), true},
  {AIRCRAFT_MISSIONCOMPUTER_VR_AUTOPILOTINPUT_THROTTLE_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_MissionComputer_Instance, autopilotInput) + offsetof(Aircraft_PilotCommand, throttle_norm), true},
  {AIRCRAFT_MISSIONCOMPUTER_VR_AUTOPILOTINPUT_THROTTLE_AUX_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_MissionComputer_Instance, autopilotInput) + offsetof(Aircraft_PilotCommand, throttle_aux_norm), true},
  {AIRCRAFT_MISSIONCOMPUTER_VR_AUTOPILOTINPUT_BUTTON_MASK, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_MissionComputer_Instance, autopilotInput) + offsetof(Aircraft_PilotCommand, button_mask), true},
  {AIRCRAFT_MISSIONCOMPUTER_VR_AUTOPILOTINPUT_HAT_X, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_MissionComputer_Instance, autopilotInput) + offsetof(Aircraft_PilotCommand, hat_x), true},
  {AIRCRAFT_MISSIONCOMPUTER_VR_AUTOPILOTINPUT_HAT_Y, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_MissionComputer_Instance, autopilotInput) + offsetof(Aircraft_PilotCommand, hat_y), true},
  {AIRCRAFT_MISSIONCOMPUTER_VR_AUTOPILOTINPUT_MODE_SWITCH, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_MissionComputer_Instance, autopilotInput) + offsetof(Aircraft_PilotCommand, mode_switch), true},
  {AIRCRAFT_MISSIONCOMPUTER_VR_AUTOPILOTINPUT_RESERVED, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_MissionComputer_Instance, autopilotInput) + offsetof(Aircraft_PilotCommand, reserved), true},
  {AIRCRAFT_MISSIONCOMPUTER_VR_FUELSTATUS_FUEL_REMAINING_KG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_MissionComputer_Instance, fuelStatus) + offsetof(Aircraft_FuelLevelState, fuel_remaining_kg), true},
  {AIRCRAFT_MISSIONCOMPUTER_VR_FUELSTATUS_FUEL_LEVEL_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_MissionComputer_Instance, fuelStatus) + offsetof(Aircraft_FuelLevelState, fuel_level_norm), true},
  {AIRCRAFT_MISSIONCOMPUTER_VR_FUELSTATUS_FUEL_STARVED, AIRCRAFT_SCALAR_BOOLEAN, offsetof(Aircraft_MissionComputer_Instance, fuelStatus) + offsetof(Aircraft_FuelLevelState, fuel_starved), true},
  {AIRCRAFT_MISSIONCOMPUTER_VR_ENGINETHROTTLE_THROTTLE_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_MissionComputer_Instance, engineThrottle) + offsetof(Aircraft_ThrottleCommand, throttle_norm), false},
  {AIRCRAFT_MISSIONCOMPUTER_VR_ENGINETHROTTLE_FUEL_ENABLE, AIRCRAFT_SCALAR_BOOLEAN, offsetof(Aircraft_MissionComputer_Instance, engineThrottle) + offsetof(Aircraft_ThrottleCommand, fuel_enable), false},
  {AIRCRAFT_MISSIONCOMPUTER_VR_ENGINETHROTTLE_AFTERBURNER_ENABLE, AIRCRAFT_SCALAR_BOOLEAN, offsetof(Aircraft_MissionComputer_Instance, engineThrottle) + offsetof(Aircraft_ThrottleCommand, afterburner_enable), false},
  {AIRCRAFT_MISSIONCOMPUTER_VR_DIRECTION_COMMAND_ROLL_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_MissionComputer_Instance, direction_command) + offsetof(Aircraft_OrientationEuler, roll_deg), false},
  {AIRCRAFT_MISSIONCOMPUTER_VR_DIRECTION_COMMAND_PITCH_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_MissionComputer_Instance, direction_command) + offsetof(Aircraft_OrientationEuler, pitch_deg), false},
  {AIRCRAFT_MISSIONCOMPUTER_VR_DIRECTION_COMMAND_YAW_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_MissionComputer_Instance, direction_command) + offsetof(Aircraft_OrientationEuler, yaw_deg), false},
};
inline constexpr size_t Aircraft_MissionComputer_BindingCount = sizeof(Aircraft_MissionComputer_Bindings) / sizeof(Aircraft_MissionComputer_Bindings[0]);

inline constexpr const Aircraft_StringFieldBinding* Aircraft_MissionComputer_StringBindings = nullptr;
inline constexpr size_t Aircraft_MissionComputer_StringBindingCount = 0;

#endif  /* __cplusplus */