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

inline constexpr size_t Aircraft_FuelSystem_VrCount = 6;

struct Aircraft_FuelSystem_Instance {
  Aircraft_VrMapping vr_map[6] = {};
  int fuel_capacity_kg = 3160;
  double reserve_fraction = 0.08;
  Aircraft_FuelConsumptionRate fuel_consumption_rate = {};
  Aircraft_FuelLevelState fuelState = {};
};

inline void Aircraft_FuelSystem_initialize_vr_map(Aircraft_FuelSystem_Instance* instance) {
  for (size_t i = 0; i < Aircraft_FuelSystem_VrCount; ++i) {
    instance->vr_map[i] = {nullptr, AIRCRAFT_DATA_NONE, false};
  }
  instance->vr_map[AIRCRAFT_FUELSYSTEM_VR_FUEL_CAPACITY_KG] = {&instance->fuel_capacity_kg, AIRCRAFT_DATA_INTEGER, true};
  instance->vr_map[AIRCRAFT_FUELSYSTEM_VR_RESERVE_FRACTION] = {&instance->reserve_fraction, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_FUELSYSTEM_VR_FUEL_CONSUMPTION_RATE_MASS_FLOW_KGPS] = {&instance->fuel_consumption_rate.mass_flow_kgps, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_FUELSYSTEM_VR_FUELSTATE_FUEL_REMAINING_KG] = {&instance->fuelState.fuel_remaining_kg, AIRCRAFT_DATA_REAL, false};
  instance->vr_map[AIRCRAFT_FUELSYSTEM_VR_FUELSTATE_FUEL_LEVEL_NORM] = {&instance->fuelState.fuel_level_norm, AIRCRAFT_DATA_REAL, false};
  instance->vr_map[AIRCRAFT_FUELSYSTEM_VR_FUELSTATE_FUEL_STARVED] = {&instance->fuelState.fuel_starved, AIRCRAFT_DATA_BOOLEAN, false};
}

#endif  /* __cplusplus */