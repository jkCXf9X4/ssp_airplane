#pragma once

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/* Generated from architecture package Aircraft. Do not edit manually. */

typedef enum Aircraft_ScalarType {
  AIRCRAFT_SCALAR_REAL = 0,
  AIRCRAFT_SCALAR_INTEGER = 1,
  AIRCRAFT_SCALAR_BOOLEAN = 2,
  AIRCRAFT_SCALAR_STRING = 3,
} Aircraft_ScalarType;

typedef struct Aircraft_FieldBinding {
  int value_reference;
  Aircraft_ScalarType scalar_type;
  size_t offset;
  bool writable;
} Aircraft_FieldBinding;

#ifdef __cplusplus
#include <string>

typedef const std::string& (*Aircraft_StringFieldGetter)(const void* instance);
typedef std::string& (*Aircraft_StringFieldGetterMut)(void* instance);

typedef struct Aircraft_StringFieldBinding {
  int value_reference;
  Aircraft_StringFieldGetter get;
  Aircraft_StringFieldGetterMut get_mut;
  bool writable;
} Aircraft_StringFieldBinding;
#endif  /* __cplusplus */

typedef struct Aircraft_PilotCommand {
  double stick_pitch_norm;
  double stick_roll_norm;
  double rudder_norm;
  double throttle_norm;
  double throttle_aux_norm;
  int button_mask;
  int hat_x;
  int hat_y;
  int mode_switch;
  int reserved;
} Aircraft_PilotCommand;

typedef struct Aircraft_OrientationEuler {
  double roll_deg;
  double pitch_deg;
  double yaw_deg;
} Aircraft_OrientationEuler;

typedef struct Aircraft_PositionXYZ {
  double x_km;
  double y_km;
  double z_km;
} Aircraft_PositionXYZ;

typedef struct Aircraft_SurfaceActuationCommand {
  double left_aileron_deg;
  double right_aileron_deg;
  double elevator_deg;
  double rudder_deg;
  double flaperon_deg;
} Aircraft_SurfaceActuationCommand;

typedef struct Aircraft_LiftState {
  double lift_kn;
  double drag_kn;
  double pitching_moment_knm;
} Aircraft_LiftState;

typedef struct Aircraft_ThrottleCommand {
  double throttle_norm;
  bool fuel_enable;
  bool afterburner_enable;
} Aircraft_ThrottleCommand;

typedef struct Aircraft_ThrustState {
  double thrust_kn;
  double mass_flow_kgps;
  double exhaust_velocity_mps;
} Aircraft_ThrustState;

typedef struct Aircraft_FuelLevelState {
  double fuel_remaining_kg;
  double fuel_level_norm;
  bool fuel_starved;
} Aircraft_FuelLevelState;

typedef struct Aircraft_FuelConsumptionRate {
  double mass_flow_kgps;
} Aircraft_FuelConsumptionRate;

typedef struct Aircraft_FlightStatusPacket {
  double airspeed_mps;
  double energy_state_norm;
  double angle_of_attack_deg;
  double climb_rate;
  int health_code;
} Aircraft_FlightStatusPacket;

typedef struct Aircraft_MissionStatus {
  int waypoint_index;
  int total_waypoints;
  double distance_to_waypoint_km;
  bool arrived;
  bool complete;
} Aircraft_MissionStatus;
