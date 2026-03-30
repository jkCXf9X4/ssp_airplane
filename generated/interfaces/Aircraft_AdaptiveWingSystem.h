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

inline constexpr size_t Aircraft_AdaptiveWingSystem_VrCount = 21;

struct Aircraft_AdaptiveWingSystem_Instance {
  Aircraft_VrMapping vr_map[21] = {};
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

inline void Aircraft_AdaptiveWingSystem_initialize_vr_map(Aircraft_AdaptiveWingSystem_Instance* instance) {
  for (size_t i = 0; i < Aircraft_AdaptiveWingSystem_VrCount; ++i) {
    instance->vr_map[i] = {nullptr, AIRCRAFT_DATA_NONE, false};
  }
  instance->vr_map[AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_REFERENCE_AREA_M2] = {&instance->reference_area_m2, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_SPAN_M] = {&instance->span_m, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_ASPECT_RATIO] = {&instance->aspect_ratio, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_CONTROL_AUTHORITY_DEG] = {&instance->control_authority_deg, AIRCRAFT_DATA_INTEGER, true};
  instance->vr_map[AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_LOAD_FACTOR_LIMIT_G] = {&instance->load_factor_limit_g, AIRCRAFT_DATA_INTEGER, true};
  instance->vr_map[AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_DIRECTION_COMMAND_ROLL_DEG] = {&instance->direction_command.roll_deg, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_DIRECTION_COMMAND_PITCH_DEG] = {&instance->direction_command.pitch_deg, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_DIRECTION_COMMAND_YAW_DEG] = {&instance->direction_command.yaw_deg, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_FLIGHT_SPEED_AIRSPEED_MPS] = {&instance->flight_speed.airspeed_mps, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_FLIGHT_SPEED_ENERGY_STATE_NORM] = {&instance->flight_speed.energy_state_norm, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_FLIGHT_SPEED_ANGLE_OF_ATTACK_DEG] = {&instance->flight_speed.angle_of_attack_deg, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_FLIGHT_SPEED_CLIMB_RATE] = {&instance->flight_speed.climb_rate, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_FLIGHT_SPEED_HEALTH_CODE] = {&instance->flight_speed.health_code, AIRCRAFT_DATA_INTEGER, true};
  instance->vr_map[AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_ACTUATION_COMMAND_LEFT_AILERON_DEG] = {&instance->actuation_command.left_aileron_deg, AIRCRAFT_DATA_REAL, false};
  instance->vr_map[AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_ACTUATION_COMMAND_RIGHT_AILERON_DEG] = {&instance->actuation_command.right_aileron_deg, AIRCRAFT_DATA_REAL, false};
  instance->vr_map[AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_ACTUATION_COMMAND_ELEVATOR_DEG] = {&instance->actuation_command.elevator_deg, AIRCRAFT_DATA_REAL, false};
  instance->vr_map[AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_ACTUATION_COMMAND_RUDDER_DEG] = {&instance->actuation_command.rudder_deg, AIRCRAFT_DATA_REAL, false};
  instance->vr_map[AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_ACTUATION_COMMAND_FLAPERON_DEG] = {&instance->actuation_command.flaperon_deg, AIRCRAFT_DATA_REAL, false};
  instance->vr_map[AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_LIFTINTERFACE_LIFT_KN] = {&instance->liftInterface.lift_kn, AIRCRAFT_DATA_REAL, false};
  instance->vr_map[AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_LIFTINTERFACE_DRAG_KN] = {&instance->liftInterface.drag_kn, AIRCRAFT_DATA_REAL, false};
  instance->vr_map[AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_LIFTINTERFACE_PITCHING_MOMENT_KNM] = {&instance->liftInterface.pitching_moment_knm, AIRCRAFT_DATA_REAL, false};
}

#endif  /* __cplusplus */