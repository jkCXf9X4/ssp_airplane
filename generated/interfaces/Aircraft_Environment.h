#pragma once

#include "Aircraft_InterfaceCommon.h"

/* Generated interface for Aircraft.Environment. Do not edit manually. */

typedef enum Aircraft_Environment_ValueReference {
  AIRCRAFT_ENVIRONMENT_VR_ACTUATION_COMMAND_LEFT_AILERON_DEG = 0,
  AIRCRAFT_ENVIRONMENT_VR_ACTUATION_COMMAND_RIGHT_AILERON_DEG = 1,
  AIRCRAFT_ENVIRONMENT_VR_ACTUATION_COMMAND_ELEVATOR_DEG = 2,
  AIRCRAFT_ENVIRONMENT_VR_ACTUATION_COMMAND_RUDDER_DEG = 3,
  AIRCRAFT_ENVIRONMENT_VR_ACTUATION_COMMAND_FLAPERON_DEG = 4,
  AIRCRAFT_ENVIRONMENT_VR_DIRECTION_COMMAND_ROLL_DEG = 5,
  AIRCRAFT_ENVIRONMENT_VR_DIRECTION_COMMAND_PITCH_DEG = 6,
  AIRCRAFT_ENVIRONMENT_VR_DIRECTION_COMMAND_YAW_DEG = 7,
  AIRCRAFT_ENVIRONMENT_VR_LIFT_LIFT_KN = 8,
  AIRCRAFT_ENVIRONMENT_VR_LIFT_DRAG_KN = 9,
  AIRCRAFT_ENVIRONMENT_VR_LIFT_PITCHING_MOMENT_KNM = 10,
  AIRCRAFT_ENVIRONMENT_VR_THRUST_IN_THRUST_KN = 11,
  AIRCRAFT_ENVIRONMENT_VR_THRUST_IN_MASS_FLOW_KGPS = 12,
  AIRCRAFT_ENVIRONMENT_VR_THRUST_IN_EXHAUST_VELOCITY_MPS = 13,
  AIRCRAFT_ENVIRONMENT_VR_ORIENTATION_ROLL_DEG = 14,
  AIRCRAFT_ENVIRONMENT_VR_ORIENTATION_PITCH_DEG = 15,
  AIRCRAFT_ENVIRONMENT_VR_ORIENTATION_YAW_DEG = 16,
  AIRCRAFT_ENVIRONMENT_VR_LOCATION_X_KM = 17,
  AIRCRAFT_ENVIRONMENT_VR_LOCATION_Y_KM = 18,
  AIRCRAFT_ENVIRONMENT_VR_LOCATION_Z_KM = 19,
  AIRCRAFT_ENVIRONMENT_VR_FLIGHT_STATUS_AIRSPEED_MPS = 20,
  AIRCRAFT_ENVIRONMENT_VR_FLIGHT_STATUS_ENERGY_STATE_NORM = 21,
  AIRCRAFT_ENVIRONMENT_VR_FLIGHT_STATUS_ANGLE_OF_ATTACK_DEG = 22,
  AIRCRAFT_ENVIRONMENT_VR_FLIGHT_STATUS_CLIMB_RATE = 23,
  AIRCRAFT_ENVIRONMENT_VR_FLIGHT_STATUS_HEALTH_CODE = 24,
} Aircraft_Environment_ValueReference;

#ifdef __cplusplus

struct Aircraft_Environment_Instance {
  Aircraft_SurfaceActuationCommand actuation_command = {};
  Aircraft_OrientationEuler direction_command = {};
  Aircraft_LiftState lift = {};
  Aircraft_ThrustState thrust_in = {};
  Aircraft_OrientationEuler orientation = {};
  Aircraft_PositionXYZ location = {};
  Aircraft_FlightStatusPacket flight_status = {};
};

