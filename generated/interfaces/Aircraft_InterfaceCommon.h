#ifndef AIRCRAFT_INTERFACECOMMON_H
#define AIRCRAFT_INTERFACECOMMON_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/* Generated from architecture package Aircraft. Do not edit manually. */

typedef struct Aircraft_PositionXYZ {
  double x_km;
  double y_km;
  double z_km;
} Aircraft_PositionXYZ;

typedef struct Aircraft_OrientationEuler {
  double roll_deg;
  double pitch_deg;
  double yaw_deg;
} Aircraft_OrientationEuler;

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

typedef enum Aircraft_DataType {
  AIRCRAFT_DATA_NONE = 0,
  AIRCRAFT_DATA_REAL = 1,
  AIRCRAFT_DATA_INTEGER = 2,
  AIRCRAFT_DATA_BOOLEAN = 3,
  AIRCRAFT_DATA_STRING = 4,
} Aircraft_DataType;

typedef struct Aircraft_VrMapping {
  void* data;
  Aircraft_DataType type;
  bool writable;
} Aircraft_VrMapping;

#endif  /* AIRCRAFT_INTERFACECOMMON_H */
