#pragma once

#include "Aircraft_InterfaceCommon.h"

/* Generated interface for Aircraft.FuelSystem. Do not edit manually. */

typedef enum Aircraft_FuelSystem_ValueReference {
  AIRCRAFT_FUELSYSTEM_VR_FUEL_CAPACITY_KG = 0,
  AIRCRAFT_FUELSYSTEM_VR_RESERVE_FRACTION = 1,
  AIRCRAFT_FUELSYSTEM_VR_FUEL_CONSUMPTION_RATE_MASS_FLOW_KGPS = 2,
  AIRCRAFT_FUELSYSTEM_VR_FUELSTATE_FUEL_REMAINING_KG = 3,
  AIRCRAFT_FUELSYSTEM_VR_FUELSTATE_FUEL_LEVEL_NORM = 4,
  AIRCRAFT_FUELSYSTEM_VR_FUELSTATE_FUEL_STARVED = 5,
} Aircraft_FuelSystem_ValueReference;

#ifdef __cplusplus

struct Aircraft_FuelSystem_Instance {
  int fuel_capacity_kg = 3160;
  double reserve_fraction = 0.08;
  Aircraft_FuelConsumptionRate fuel_consumption_rate = {};
  Aircraft_FuelLevelState fuelState = {};
};

inline constexpr Aircraft_FieldBinding Aircraft_FuelSystem_Bindings[] = {
  {AIRCRAFT_FUELSYSTEM_VR_FUEL_CAPACITY_KG, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_FuelSystem_Instance, fuel_capacity_kg), true},
  {AIRCRAFT_FUELSYSTEM_VR_RESERVE_FRACTION, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_FuelSystem_Instance, reserve_fraction), true},
  {AIRCRAFT_FUELSYSTEM_VR_FUEL_CONSUMPTION_RATE_MASS_FLOW_KGPS, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_FuelSystem_Instance, fuel_consumption_rate) + offsetof(Aircraft_FuelConsumptionRate, mass_flow_kgps), true},
  {AIRCRAFT_FUELSYSTEM_VR_FUELSTATE_FUEL_REMAINING_KG, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_FuelSystem_Instance, fuelState) + offsetof(Aircraft_FuelLevelState, fuel_remaining_kg), false},
  {AIRCRAFT_FUELSYSTEM_VR_FUELSTATE_FUEL_LEVEL_NORM, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_FuelSystem_Instance, fuelState) + offsetof(Aircraft_FuelLevelState, fuel_level_norm), false},
  {AIRCRAFT_FUELSYSTEM_VR_FUELSTATE_FUEL_STARVED, AIRCRAFT_SCALAR_BOOLEAN, offsetof(Aircraft_FuelSystem_Instance, fuelState) + offsetof(Aircraft_FuelLevelState, fuel_starved), false},
};
inline constexpr size_t Aircraft_FuelSystem_BindingCount = sizeof(Aircraft_FuelSystem_Bindings) / sizeof(Aircraft_FuelSystem_Bindings[0]);

inline constexpr const Aircraft_StringFieldBinding* Aircraft_FuelSystem_StringBindings = nullptr;
inline constexpr size_t Aircraft_FuelSystem_StringBindingCount = 0;

#endif  /* __cplusplus */