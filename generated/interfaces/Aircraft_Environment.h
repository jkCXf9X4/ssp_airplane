#ifndef AIRCRAFT_ENVIRONMENT_H
#define AIRCRAFT_ENVIRONMENT_H

#include "Aircraft_InterfaceCommon.h"

/* Generated interface for Aircraft.Environment. Do not edit manually. */

typedef enum Aircraft_Environment_ValueReference {
  AIRCRAFT_ENVIRONMENT_VR_INITX_KM = 0,
  AIRCRAFT_ENVIRONMENT_VR_INITY_KM = 1,
  AIRCRAFT_ENVIRONMENT_VR_INITZ_KM = 2,
  AIRCRAFT_ENVIRONMENT_VR_TAUDIRECTION_S = 3,
  AIRCRAFT_ENVIRONMENT_VR_THRUSTTOSPEEDGAIN = 4,
  AIRCRAFT_ENVIRONMENT_VR_CLIMBBLEEDFRACTION = 5,
  AIRCRAFT_ENVIRONMENT_VR_MINAIRSPEED_MPS = 6,
  AIRCRAFT_ENVIRONMENT_VR_REFERENCEENERGYSPEED_MPS = 7,
  AIRCRAFT_ENVIRONMENT_VR_ACTUATION_COMMAND_LEFT_AILERON_DEG = 8,
  AIRCRAFT_ENVIRONMENT_VR_ACTUATION_COMMAND_RIGHT_AILERON_DEG = 9,
  AIRCRAFT_ENVIRONMENT_VR_ACTUATION_COMMAND_ELEVATOR_DEG = 10,
  AIRCRAFT_ENVIRONMENT_VR_ACTUATION_COMMAND_RUDDER_DEG = 11,
  AIRCRAFT_ENVIRONMENT_VR_ACTUATION_COMMAND_FLAPERON_DEG = 12,
  AIRCRAFT_ENVIRONMENT_VR_DIRECTION_COMMAND_ROLL_DEG = 13,
  AIRCRAFT_ENVIRONMENT_VR_DIRECTION_COMMAND_PITCH_DEG = 14,
  AIRCRAFT_ENVIRONMENT_VR_DIRECTION_COMMAND_YAW_DEG = 15,
  AIRCRAFT_ENVIRONMENT_VR_LIFT_LIFT_KN = 16,
  AIRCRAFT_ENVIRONMENT_VR_LIFT_DRAG_KN = 17,
  AIRCRAFT_ENVIRONMENT_VR_LIFT_PITCHING_MOMENT_KNM = 18,
  AIRCRAFT_ENVIRONMENT_VR_THRUST_IN_THRUST_KN = 19,
  AIRCRAFT_ENVIRONMENT_VR_THRUST_IN_MASS_FLOW_KGPS = 20,
  AIRCRAFT_ENVIRONMENT_VR_THRUST_IN_EXHAUST_VELOCITY_MPS = 21,
  AIRCRAFT_ENVIRONMENT_VR_ORIENTATION_ROLL_DEG = 22,
  AIRCRAFT_ENVIRONMENT_VR_ORIENTATION_PITCH_DEG = 23,
  AIRCRAFT_ENVIRONMENT_VR_ORIENTATION_YAW_DEG = 24,
  AIRCRAFT_ENVIRONMENT_VR_LOCATION_X_KM = 25,
  AIRCRAFT_ENVIRONMENT_VR_LOCATION_Y_KM = 26,
  AIRCRAFT_ENVIRONMENT_VR_LOCATION_Z_KM = 27,
  AIRCRAFT_ENVIRONMENT_VR_FLIGHT_STATUS_AIRSPEED_MPS = 28,
  AIRCRAFT_ENVIRONMENT_VR_FLIGHT_STATUS_ENERGY_STATE_NORM = 29,
  AIRCRAFT_ENVIRONMENT_VR_FLIGHT_STATUS_ANGLE_OF_ATTACK_DEG = 30,
  AIRCRAFT_ENVIRONMENT_VR_FLIGHT_STATUS_CLIMB_RATE = 31,
  AIRCRAFT_ENVIRONMENT_VR_FLIGHT_STATUS_HEALTH_CODE = 32,
} Aircraft_Environment_ValueReference;

enum { Aircraft_Environment_VrCount = 33 };

#ifdef __cplusplus
#include <string>

struct Aircraft_Environment_Instance {
  Aircraft_VrMapping vr_map[33] = {};
  double initX_km = 0;
  double initY_km = 0;
  double initZ_km = 1;
  double tauDirection_s = 2;
  double thrustToSpeedGain = 4;
  double climbBleedFraction = 0.35;
  double minAirspeed_mps = 50;
  double referenceEnergySpeed_mps = 300;
  Aircraft_SurfaceActuationCommand actuation_command = {};
  Aircraft_OrientationEuler direction_command = {};
  Aircraft_LiftState lift = {};
  Aircraft_ThrustState thrust_in = {};
  Aircraft_OrientationEuler orientation = {};
  Aircraft_PositionXYZ location = {};
  Aircraft_FlightStatusPacket flight_status = {};
};

