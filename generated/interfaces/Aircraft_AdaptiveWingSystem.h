#pragma once

#include "Aircraft_InterfaceCommon.h"

/* Generated interface for Aircraft.AdaptiveWingSystem. Do not edit manually. */

typedef enum Aircraft_AdaptiveWingSystem_ValueReference {
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_REFERENCE_AREA_M2 = 0,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_SPAN_M = 1,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_ASPECT_RATIO = 2,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_CONTROL_AUTHORITY_DEG = 3,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_LOAD_FACTOR_LIMIT_G = 4,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_DIRECTION_COMMAND_ROLL_DEG = 5,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_DIRECTION_COMMAND_PITCH_DEG = 6,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_DIRECTION_COMMAND_YAW_DEG = 7,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_FLIGHT_SPEED_AIRSPEED_MPS = 8,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_FLIGHT_SPEED_ENERGY_STATE_NORM = 9,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_FLIGHT_SPEED_ANGLE_OF_ATTACK_DEG = 10,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_FLIGHT_SPEED_CLIMB_RATE = 11,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_FLIGHT_SPEED_HEALTH_CODE = 12,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_ACTUATION_COMMAND_LEFT_AILERON_DEG = 13,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_ACTUATION_COMMAND_RIGHT_AILERON_DEG = 14,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_ACTUATION_COMMAND_ELEVATOR_DEG = 15,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_ACTUATION_COMMAND_RUDDER_DEG = 16,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_ACTUATION_COMMAND_FLAPERON_DEG = 17,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_LIFTINTERFACE_LIFT_KN = 18,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_LIFTINTERFACE_DRAG_KN = 19,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_LIFTINTERFACE_PITCHING_MOMENT_KNM = 20,
} Aircraft_AdaptiveWingSystem_ValueReference;

#ifdef __cplusplus

struct Aircraft_AdaptiveWingSystem_Instance {
  double reference_area_m2 = 28.0;
  double span_m = 10.0;
  double aspect_ratio = 3.6;
  int control_authority_deg = 25;
  int load_factor_limit_g = 9;
  Aircraft_OrientationEuler direction_command = {};
  Aircraft_FlightStatusPacket flight_speed = {};
  Aircraft_SurfaceActuationCommand actuation_command = {};
  Aircraft_LiftState liftInterface = {};
};

inline constexpr Aircraft_FieldBinding Aircraft_AdaptiveWingSystem_Bindings[] = {
  {AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_REFERENCE_AREA_M2, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_AdaptiveWingSystem_Instance, reference_area_m2), true},
  {AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_SPAN_M, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_AdaptiveWingSystem_Instance, span_m), true},
  {AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_ASPECT_RATIO, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_AdaptiveWingSystem_Instance, aspect_ratio), true},
  {AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_CONTROL_AUTHORITY_DEG, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_AdaptiveWingSystem_Instance, control_authority_deg), true},
  {AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_LOAD_FACTOR_LIMIT_G, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_AdaptiveWingSystem_Instance, load_factor_limit_g), true},
  {AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_DIRECTION_COMMAND_ROLL_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_AdaptiveWingSystem_Instance, direction_command) + offsetof(Aircraft_OrientationEuler, roll_deg), true},
  {AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_DIRECTION_COMMAND_PITCH_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_AdaptiveWingSystem_Instance, direction_command) + offsetof(Aircraft_OrientationEuler, pitch_deg), true},
  {AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_DIRECTION_COMMAND_YAW_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_AdaptiveWingSystem_Instance, direction_command) + offsetof(Aircraft_OrientationEuler, yaw_deg), true},
  {AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_FLIGHT_SPEED_AIRSPEED_MPS, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_AdaptiveWingSystem_Instance, flight_speed) + offsetof(Aircraft_FlightStatusPacket, airspeed_mps), true},
  {AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_FLIGHT_SPEED_ENERGY_STATE_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_AdaptiveWingSystem_Instance, flight_speed) + offsetof(Aircraft_FlightStatusPacket, energy_state_norm), true},
  {AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_FLIGHT_SPEED_ANGLE_OF_ATTACK_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_AdaptiveWingSystem_Instance, flight_speed) + offsetof(Aircraft_FlightStatusPacket, angle_of_attack_deg), true},
  {AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_FLIGHT_SPEED_CLIMB_RATE, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_AdaptiveWingSystem_Instance, flight_speed) + offsetof(Aircraft_FlightStatusPacket, climb_rate), true},
  {AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_FLIGHT_SPEED_HEALTH_CODE, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_AdaptiveWingSystem_Instance, flight_speed) + offsetof(Aircraft_FlightStatusPacket, health_code), true},
  {AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_ACTUATION_COMMAND_LEFT_AILERON_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_AdaptiveWingSystem_Instance, actuation_command) + offsetof(Aircraft_SurfaceActuationCommand, left_aileron_deg), false},
  {AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_ACTUATION_COMMAND_RIGHT_AILERON_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_AdaptiveWingSystem_Instance, actuation_command) + offsetof(Aircraft_SurfaceActuationCommand, right_aileron_deg), false},
  {AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_ACTUATION_COMMAND_ELEVATOR_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_AdaptiveWingSystem_Instance, actuation_command) + offsetof(Aircraft_SurfaceActuationCommand, elevator_deg), false},
  {AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_ACTUATION_COMMAND_RUDDER_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_AdaptiveWingSystem_Instance, actuation_command) + offsetof(Aircraft_SurfaceActuationCommand, rudder_deg), false},
  {AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_ACTUATION_COMMAND_FLAPERON_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_AdaptiveWingSystem_Instance, actuation_command) + offsetof(Aircraft_SurfaceActuationCommand, flaperon_deg), false},
  {AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_LIFTINTERFACE_LIFT_KN, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_AdaptiveWingSystem_Instance, liftInterface) + offsetof(Aircraft_LiftState, lift_kn), false},
  {AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_LIFTINTERFACE_DRAG_KN, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_AdaptiveWingSystem_Instance, liftInterface) + offsetof(Aircraft_LiftState, drag_kn), false},
  {AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_LIFTINTERFACE_PITCHING_MOMENT_KNM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_AdaptiveWingSystem_Instance, liftInterface) + offsetof(Aircraft_LiftState, pitching_moment_knm), false},
};
inline constexpr size_t Aircraft_AdaptiveWingSystem_BindingCount = sizeof(Aircraft_AdaptiveWingSystem_Bindings) / sizeof(Aircraft_AdaptiveWingSystem_Bindings[0]);

inline constexpr const Aircraft_StringFieldBinding* Aircraft_AdaptiveWingSystem_StringBindings = nullptr;
inline constexpr size_t Aircraft_AdaptiveWingSystem_StringBindingCount = 0;

#endif  /* __cplusplus */