#pragma once

#include "Aircraft_InterfaceCommon.h"

/* Generated interface for Aircraft.TurbofanPropulsion. Do not edit manually. */

typedef enum Aircraft_TurbofanPropulsion_ValueReference {
  AIRCRAFT_TURBOFANPROPULSION_VR_MAX_THRUST_KN = 0,
  AIRCRAFT_TURBOFANPROPULSION_VR_DRY_THRUST_KN = 1,
  AIRCRAFT_TURBOFANPROPULSION_VR_SPECIFIC_FUEL_CONSUMPTION = 2,
  AIRCRAFT_TURBOFANPROPULSION_VR_FUEL_CAPACITY_KG = 3,
  AIRCRAFT_TURBOFANPROPULSION_VR_GENERATOR_OUTPUT_KW = 4,
  AIRCRAFT_TURBOFANPROPULSION_VR_THROTTLECMD_THROTTLE_NORM = 5,
  AIRCRAFT_TURBOFANPROPULSION_VR_THROTTLECMD_FUEL_ENABLE = 6,
  AIRCRAFT_TURBOFANPROPULSION_VR_THROTTLECMD_AFTERBURNER_ENABLE = 7,
  AIRCRAFT_TURBOFANPROPULSION_VR_THRUSTOUT_THRUST_KN = 8,
  AIRCRAFT_TURBOFANPROPULSION_VR_THRUSTOUT_MASS_FLOW_KGPS = 9,
  AIRCRAFT_TURBOFANPROPULSION_VR_THRUSTOUT_EXHAUST_VELOCITY_MPS = 10,
  AIRCRAFT_TURBOFANPROPULSION_VR_FUEL_CONSUMPTION_MASS_FLOW_KGPS = 11,
} Aircraft_TurbofanPropulsion_ValueReference;

#ifdef __cplusplus

inline constexpr size_t Aircraft_TurbofanPropulsion_VrCount = 12;

struct Aircraft_TurbofanPropulsion_Instance {
  Aircraft_VrMapping vr_map[12] = {};
  double max_thrust_kn = 129.7;
  double dry_thrust_kn = 79.0;
  double specific_fuel_consumption = 0.76;
  int fuel_capacity_kg = 3160;
  int generator_output_kw = 80;
  Aircraft_ThrottleCommand throttleCmd = {};
  Aircraft_ThrustState thrustOut = {};
  Aircraft_FuelConsumptionRate fuel_consumption = {};
};

inline void Aircraft_TurbofanPropulsion_initialize_vr_map(Aircraft_TurbofanPropulsion_Instance* instance) {
  for (size_t i = 0; i < Aircraft_TurbofanPropulsion_VrCount; ++i) {
    instance->vr_map[i] = {nullptr, AIRCRAFT_DATA_NONE, false};
  }
  instance->vr_map[AIRCRAFT_TURBOFANPROPULSION_VR_MAX_THRUST_KN] = {&instance->max_thrust_kn, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_TURBOFANPROPULSION_VR_DRY_THRUST_KN] = {&instance->dry_thrust_kn, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_TURBOFANPROPULSION_VR_SPECIFIC_FUEL_CONSUMPTION] = {&instance->specific_fuel_consumption, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_TURBOFANPROPULSION_VR_FUEL_CAPACITY_KG] = {&instance->fuel_capacity_kg, AIRCRAFT_DATA_INTEGER, true};
  instance->vr_map[AIRCRAFT_TURBOFANPROPULSION_VR_GENERATOR_OUTPUT_KW] = {&instance->generator_output_kw, AIRCRAFT_DATA_INTEGER, true};
  instance->vr_map[AIRCRAFT_TURBOFANPROPULSION_VR_THROTTLECMD_THROTTLE_NORM] = {&instance->throttleCmd.throttle_norm, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_TURBOFANPROPULSION_VR_THROTTLECMD_FUEL_ENABLE] = {&instance->throttleCmd.fuel_enable, AIRCRAFT_DATA_BOOLEAN, true};
  instance->vr_map[AIRCRAFT_TURBOFANPROPULSION_VR_THROTTLECMD_AFTERBURNER_ENABLE] = {&instance->throttleCmd.afterburner_enable, AIRCRAFT_DATA_BOOLEAN, true};
  instance->vr_map[AIRCRAFT_TURBOFANPROPULSION_VR_THRUSTOUT_THRUST_KN] = {&instance->thrustOut.thrust_kn, AIRCRAFT_DATA_REAL, false};
  instance->vr_map[AIRCRAFT_TURBOFANPROPULSION_VR_THRUSTOUT_MASS_FLOW_KGPS] = {&instance->thrustOut.mass_flow_kgps, AIRCRAFT_DATA_REAL, false};
  instance->vr_map[AIRCRAFT_TURBOFANPROPULSION_VR_THRUSTOUT_EXHAUST_VELOCITY_MPS] = {&instance->thrustOut.exhaust_velocity_mps, AIRCRAFT_DATA_REAL, false};
  instance->vr_map[AIRCRAFT_TURBOFANPROPULSION_VR_FUEL_CONSUMPTION_MASS_FLOW_KGPS] = {&instance->fuel_consumption.mass_flow_kgps, AIRCRAFT_DATA_REAL, false};
}

#endif  /* __cplusplus */