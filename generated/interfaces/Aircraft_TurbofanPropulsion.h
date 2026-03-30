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

struct Aircraft_TurbofanPropulsion_Instance {
  double max_thrust_kn = 129.7;
  double dry_thrust_kn = 79.0;
  double specific_fuel_consumption = 0.76;
  int fuel_capacity_kg = 3160;
  int generator_output_kw = 80;
  Aircraft_ThrottleCommand throttleCmd = {};
  Aircraft_ThrustState thrustOut = {};
  Aircraft_FuelConsumptionRate fuel_consumption = {};
};

inline constexpr Aircraft_FieldBinding Aircraft_TurbofanPropulsion_Bindings[] = {
  {AIRCRAFT_TURBOFANPROPULSION_VR_MAX_THRUST_KN, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_TurbofanPropulsion_Instance, max_thrust_kn), true},
  {AIRCRAFT_TURBOFANPROPULSION_VR_DRY_THRUST_KN, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_TurbofanPropulsion_Instance, dry_thrust_kn), true},
  {AIRCRAFT_TURBOFANPROPULSION_VR_SPECIFIC_FUEL_CONSUMPTION, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_TurbofanPropulsion_Instance, specific_fuel_consumption), true},
  {AIRCRAFT_TURBOFANPROPULSION_VR_FUEL_CAPACITY_KG, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_TurbofanPropulsion_Instance, fuel_capacity_kg), true},
  {AIRCRAFT_TURBOFANPROPULSION_VR_GENERATOR_OUTPUT_KW, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_TurbofanPropulsion_Instance, generator_output_kw), true},
  {AIRCRAFT_TURBOFANPROPULSION_VR_THROTTLECMD_THROTTLE_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_TurbofanPropulsion_Instance, throttleCmd) + offsetof(Aircraft_ThrottleCommand, throttle_norm), true},
  {AIRCRAFT_TURBOFANPROPULSION_VR_THROTTLECMD_FUEL_ENABLE, AIRCRAFT_SCALAR_BOOLEAN, offsetof(Aircraft_TurbofanPropulsion_Instance, throttleCmd) + offsetof(Aircraft_ThrottleCommand, fuel_enable), true},
  {AIRCRAFT_TURBOFANPROPULSION_VR_THROTTLECMD_AFTERBURNER_ENABLE, AIRCRAFT_SCALAR_BOOLEAN, offsetof(Aircraft_TurbofanPropulsion_Instance, throttleCmd) + offsetof(Aircraft_ThrottleCommand, afterburner_enable), true},
  {AIRCRAFT_TURBOFANPROPULSION_VR_THRUSTOUT_THRUST_KN, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_TurbofanPropulsion_Instance, thrustOut) + offsetof(Aircraft_ThrustState, thrust_kn), false},
  {AIRCRAFT_TURBOFANPROPULSION_VR_THRUSTOUT_MASS_FLOW_KGPS, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_TurbofanPropulsion_Instance, thrustOut) + offsetof(Aircraft_ThrustState, mass_flow_kgps), false},
  {AIRCRAFT_TURBOFANPROPULSION_VR_THRUSTOUT_EXHAUST_VELOCITY_MPS, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_TurbofanPropulsion_Instance, thrustOut) + offsetof(Aircraft_ThrustState, exhaust_velocity_mps), false},
  {AIRCRAFT_TURBOFANPROPULSION_VR_FUEL_CONSUMPTION_MASS_FLOW_KGPS, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_TurbofanPropulsion_Instance, fuel_consumption) + offsetof(Aircraft_FuelConsumptionRate, mass_flow_kgps), false},
};
inline constexpr size_t Aircraft_TurbofanPropulsion_BindingCount = sizeof(Aircraft_TurbofanPropulsion_Bindings) / sizeof(Aircraft_TurbofanPropulsion_Bindings[0]);

inline constexpr const Aircraft_StringFieldBinding* Aircraft_TurbofanPropulsion_StringBindings = nullptr;
inline constexpr size_t Aircraft_TurbofanPropulsion_StringBindingCount = 0;

#endif  /* __cplusplus */