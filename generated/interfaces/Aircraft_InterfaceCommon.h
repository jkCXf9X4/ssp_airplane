#pragma once

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/* Generated from architecture package Aircraft. Do not edit manually. */

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

#ifdef __cplusplus
#include <string>

enum Aircraft_DataType {
  AIRCRAFT_DATA_NONE = 0,
  AIRCRAFT_DATA_REAL = 1,
  AIRCRAFT_DATA_INTEGER = 2,
  AIRCRAFT_DATA_BOOLEAN = 3,
  AIRCRAFT_DATA_STRING = 4,
};

struct Aircraft_VrMapping {
  void* data = nullptr;
  Aircraft_DataType type = AIRCRAFT_DATA_NONE;
  bool writable = false;
};
#endif  /* __cplusplus */