inline constexpr Aircraft_FieldBinding Aircraft_Environment_Bindings[] = {
  {AIRCRAFT_ENVIRONMENT_VR_ACTUATION_COMMAND_LEFT_AILERON_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_Environment_Instance, actuation_command) + offsetof(Aircraft_SurfaceActuationCommand, left_aileron_deg), true},
  {AIRCRAFT_ENVIRONMENT_VR_ACTUATION_COMMAND_RIGHT_AILERON_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_Environment_Instance, actuation_command) + offsetof(Aircraft_SurfaceActuationCommand, right_aileron_deg), true},
  {AIRCRAFT_ENVIRONMENT_VR_ACTUATION_COMMAND_ELEVATOR_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_Environment_Instance, actuation_command) + offsetof(Aircraft_SurfaceActuationCommand, elevator_deg), true},
  {AIRCRAFT_ENVIRONMENT_VR_ACTUATION_COMMAND_RUDDER_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_Environment_Instance, actuation_command) + offsetof(Aircraft_SurfaceActuationCommand, rudder_deg), true},
  {AIRCRAFT_ENVIRONMENT_VR_ACTUATION_COMMAND_FLAPERON_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_Environment_Instance, actuation_command) + offsetof(Aircraft_SurfaceActuationCommand, flaperon_deg), true},
  {AIRCRAFT_ENVIRONMENT_VR_DIRECTION_COMMAND_ROLL_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_Environment_Instance, direction_command) + offsetof(Aircraft_OrientationEuler, roll_deg), true},
  {AIRCRAFT_ENVIRONMENT_VR_DIRECTION_COMMAND_PITCH_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_Environment_Instance, direction_command) + offsetof(Aircraft_OrientationEuler, pitch_deg), true},
  {AIRCRAFT_ENVIRONMENT_VR_DIRECTION_COMMAND_YAW_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_Environment_Instance, direction_command) + offsetof(Aircraft_OrientationEuler, yaw_deg), true},
  {AIRCRAFT_ENVIRONMENT_VR_LIFT_LIFT_KN, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_Environment_Instance, lift) + offsetof(Aircraft_LiftState, lift_kn), true},
  {AIRCRAFT_ENVIRONMENT_VR_LIFT_DRAG_KN, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_Environment_Instance, lift) + offsetof(Aircraft_LiftState, drag_kn), true},
  {AIRCRAFT_ENVIRONMENT_VR_LIFT_PITCHING_MOMENT_KNM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_Environment_Instance, lift) + offsetof(Aircraft_LiftState, pitching_moment_knm), true},
  {AIRCRAFT_ENVIRONMENT_VR_THRUST_IN_THRUST_KN, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_Environment_Instance, thrust_in) + offsetof(Aircraft_ThrustState, thrust_kn), true},
  {AIRCRAFT_ENVIRONMENT_VR_THRUST_IN_MASS_FLOW_KGPS, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_Environment_Instance, thrust_in) + offsetof(Aircraft_ThrustState, mass_flow_kgps), true},
  {AIRCRAFT_ENVIRONMENT_VR_THRUST_IN_EXHAUST_VELOCITY_MPS, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_Environment_Instance, thrust_in) + offsetof(Aircraft_ThrustState, exhaust_velocity_mps), true},
  {AIRCRAFT_ENVIRONMENT_VR_ORIENTATION_ROLL_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_Environment_Instance, orientation) + offsetof(Aircraft_OrientationEuler, roll_deg), false},
  {AIRCRAFT_ENVIRONMENT_VR_ORIENTATION_PITCH_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_Environment_Instance, orientation) + offsetof(Aircraft_OrientationEuler, pitch_deg), false},
  {AIRCRAFT_ENVIRONMENT_VR_ORIENTATION_YAW_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_Environment_Instance, orientation) + offsetof(Aircraft_OrientationEuler, yaw_deg), false},
  {AIRCRAFT_ENVIRONMENT_VR_LOCATION_X_KM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_Environment_Instance, location) + offsetof(Aircraft_PositionXYZ, x_km), false},
  {AIRCRAFT_ENVIRONMENT_VR_LOCATION_Y_KM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_Environment_Instance, location) + offsetof(Aircraft_PositionXYZ, y_km), false},
  {AIRCRAFT_ENVIRONMENT_VR_LOCATION_Z_KM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_Environment_Instance, location) + offsetof(Aircraft_PositionXYZ, z_km), false},
  {AIRCRAFT_ENVIRONMENT_VR_FLIGHT_STATUS_AIRSPEED_MPS, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_Environment_Instance, flight_status) + offsetof(Aircraft_FlightStatusPacket, airspeed_mps), false},
  {AIRCRAFT_ENVIRONMENT_VR_FLIGHT_STATUS_ENERGY_STATE_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_Environment_Instance, flight_status) + offsetof(Aircraft_FlightStatusPacket, energy_state_norm), false},
  {AIRCRAFT_ENVIRONMENT_VR_FLIGHT_STATUS_ANGLE_OF_ATTACK_DEG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_Environment_Instance, flight_status) + offsetof(Aircraft_FlightStatusPacket, angle_of_attack_deg), false},
  {AIRCRAFT_ENVIRONMENT_VR_FLIGHT_STATUS_CLIMB_RATE, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_Environment_Instance, flight_status) + offsetof(Aircraft_FlightStatusPacket, climb_rate), false},
  {AIRCRAFT_ENVIRONMENT_VR_FLIGHT_STATUS_HEALTH_CODE, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_Environment_Instance, flight_status) + offsetof(Aircraft_FlightStatusPacket, health_code), false},
};
inline constexpr size_t Aircraft_Environment_BindingCount = sizeof(Aircraft_Environment_Bindings) / sizeof(Aircraft_Environment_Bindings[0]);

inline constexpr const Aircraft_StringFieldBinding* Aircraft_Environment_StringBindings = nullptr;
inline constexpr size_t Aircraft_Environment_StringBindingCount = 0;

#endif  /* __cplusplus */