inline void Aircraft_Environment_initialize_vr_map(Aircraft_Environment_Instance* instance) {
  for (size_t i = 0; i < Aircraft_Environment_VrCount; ++i) {
    instance->vr_map[i] = {nullptr, AIRCRAFT_DATA_NONE, false};
  }
  instance->vr_map[AIRCRAFT_ENVIRONMENT_VR_INITX_KM] = {&instance->initX_km, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_ENVIRONMENT_VR_INITY_KM] = {&instance->initY_km, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_ENVIRONMENT_VR_INITZ_KM] = {&instance->initZ_km, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_ENVIRONMENT_VR_TAUDIRECTION_S] = {&instance->tauDirection_s, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_ENVIRONMENT_VR_THRUSTTOSPEEDGAIN] = {&instance->thrustToSpeedGain, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_ENVIRONMENT_VR_CLIMBBLEEDFRACTION] = {&instance->climbBleedFraction, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_ENVIRONMENT_VR_MINAIRSPEED_MPS] = {&instance->minAirspeed_mps, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_ENVIRONMENT_VR_REFERENCEENERGYSPEED_MPS] = {&instance->referenceEnergySpeed_mps, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_ENVIRONMENT_VR_ACTUATION_COMMAND_LEFT_AILERON_DEG] = {&instance->actuation_command.left_aileron_deg, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_ENVIRONMENT_VR_ACTUATION_COMMAND_RIGHT_AILERON_DEG] = {&instance->actuation_command.right_aileron_deg, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_ENVIRONMENT_VR_ACTUATION_COMMAND_ELEVATOR_DEG] = {&instance->actuation_command.elevator_deg, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_ENVIRONMENT_VR_ACTUATION_COMMAND_RUDDER_DEG] = {&instance->actuation_command.rudder_deg, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_ENVIRONMENT_VR_ACTUATION_COMMAND_FLAPERON_DEG] = {&instance->actuation_command.flaperon_deg, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_ENVIRONMENT_VR_DIRECTION_COMMAND_ROLL_DEG] = {&instance->direction_command.roll_deg, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_ENVIRONMENT_VR_DIRECTION_COMMAND_PITCH_DEG] = {&instance->direction_command.pitch_deg, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_ENVIRONMENT_VR_DIRECTION_COMMAND_YAW_DEG] = {&instance->direction_command.yaw_deg, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_ENVIRONMENT_VR_LIFT_LIFT_KN] = {&instance->lift.lift_kn, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_ENVIRONMENT_VR_LIFT_DRAG_KN] = {&instance->lift.drag_kn, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_ENVIRONMENT_VR_LIFT_PITCHING_MOMENT_KNM] = {&instance->lift.pitching_moment_knm, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_ENVIRONMENT_VR_THRUST_IN_THRUST_KN] = {&instance->thrust_in.thrust_kn, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_ENVIRONMENT_VR_THRUST_IN_MASS_FLOW_KGPS] = {&instance->thrust_in.mass_flow_kgps, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_ENVIRONMENT_VR_THRUST_IN_EXHAUST_VELOCITY_MPS] = {&instance->thrust_in.exhaust_velocity_mps, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_ENVIRONMENT_VR_ORIENTATION_ROLL_DEG] = {&instance->orientation.roll_deg, AIRCRAFT_DATA_REAL, false};
  instance->vr_map[AIRCRAFT_ENVIRONMENT_VR_ORIENTATION_PITCH_DEG] = {&instance->orientation.pitch_deg, AIRCRAFT_DATA_REAL, false};
  instance->vr_map[AIRCRAFT_ENVIRONMENT_VR_ORIENTATION_YAW_DEG] = {&instance->orientation.yaw_deg, AIRCRAFT_DATA_REAL, false};
  instance->vr_map[AIRCRAFT_ENVIRONMENT_VR_LOCATION_X_KM] = {&instance->location.x_km, AIRCRAFT_DATA_REAL, false};
  instance->vr_map[AIRCRAFT_ENVIRONMENT_VR_LOCATION_Y_KM] = {&instance->location.y_km, AIRCRAFT_DATA_REAL, false};
  instance->vr_map[AIRCRAFT_ENVIRONMENT_VR_LOCATION_Z_KM] = {&instance->location.z_km, AIRCRAFT_DATA_REAL, false};
  instance->vr_map[AIRCRAFT_ENVIRONMENT_VR_FLIGHT_STATUS_AIRSPEED_MPS] = {&instance->flight_status.airspeed_mps, AIRCRAFT_DATA_REAL, false};
  instance->vr_map[AIRCRAFT_ENVIRONMENT_VR_FLIGHT_STATUS_ENERGY_STATE_NORM] = {&instance->flight_status.energy_state_norm, AIRCRAFT_DATA_REAL, false};
  instance->vr_map[AIRCRAFT_ENVIRONMENT_VR_FLIGHT_STATUS_ANGLE_OF_ATTACK_DEG] = {&instance->flight_status.angle_of_attack_deg, AIRCRAFT_DATA_REAL, false};
  instance->vr_map[AIRCRAFT_ENVIRONMENT_VR_FLIGHT_STATUS_CLIMB_RATE] = {&instance->flight_status.climb_rate, AIRCRAFT_DATA_REAL, false};
  instance->vr_map[AIRCRAFT_ENVIRONMENT_VR_FLIGHT_STATUS_HEALTH_CODE] = {&instance->flight_status.health_code, AIRCRAFT_DATA_INTEGER, false};
}

#endif  /* __cplusplus */
#endif  /* AIRCRAFT_ENVIRONMENT_H */