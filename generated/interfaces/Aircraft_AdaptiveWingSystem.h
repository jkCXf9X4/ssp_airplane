#ifndef AIRCRAFT_ADAPTIVEWINGSYSTEM_H
#define AIRCRAFT_ADAPTIVEWINGSYSTEM_H

#include "Aircraft_InterfaceCommon.h"

/* Generated interface for Aircraft.AdaptiveWingSystem. Do not edit manually. */

#define AIRCRAFT_ADAPTIVEWINGSYSTEM_GUID "{8fa06bf4-c120-5d50-99f6-883f9ac468a4}"

typedef enum Aircraft_AdaptiveWingSystem_ValueReference {
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_REFERENCE_AREA_M2 = 0,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_SPAN_M = 1,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_ASPECT_RATIO = 2,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_CONTROL_AUTHORITY_DEG = 3,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_LOAD_FACTOR_LIMIT_G = 4,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_REFERENCEAREA = 5,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_SPAN = 6,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_WINGAREASCALE = 7,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_ASPECTRATIO = 8,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_LIFTCOEFFBASE = 9,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_ROLLAUTHORITY_DEG = 10,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_PITCHAUTHORITY_DEG = 11,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_DIRECTION_COMMAND_ROLL_DEG = 12,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_DIRECTION_COMMAND_PITCH_DEG = 13,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_DIRECTION_COMMAND_YAW_DEG = 14,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_FLIGHT_SPEED_AIRSPEED_MPS = 15,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_FLIGHT_SPEED_ENERGY_STATE_NORM = 16,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_FLIGHT_SPEED_ANGLE_OF_ATTACK_DEG = 17,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_FLIGHT_SPEED_CLIMB_RATE = 18,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_FLIGHT_SPEED_HEALTH_CODE = 19,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_ACTUATION_COMMAND_LEFT_AILERON_DEG = 20,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_ACTUATION_COMMAND_RIGHT_AILERON_DEG = 21,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_ACTUATION_COMMAND_ELEVATOR_DEG = 22,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_ACTUATION_COMMAND_RUDDER_DEG = 23,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_ACTUATION_COMMAND_FLAPERON_DEG = 24,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_LIFTINTERFACE_LIFT_KN = 25,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_LIFTINTERFACE_DRAG_KN = 26,
  AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_LIFTINTERFACE_PITCHING_MOMENT_KNM = 27,
} Aircraft_AdaptiveWingSystem_ValueReference;

enum { Aircraft_AdaptiveWingSystem_VrCount = 28 };

#ifdef __cplusplus
#include <string>

struct Aircraft_AdaptiveWingSystem_Instance {
  Aircraft_VrMapping vr_map[28] = {};
  double reference_area_m2 = 28;
  double span_m = 10;
  double aspect_ratio = 3.6;
  double control_authority_deg = 25;
  int load_factor_limit_g = 9;
  double referenceArea = 28;
  double span = 10;
  double wingAreaScale = 1;
  double aspectRatio = 3.6;
  double liftCoeffBase = 0.75;
  double rollAuthority_deg = 25;
  double pitchAuthority_deg = 20;
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
  instance->vr_map[AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_CONTROL_AUTHORITY_DEG] = {&instance->control_authority_deg, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_LOAD_FACTOR_LIMIT_G] = {&instance->load_factor_limit_g, AIRCRAFT_DATA_INTEGER, true};
  instance->vr_map[AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_REFERENCEAREA] = {&instance->referenceArea, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_SPAN] = {&instance->span, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_WINGAREASCALE] = {&instance->wingAreaScale, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_ASPECTRATIO] = {&instance->aspectRatio, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_LIFTCOEFFBASE] = {&instance->liftCoeffBase, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_ROLLAUTHORITY_DEG] = {&instance->rollAuthority_deg, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_ADAPTIVEWINGSYSTEM_VR_PITCHAUTHORITY_DEG] = {&instance->pitchAuthority_deg, AIRCRAFT_DATA_REAL, true};
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
#endif  /* AIRCRAFT_ADAPTIVEWINGSYSTEM_H */